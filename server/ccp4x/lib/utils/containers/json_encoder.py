"""JSON encoder for CData container serialization."""
import json
import logging
from core import CCP4Container
from core import CCP4File
from core.base_object import CData
from core.base_object.fundamental_types import (
    CInt, CFloat, CString, CBoolean, CList
)


logger = logging.getLogger(f"ccp4x:{__name__}")


def base_class(o):
    """Determine the base class name for a CData object."""
    if isinstance(o, CCP4File.CDataFile):
        result = "CDataFile"
    elif isinstance(o, CList):
        result = "CList"
    elif isinstance(o, CCP4Container.CContainer):
        result = "CContainer"
    elif isinstance(o, CString):
        result = "CString"
    elif isinstance(o, CInt):
        result = "CInt"
    elif isinstance(o, CFloat):
        result = "CFloat"
    elif isinstance(o, CBoolean):
        result = "CBoolean"
    else:
        result = "CData"
    return result


class CCP4i2JsonEncoder(json.JSONEncoder):
    """JSON encoder that serializes CData objects with full metadata."""

    def default(self, o):
        if isinstance(o, CData):
            qualifiers = {}
            # Safely get qualifiers from all possible sources
            # 1. Legacy QUALIFIERS class attribute (old style)
            if hasattr(type(o), 'QUALIFIERS'):
                qualifiers.update(type(o).QUALIFIERS)
            # 2. New metadata system: _class_qualifiers (@cdata_class)
            if hasattr(type(o), '_class_qualifiers'):
                class_quals = type(o)._class_qualifiers
                if isinstance(class_quals, dict):
                    qualifiers.update(class_quals)
            # 3. Instance-level _qualifiers (copied from class or overridden)
            if hasattr(o, '_qualifiers') and o._qualifiers:
                qualifiers.update(o._qualifiers)
            # Filter out NotImplemented values
            qualifiers = {
                k: v for k, v in qualifiers.items()
                if v is not NotImplemented
            }

            # Get CONTENTS_ORDER from multiple sources
            # 1. Instance property (modern CData has CONTENTS_ORDER property)
            # 2. Instance attribute CONTENT_ORDER (@cdata_class decorator)
            contents_order = []
            if hasattr(o, 'CONTENTS_ORDER'):
                try:
                    val = o.CONTENTS_ORDER
                    # Ensure we got an actual list, not a property descriptor
                    if isinstance(val, (list, tuple)):
                        contents_order = list(val)
                except Exception:
                    pass
            if not contents_order and hasattr(o, 'CONTENT_ORDER'):
                val = getattr(o, 'CONTENT_ORDER', None)
                if isinstance(val, (list, tuple)):
                    contents_order = list(val)

            obj_path = ""
            if hasattr(o, 'objectPath'):
                obj_path = o.objectPath()

            # Determine _value based on object type
            # For CContainer: build dict of named children
            # For CList: use the list items
            # For primitives: use _value attribute
            if isinstance(o, CCP4Container.CContainer):
                # Build dict of children by name
                value_dict = {}
                for child in o.children():
                    if isinstance(child, CData):
                        child_name = child.objectName()
                        if child_name:
                            value_dict[child_name] = child
                value = value_dict
            elif isinstance(o, CList):
                # CList stores items - they'll be serialized recursively
                value = list(o) if hasattr(o, '__iter__') else []
            else:
                # Primitives (CInt, CFloat, CString, CBoolean)
                value = getattr(o, '_value', None)

            result = {
                "_class": type(o).__name__,
                "_value": value,
                "_qualifiers": qualifiers,
                "_CONTENTS_ORDER": contents_order,
                "_objectPath": obj_path,
            }
            result["_baseClass"] = base_class(o)
            if isinstance(o, CList) and hasattr(o, 'makeItem'):
                result["_subItem"] = o.makeItem()
            return result
        if o is NotImplemented:
            return None
        if o.__class__.__name__ == "ObjectType":
            # Hack for container objects rooted as QObjects
            return None
        # Handle class/type objects (e.g., ABCMeta in columnGroupClassList)
        if isinstance(o, type):
            # Return class name as string for class references
            return f"{o.__module__}.{o.__name__}" if o.__module__ else o.__name__
        try:
            result = json.dumps(o)
        except TypeError:
            # Fall back to string representation without logging (reduces noise)
            result = str(o)
        return result
