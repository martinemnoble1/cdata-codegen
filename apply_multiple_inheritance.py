#!/usr/bin/env python3
"""
Automated refactoring script to apply multiple inheritance pattern.

This script:
1. Analyzes class definition order in each file
2. Adds full-fat parent to inheritance where safe (parent defined first)
3. Adds explanatory comments where not possible
4. Generates a detailed report
5. Creates backup before modifying
"""

import re
import shutil
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from collections import defaultdict


@dataclass
class ClassInfo:
    """Information about a class definition."""
    name: str
    line_number: int
    current_parents: List[str]
    stub_parent: str
    full_fat_parent: str
    can_use_multiple_inheritance: bool
    reason: str


class MultipleInheritanceRefactor:
    """Refactor implementation classes to use multiple inheritance."""

    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.changes = defaultdict(list)
        self.errors = []

    def parse_class_definitions(self, content: str) -> Dict[str, int]:
        """
        Parse file to get class names and their line numbers.

        Returns: {class_name: line_number}
        """
        class_positions = {}

        # Pattern: class ClassName(Parents):
        pattern = r'^class (\w+)\([^)]+\):'

        for i, line in enumerate(content.split('\n'), 1):
            match = re.match(pattern, line)
            if match:
                class_name = match.group(1)
                class_positions[class_name] = i

        return class_positions

    def parse_class_inheritance(self, content: str, class_name: str) -> Tuple[List[str], int]:
        """
        Parse the inheritance list for a specific class.

        Returns: (parent_list, line_number)
        """
        # Pattern: class ClassName(Parent1, Parent2, ...):
        pattern = rf'^class {re.escape(class_name)}\(([^)]+)\):'

        for i, line in enumerate(content.split('\n'), 1):
            match = re.match(pattern, line)
            if match:
                parents_str = match.group(1)
                parents = [p.strip() for p in parents_str.split(',')]
                return parents, i

        return [], 0

    def should_add_multiple_inheritance(
        self,
        class_name: str,
        current_parents: List[str],
        class_positions: Dict[str, int],
        current_line: int
    ) -> Optional[ClassInfo]:
        """
        Determine if a class should use multiple inheritance.

        Returns ClassInfo with decision and reasoning, or None if not applicable.
        """
        # Must have exactly one parent currently (the stub)
        if len(current_parents) != 1:
            return None

        stub_parent = current_parents[0]

        # Stub must end with 'Stub'
        if not stub_parent.endswith('Stub'):
            return None

        # Calculate full-fat parent name
        full_fat_parent = stub_parent.replace('Stub', '')

        # Skip if full-fat parent is a base class
        if full_fat_parent in ['CData', 'CContainer', 'CDataFile', 'CDataFileContent']:
            return None

        # Skip if the class IS the full-fat parent (base implementation class)
        if class_name == full_fat_parent:
            return None

        # Check if full-fat parent exists in this file
        if full_fat_parent not in class_positions:
            # Parent not in this file - can't use multiple inheritance
            return None

        # Check definition order
        parent_line = class_positions[full_fat_parent]

        if parent_line >= current_line:
            return ClassInfo(
                name=class_name,
                line_number=current_line,
                current_parents=current_parents,
                stub_parent=stub_parent,
                full_fat_parent=full_fat_parent,
                can_use_multiple_inheritance=False,
                reason=f"{full_fat_parent} defined later (line {parent_line} >= {current_line})"
            )

        # All checks passed!
        return ClassInfo(
            name=class_name,
            line_number=current_line,
            current_parents=current_parents,
            stub_parent=stub_parent,
            full_fat_parent=full_fat_parent,
            can_use_multiple_inheritance=True,
            reason=f"Can inherit from {full_fat_parent} (line {parent_line} < {current_line})"
        )

    def update_class_definition(
        self,
        content: str,
        class_info: ClassInfo
    ) -> Tuple[str, bool]:
        """
        Update a single class definition to use multiple inheritance.

        Returns: (updated_content, was_modified)
        """
        if not class_info.can_use_multiple_inheritance:
            return content, False

        # Find the class definition line
        lines = content.split('\n')

        # Pattern to match: class ClassName(StubParent):
        old_pattern = rf'^(\s*)class {re.escape(class_info.name)}\({re.escape(class_info.stub_parent)}\):'

        modified = False
        for i, line in enumerate(lines):
            if re.match(old_pattern, line):
                # Extract indentation
                indent_match = re.match(r'^(\s*)', line)
                indent = indent_match.group(1) if indent_match else ''

                # New inheritance: class ClassName(StubParent, FullFatParent):
                new_line = f'{indent}class {class_info.name}({class_info.stub_parent}, {class_info.full_fat_parent}):'
                lines[i] = new_line

                # Update docstring to explain inheritance
                # Look for docstring start
                for j in range(i + 1, min(i + 10, len(lines))):
                    if '"""' in lines[j]:
                        # Found docstring - check if it already has inheritance info
                        if 'Inherits from:' not in lines[j]:
                            # Add inheritance explanation after opening """
                            opening_line = j

                            # Find the line after the opening quotes
                            insert_pos = opening_line + 1

                            # Create inheritance documentation
                            inheritance_doc = [
                                f'{indent}    ',
                                f'{indent}    Inherits from:',
                                f'{indent}    - {class_info.stub_parent}: Metadata and structure',
                                f'{indent}    - {class_info.full_fat_parent}: Shared full-fat methods',
                            ]

                            # Insert the documentation
                            for doc_line in reversed(inheritance_doc):
                                lines.insert(insert_pos, doc_line)

                        break

                modified = True
                break

        return '\n'.join(lines), modified

    def add_explanation_comment(
        self,
        content: str,
        class_info: ClassInfo
    ) -> Tuple[str, bool]:
        """
        Add explanatory comment for classes that CAN'T use multiple inheritance.

        Returns: (updated_content, was_modified)
        """
        if class_info.can_use_multiple_inheritance:
            return content, False

        # Only add comment if it's due to definition order
        if "defined later" not in class_info.reason:
            return content, False

        lines = content.split('\n')

        # Find the class definition
        pattern = rf'^(\s*)class {re.escape(class_info.name)}\('

        modified = False
        for i, line in enumerate(lines):
            if re.match(pattern, line):
                # Check if comment already exists
                if i > 0 and 'Cannot inherit from' in lines[i - 1]:
                    break

                # Extract indentation
                indent_match = re.match(r'^(\s*)', line)
                indent = indent_match.group(1) if indent_match else ''

                # Look for docstring
                for j in range(i + 1, min(i + 10, len(lines))):
                    if '"""' in lines[j]:
                        # Found docstring - add note
                        insert_pos = j + 1

                        # Check if already has note
                        if insert_pos < len(lines) and 'NOTE:' in lines[insert_pos]:
                            break

                        note = [
                            f'{indent}    ',
                            f'{indent}    NOTE: Cannot inherit from {class_info.full_fat_parent} due to definition order.',
                            f'{indent}    {class_info.full_fat_parent} is defined later in the file.',
                        ]

                        for note_line in reversed(note):
                            lines.insert(insert_pos, note_line)

                        modified = True
                        break

                break

        return '\n'.join(lines), modified

    def process_file(self, impl_path: Path) -> Dict:
        """
        Process a single implementation file.

        Returns: Report dictionary
        """
        print(f"\nProcessing {impl_path.name}...")

        content = impl_path.read_text()
        original_content = content

        # Parse all class definitions
        class_positions = self.parse_class_definitions(content)

        # Analyze each class
        classes_to_update = []
        classes_with_notes = []

        for class_name in class_positions.keys():
            # Skip stub classes
            if class_name.endswith('Stub'):
                continue

            current_parents, line_num = self.parse_class_inheritance(content, class_name)

            if not current_parents:
                continue

            class_info = self.should_add_multiple_inheritance(
                class_name,
                current_parents,
                class_positions,
                line_num
            )

            # Skip if not applicable
            if class_info is None:
                continue

            if class_info.can_use_multiple_inheritance:
                classes_to_update.append(class_info)
            elif "defined later" in class_info.reason:
                classes_with_notes.append(class_info)

        # Apply updates
        modified = False

        for class_info in classes_to_update:
            content, was_modified = self.update_class_definition(content, class_info)
            if was_modified:
                modified = True
                self.changes[impl_path.name].append(
                    f"✓ {class_info.name}: Added {class_info.full_fat_parent} to inheritance"
                )

        for class_info in classes_with_notes:
            content, was_modified = self.add_explanation_comment(content, class_info)
            if was_modified:
                modified = True
                self.changes[impl_path.name].append(
                    f"📝 {class_info.name}: Added note about {class_info.full_fat_parent} ordering"
                )

        # Write changes
        if modified and not self.dry_run:
            # Create backup
            backup_path = impl_path.with_suffix('.py.backup')
            shutil.copy2(impl_path, backup_path)

            # Write updated content
            impl_path.write_text(content)

        return {
            'file': impl_path.name,
            'total_classes': len([c for c in class_positions.keys() if not c.endswith('Stub')]),
            'updated': len(classes_to_update),
            'noted': len(classes_with_notes),
            'modified': modified,
            'classes_updated': [c.name for c in classes_to_update],
            'classes_noted': [c.name for c in classes_with_notes]
        }

    def process_all_files(self) -> None:
        """Process all CCP4*.py implementation files."""
        core_dir = Path(__file__).parent / 'core'
        impl_files = sorted(core_dir.glob('CCP4*.py'))

        reports = []

        print("="*80)
        print(f"Multiple Inheritance Refactoring")
        print(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE'}")
        print("="*80)

        for impl_file in impl_files:
            report = self.process_file(impl_file)
            reports.append(report)

        # Summary
        self.print_summary(reports)

    def print_summary(self, reports: List[Dict]) -> None:
        """Print summary of all changes."""
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)

        total_files = len(reports)
        files_modified = sum(1 for r in reports if r['modified'])
        total_updated = sum(r['updated'] for r in reports)
        total_noted = sum(r['noted'] for r in reports)

        print(f"\nFiles analyzed: {total_files}")
        print(f"Files modified: {files_modified}")
        print(f"Classes updated with multiple inheritance: {total_updated}")
        print(f"Classes with ordering notes added: {total_noted}")

        if self.changes:
            print("\n" + "="*80)
            print("DETAILED CHANGES")
            print("="*80)

            for filename, changes in sorted(self.changes.items()):
                print(f"\n{filename}:")
                for change in changes:
                    print(f"  {change}")

        if self.dry_run:
            print("\n" + "="*80)
            print("⚠️  DRY RUN - No files were modified")
            print("Run with --apply to apply changes")
            print("="*80)
        else:
            print("\n" + "="*80)
            print("✓ Changes applied!")
            print("Backup files created with .backup extension")
            print("="*80)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Apply multiple inheritance pattern to CData classes'
    )
    parser.add_argument(
        '--apply',
        action='store_true',
        help='Apply changes (default is dry-run)'
    )
    parser.add_argument(
        '--file',
        type=str,
        help='Process only specific file (e.g., CCP4XtalData.py)'
    )

    args = parser.parse_args()

    refactor = MultipleInheritanceRefactor(dry_run=not args.apply)

    if args.file:
        # Process single file
        core_dir = Path(__file__).parent / 'core'
        impl_path = core_dir / args.file

        if not impl_path.exists():
            print(f"Error: File not found: {impl_path}")
            return

        report = refactor.process_file(impl_path)
        refactor.print_summary([report])
    else:
        # Process all files
        refactor.process_all_files()


if __name__ == '__main__':
    main()
