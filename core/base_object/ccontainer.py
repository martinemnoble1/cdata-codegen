"""
CContainer - Container class for heterogeneous collections of CData objects.

Provides list-like collection management with:
- add_item() / get_items() for item management
- addContent() / addObject() for child object creation
- deleteObject() for removal
- dataOrder() for ordered access
- XML serialization (loadContentsFromXml, saveContentsToXml)
- DEF file support (loadDefFile, saveDefFile)
- Params file support (loadParamsFile, saveParamsFile)

Supports both list-style and dict-style access:
- container[0] - Access by index
- container.itemName - Access by name (if item has name attribute)
"""

from typing import List, Optional

from .cdata import CData
from .hierarchy_system import HierarchicalObject


class CContainer(CData):
    """Base class for container CData classes."""

    def __init__(self, items=None, parent=None, name=None, **kwargs):
        super().__init__(parent=parent, name=name, **kwargs)
        self._container_items = []
        self._data_order = []  # Track order of content items for dataOrder()
        if items is not None:
            for item in items:
                self.add_item(item)

    def add_item(self, item):
        """Add an item to the container."""
        if isinstance(item, CData):
            item.set_parent(self)
        self._container_items.append(item)

    def get_items(self):
        """Get all container items."""
        return self._container_items[:]

    def addContent(self, content_class, name: str, **kwargs):
        """Add a new content item to the container (old API compatibility).

        Args:
            content_class: The class type to instantiate
            name: Name for the new content item
            **kwargs: Additional arguments to pass to the constructor

        Returns:
            The newly created content object
        """
        # Create instance of the content class WITHOUT parent (to avoid setattr issues)
        if isinstance(content_class, type):
            new_obj = content_class(name=name, **kwargs)
        else:
            # If it's a string, try to resolve it
            from .fundamental_types import CInt, CFloat, CBoolean, CString, CList
            class_map = {
                'CInt': CInt,
                'CFloat': CFloat,
                'CBoolean': CBoolean,
                'CString': CString,
                'CList': CList,
                'CContainer': CContainer,
            }
            cls = class_map.get(content_class)
            if cls is None:
                raise ValueError(f"Unknown content class: {content_class}")
            new_obj = cls(name=name, **kwargs)

        # Add to container
        setattr(self, name, new_obj)

        # Explicitly set parent relationship (in case setattr doesn't handle it)
        if hasattr(new_obj, 'set_parent'):
            new_obj.set_parent(self)

        self._data_order.append(name)
        return new_obj

    def addObject(self, obj: CData, name: str = None):
        """Add an existing object to the container (old API compatibility).

        Args:
            obj: The CData object to add
            name: Optional name for the object (uses obj.name if not provided)

        Returns:
            The added object
        """
        if not isinstance(obj, CData):
            raise TypeError("Object must be a CData instance")

        obj_name = name if name is not None else getattr(obj, 'name', None)
        if not obj_name:
            raise ValueError("Object must have a name")

        # Set parent relationship
        obj.set_parent(self)
        obj.name = obj_name

        # Add to container
        setattr(self, obj_name, obj)
        if obj_name not in self._data_order:
            self._data_order.append(obj_name)

        return obj

    def deleteObject(self, name: str):
        """Delete an object from the container (old API compatibility).

        Args:
            name: Name of the object to delete
        """
        if not hasattr(self, name):
            raise AttributeError(f"Container has no object named '{name}'")

        obj = getattr(self, name)

        # Cleanup hierarchy if it's a CData object
        if isinstance(obj, HierarchicalObject):
            try:
                obj.destroy()
            except Exception:
                pass

        # Remove from container
        delattr(self, name)

        # Remove from data order
        if name in self._data_order:
            self._data_order.remove(name)

    def dataOrder(self) -> list:
        """Return the order of data items in this container (old API compatibility).

        Returns:
            List of names in the order they were added
        """
        # First check if there's a CONTENT_ORDER defined
        if hasattr(self, 'CONTENT_ORDER') and self.CONTENT_ORDER:
            return list(self.CONTENT_ORDER)

        # If _data_order is populated, use it
        if self._data_order:
            return list(self._data_order)

        # Backward compatibility: if _data_order is empty but we have children,
        # return names from children. This handles the case where parameters
        # were loaded from def.xml rather than added via addContent().
        return [child.objectName() for child in self.children()]

    def copyData(self, otherContainer, dataList: Optional[List[str]] = None):
        """Copy data from another container into this container.

        This performs a deep copy by serializing the source data to XML (via getEtree)
        and deserializing it back into this container (via setEtree). This ensures
        that all nested structures, qualifiers, and metadata are properly copied.

        Args:
            otherContainer: Source CContainer to copy from
            dataList: Optional list of item names to copy. If None, copies all items
                     from the source container.

        Example:
            # Copy all data from source to destination
            dest.copyData(source)

            # Copy specific items only (as shown in pipelines.rst documentation)
            self.pdbset.container.inputData.copyData(self.container.inputData, ['XYZIN'])
        """
        if not isinstance(otherContainer, CContainer):
            raise TypeError(f"otherContainer must be a CContainer, got {type(otherContainer).__name__}")

        # Determine which items to copy
        if dataList is None:
            # Copy all items from source
            # Use dataOrder() if it has items, otherwise find all CData children
            items_from_order = otherContainer.dataOrder()
            if items_from_order:
                items_to_copy = items_from_order
            else:
                # Fallback: Find all CData attributes by iterating children
                # This handles cases where items weren't added to _data_order
                from core.base_object.base_classes import CData
                items_to_copy = [child.name for child in otherContainer.children()
                                if isinstance(child, CData)]
        else:
            items_to_copy = dataList

        # Copy each item
        for item_name in items_to_copy:
            if not hasattr(otherContainer, item_name):
                # Skip items that don't exist in source
                continue

            source_item = getattr(otherContainer, item_name)

            # Serialize the source item to XML
            # excludeUnset=False ensures we copy everything including unset values
            source_etree = source_item.getEtree(name=item_name, excludeUnset=False)

            # Check if we already have this item in the destination
            if hasattr(self, item_name):
                # Item exists - update it in place
                dest_item = getattr(self, item_name)
                dest_item.setEtree(source_etree, ignore_missing=True)
            else:
                # Item doesn't exist - need to create it first
                # Get the class of the source item
                source_class = type(source_item)

                # Create a new instance
                new_item = source_class(name=item_name)

                # Add it to this container
                setattr(self, item_name, new_item)
                if hasattr(new_item, 'set_parent'):
                    new_item.set_parent(self)
                if item_name not in self._data_order:
                    self._data_order.append(item_name)

                # Now populate it with the source data
                new_item.setEtree(source_etree, ignore_missing=True)

    def clear(self):
        """Remove all content items from the container (old API compatibility)."""
        # Get list of all content items
        items_to_remove = list(self._data_order)

        # Delete each one
        for name in items_to_remove:
            try:
                self.deleteObject(name)
            except Exception:
                pass

        # Clear the order list
        self._data_order.clear()

    def loadContentsFromXml(self, xml_file: str):
        """Load container contents from an XML file (old API compatibility).

        Args:
            xml_file: Path to the XML file to load
        """
        import xml.etree.ElementTree as ET
        from pathlib import Path

        xml_path = Path(xml_file)
        if not xml_path.exists():
            raise FileNotFoundError(f"XML file not found: {xml_file}")

        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Use setEtree to deserialize
        self.setEtree(root, ignore_missing=True)

    def saveContentsToXml(self, xml_file: str):
        """Save container contents to an XML file (old API compatibility).

        Args:
            xml_file: Path to the XML file to save
        """
        import xml.etree.ElementTree as ET
        from pathlib import Path

        # Get the XML element tree
        root = self.getEtree()

        # Create the tree and write to file
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")  # Pretty print with 2-space indentation
        tree.write(xml_file, encoding='utf-8', xml_declaration=True)

    def loadDataFromXml(self, xml_file: str):
        """Alias for loadContentsFromXml (old API compatibility)."""
        self.loadContentsFromXml(xml_file)

    def saveDataToXml(self, xml_file: str):
        """Alias for saveContentsToXml (old API compatibility)."""
        self.saveContentsToXml(xml_file)

    # Priority 3: DEF and PARAMS file-specific methods
    def loadDefFile(self, filename: str):
        """Load container structure from a .def.xml file (old API compatibility).

        DEF files define the structure and qualifiers of a container,
        but not the actual data values.

        Args:
            filename: Path to the .def.xml file
        """
        # For now, use loadContentsFromXml
        # In future, this could use the DEF XML parser specifically
        self.loadContentsFromXml(filename)

    def saveDefFile(self, filename: str):
        """Save container structure to a .def.xml file (old API compatibility).

        DEF files define the structure and qualifiers of a container,
        but not the actual data values.

        Args:
            filename: Path to the .def.xml file
        """
        # Save structure with qualifiers but without data values
        self.saveContentsToXml(filename)

    def loadParamsFile(self, filename: str):
        """Load container data values from a .params.xml file (old API compatibility).

        PARAMS files contain the actual data values for a container
        whose structure is already defined.

        Args:
            filename: Path to the .params.xml file
        """
        # Load data values into existing structure
        self.loadDataFromXml(filename)

    def saveParamsFile(self, filename: str):
        """Save container data values to a .params.xml file (old API compatibility).

        PARAMS files contain the actual data values for a container.

        Args:
            filename: Path to the .params.xml file
        """
        # Save only data values, not structure
        self.saveDataToXml(filename)

    def __len__(self):
        """Return number of items in container."""
        return len(self._container_items)

    def __getitem__(self, index):
        """Get item by index."""
        return self._container_items[index]

    def __getattr__(self, name: str):
        """Allow attribute-style access to children by name.

        This enables accessing child objects like container.inputData
        instead of having to search through children manually.

        Args:
            name: Name of the child to access

        Returns:
            The child object with matching name

        Raises:
            AttributeError: If no child with that name exists
        """
        # Avoid infinite recursion for internal attributes
        if name.startswith('_'):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

        # Check children from HierarchicalObject hierarchy
        # Use object.__getattribute__ to avoid recursion
        try:
            # Get the 'children' method from HierarchicalObject
            children_method = object.__getattribute__(self, 'children')
            children_list = children_method()  # Call the method
            for child in children_list:
                # Skip destroyed children
                if hasattr(child, 'state'):
                    from .hierarchy_system import ObjectState
                    if child.state == ObjectState.DESTROYED:
                        continue
                # Check if name matches
                if hasattr(child, 'name') and child.name == name:
                    return child
        except (AttributeError, TypeError):
            pass

        # Also check _container_items (in case items were added via add_item)
        try:
            container_items = object.__getattribute__(self, '_container_items')
            for item in container_items:
                if hasattr(item, 'name') and item.name == name:
                    return item
        except (AttributeError, TypeError):
            pass

        # Not found - raise AttributeError
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

