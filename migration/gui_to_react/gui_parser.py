#!/usr/bin/env python3
"""
Parse legacy CCP4i2 Python GUI definitions and generate React TSX interfaces.

This parses the drawContents() method of CTaskWidget subclasses and extracts:
- openFolder() calls -> Tabs (CCP4i2Tab)
- createLine() calls -> CCP4i2TaskElement components
- openSubFrame/closeSubFrame() -> CCP4i2ContainerElement sections
- toggle parameters -> visibility conditions
- for loops -> expanded into individual elements
"""

import ast
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class GuiElement:
    """Represents a GUI element from the legacy interface"""
    element_type: str  # 'line', 'folder', 'subframe_open', 'subframe_close', 'subtitle'
    params: List[Any] = field(default_factory=list)
    kwargs: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ParsedGui:
    """Parsed GUI structure"""
    task_name: str
    title: str
    elements: List[GuiElement] = field(default_factory=list)
    task_module: str = ''
    description: str = ''


class GuiParser:
    """Parse legacy Python GUI definitions"""

    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.source = self.filepath.read_text()
        self.tree = ast.parse(self.source)

    def parse(self) -> ParsedGui:
        """Parse the GUI file and return structured data"""
        # Find the class definition
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                if 'CTaskWidget' in [self._get_base_name(b) for b in node.bases]:
                    return self._parse_class(node)

        raise ValueError(f"No CTaskWidget subclass found in {self.filepath}")

    def _get_base_name(self, base) -> str:
        """Get the name of a base class"""
        if isinstance(base, ast.Name):
            return base.id
        elif isinstance(base, ast.Attribute):
            return base.attr
        return ''

    def _parse_class(self, class_node: ast.ClassDef) -> ParsedGui:
        """Parse a CTaskWidget class"""
        result = ParsedGui(task_name=class_node.name, title=class_node.name)

        # Build a map of all methods in the class for following self.methodName() calls
        self.class_methods: Dict[str, ast.FunctionDef] = {}
        for node in class_node.body:
            if isinstance(node, ast.FunctionDef):
                self.class_methods[node.name] = node

        # Extract class attributes
        for node in class_node.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        value = self._eval_node(node.value)
                        if target.id == 'TASKNAME':
                            result.task_name = value
                        elif target.id == 'TASKTITLE':
                            result.title = value
                        elif target.id == 'TASKMODULE':
                            result.task_module = value
                        elif target.id == 'DESCRIPTION':
                            result.description = value

            # Find drawContents method
            elif isinstance(node, ast.FunctionDef) and node.name == 'drawContents':
                result.elements = self._parse_draw_contents(node)

        return result

    def _parse_draw_contents(self, func_node: ast.FunctionDef) -> List[GuiElement]:
        """Parse the drawContents method - walks body in order to preserve sequence"""
        elements = []
        self._parse_statements(func_node.body, elements, {})
        return elements

    def _parse_statements(self, statements: List[ast.stmt], elements: List[GuiElement],
                          loop_vars: Dict[str, Any]):
        """Parse a list of statements, handling control flow properly"""
        for stmt in statements:
            # Get the call from either expression or assignment
            call = None
            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                call = stmt.value
            elif isinstance(stmt, ast.Assign) and isinstance(stmt.value, ast.Call):
                # Handle assignments like: folder = self.openFolder(...)
                call = stmt.value

            if call:
                func_name = self._get_call_name(call)

                if func_name == 'openFolder':
                    elements.append(self._parse_open_folder(call))
                elif func_name == 'closeFolder':
                    elements.append(GuiElement('folder_close'))
                elif func_name == 'createLine':
                    elements.append(self._parse_create_line(call, loop_vars))
                elif func_name == 'openSubFrame':
                    elements.append(self._parse_open_subframe(call))
                elif func_name == 'closeSubFrame':
                    elements.append(GuiElement('subframe_close'))
                elif self._is_self_method_call(call):
                    # Follow self.methodName() calls to other drawing methods
                    method_name = self._get_self_method_name(call)
                    if method_name and method_name in self.class_methods:
                        method_node = self.class_methods[method_name]
                        self._parse_statements(method_node.body, elements, loop_vars)

            elif isinstance(stmt, ast.For):
                # Handle for loops by expanding them
                self._expand_for_loop(stmt, elements, loop_vars)

            elif isinstance(stmt, ast.If):
                # Handle if statements - parse both branches
                # For simplicity, we'll just parse the if body (not else)
                # A more complete implementation would track conditions
                self._parse_statements(stmt.body, elements, loop_vars)

    def _is_self_method_call(self, call: ast.Call) -> bool:
        """Check if this is a self.methodName() call"""
        if isinstance(call.func, ast.Attribute):
            if isinstance(call.func.value, ast.Name) and call.func.value.id == 'self':
                return True
        return False

    def _get_self_method_name(self, call: ast.Call) -> Optional[str]:
        """Get method name from self.methodName() call"""
        if isinstance(call.func, ast.Attribute):
            if isinstance(call.func.value, ast.Name) and call.func.value.id == 'self':
                return call.func.attr
        return None

    def _expand_for_loop(self, for_stmt: ast.For, elements: List[GuiElement],
                         loop_vars: Dict[str, Any]):
        """Expand a for loop by iterating over its values"""
        # Get the loop variable name
        if isinstance(for_stmt.target, ast.Name):
            var_name = for_stmt.target.id
        else:
            # Complex target like tuple unpacking - skip for now
            return

        # Get the iterable values
        iter_values = self._eval_node(for_stmt.iter)
        if not isinstance(iter_values, list):
            return

        # Expand the loop body for each value
        for val in iter_values:
            new_loop_vars = loop_vars.copy()
            new_loop_vars[var_name] = val
            self._parse_statements(for_stmt.body, elements, new_loop_vars)

    def _get_call_name(self, call: ast.Call) -> str:
        """Get the name of a function call"""
        if isinstance(call.func, ast.Name):
            return call.func.id
        elif isinstance(call.func, ast.Attribute):
            return call.func.attr
        return ''

    def _eval_node(self, node, loop_vars: Dict[str, Any] = None) -> Any:
        """Safely evaluate an AST node to get its value, with loop variable substitution"""
        if loop_vars is None:
            loop_vars = {}

        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.List):
            return [self._eval_node(e, loop_vars) for e in node.elts]
        elif isinstance(node, ast.Dict):
            return {self._eval_node(k, loop_vars): self._eval_node(v, loop_vars)
                    for k, v in zip(node.keys, node.values)}
        elif isinstance(node, ast.Name):
            # Check if this is a loop variable
            if node.id in loop_vars:
                return loop_vars[node.id]
            if node.id == 'True':
                return True
            elif node.id == 'False':
                return False
            return node.id
        elif isinstance(node, ast.JoinedStr):
            # f-string - evaluate each part
            parts = []
            for value in node.values:
                if isinstance(value, ast.Constant):
                    parts.append(str(value.value))
                elif isinstance(value, ast.FormattedValue):
                    val = self._eval_node(value.value, loop_vars)
                    # Handle format spec like :02d
                    if value.format_spec:
                        fmt = self._eval_node(value.format_spec, loop_vars)
                        parts.append(f"{val:{fmt}}")
                    else:
                        parts.append(str(val))
            return ''.join(parts)
        elif isinstance(node, ast.Call):
            # Handle function calls like str(i)
            func_name = self._get_call_name(node)
            if func_name == 'str' and node.args:
                return str(self._eval_node(node.args[0], loop_vars))
            elif func_name == 'int' and node.args:
                return int(self._eval_node(node.args[0], loop_vars))
        elif isinstance(node, ast.BinOp):
            # Handle binary operations like i + 1
            left = self._eval_node(node.left, loop_vars)
            right = self._eval_node(node.right, loop_vars)
            if isinstance(node.op, ast.Add):
                return left + right
            elif isinstance(node.op, ast.Sub):
                return left - right
            elif isinstance(node.op, ast.Mult):
                return left * right
            elif isinstance(node.op, ast.Mod):
                # Handle string formatting like "%02d" % i
                if isinstance(left, str) and '%' in left:
                    return left % right
                return left % right
        return None

    def _parse_open_folder(self, call: ast.Call) -> GuiElement:
        """Parse openFolder call"""
        kwargs = {}
        for kw in call.keywords:
            kwargs[kw.arg] = self._eval_node(kw.value)
        return GuiElement('folder', kwargs=kwargs)

    def _parse_create_line(self, call: ast.Call, loop_vars: Dict[str, Any] = None) -> GuiElement:
        """Parse createLine call with loop variable substitution"""
        if loop_vars is None:
            loop_vars = {}

        params = []
        kwargs = {}

        for arg in call.args:
            params.append(self._eval_node(arg, loop_vars))

        for kw in call.keywords:
            kwargs[kw.arg] = self._eval_node(kw.value, loop_vars)

        return GuiElement('line', params=params, kwargs=kwargs)

    def _parse_open_subframe(self, call: ast.Call) -> GuiElement:
        """Parse openSubFrame call"""
        kwargs = {}
        for kw in call.keywords:
            kwargs[kw.arg] = self._eval_node(kw.value)
        return GuiElement('subframe_open', kwargs=kwargs)


