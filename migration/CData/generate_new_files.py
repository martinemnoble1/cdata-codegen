import json
import subprocess
from pathlib import Path

# Type mapping from JSON to AttributeType
TYPE_MAP = {
    "str": "AttributeType.STRING",
    "int": "AttributeType.INT",
    "float": "AttributeType.FLOAT",
    "bool": "AttributeType.BOOLEAN",
    "CString": "AttributeType.STRING",
    "CInt": "AttributeType.INT",
    "CFloat": "AttributeType.FLOAT",
    "CBoolean": "AttributeType.BOOLEAN",
    # Add more as needed
}


def map_type(type_str):
    return TYPE_MAP.get(type_str, "AttributeType.CUSTOM")


def render_attribute(attr_name, attr_info):
    type_str = attr_info.get("class", "str")
    # Clean up type string if it looks like "<class 'float'>"
    if (
        isinstance(type_str, str)
        and type_str.startswith("<class '")
        and type_str.endswith("'>")
    ):
        type_str = type_str[8:-2]
    tooltip = attr_info.get("tooltip", f"{attr_name} attribute")
    mapped_type = map_type(type_str)

    if mapped_type == "AttributeType.CUSTOM":
        # Not a recognised fundamental type, treat as custom
        return f'"{attr_name}": attribute(AttributeType.CUSTOM, custom_class="{type_str}", tooltip="{tooltip}")'
    else:
        return f'"{attr_name}": attribute({mapped_type}, tooltip="{tooltip}")'


def render_class(name, data):
    base = data.get("immediate_parent", "CData")
    doc = data.get("docstring", f"Generated {name} class from CData metadata.")
    attributes = data.get("CONTENTS", {})
    error_codes = data.get("ERROR_CODES", {})
    qualifiers = data.get("QUALIFIERS", {})
    contents_order = data.get("CONTENTS_ORDER", [])
    qualifiers_order = data.get("QUALIFIERS_ORDER", [])
    qualifiers_definition = data.get("QUALIFIERS_DEFINITION", {})

    # Normalize 'type' fields in qualifiers_definition
    def normalize_type(type_val):
        if (
            isinstance(type_val, str)
            and type_val.startswith("<class '")
            and type_val.endswith("'>")
        ):
            return type_val[8:-2]
        return type_val

    if isinstance(qualifiers_definition, dict):
        for qname, qdef in qualifiers_definition.items():
            if isinstance(qdef, dict) and "type" in qdef:
                qdef["type"] = normalize_type(qdef["type"])
    gui_label = data.get("gui_label", name)

    # Filter qualifiers to exclude members whose value is "NotImplemented"
    if isinstance(qualifiers, dict):
        qualifiers = {k: v for k, v in qualifiers.items() if v != "NotImplemented"}

    # Map boolean qualifier values from JSON (true/false) to Python (True/False)
    if isinstance(qualifiers, dict):
        for k, v in qualifiers.items():
            if v is True:
                qualifiers[k] = True
            elif v is False:
                qualifiers[k] = False
    lines = []
    lines.append(f"@cdata_class(")
    if attributes:
        attr_lines = ",\n        ".join(
            [render_attribute(k, v) for k, v in attributes.items()]
        )
        lines.append(f"    attributes={{\n        {attr_lines}\n    }},")
    if error_codes:
        lines.append(f"    error_codes={json.dumps(error_codes, indent=8)},")
    if qualifiers:
        # Render qualifiers as Python code, not JSON
        def render_qualifiers(qdict):
            items = []
            for k, v in qdict.items():
                items.append(f'"{k}": {repr(v)}')
            return "{\n        " + ",\n        ".join(items) + "\n    }"

        lines.append(f"    qualifiers={render_qualifiers(qualifiers)},")
    if contents_order:
        lines.append(f"    contents_order={contents_order},")
    if qualifiers_order:
        # Render qualifiers as Python code, not JSON
        def render_qualifiers_order(qlist):
            items = []
            for k, v in enumerate(qlist):
                items.append(f"{repr(v)}")
            return "[\n        " + ",\n        ".join(items) + "\n    ]"

        lines.append(
            f"    qualifiers_order={render_qualifiers_order(qualifiers_order)},"
        )
    if qualifiers_definition:
        # Render qualifiers_definition with type values as Python objects
        def py_type(type_str):
            mapping = {
                "str": "str",
                "int": "int",
                "float": "float",
                "bool": "bool",
                "dict": "dict",
                "list": "list",
            }
            return mapping.get(type_str, f'"{type_str}"')

        def render_qualdef(qdef):
            if isinstance(qdef, dict):
                items = []
                for k, v in qdef.items():
                    if k == "type":
                        tval = v
                        if (
                            isinstance(tval, str)
                            and tval.startswith("<class '")
                            and tval.endswith("'>")
                        ):
                            tval = tval[8:-2]
                        items.append(f'"type": {py_type(tval)}')
                    else:
                        items.append(
                            f'"{k}": {json.dumps(v if not isinstance(v, bool) else repr(v))}'
                        )
                return "{ " + ", ".join(items) + " }"
            else:
                return json.dumps(qdef)

        qualdef_lines = []
        for qname, qdef in qualifiers_definition.items():
            qualdef_lines.append(f'        "{qname}": {render_qualdef(qdef)}')
        lines.append(
            "    qualifiers_definition={\n" + ",\n".join(qualdef_lines) + "\n    },"
        )
    lines.append(f'    gui_label="{gui_label}",')
    lines.append(")")
    lines.append(f"class {name}({base}):")
    lines.append(f'    """{doc}"""')
    lines.append("    pass\n")
    return "\n".join(lines)


