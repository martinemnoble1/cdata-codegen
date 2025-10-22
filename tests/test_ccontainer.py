import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.generated.CCP4File import CDataFile
from core.base_object.base_classes import CContainer
from core.base_object.fundamental_types import CInt, CList

class TestExample:
    @classmethod
    def setup_class(cls):
        # Class-level setup (runs once before all tests)
        cls.shared_resource = "initialized"

    def test_ccontainer_inheritance(self):
        c = CContainer()
        # Check that CContainer is indeed a subclass of the base CContainer
        assert isinstance(c, CContainer)

    def test_ccontainer_methods(self):
        c = CContainer(name="container")
        # Check that CContainer has methods from its parent class
        assert hasattr(c, "add_item")
        b=CInt(10, name="test_int")
        d=CDataFile(name="test_file")
        d.update({"baseName": "changed"})
        c.add_item(b)
        c.add_item(d)
        items = c.get_items()
        assert len(items) == 2
        assert b.name == "test_int"
        assert b.object_path() == "container.test_int"
        assert d.name == "test_file"
        assert d.object_path() == "container.test_file"
        l=CList(name="test_list")
        c.add_item(l)
        items = c.get_items()
        assert len(items) == 3
        the_list:CList = items[2]
        assert the_list.name == "test_list"
        assert the_list.object_path() == "container.test_list"
        assert isinstance(the_list, CList)
        assert l is the_list
        print(b.get_qualifier("min"))
        b.set_qualifier("min", 2)
        b.set_qualifier("max", 100)
        with pytest.raises(ValueError):
            b.value = 120  # This should raise a ValueError due to the max qualifier