class ReactGenerator:
    """Generate React TSX from parsed GUI"""

    def __init__(self, parsed: ParsedGui):
        self.parsed = parsed
        self.indent = 0
        self.lines = []
        self.toggle_vars = set()  # Track which variables we need to watch
        self.current_toggles = []  # Stack of active toggle conditions
        self.has_containers = False  # Track if we need CCP4i2ContainerElement
        self.has_subtitles = False  # Track if we have subtitles (Typography)

    def generate(self) -> str:
        """Generate the React TSX code"""
        self._analyze_elements()
        self._emit_header()
        self._emit_component()
        self._emit_footer()
        return '\n'.join(self.lines)

    def _analyze_elements(self):
        """Analyze elements to determine what we need to import"""
        for elem in self.parsed.elements:
            if elem.element_type == 'line':
                # Check for toggle
                if 'toggle' in elem.kwargs:
                    toggle = elem.kwargs['toggle']
                    if isinstance(toggle, list) and len(toggle) >= 1:
                        self.toggle_vars.add(toggle[0])
                # Check for subtitle or advice (both use Typography)
                params = elem.params[0] if elem.params else []
                if 'subtitle' in params or 'advice' in params:
                    self.has_subtitles = True

            elif elem.element_type == 'subframe_open':
                # Check for toggle
                if 'toggle' in elem.kwargs:
                    toggle = elem.kwargs['toggle']
                    if isinstance(toggle, list) and len(toggle) >= 1:
                        self.toggle_vars.add(toggle[0])
                # Check for title or frame - means we use CCP4i2ContainerElement
                if 'title' in elem.kwargs:
                    self.has_containers = True
                # Check for frame=True or frame=[True]
                frame = elem.kwargs.get('frame')
                if frame is True or frame == [True]:
                    self.has_containers = True

    def _emit(self, text: str):
        """Emit a line with current indentation"""
        self.lines.append('  ' * self.indent + text)

    def _strip_html(self, text: str) -> str:
        """Remove HTML tags from text and convert to plain text"""
        if not text:
            return text
        # Common HTML entities
        text = text.replace('<br/>', ' ').replace('<br>', ' ')
        text = text.replace('&lt;', '<').replace('&gt;', '>')
        text = text.replace('&amp;', '&')
        # Remove remaining tags
        import re
        text = re.sub(r'<[^>]+>', '', text)
        return text.strip()

    def _escape_jsx_content(self, text: str) -> str:
        """Escape text for use as JSX content (not attribute values)"""
        if not text:
            return text
        # Escape characters that are special in JSX
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('{', '&#123;')
        text = text.replace('}', '&#125;')
        return text

    def _emit_header(self):
        """Emit the header imports

        Note: These paths are for files in the generated/ subfolder.
        """
        # Build MUI imports
        mui_imports = ['LinearProgress', 'Paper']
        if self.has_subtitles:
            mui_imports.append('Typography')
        self._emit(f'import {{ {", ".join(mui_imports)} }} from "@mui/material";')

        # Import paths relative to generated/ subfolder
        self._emit('import { CCP4i2TaskInterfaceProps } from "../task-container";')
        self._emit('import { CCP4i2TaskElement } from "../../task-elements/task-element";')
        self._emit('import { CCP4i2Tab, CCP4i2Tabs } from "../../task-elements/tabs";')
        if self.has_containers:
            self._emit('import { CCP4i2ContainerElement } from "../../task-elements/ccontainer";')
        self._emit('import { useJob } from "../../../../utils";')
        if self.toggle_vars:
            self._emit('import { useMemo } from "react";')
        self._emit('')

    def _emit_component(self):
        """Emit the main component"""
        self._emit('const TaskInterface: React.FC<CCP4i2TaskInterfaceProps> = (props) => {')
        self.indent += 1

        self._emit('const { useTaskItem, container } = useJob(props.job.id);')

        # Emit toggle variable watches
        for var in sorted(self.toggle_vars):
            self._emit(f'const {{ value: {var} }} = useTaskItem("{var}");')

        self._emit('')
        self._emit('if (!container) return <LinearProgress />;')
        self._emit('')

        self._emit('return (')
        self.indent += 1
        self._emit('<Paper>')
        self.indent += 1
        self._emit('<CCP4i2Tabs>')
        self.indent += 1

        self._emit_elements()

        self.indent -= 1
        self._emit('</CCP4i2Tabs>')
        self.indent -= 1
        self._emit('</Paper>')
        self.indent -= 1
        self._emit(');')

        self.indent -= 1
        self._emit('};')

    def _emit_elements(self):
        """Emit the GUI elements"""
        current_folder = None
        subframe_stack = []  # Track open subframes
        folder_count = 0  # Track folder count for unique keys

        for elem in self.parsed.elements:
            if elem.element_type == 'folder':
                # Close any remaining subframes from previous folder
                while subframe_stack:
                    frame_info = subframe_stack.pop()
                    if frame_info['title'] or frame_info.get('frame'):
                        self.indent -= 1
                        self._emit('</CCP4i2ContainerElement>')
                        if frame_info['toggle']:
                            self.indent -= 1
                            self._emit(')}')
                    elif frame_info['toggle']:
                        self.indent -= 1
                        self._emit('</>')
                        self.indent -= 1
                        self._emit(')}')
                # Close previous folder if open
                if current_folder is not None:
                    self.indent -= 1
                    self._emit('</CCP4i2Tab>')

                # Open new folder
                title = elem.kwargs.get('title', 'Input data')
                folder_func = elem.kwargs.get('folderFunction', f'folder_{folder_count}')
                folder_count += 1
                self._emit(f'<CCP4i2Tab key="{folder_func}" label="{title}">')
                self.indent += 1
                current_folder = folder_func

            elif elem.element_type == 'line':
                self._emit_line(elem)

            elif elem.element_type == 'subframe_open':
                toggle = elem.kwargs.get('toggle')
                title = elem.kwargs.get('title')
                frame = elem.kwargs.get('frame')
                is_framed = frame is True or frame == [True]

                if title:
                    # Use CCP4i2ContainerElement for titled subframes with FolderLevel
                    title_escaped = self._strip_html(title).replace('"', '\\"')
                    if toggle:
                        condition = self._make_toggle_condition(toggle)
                        self._emit(f'{{({condition}) && (')
                        self.indent += 1
                    self._emit(f'<CCP4i2ContainerElement')
                    self.indent += 1
                    self._emit('{...props}')
                    self._emit('itemName=""')
                    self._emit(f'qualifiers={{{{ guiLabel: "{title_escaped}", initiallyOpen: true }}}}')
                    self._emit('containerHint="FolderLevel"')
                    self.indent -= 1
                    self._emit('>')
                    self.indent += 1
                    subframe_stack.append({'title': title, 'toggle': toggle, 'frame': False})
                elif is_framed:
                    # Use CCP4i2ContainerElement for framed subframes with BlockLevel
                    if toggle:
                        condition = self._make_toggle_condition(toggle)
                        self._emit(f'{{({condition}) && (')
                        self.indent += 1
                    self._emit(f'<CCP4i2ContainerElement')
                    self.indent += 1
                    self._emit('{...props}')
                    self._emit('itemName=""')
                    self._emit('qualifiers={{ initiallyOpen: true }}')
                    self._emit('containerHint="BlockLevel"')
                    self.indent -= 1
                    self._emit('>')
                    self.indent += 1
                    subframe_stack.append({'title': None, 'toggle': toggle, 'frame': True})
                elif toggle:
                    # Toggle-only subframe (no title, no frame)
                    condition = self._make_toggle_condition(toggle)
                    self._emit(f'{{({condition}) && (')
                    self.indent += 1
                    self._emit('<>')
                    self.indent += 1
                    subframe_stack.append({'title': None, 'toggle': toggle, 'frame': False})
                else:
                    # Plain subframe without toggle, title, or frame
                    subframe_stack.append({'title': None, 'toggle': None, 'frame': False})

            elif elem.element_type == 'subframe_close':
                if subframe_stack:
                    frame_info = subframe_stack.pop()
                    if frame_info['title'] or frame_info.get('frame'):
                        # Close CCP4i2ContainerElement (titled or framed)
                        self.indent -= 1
                        self._emit('</CCP4i2ContainerElement>')
                        if frame_info['toggle']:
                            self.indent -= 1
                            self._emit(')}')
                    elif frame_info['toggle']:
                        # Close toggle-only fragment
                        self.indent -= 1
                        self._emit('</>')
                        self.indent -= 1
                        self._emit(')}')

            elif elem.element_type == 'folder_close':
                # Explicit folder close - first close any open subframes
                while subframe_stack:
                    frame_info = subframe_stack.pop()
                    if frame_info['title'] or frame_info.get('frame'):
                        # Close CCP4i2ContainerElement (titled or framed)
                        self.indent -= 1
                        self._emit('</CCP4i2ContainerElement>')
                        if frame_info['toggle']:
                            self.indent -= 1
                            self._emit(')}')
                    elif frame_info['toggle']:
                        # Close toggle-only fragment
                        self.indent -= 1
                        self._emit('</>')
                        self.indent -= 1
                        self._emit(')}')
                # Then close current tab
                if current_folder is not None:
                    self.indent -= 1
                    self._emit('</CCP4i2Tab>')
                    current_folder = None

        # Close last folder
        if current_folder is not None:
            self.indent -= 1
            self._emit('</CCP4i2Tab>')

    def _emit_line(self, elem: GuiElement):
        """Emit a createLine element"""
        params = elem.params[0] if elem.params else []

        # Handle 'advice' lines as help text
        if 'advice' in params:
            idx = params.index('advice')
            if idx + 1 < len(params):
                # Strip HTML then escape for JSX content
                advice_text = self._strip_html(str(params[idx + 1]))
                advice_escaped = self._escape_jsx_content(advice_text)
                self._emit('<Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>')
                self.indent += 1
                self._emit(f'{advice_escaped}')
                self.indent -= 1
                self._emit('</Typography>')
            return

        # Check for subtitle
        if 'subtitle' in params:
            idx = params.index('subtitle')
            if idx + 1 < len(params):
                subtitle_text = params[idx + 1]
                # Strip HTML then escape for JSX content
                subtitle_clean = self._strip_html(str(subtitle_text))
                subtitle_escaped = self._escape_jsx_content(subtitle_clean)
                self._emit('<Typography variant="subtitle1" sx={{ fontWeight: "bold", mt: 2, mb: 1 }}>')
                self.indent += 1
                self._emit(f'{subtitle_escaped}')
                self.indent -= 1
                self._emit('</Typography>')

            # Check if there's also a widget in this line (subtitle + widget pattern)
            if 'widget' in params:
                widget_idx = params.index('widget')
                # Find the actual widget name, skipping flags like -guiMode, radio, etc.
                widget_name = self._extract_widget_name(params, widget_idx + 1)
                if widget_name:
                    self._emit(f'<CCP4i2TaskElement itemName="{widget_name}" {{...props}} />')
            return

        # Find the widget name and label
        widget_name = None
        label = None
        tip = None

        i = 0
        while i < len(params):
            p = params[i]
            if p == 'widget':
                if i + 1 < len(params):
                    widget_name = params[i + 1]
                    i += 2
                    continue
            elif p == 'label':
                if i + 1 < len(params):
                    label = params[i + 1]
                    i += 2
                    continue
            elif p == 'tip':
                if i + 1 < len(params):
                    tip = params[i + 1]
                    i += 2
                    continue
            elif p == 'stretch':
                i += 1
                continue
            elif isinstance(p, str) and not p.startswith('-'):
                # Could be a widget name directly (if uppercase)
                if p.isupper() or (len(p) > 0 and p[0].isupper()):
                    widget_name = p
            i += 1

        if widget_name:
            # Check for line-level toggle
            toggle = elem.kwargs.get('toggle')

            if toggle:
                condition = self._make_toggle_condition(toggle)
                self._emit(f'{{({condition}) && (')
                self.indent += 1

            # Build qualifiers
            qualifiers_parts = []
            if label:
                label_clean = self._strip_html(label).replace('"', '\\"').replace('\n', ' ')
                qualifiers_parts.append(f'guiLabel: "{label_clean}"')
            if tip:
                tip_clean = self._strip_html(tip).replace('"', '\\"').replace('\n', ' ')
                qualifiers_parts.append(f'toolTip: "{tip_clean}"')

            qualifiers = ''
            if qualifiers_parts:
                qualifiers = f' qualifiers={{{{ {", ".join(qualifiers_parts)} }}}}'

            self._emit(f'<CCP4i2TaskElement itemName="{widget_name}" {{...props}}{qualifiers} />')

            if toggle:
                self.indent -= 1
                self._emit(')}')

    def _extract_widget_name(self, params: List[Any], start_idx: int) -> Optional[str]:
        """Extract widget name from params, skipping flags like -guiMode, radio, etc."""
        # Known flag values that follow -guiMode or other flags
        flag_values = {'radio', 'multiLine', 'comboBox', 'checkBox', 'lineEdit'}

        idx = start_idx
        while idx < len(params):
            p = params[idx]
            if isinstance(p, str):
                if p.startswith('-'):
                    # Skip flag and its value
                    idx += 2
                    continue
                elif p in flag_values:
                    # Skip known flag values
                    idx += 1
                    continue
                elif p.isupper() or (len(p) > 1 and p[0].isupper() and '_' in p):
                    # Looks like a widget name (UPPERCASE or CamelCase_with_underscore)
                    return p
            idx += 1
        return None

    def _make_toggle_condition(self, toggle: list) -> str:
        """Convert a toggle specification to a React condition"""
        if len(toggle) >= 3:
            var_name = toggle[0]
            # toggle[1] is usually 'open' or 'close'
            values = toggle[2]

            if isinstance(values, list):
                if len(values) == 1:
                    val = values[0]
                    if isinstance(val, bool):
                        return f'{var_name} === {str(val).lower()}'
                    elif isinstance(val, str):
                        return f'{var_name} === "{val}"'
                    else:
                        return f'{var_name} === {val}'
                else:
                    conditions = []
                    for val in values:
                        if isinstance(val, bool):
                            conditions.append(f'{var_name} === {str(val).lower()}')
                        elif isinstance(val, str):
                            conditions.append(f'{var_name} === "{val}"')
                        else:
                            conditions.append(f'{var_name} === {val}')
                    return ' || '.join(conditions)

        return 'true'

    def _emit_footer(self):
        """Emit the footer"""
        self._emit('')
        self._emit('export default TaskInterface;')


def convert_gui_file(input_path: str, output_path: Optional[str] = None) -> str:
    """Convert a legacy GUI file to React TSX"""
    parser = GuiParser(input_path)
    parsed = parser.parse()

    generator = ReactGenerator(parsed)
    tsx_code = generator.generate()

    if output_path:
        Path(output_path).write_text(tsx_code)

    return tsx_code


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: gui_parser.py <input_gui.py> [output.tsx]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    result = convert_gui_file(input_file, output_file)
    if not output_file:
        print(result)
