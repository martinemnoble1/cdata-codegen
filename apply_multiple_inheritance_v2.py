#!/usr/bin/env python3
"""
Automated refactoring script to apply multiple inheritance pattern.

Strategy:
1. Parse stub file to find: StubChild(StubParent) relationships
2. For each impl class, check if it should inherit from both its stub AND the full-fat parent
3. Apply changes where definition order allows
"""

import re
import shutil
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Tuple
from collections import defaultdict


@dataclass
class InheritanceInfo:
    """Information about what a class should inherit from."""
    impl_class: str
    line_number: int
    current_parents: List[str]
    should_have_parents: List[str]
    can_apply: bool
    reason: str


class MultipleInheritanceRefactor:
    """Refactor implementation classes to use multiple inheritance."""

    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.changes = defaultdict(list)

    def parse_stub_inheritance(self, stub_path: Path) -> Dict[str, str]:
        """
        Parse stub file to find inheritance relationships.

        Returns: {ChildStub: ParentStub}
        """
        content = stub_path.read_text()
        relationships = {}

        # Pattern: class ChildStub(ParentStub):
        pattern = r'^class (\w+Stub)\((\w+(?:Stub)?)\):'

        for match in re.finditer(pattern, content, re.MULTILINE):
            child_stub = match.group(1)
            parent = match.group(2)

            # Only track if parent is a stub (not base like CData)
            if parent.endswith('Stub'):
                relationships[child_stub] = parent

        return relationships

    def get_class_positions(self, content: str) -> Dict[str, int]:
        """Get line numbers where classes are defined."""
        positions = {}
        pattern = r'^class (\w+)\('

        for i, line in enumerate(content.split('\n'), 1):
            match = re.match(pattern, line)
            if match:
                positions[match.group(1)] = i

        return positions

    def get_class_inheritance(self, content: str, class_name: str) -> List[str]:
        """Get current parent classes for a class."""
        pattern = rf'^class {re.escape(class_name)}\(([^)]+)\):'

        for line in content.split('\n'):
            match = re.match(pattern, line)
            if match:
                parents_str = match.group(1)
                return [p.strip() for p in parents_str.split(',')]

        return []

    def analyze_class(
        self,
        impl_class: str,
        current_parents: List[str],
        stub_relationships: Dict[str, str],
        class_positions: Dict[str, int]
    ) -> InheritanceInfo:
        """Determine if class should use multiple inheritance."""

        line_num = class_positions.get(impl_class, 0)

        # Already has multiple inheritance?
        if len(current_parents) > 1:
            return InheritanceInfo(
                impl_class=impl_class,
                line_number=line_num,
                current_parents=current_parents,
                should_have_parents=current_parents,
                can_apply=False,
                reason="Already uses multiple inheritance"
            )

        if len(current_parents) != 1:
            return InheritanceInfo(
                impl_class=impl_class,
                line_number=line_num,
                current_parents=current_parents,
                should_have_parents=current_parents,
                can_apply=False,
                reason="No parents found"
            )

        stub_parent = current_parents[0]

        # Not a stub?
        if not stub_parent.endswith('Stub'):
            return InheritanceInfo(
                impl_class=impl_class,
                line_number=line_num,
                current_parents=current_parents,
                should_have_parents=current_parents,
                can_apply=False,
                reason="Parent is not a stub"
            )

        # Check stub inheritance
        if stub_parent not in stub_relationships:
            # Stub has no parent stub - this is a base class
            return InheritanceInfo(
                impl_class=impl_class,
                line_number=line_num,
                current_parents=current_parents,
                should_have_parents=current_parents,
                can_apply=False,
                reason="Stub has no parent stub (base class)"
            )

        # Get the parent stub's parent
        parent_stub = stub_relationships[stub_parent]
        full_fat_parent = parent_stub.replace('Stub', '')

        # Check if full-fat parent exists in this file
        if full_fat_parent not in class_positions:
            return InheritanceInfo(
                impl_class=impl_class,
                line_number=line_num,
                current_parents=current_parents,
                should_have_parents=[stub_parent, full_fat_parent],
                can_apply=False,
                reason=f"{full_fat_parent} not in this file"
            )

        # Check definition order
        parent_line = class_positions[full_fat_parent]

        if parent_line >= line_num:
            return InheritanceInfo(
                impl_class=impl_class,
                line_number=line_num,
                current_parents=current_parents,
                should_have_parents=[stub_parent, full_fat_parent],
                can_apply=False,
                reason=f"{full_fat_parent} defined later (line {parent_line} >= {line_num})"
            )

        # All checks passed!
        return InheritanceInfo(
            impl_class=impl_class,
            line_number=line_num,
            current_parents=current_parents,
            should_have_parents=[stub_parent, full_fat_parent],
            can_apply=True,
            reason=f"Can add {full_fat_parent} (line {parent_line} < {line_num})"
        )

    def apply_multiple_inheritance(self, content: str, info: InheritanceInfo) -> Tuple[str, bool]:
        """Apply multiple inheritance to a class."""
        if not info.can_apply:
            return content, False

        lines = content.split('\n')
        stub_parent = info.should_have_parents[0]
        full_fat_parent = info.should_have_parents[1]

        # Find class definition
        pattern = rf'^(\s*)class {re.escape(info.impl_class)}\({re.escape(stub_parent)}\):'

        for i, line in enumerate(lines):
            if re.match(pattern, line):
                # Replace with multiple inheritance
                indent = re.match(r'^(\s*)', line).group(1)
                new_line = f'{indent}class {info.impl_class}({stub_parent}, {full_fat_parent}):'
                lines[i] = new_line

                # Add docstring explanation
                for j in range(i + 1, min(i + 10, len(lines))):
                    if '"""' in lines[j]:
                        # Add inheritance info after opening """
                        inheritance_doc = [
                            f'{indent}    ',
                            f'{indent}    Inherits from:',
                            f'{indent}    - {stub_parent}: Metadata and structure',
                            f'{indent}    - {full_fat_parent}: Shared full-fat methods',
                        ]

                        # Insert after opening docstring
                        for doc_line in reversed(inheritance_doc):
                            lines.insert(j + 1, doc_line)
                        break

                return '\n'.join(lines), True

        return content, False

    def process_file(self, impl_path: Path, stub_path: Path) -> Dict:
        """Process a single file."""
        print(f"\nProcessing {impl_path.name}...")

        # Parse stub relationships
        stub_relationships = self.parse_stub_inheritance(stub_path)

        if not stub_relationships:
            print(f"  No stub inheritance relationships found")
            return {'file': impl_path.name, 'modified': False}

        # Read implementation
        content = impl_path.read_text()
        original_content = content

        # Get class positions
        class_positions = self.get_class_positions(content)

        # Analyze each implementation class
        to_update = []

        for impl_class in class_positions.keys():
            if impl_class.endswith('Stub'):
                continue

            current_parents = self.get_class_inheritance(content, impl_class)
            if not current_parents:
                continue

            info = self.analyze_class(
                impl_class,
                current_parents,
                stub_relationships,
                class_positions
            )

            if info.can_apply:
                to_update.append(info)
                print(f"  ✓ {impl_class}: {info.reason}")
            elif "defined later" in info.reason:
                print(f"  ⚠ {impl_class}: {info.reason}")

        # Apply changes
        modified = False
        for info in to_update:
            content, was_modified = self.apply_multiple_inheritance(content, info)
            if was_modified:
                modified = True
                self.changes[impl_path.name].append(
                    f"✓ {info.impl_class}: Added {info.should_have_parents[1]}"
                )

        # Write if modified
        if modified and not self.dry_run:
            backup_path = impl_path.with_suffix('.py.backup')
            shutil.copy2(impl_path, backup_path)
            impl_path.write_text(content)

        return {
            'file': impl_path.name,
            'modified': modified,
            'count': len(to_update)
        }

    def process_all(self):
        """Process all CCP4*.py files."""
        core_dir = Path(__file__).parent / 'core'
        stub_dir = core_dir / 'cdata_stubs'

        print("="*80)
        print(f"Multiple Inheritance Refactoring")
        print(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE'}")
        print("="*80)

        impl_files = sorted(core_dir.glob('CCP4*.py'))
        reports = []

        for impl_file in impl_files:
            stub_file = stub_dir / impl_file.name
            if stub_file.exists():
                report = self.process_file(impl_file, stub_file)
                reports.append(report)

        self.print_summary(reports)

    def print_summary(self, reports: List[Dict]):
        """Print summary."""
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)

        total_files = len(reports)
        modified_files = sum(1 for r in reports if r['modified'])
        total_classes = sum(r.get('count', 0) for r in reports)

        print(f"\nFiles analyzed: {total_files}")
        print(f"Files modified: {modified_files}")
        print(f"Classes updated: {total_classes}")

        if self.changes:
            print("\n" + "="*80)
            print("CHANGES")
            print("="*80)
            for filename, changes in sorted(self.changes.items()):
                print(f"\n{filename}:")
                for change in changes:
                    print(f"  {change}")

        if self.dry_run:
            print("\n⚠️  DRY RUN - Run with --apply to make changes")
        else:
            print("\n✓ Changes applied!")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Apply multiple inheritance')
    parser.add_argument('--apply', action='store_true', help='Apply changes')
    parser.add_argument('--file', type=str, help='Process single file')

    args = parser.parse_args()

    refactor = MultipleInheritanceRefactor(dry_run=not args.apply)

    if args.file:
        core_dir = Path(__file__).parent / 'core'
        stub_dir = core_dir / 'cdata_stubs'
        impl_path = core_dir / args.file
        stub_path = stub_dir / args.file

        if not impl_path.exists() or not stub_path.exists():
            print(f"Error: Files not found")
            return

        report = refactor.process_file(impl_path, stub_path)
        refactor.print_summary([report])
    else:
        refactor.process_all()


if __name__ == '__main__':
    main()
