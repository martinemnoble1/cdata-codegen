import json
import logging
from core import CCP4Container
from core import CCP4File
from core.base_object import CData


logger = logging.getLogger(f"ccp4x:{__name__}")


def base_class(o):
    """Determine the base class name for a CData object."""
    from core.base_object.fundamental_types import CInt, CFloat, CString, CBoolean, CList

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
    def default(self, o):
        from core.base_object.fundamental_types import CList

        if isinstance(o, CData):
            qualifiers = {}
            # Safely get qualifiers
            if hasattr(type(o), 'QUALIFIERS'):
                qualifiers.update(type(o).QUALIFIERS)
            if hasattr(o, '_qualifiers') and o._qualifiers:
                qualifiers.update(o._qualifiers)
            qualifiers = dict(
                filter(lambda elem: elem[1] != NotImplemented, qualifiers.items())
            )

            result = {
                "_class": type(o).__name__,
                "_value": getattr(o, '_value', None),
                "_qualifiers": qualifiers,
                "_CONTENTS_ORDER": getattr(o.__class__, 'CONTENTS_ORDER', []),
                "_objectPath": o.objectPath() if hasattr(o, 'objectPath') else "",
            }
            result["_baseClass"] = base_class(o)
            if isinstance(o, CList) and hasattr(o, 'makeItem'):
                result["_subItem"] = o.makeItem()
            # print(result)
            return result
        if o is NotImplemented:
            return None
        if o.__class__.__name__ == "ObjectType":
            # This is a hack to deal with the fact that (for now) container objects are Rooted as QObjects
            return None
        try:
            result = json.dumps(o)
        except TypeError as exc:
            logger.exception(
                "Exception in json encoding CData object %s", type(o), exc_info=exc
            )
            result = json.dumps(str(o), indent="\t")
        return result
