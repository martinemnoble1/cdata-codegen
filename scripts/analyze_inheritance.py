#!/usr/bin/env python3
"""
Analyze stub inheritance to identify where full-fat classes should use multiple inheritance.
"""

import re
from pathlib import Path
from collections import defaultdict

def parse_stub_inheritance(stub_file):
    """Parse stub file to extract class inheritance relationships."""
    content = stub_file.read_text()

    # Pattern: class ChildStub(ParentStub):
    pattern = r'^class (\w+Stub)\((\w+)\):'

    relationships = {}
    for match in re.finditer(pattern, content, re.MULTILINE):
        child = match.group(1)
        parent = match.group(2)

        # Only track if parent is also a Stub class (not CData, CContainer, etc.)
        if parent.endswith('Stub') or parent in ['CData', 'CContainer', 'CDataFile', 'CDataFileContent']:
            relationships[child] = parent

    return relationships

def parse_implementation_classes(impl_file):
    """Parse implementation file to see current inheritance."""
    content = impl_file.read_text()

    # Pattern: class Child(Parent1, Parent2, ...):
    pattern = r'^class (\w+)\(([^)]+)\):'

    implementations = {}
    for match in re.finditer(pattern, content, re.MULTILINE):
        child = match.group(1)
        parents = [p.strip() for p in match.group(2).split(',')]
        implementations[child] = parents

    return implementations

def analyze_file(stub_path, impl_path):
    """Analyze a single pair of stub/implementation files."""
    print(f"\n{'='*80}")
    print(f"File: {impl_path.name}")
    print(f"{'='*80}")

    stub_relationships = parse_stub_inheritance(stub_path)
    impl_classes = parse_implementation_classes(impl_path)

    # Build recommendations
    recommendations = []

    for stub_class, stub_parent in stub_relationships.items():
        # Get the implementation class name (remove "Stub" suffix)
        impl_class = stub_class.replace('Stub', '')
        full_fat_parent = stub_parent.replace('Stub', '')

        # Check if implementation exists
        if impl_class not in impl_classes:
            continue

        # Check current inheritance
        current_parents = impl_classes[impl_class]

        # Should inherit from both stub and full-fat parent
        expected_parents = [stub_class, full_fat_parent]

        # Skip if parent is a base class (CData, CContainer, etc.)
        if full_fat_parent in ['CData', 'CContainer', 'CDataFile', 'CDataFileContent']:
            continue

        # Check if missing full-fat parent
        if stub_class in current_parents and full_fat_parent not in current_parents:
            recommendations.append({
                'class': impl_class,
                'current': current_parents,
                'should_add': full_fat_parent,
                'recommended': expected_parents
            })

    if recommendations:
        print(f"\n{len(recommendations)} classes should use multiple inheritance:\n")
        for rec in recommendations:
            print(f"  {rec['class']}:")
            print(f"    Current:     {', '.join(rec['current'])}")
            print(f"    Should be:   {', '.join(rec['recommended'])}")
            print()
    else:
        print("\n✓ All classes already using correct inheritance pattern")

    return recommendations

def main():
    """Analyze all CCP4*.py files."""
    core_dir = Path(__file__).parent / 'core'
    stub_dir = core_dir / 'cdata_stubs'

    all_recommendations = []

    # Find all CCP4*.py implementation files
    impl_files = sorted(core_dir.glob('CCP4*.py'))

    for impl_file in impl_files:
        stub_file = stub_dir / impl_file.name

        if not stub_file.exists():
            continue

        recs = analyze_file(stub_file, impl_file)
        if recs:
            all_recommendations.extend([(impl_file.name, rec) for rec in recs])

    # Summary
    print(f"\n{'='*80}")
    print(f"SUMMARY")
    print(f"{'='*80}")
    print(f"\nTotal files analyzed: {len(impl_files)}")
    print(f"Total classes needing multiple inheritance: {len(all_recommendations)}")

    if all_recommendations:
        print("\n\nClasses by file:")
        by_file = defaultdict(list)
        for filename, rec in all_recommendations:
            by_file[filename].append(rec['class'])

        for filename, classes in sorted(by_file.items()):
            print(f"\n{filename}:")
            for cls in classes:
                print(f"  - {cls}")

if __name__ == '__main__':
    main()