def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def topo_sort_classes(class_list):
    # class_list: list of (name, class_data)
    # Build dependency graph
    name_map = {name: data for name, data in class_list}
    graph = {name: set() for name, _ in class_list}
    for name, data in class_list:
        parent = data.get("immediate_parent")
        if parent and parent in graph:
            graph[name].add(parent)
    # Kahn's algorithm for topological sort
    sorted_classes = []
    no_deps = [name for name, deps in graph.items() if not deps]
    print(no_deps)
    while no_deps:
        n = no_deps.pop()
        sorted_classes.append((n, name_map[n]))
        for m in graph:
            if n in graph[m]:
                graph[m].remove(n)
        graph.pop(n)
        # Recompute no_deps after removal
        no_deps = [name for name, deps in graph.items() if not deps]
    # If any remain, these are in a cycle
    if graph:
        print(
            "Warning: Circular dependency detected among classes:",
            list(graph.keys()),
        )
        # Output cyclic classes in original order
        for name in graph:
            sorted_classes.append((name, name_map[name]))
    return sorted_classes


def main():
    migration_dir = Path(__file__).resolve().parent
    data = load_json(migration_dir / "cdata.json")
    classes = data.get("classes", {})
    # Exclude fundamental classes from processing
    # fundamental_classes = {"CInt", "CString", "CFloat", "CBoolean", "COneWord"}
    # classes = {k: v for k, v in classes.items() if k not in fundamental_classes}
    # Set your output directory here
    out_dir = migration_dir.parent.parent / "core" / "cdata_stubs"
    print(f"Output directory: {out_dir}")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Group classes by file_path basename
    file_class_map = {"CCP4BaseFile.py": []}
    for name, class_data in classes.items():
        file_path = class_data.get("file_path", "unknown.py")
        basename = Path(file_path).name
        if name in [
            "CDataFile",
            "CDataFileContent",
            "CXmlDataFile",
            "CI2XmlDataFile"
        ]:
            basename = "CCP4BaseFile.py"
        if name in [
            "CInt",
            "CString",
            "CFloat",
            "CBoolean",
            "CList"
        ]:
            basename = "CCP4FundamentalTypes.py"
        if basename not in file_class_map:
            file_class_map[basename] = []
        file_class_map[basename].append((name, class_data))

    for basename, class_list in file_class_map.items():
        sorted_class_data = topo_sort_classes(class_list)
        # Sort class_list so base classes come first
        out_path = out_dir / basename.replace(".py", "Stub.py")
        print(f"Writing {len(sorted_class_data)} classes to {out_path}")
        with out_path.open("w", encoding="utf-8") as f:
            # Write file header and imports
            f.write(f'"""Generated classes from {basename}"""\n\n')
            f.write(
                "from ..base_object.base_classes import CData, CContainer\n"
            )
            f.write(
                "from ..base_object.fundamental_types import CInt, CList, CBoolean, CFloat, "
                "CString\n"
            )
            f.write(
                "from ..base_object.class_metadata import cdata_class, attribute, "
                "AttributeType\n\n"
            )
            if basename not in ["CCP4BaseFile.py"]:
                f.write(
                    "from .CCP4BaseFileStub import CDataFileContent, CDataFile, "
                    "CXmlDataFile, CI2XmlDataFile\n\n"
                )
            # Write all classes for this file
            for name, class_data in sorted_class_data:
                f.write(render_class(name, class_data))
                f.write("\n")
        # Format the file with autopep8 for PEP8 compliance
        try:
            subprocess.run([
                "autopep8", "--in-place", str(out_path)
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Warning: autopep8 formatting failed for {out_path}: {e}")


if __name__ == "__main__":
    main()
