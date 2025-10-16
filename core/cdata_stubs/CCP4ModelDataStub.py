"""Generated classes from CCP4ModelData.py"""

from ..base_object.base_classes import CData, CContainer
from ..CCP4FundamentalTypes import CInt, CList, CBoolean, CFloat, CString, COneWord
from ..base_object.class_metadata import cdata_class, attribute, AttributeType

from .CCP4BaseFile-stub import CDataFileContent, CDataFile, CXmlDataFile, CI2XmlDataFile


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute")
    },
    error_codes={
        "101": {
            "description": "File does not exist"
        },
        "102": {
            "description": "No mime type for data file"
        },
        "103": {
            "description": "Attempting to set file content with inappropriate data"
        },
        "104": {
            "description": "There is no file content class specified for this type of file"
        },
        "105": {
            "description": "The file content class specified for this type of file can not be found"
        },
        "300": {
            "description": "Passed",
            "severity": 0
        },
        "305": {
            "description": "Neither original nor test file exists",
            "severity": 0
        },
        "306": {
            "description": "Original file does not exists"
        },
        "307": {
            "description": "Test file does not exist "
        },
        "308": {
            "description": "Files failed checksum comparison"
        },
        "309": {
            "description": "Files failed size comparison"
        },
        "310": {
            "description": "No comparison testing implemented for this file type",
            "severity": 2
        },
        "311": {
            "description": "Failed loading original file for comparison"
        },
        "312": {
            "description": "Failed loading test file for comparison"
        },
        "313": {
            "description": "Files failed simple text diff comparison"
        },
        "320": {
            "description": "Unrecognised error attempting to load file"
        }
    },
    qualifiers={
        "fileLabel": 'tls',
        "mimeTypeName": 'application/refmac-TLS',
        "mimeTypeDescription": 'Refmac TLS file',
        "guiLabel": 'TLS coefficients',
        "toolTip": 'Definition of model domains for TLS refinement',
        "fileExtensions": ['tls'],
        "fileContentClassName": None,
        "helpFile": 'model_data#tls_file'
    },
    qualifiers_order=[
        'fileExtensions',
        'mimeTypeName',
        'mimeTypeDescription',
        'fileLabel',
        'allowUndefined',
        'mustExist',
        'fromPreviousJob',
        'jobCombo',
        'fileContentClassName',
        'isDirectory',
        'saveToDb',
        'requiredSubType',
        'requiredContentFlag'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool, "description": "Flag if data file can be undefined at run time"},
        "mustExist": {"type": bool, "description": "Flag if data file must exist at run time"},
        "fromPreviousJob": {"type": bool, "description": "Flag if input data file can be inferred from preceeding jobs"},
        "jobCombo": {"type": bool, "description": "Flag if data widget should be a combo box "},
        "mimeTypeName": {"type": str, "description": ""},
        "mimeTypeDescription": {"type": str, "description": ""},
        "fileLabel": {"type": str, "description": "Label for file"},
        "fileExtensions": {"type": list, "listItemType": "<class 'str'>", "description": "A list of strings containing allowed file extensions (no dot)"},
        "fileContentClassName": {"type": str, "editable": "False", "description": "A string containing the name of a class which will hold the file contents"},
        "isDirectory": {"type": bool, "description": "Flag if the data is a directory"},
        "ifInfo": {"type": bool, "description": "Flag if gui widget should have info icon"},
        "saveToDb": {"type": bool, "description": "Save the name of this file in the database"},
        "requiredSubType": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed sub types"},
        "requiredContentFlag": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed content flags"}
    },
    gui_label="CTLSDataFile",
)
class CTLSDataFile(CDataFile):
    """A refmac TLS file"""
    pass


@cdata_class(
    error_codes={
        "401": {
            "description": "Non-alphabet character removed from sequence",
            "severity": 2
        },
        "402": {
            "description": "Invalid characters (BJOXZ) in sequence"
        },
        "403": {
            "description": "Sequence undefined",
            "severity": 2
        }
    },
    qualifiers={
        "minLength": None,
        "maxLength": None,
        "enumerators": [],
        "menuText": [],
        "onlyEnumerators": False,
        "charWidth": -1,
        "allowedCharsCode": 0
    },
    qualifiers_order=[
        'minLength',
        'maxLength',
        'onlyEnumerators',
        'enumerators',
        'menuText',
        'allowedCharsCode'
    ],
    qualifiers_definition={
        "default": {"type": str},
        "maxLength": {"type": int, "description": "Maximum length of string"},
        "minLength": {"type": int, "description": "Minimum length of string"},
        "enumerators": {"type": list, "description": "A list of allowed or recommended values for string"},
        "menuText": {"type": list, "description": "A list of strings equivalent to the enumerators that will appear in the GUI"},
        "onlyEnumerators": {"type": bool, "description": "If this is true then the enumerators are obligatory - otherwise they are treated as recommended values"},
        "allowedCharsCode": {"type": int, "description": "Flag if the text is limited to set of allowed characters"}
    },
    gui_label="CSequenceString",
)
class CSequenceString(CString):
    """A string"""
    pass


@cdata_class(
    attributes={
        "uniprotId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="uniprotId attribute"),
        "organism": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="organism attribute"),
        "expressionSystem": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="expressionSystem attribute")
    },
    error_codes={
        "401": {
            "description": "No uniprot id available"
        },
        "402": {
            "description": "No uniprot xml file available to read"
        },
        "403": {
            "description": "No project id provided to determine uniprot xml filename"
        },
        "404": {
            "description": "Reading uniprot xml file failed"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CSequenceMeta",
)
class CSequenceMeta(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass


@cdata_class(
    attributes={
        "identifier": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="identifier attribute"),
        "moleculeType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="moleculeType attribute")
    },
    error_codes={
        "0": {
            "severity": 0,
            "description": "OK"
        },
        "1": {
            "severity": 1,
            "description": "Data has undefined value"
        },
        "2": {
            "severity": 3,
            "description": "Data has undefined value"
        },
        "3": {
            "severity": 2,
            "description": "Missing data"
        },
        "4": {
            "description": "Missing data"
        },
        "5": {
            "description": "Attempting to set data of wrong type"
        },
        "6": {
            "description": "Default value does not satisfy validity check"
        },
        "7": {
            "severity": 2,
            "description": "Unrecognised qualifier in data input"
        },
        "8": {
            "severity": 2,
            "description": "Attempting to get inaccessible attribute:"
        },
        "9": {
            "description": "Failed to get property"
        },
        "10": {
            "severity": 2,
            "description": "Attempting to set inaccessible attribute:"
        },
        "11": {
            "description": "Failed to set property:"
        },
        "12": {
            "description": "Undetermined error setting value from XML"
        },
        "13": {
            "description": "Unrecognised class name in qualifier"
        },
        "14": {
            "severity": 2,
            "description": "No object name when saving qualifiers to XML"
        },
        "15": {
            "description": "Error saving qualifier to XML"
        },
        "16": {
            "severity": 2,
            "description": "Unrecognised item in XML data file"
        },
        "17": {
            "description": "Attempting to set unrecognised qualifier"
        },
        "18": {
            "description": "Attempting to set qualifier with wrong type"
        },
        "19": {
            "description": "Attempting to set qualifier with wrong list item type"
        },
        "20": {
            "description": "Error creating a list/dict item object"
        },
        "21": {
            "description": "Unknown error setting qualifiers from Xml file"
        },
        "22": {
            "description": "Unknown error testing validity"
        },
        "23": {
            "description": "Error saving data object to XML"
        },
        "24": {
            "description": "Unable to test validity of default",
            "severity": 2
        },
        "300": {
            "description": "Compared objects are the same",
            "severity": 0
        },
        "315": {
            "description": "Both compared objects are null",
            "severity": 0
        },
        "301": {
            "description": "Unable to compare this class of data",
            "severity": 2
        },
        "302": {
            "description": "Other data has null value"
        },
        "303": {
            "description": "My data has null value"
        },
        "304": {
            "description": "Data has different values"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    contents_order=['identifier', 'moleculeType'],
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CSequenceAlignment",
)
class CSequenceAlignment(CData):
    """An alignment of two or more sequences.
Each sequence is obviously related to class CSequence, but
will also contain gaps relevant to the alignment. We could
implement the contents as a list of CSequence objects?
The alignment is typically formatted in a file as consecutive 
or interleaved sequences."""
    pass


@cdata_class(
    attributes={
        "identifier": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="identifier attribute"),
        "referenceDb": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="referenceDb attribute"),
        "reference": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="reference attribute"),
        "name": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="name attribute"),
        "description": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="description attribute"),
        "sequence": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="sequence attribute"),
        "moleculeType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="moleculeType attribute")
    },
    error_codes={
        "201": {
            "description": "Sequence undefined",
            "severity": 1
        },
        "202": {
            "description": "error reading from file"
        },
        "203": {
            "description": "Comparing sequences: Sequence item different"
        },
        "204": {
            "description": "Comparing sequences: One item set - the other is unset"
        },
        "401": {
            "description": "Attempting to load from non-existent file"
        },
        "402": {
            "description": "Error reading from file"
        },
        "403": {
            "description": "Unknown sequence file format"
        },
        "405": {
            "description": "Error reading identifiers from multi-record file"
        },
        "406": {
            "description": "Error opening file"
        },
        "407": {
            "description": "The 'PIR' file did not have the correct format"
        },
        "408": {
            "severity": 2,
            "description": "The 'PIR' file format was corrected"
        },
        "409": {
            "description": "Error opening file to write"
        },
        "410": {
            "description": "Error attempting to write out sequence file"
        },
        "411": {
            "description": "Error attempting to create a temporary sequence file"
        },
        "412": {
            "description": "Sequence file is empty"
        },
        "413": {
            "description": "Unable to read BLAST format file"
        },
        "414": {
            "description": "Unable to read hhpred format file"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    contents_order=['identifier', 'name', 'description',
                    'referenceDb', 'reference', 'moleculeType', 'sequence'],
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CSequence",
)
class CSequence(CData):
    """A string of sequence one-letter codes
Need to be able to parse common seq file formats
Do we need to support alternative residues
What about nucleic/polysach?"""
    pass


@cdata_class(
    error_codes={
        "150": {
            "description": "No file content information"
        },
        "151": {
            "description": "Two sequences have the same identifier"
        },
        "152": {
            "description": "Failed in merging sequence files to read sequence file"
        },
        "153": {
            "description": "Failed in merging sequence files to write merged file"
        }
    },
    qualifiers={
        "listMinLength": 0
    },
    qualifiers_order=[
        'listMinLength',
        'listMaxLength',
        'listCompare'
    ],
    qualifiers_definition={
        "default": {"type": list},
        "listMaxLength": {"type": int, "description": "Inclusive maximum length of list"},
        "listMinLength": {"type": int, "description": "Inclusive minimum length of list"},
        "listCompare": {"type": int, "description": "If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method."}
    },
    gui_label="CSeqDataFileList",
)
class CSeqDataFileList(CList):
    """A list with all items of one CData sub-class"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute")
    },
    error_codes={
        "201": {
            "description": "Error reading sequence file"
        },
        "202": {
            "description": "Error in BioPython attempting to identify file type"
        }
    },
    qualifiers={
        "fileLabel": 'sequence',
        "mimeTypeName": 'application/CCP4-seq',
        "mimeTypeDescription": 'Sequence file',
        "guiLabel": 'Sequence',
        "tooltip": 'Sequence in any of the common formats (pir,fasta..)',
        "fileExtensions": ['seq', 'pir', 'fasta'],
        "fileContentClassName": 'CSequence',
        "downloadModes": ['uniprotFasta'],
        "helpFile": 'model_data#sequences'
    },
    qualifiers_order=[
        'fileExtensions',
        'mimeTypeName',
        'mimeTypeDescription',
        'fileLabel',
        'allowUndefined',
        'mustExist',
        'fromPreviousJob',
        'jobCombo',
        'fileContentClassName',
        'isDirectory',
        'saveToDb',
        'requiredSubType',
        'requiredContentFlag'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool, "description": "Flag if data file can be undefined at run time"},
        "mustExist": {"type": bool, "description": "Flag if data file must exist at run time"},
        "fromPreviousJob": {"type": bool, "description": "Flag if input data file can be inferred from preceeding jobs"},
        "jobCombo": {"type": bool, "description": "Flag if data widget should be a combo box "},
        "mimeTypeName": {"type": str, "description": ""},
        "mimeTypeDescription": {"type": str, "description": ""},
        "fileLabel": {"type": str, "description": "Label for file"},
        "fileExtensions": {"type": list, "listItemType": "<class 'str'>", "description": "A list of strings containing allowed file extensions (no dot)"},
        "fileContentClassName": {"type": str, "editable": "False", "description": "A string containing the name of a class which will hold the file contents"},
        "isDirectory": {"type": bool, "description": "Flag if the data is a directory"},
        "ifInfo": {"type": bool, "description": "Flag if gui widget should have info icon"},
        "saveToDb": {"type": bool, "description": "Save the name of this file in the database"},
        "requiredSubType": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed sub types"},
        "requiredContentFlag": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed content flags"}
    },
    gui_label="CSeqDataFile",
)
class CSeqDataFile(CDataFile):
    """A sequence file"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute")
    },
    error_codes={
        "202": {
            "description": "Error reading from file"
        },
        "203": {
            "description": "Unknown alignment file format"
        },
        "204": {
            "description": "Can not read Blast or HHPred file format"
        },
        "205": {
            "description": "Error reading identifiers from multi-record file"
        },
        "206": {
            "description": "Error attempting to identify file format"
        },
        "250": {
            "description": "Alignment file format not recognised - can not convert"
        },
        "251": {
            "description": "Alignment file conversion failed to overwrite existing file"
        },
        "252": {
            "description": "Alignment file conversion failed writing file"
        },
        "260": {
            "description": "Alignment file does not contain required number of sequences"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "mustExist": False,
        "fromPreviousJob": False,
        "jobCombo": True,
        "mimeTypeName": 'application/CCP4-seqalign',
        "mimeTypeDescription": 'Sequence alignment file',
        "fileLabel": None,
        "fileExtensions": ['aln', 'pir', 'fasta', 'msf', 'phy'],
        "fileContentClassName": 'CSequenceAlignment',
        "isDirectory": False,
        "saveToDb": True,
        "requiredSubType": None,
        "requiredContentFlag": None,
        "guiLabel": 'Aligned sequences',
        "toolTip": 'Multiple sequence alignment in any of the common formats (pir,fasta..)',
        "helpFile": 'model_data#alignments'
    },
    qualifiers_order=[
        'requiredSequences'
    ],
    qualifiers_definition={
        "requiredSequences": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed numbers of sequences in file (usually [2])"}
    },
    gui_label="CSeqAlignDataFile",
)
class CSeqAlignDataFile(CDataFile):
    """A (multiple) sequence alignment file"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "List shorter than required minimum length"
        },
        "102": {
            "description": "List longer than required maximum length"
        },
        "103": {
            "description": "Consecutive values in list fail comparison test"
        },
        "104": {
            "description": "Attempting to add object of wrong type"
        },
        "105": {
            "description": "Attempting to add object of correct type but wrong qualifiers"
        },
        "106": {
            "description": "Attempting to add data which does not satisfy the qualifiers for a list item"
        },
        "107": {
            "description": "Deleting item will reduce list below minimum length"
        },
        "108": {
            "description": "Adding item will extend list beyond maximum length"
        },
        "109": {
            "description": "Invalid item class"
        },
        "110": {
            "description": "etree (XML) list item of wrong type"
        },
        "112": {
            "description": "No list item object set for list"
        }
    },
    qualifiers={
        "listMinLength": 0
    },
    qualifiers_order=[
        'listMinLength',
        'listMaxLength',
        'listCompare'
    ],
    qualifiers_definition={
        "default": {"type": list},
        "listMaxLength": {"type": int, "description": "Inclusive maximum length of list"},
        "listMinLength": {"type": int, "description": "Inclusive minimum length of list"},
        "listCompare": {"type": int, "description": "If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method."}
    },
    gui_label="CResidueRangeList",
)
class CResidueRangeList(CList):
    """A list of residue range selections"""
    pass


@cdata_class(
    attributes={
        "chainId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.COneWord", tooltip="chainId attribute"),
        "firstRes": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.COneWord", tooltip="firstRes attribute"),
        "lastRes": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.COneWord", tooltip="lastRes attribute")
    },
    error_codes={
        "0": {
            "severity": 0,
            "description": "OK"
        },
        "1": {
            "severity": 1,
            "description": "Data has undefined value"
        },
        "2": {
            "severity": 3,
            "description": "Data has undefined value"
        },
        "3": {
            "severity": 2,
            "description": "Missing data"
        },
        "4": {
            "description": "Missing data"
        },
        "5": {
            "description": "Attempting to set data of wrong type"
        },
        "6": {
            "description": "Default value does not satisfy validity check"
        },
        "7": {
            "severity": 2,
            "description": "Unrecognised qualifier in data input"
        },
        "8": {
            "severity": 2,
            "description": "Attempting to get inaccessible attribute:"
        },
        "9": {
            "description": "Failed to get property"
        },
        "10": {
            "severity": 2,
            "description": "Attempting to set inaccessible attribute:"
        },
        "11": {
            "description": "Failed to set property:"
        },
        "12": {
            "description": "Undetermined error setting value from XML"
        },
        "13": {
            "description": "Unrecognised class name in qualifier"
        },
        "14": {
            "severity": 2,
            "description": "No object name when saving qualifiers to XML"
        },
        "15": {
            "description": "Error saving qualifier to XML"
        },
        "16": {
            "severity": 2,
            "description": "Unrecognised item in XML data file"
        },
        "17": {
            "description": "Attempting to set unrecognised qualifier"
        },
        "18": {
            "description": "Attempting to set qualifier with wrong type"
        },
        "19": {
            "description": "Attempting to set qualifier with wrong list item type"
        },
        "20": {
            "description": "Error creating a list/dict item object"
        },
        "21": {
            "description": "Unknown error setting qualifiers from Xml file"
        },
        "22": {
            "description": "Unknown error testing validity"
        },
        "23": {
            "description": "Error saving data object to XML"
        },
        "24": {
            "description": "Unable to test validity of default",
            "severity": 2
        },
        "300": {
            "description": "Compared objects are the same",
            "severity": 0
        },
        "315": {
            "description": "Both compared objects are null",
            "severity": 0
        },
        "301": {
            "description": "Unable to compare this class of data",
            "severity": 2
        },
        "302": {
            "description": "Other data has null value"
        },
        "303": {
            "description": "My data has null value"
        },
        "304": {
            "description": "Data has different values"
        }
    },
    qualifiers={
        "pdbFileKey": None
    },
    contents_order=['chainId', 'firstRes', 'lastRes'],
    qualifiers_order=[
        'pdbFileKey'
    ],
    qualifiers_definition={
        "pdbFileKey": {"type": str, "description": "The key for a CPdbDataFile in the same CContainer"}
    },
    gui_label="CResidueRange",
)
class CResidueRange(CData):
    """A residue range selection"""
    pass


@cdata_class(
    attributes={
        "structure": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4ModelData.CPdbDataFile", tooltip="structure attribute"),
        "identity_to_target": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CFloat", tooltip="identity_to_target attribute"),
        "rms_to_target": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CFloat", tooltip="rms_to_target attribute")
    },
    error_codes={
        "101": {
            "description": "No sequence identity or structure RMS to target set"
        }
    },
    qualifiers={
        "guiLabel": 'Structure in ensemble',
        "toolTip": 'Homologous model and its similarity to the target structure',
        "allowUndefined": False
    },
    contents_order=['structure', 'identity_to_target', 'rms_to_target'],
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CPdbEnsembleItem",
)
class CPdbEnsembleItem(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "List shorter than required minimum length"
        },
        "102": {
            "description": "List longer than required maximum length"
        },
        "103": {
            "description": "Consecutive values in list fail comparison test"
        },
        "104": {
            "description": "Attempting to add object of wrong type"
        },
        "105": {
            "description": "Attempting to add object of correct type but wrong qualifiers"
        },
        "106": {
            "description": "Attempting to add data which does not satisfy the qualifiers for a list item"
        },
        "107": {
            "description": "Deleting item will reduce list below minimum length"
        },
        "108": {
            "description": "Adding item will extend list beyond maximum length"
        },
        "109": {
            "description": "Invalid item class"
        },
        "110": {
            "description": "etree (XML) list item of wrong type"
        },
        "112": {
            "description": "No list item object set for list"
        }
    },
    qualifiers={
        "listMinLength": 0
    },
    qualifiers_order=[
        'listMinLength',
        'listMaxLength',
        'listCompare'
    ],
    qualifiers_definition={
        "default": {"type": list},
        "listMaxLength": {"type": int, "description": "Inclusive maximum length of list"},
        "listMinLength": {"type": int, "description": "Inclusive minimum length of list"},
        "listCompare": {"type": int, "description": "If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method."}
    },
    gui_label="CPdbDataFileList",
)
class CPdbDataFileList(CList):
    """A list with all items of one CData sub-class"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute"),
        "selection": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4ModelData.CAtomSelection", tooltip="selection attribute")
    },
    error_codes={
        "401": {
            "description": "Failed running coord_format to fix coordinate file - is it a PDB file?"
        },
        "402": {
            "severity": 2,
            "description": "Badly formated PDB file fixed"
        },
        "403": {
            "severity": 2,
            "description": "Fixed by removing text"
        },
        "404": {
            "severity": 2,
            "description": "Fixed by adding text"
        },
        "405": {
            "description": "There are no ATOM or HETATM lines in the PDB file"
        },
        "410": {
            "description": "No file loaded - can not convert coordinate file format"
        },
        "411": {
            "description": "Failed loading file - can not convert coordinate file format"
        },
        "412": {
            "description": "Can not overwrite existing file - can not convert coordinate file format"
        },
        "413": {
            "description": "Failed writing coordinate file"
        },
        "414": {
            "description": "Failed to identify coordinate file format"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "mustExist": False,
        "fromPreviousJob": False,
        "jobCombo": True,
        "mimeTypeName": 'chemical/x-pdb',
        "mimeTypeDescription": 'Model coordinates',
        "fileLabel": 'coordinates',
        "fileExtensions": ['pdb', 'cif', 'mmcif', 'ent'],
        "fileContentClassName": 'CPdbData',
        "isDirectory": False,
        "saveToDb": True,
        "requiredSubType": None,
        "requiredContentFlag": None,
        "guiLabel": 'Atomic model',
        "toolTip": 'A model coordinate file in PDB or mmCIF format',
        "ifInfo": True,
        "ifAtomSelection": False,
        "downloadModes": ['ebiPdb', 'rcsbPdb', 'uniprotAFPdb'],
        "helpFile": 'model_data#coordinate_files'
    },
    qualifiers_order=[
        'fileExtensions',
        'mimeTypeName',
        'mimeTypeDescription',
        'fileLabel',
        'allowUndefined',
        'mustExist',
        'fromPreviousJob',
        'jobCombo',
        'fileContentClassName',
        'isDirectory',
        'saveToDb',
        'requiredSubType',
        'requiredContentFlag'
    ],
    qualifiers_definition={
        "ifAtomSelection": {"type": bool, "description": "Atom selection option enabled"}
    },
    gui_label="CPdbDataFile",
)
class CPdbDataFile(CDataFile):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "Unable to load mmdb - ensure LD_LIBRARY_PATH is set"
        },
        "102": {
            "description": "Error reading PDB file into MMDB object"
        },
        "103": {
            "description": "Residue range selection does not specify chain"
        },
        "104": {
            "description": "Residue range selection specifies non-existant chain id"
        },
        "105": {
            "description": "Residue range selection - no residues selected"
        },
        "106": {
            "description": "Residue range selection - residue number is not an integer"
        },
        "112": {
            "description": "Atom selection failed. Failed creating CMMDBManager object"
        },
        "113": {
            "description": "Atom selection failed. Faied reading coordinate file."
        },
        "114": {
            "description": "Atom selection failed. Failed parsing command"
        },
        "115": {
            "description": "Atom selection failed. Error creating PPCAtom"
        },
        "116": {
            "description": "Atom selection failed. Error in GetSelIndex"
        },
        "117": {
            "description": "Atom selection failed. Error loading selection tree"
        },
        "118": {
            "description": "Atom selection failed. Error applying selection tree"
        },
        "119": {
            "description": "Creating new PDB file failed on writing file"
        },
        "120": {
            "description": "Creating new PDB file failed converting from fractional coordinates"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CPdbData",
)
class CPdbData(CDataFileContent):
    """Contents of a PDB file - a subset with functionality for GUI"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "List shorter than required minimum length"
        },
        "102": {
            "description": "List longer than required maximum length"
        },
        "103": {
            "description": "Consecutive values in list fail comparison test"
        },
        "104": {
            "description": "Attempting to add object of wrong type"
        },
        "105": {
            "description": "Attempting to add object of correct type but wrong qualifiers"
        },
        "106": {
            "description": "Attempting to add data which does not satisfy the qualifiers for a list item"
        },
        "107": {
            "description": "Deleting item will reduce list below minimum length"
        },
        "108": {
            "description": "Adding item will extend list beyond maximum length"
        },
        "109": {
            "description": "Invalid item class"
        },
        "110": {
            "description": "etree (XML) list item of wrong type"
        },
        "112": {
            "description": "No list item object set for list"
        }
    },
    qualifiers={
        "listMinLength": 0
    },
    qualifiers_order=[
        'listMinLength',
        'listMaxLength',
        'listCompare'
    ],
    qualifiers_definition={
        "default": {"type": list},
        "listMaxLength": {"type": int, "description": "Inclusive maximum length of list"},
        "listMinLength": {"type": int, "description": "Inclusive minimum length of list"},
        "listCompare": {"type": int, "description": "If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method."}
    },
    gui_label="COccRelationRefmacList",
)
class COccRelationRefmacList(CList):
    """A list with all items of one CData sub-class"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "List shorter than required minimum length"
        },
        "102": {
            "description": "List longer than required maximum length"
        },
        "103": {
            "description": "Consecutive values in list fail comparison test"
        },
        "104": {
            "description": "Attempting to add object of wrong type"
        },
        "105": {
            "description": "Attempting to add object of correct type but wrong qualifiers"
        },
        "106": {
            "description": "Attempting to add data which does not satisfy the qualifiers for a list item"
        },
        "107": {
            "description": "Deleting item will reduce list below minimum length"
        },
        "108": {
            "description": "Adding item will extend list beyond maximum length"
        },
        "109": {
            "description": "Invalid item class"
        },
        "110": {
            "description": "etree (XML) list item of wrong type"
        },
        "112": {
            "description": "No list item object set for list"
        }
    },
    qualifiers={
        "listMinLength": 0
    },
    qualifiers_order=[
        'listMinLength',
        'listMaxLength',
        'listCompare'
    ],
    qualifiers_definition={
        "default": {"type": list},
        "listMaxLength": {"type": int, "description": "Inclusive maximum length of list"},
        "listMinLength": {"type": int, "description": "Inclusive minimum length of list"},
        "listCompare": {"type": int, "description": "If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method."}
    },
    gui_label="COccRefmacSelectionList",
)
class COccRefmacSelectionList(CList):
    """A list with all items of one CData sub-class"""
    pass


@cdata_class(
    attributes={
        "identifier": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="identifier attribute"),
        "formula": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="formula attribute"),
        "dictionaryName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="dictionaryName attribute"),
        "smiles": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="smiles attribute")
    },
    error_codes={
        "0": {
            "severity": 0,
            "description": "OK"
        },
        "1": {
            "severity": 1,
            "description": "Data has undefined value"
        },
        "2": {
            "severity": 3,
            "description": "Data has undefined value"
        },
        "3": {
            "severity": 2,
            "description": "Missing data"
        },
        "4": {
            "description": "Missing data"
        },
        "5": {
            "description": "Attempting to set data of wrong type"
        },
        "6": {
            "description": "Default value does not satisfy validity check"
        },
        "7": {
            "severity": 2,
            "description": "Unrecognised qualifier in data input"
        },
        "8": {
            "severity": 2,
            "description": "Attempting to get inaccessible attribute:"
        },
        "9": {
            "description": "Failed to get property"
        },
        "10": {
            "severity": 2,
            "description": "Attempting to set inaccessible attribute:"
        },
        "11": {
            "description": "Failed to set property:"
        },
        "12": {
            "description": "Undetermined error setting value from XML"
        },
        "13": {
            "description": "Unrecognised class name in qualifier"
        },
        "14": {
            "severity": 2,
            "description": "No object name when saving qualifiers to XML"
        },
        "15": {
            "description": "Error saving qualifier to XML"
        },
        "16": {
            "severity": 2,
            "description": "Unrecognised item in XML data file"
        },
        "17": {
            "description": "Attempting to set unrecognised qualifier"
        },
        "18": {
            "description": "Attempting to set qualifier with wrong type"
        },
        "19": {
            "description": "Attempting to set qualifier with wrong list item type"
        },
        "20": {
            "description": "Error creating a list/dict item object"
        },
        "21": {
            "description": "Unknown error setting qualifiers from Xml file"
        },
        "22": {
            "description": "Unknown error testing validity"
        },
        "23": {
            "description": "Error saving data object to XML"
        },
        "24": {
            "description": "Unable to test validity of default",
            "severity": 2
        },
        "300": {
            "description": "Compared objects are the same",
            "severity": 0
        },
        "315": {
            "description": "Both compared objects are null",
            "severity": 0
        },
        "301": {
            "description": "Unable to compare this class of data",
            "severity": 2
        },
        "302": {
            "description": "Other data has null value"
        },
        "303": {
            "description": "My data has null value"
        },
        "304": {
            "description": "Data has different values"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    contents_order=['identifier', 'formula', 'dictionaryName', 'smiles'],
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CMonomer",
)
class CMonomer(CData):
    """A monomer compound. ?smiles"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute")
    },
    error_codes={
        "101": {
            "description": "File does not exist"
        },
        "102": {
            "description": "No mime type for data file"
        },
        "103": {
            "description": "Attempting to set file content with inappropriate data"
        },
        "104": {
            "description": "There is no file content class specified for this type of file"
        },
        "105": {
            "description": "The file content class specified for this type of file can not be found"
        },
        "300": {
            "description": "Passed",
            "severity": 0
        },
        "305": {
            "description": "Neither original nor test file exists",
            "severity": 0
        },
        "306": {
            "description": "Original file does not exists"
        },
        "307": {
            "description": "Test file does not exist "
        },
        "308": {
            "description": "Files failed checksum comparison"
        },
        "309": {
            "description": "Files failed size comparison"
        },
        "310": {
            "description": "No comparison testing implemented for this file type",
            "severity": 2
        },
        "311": {
            "description": "Failed loading original file for comparison"
        },
        "312": {
            "description": "Failed loading test file for comparison"
        },
        "313": {
            "description": "Files failed simple text diff comparison"
        },
        "320": {
            "description": "Unrecognised error attempting to load file"
        }
    },
    qualifiers={
        "fileLabel": 'mol2',
        "mimeTypeName": 'chemical/x-mol2',
        "mimeTypeDescription": 'MOL2 file',
        "guiLabel": 'MOL2 file',
        "toolTip": 'Structure geometry of ligands for refinement in MOL2 format',
        "fileExtensions": ['mol2'],
        "fileContentClassName": None,
        "helpFile": 'model_data#mol2_file'
    },
    qualifiers_order=[
        'fileExtensions',
        'mimeTypeName',
        'mimeTypeDescription',
        'fileLabel',
        'allowUndefined',
        'mustExist',
        'fromPreviousJob',
        'jobCombo',
        'fileContentClassName',
        'isDirectory',
        'saveToDb',
        'requiredSubType',
        'requiredContentFlag'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool, "description": "Flag if data file can be undefined at run time"},
        "mustExist": {"type": bool, "description": "Flag if data file must exist at run time"},
        "fromPreviousJob": {"type": bool, "description": "Flag if input data file can be inferred from preceeding jobs"},
        "jobCombo": {"type": bool, "description": "Flag if data widget should be a combo box "},
        "mimeTypeName": {"type": str, "description": ""},
        "mimeTypeDescription": {"type": str, "description": ""},
        "fileLabel": {"type": str, "description": "Label for file"},
        "fileExtensions": {"type": list, "listItemType": "<class 'str'>", "description": "A list of strings containing allowed file extensions (no dot)"},
        "fileContentClassName": {"type": str, "editable": "False", "description": "A string containing the name of a class which will hold the file contents"},
        "isDirectory": {"type": bool, "description": "Flag if the data is a directory"},
        "ifInfo": {"type": bool, "description": "Flag if gui widget should have info icon"},
        "saveToDb": {"type": bool, "description": "Save the name of this file in the database"},
        "requiredSubType": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed sub types"},
        "requiredContentFlag": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed content flags"}
    },
    gui_label="CMol2DataFile",
)
class CMol2DataFile(CDataFile):
    """A molecule definition file (MOL2)"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute")
    },
    error_codes={
        "101": {
            "description": "File does not exist"
        },
        "102": {
            "description": "No mime type for data file"
        },
        "103": {
            "description": "Attempting to set file content with inappropriate data"
        },
        "104": {
            "description": "There is no file content class specified for this type of file"
        },
        "105": {
            "description": "The file content class specified for this type of file can not be found"
        },
        "300": {
            "description": "Passed",
            "severity": 0
        },
        "305": {
            "description": "Neither original nor test file exists",
            "severity": 0
        },
        "306": {
            "description": "Original file does not exists"
        },
        "307": {
            "description": "Test file does not exist "
        },
        "308": {
            "description": "Files failed checksum comparison"
        },
        "309": {
            "description": "Files failed size comparison"
        },
        "310": {
            "description": "No comparison testing implemented for this file type",
            "severity": 2
        },
        "311": {
            "description": "Failed loading original file for comparison"
        },
        "312": {
            "description": "Failed loading test file for comparison"
        },
        "313": {
            "description": "Files failed simple text diff comparison"
        },
        "320": {
            "description": "Unrecognised error attempting to load file"
        }
    },
    qualifiers={
        "fileLabel": 'mol',
        "mimeTypeName": 'chemical/x-mdl-molfile',
        "mimeTypeDescription": 'MDL Molfile',
        "guiLabel": 'Mol file',
        "toolTip": 'Structure geometry of ligands for refinement in MDL mol format',
        "fileExtensions": ['mol', 'sdf'],
        "fileContentClassName": None,
        "helpFile": 'model_data#mol_file'
    },
    qualifiers_order=[
        'fileExtensions',
        'mimeTypeName',
        'mimeTypeDescription',
        'fileLabel',
        'allowUndefined',
        'mustExist',
        'fromPreviousJob',
        'jobCombo',
        'fileContentClassName',
        'isDirectory',
        'saveToDb',
        'requiredSubType',
        'requiredContentFlag'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool, "description": "Flag if data file can be undefined at run time"},
        "mustExist": {"type": bool, "description": "Flag if data file must exist at run time"},
        "fromPreviousJob": {"type": bool, "description": "Flag if input data file can be inferred from preceeding jobs"},
        "jobCombo": {"type": bool, "description": "Flag if data widget should be a combo box "},
        "mimeTypeName": {"type": str, "description": ""},
        "mimeTypeDescription": {"type": str, "description": ""},
        "fileLabel": {"type": str, "description": "Label for file"},
        "fileExtensions": {"type": list, "listItemType": "<class 'str'>", "description": "A list of strings containing allowed file extensions (no dot)"},
        "fileContentClassName": {"type": str, "editable": "False", "description": "A string containing the name of a class which will hold the file contents"},
        "isDirectory": {"type": bool, "description": "Flag if the data is a directory"},
        "ifInfo": {"type": bool, "description": "Flag if gui widget should have info icon"},
        "saveToDb": {"type": bool, "description": "Save the name of this file in the database"},
        "requiredSubType": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed sub types"},
        "requiredContentFlag": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed content flags"}
    },
    gui_label="CMDLMolDataFile",
)
class CMDLMolDataFile(CDataFile):
    """A molecule definition file (MDL)"""
    pass


@cdata_class(
    attributes={
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "identifier": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="identifier attribute"),
        "chain": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="chain attribute")
    },
    error_codes={
        "0": {
            "severity": 0,
            "description": "OK"
        },
        "1": {
            "severity": 1,
            "description": "Data has undefined value"
        },
        "2": {
            "severity": 3,
            "description": "Data has undefined value"
        },
        "3": {
            "severity": 2,
            "description": "Missing data"
        },
        "4": {
            "description": "Missing data"
        },
        "5": {
            "description": "Attempting to set data of wrong type"
        },
        "6": {
            "description": "Default value does not satisfy validity check"
        },
        "7": {
            "severity": 2,
            "description": "Unrecognised qualifier in data input"
        },
        "8": {
            "severity": 2,
            "description": "Attempting to get inaccessible attribute:"
        },
        "9": {
            "description": "Failed to get property"
        },
        "10": {
            "severity": 2,
            "description": "Attempting to set inaccessible attribute:"
        },
        "11": {
            "description": "Failed to set property:"
        },
        "12": {
            "description": "Undetermined error setting value from XML"
        },
        "13": {
            "description": "Unrecognised class name in qualifier"
        },
        "14": {
            "severity": 2,
            "description": "No object name when saving qualifiers to XML"
        },
        "15": {
            "description": "Error saving qualifier to XML"
        },
        "16": {
            "severity": 2,
            "description": "Unrecognised item in XML data file"
        },
        "17": {
            "description": "Attempting to set unrecognised qualifier"
        },
        "18": {
            "description": "Attempting to set qualifier with wrong type"
        },
        "19": {
            "description": "Attempting to set qualifier with wrong list item type"
        },
        "20": {
            "description": "Error creating a list/dict item object"
        },
        "21": {
            "description": "Unknown error setting qualifiers from Xml file"
        },
        "22": {
            "description": "Unknown error testing validity"
        },
        "23": {
            "description": "Error saving data object to XML"
        },
        "24": {
            "description": "Unable to test validity of default",
            "severity": 2
        },
        "300": {
            "description": "Compared objects are the same",
            "severity": 0
        },
        "315": {
            "description": "Both compared objects are null",
            "severity": 0
        },
        "301": {
            "description": "Unable to compare this class of data",
            "severity": 2
        },
        "302": {
            "description": "Other data has null value"
        },
        "303": {
            "description": "My data has null value"
        },
        "304": {
            "description": "Data has different values"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CHhpredItem",
)
class CHhpredItem(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute")
    },
    error_codes={
        "101": {
            "description": "File does not exist"
        },
        "102": {
            "description": "No mime type for data file"
        },
        "103": {
            "description": "Attempting to set file content with inappropriate data"
        },
        "104": {
            "description": "There is no file content class specified for this type of file"
        },
        "105": {
            "description": "The file content class specified for this type of file can not be found"
        },
        "300": {
            "description": "Passed",
            "severity": 0
        },
        "305": {
            "description": "Neither original nor test file exists",
            "severity": 0
        },
        "306": {
            "description": "Original file does not exists"
        },
        "307": {
            "description": "Test file does not exist "
        },
        "308": {
            "description": "Files failed checksum comparison"
        },
        "309": {
            "description": "Files failed size comparison"
        },
        "310": {
            "description": "No comparison testing implemented for this file type",
            "severity": 2
        },
        "311": {
            "description": "Failed loading original file for comparison"
        },
        "312": {
            "description": "Failed loading test file for comparison"
        },
        "313": {
            "description": "Files failed simple text diff comparison"
        },
        "320": {
            "description": "Unrecognised error attempting to load file"
        }
    },
    qualifiers={
        "fileLabel": 'HHPred sequence search',
        "mimeTypeName": 'application/HHPred-alignments',
        "mimeTypeDescription": 'HHPred sequence search results',
        "guiLabel": 'HHPred results',
        "tooltip": 'Output from HHPred search',
        "fileExtensions": ['hhr'],
        "fileContentClassName": 'CHhpredData',
        "helpFile": 'model_data#ali'
    },
    qualifiers_order=[
        'fileExtensions',
        'mimeTypeName',
        'mimeTypeDescription',
        'fileLabel',
        'allowUndefined',
        'mustExist',
        'fromPreviousJob',
        'jobCombo',
        'fileContentClassName',
        'isDirectory',
        'saveToDb',
        'requiredSubType',
        'requiredContentFlag'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool, "description": "Flag if data file can be undefined at run time"},
        "mustExist": {"type": bool, "description": "Flag if data file must exist at run time"},
        "fromPreviousJob": {"type": bool, "description": "Flag if input data file can be inferred from preceeding jobs"},
        "jobCombo": {"type": bool, "description": "Flag if data widget should be a combo box "},
        "mimeTypeName": {"type": str, "description": ""},
        "mimeTypeDescription": {"type": str, "description": ""},
        "fileLabel": {"type": str, "description": "Label for file"},
        "fileExtensions": {"type": list, "listItemType": "<class 'str'>", "description": "A list of strings containing allowed file extensions (no dot)"},
        "fileContentClassName": {"type": str, "editable": "False", "description": "A string containing the name of a class which will hold the file contents"},
        "isDirectory": {"type": bool, "description": "Flag if the data is a directory"},
        "ifInfo": {"type": bool, "description": "Flag if gui widget should have info icon"},
        "saveToDb": {"type": bool, "description": "Save the name of this file in the database"},
        "requiredSubType": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed sub types"},
        "requiredContentFlag": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed content flags"}
    },
    gui_label="CHhpredDataFile",
)
class CHhpredDataFile(CDataFile):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass


@cdata_class(
    attributes={
        "alignmentList": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CList", tooltip="alignmentList attribute")
    },
    error_codes={
        "201": {
            "description": "Failed to read HHPred file"
        },
        "202": {
            "description": "Failed to load iotbx software to read HHPred file"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CHhpredData",
)
class CHhpredData(CDataFileContent):
    """Base class for classes holding file contents"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute"),
        "selection": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4ModelData.CAtomSelection", tooltip="selection attribute")
    },
    error_codes={
        "401": {
            "description": "Failed running coord_format to fix coordinate file - is it a PDB file?"
        },
        "402": {
            "severity": 2,
            "description": "Badly formated PDB file fixed"
        },
        "403": {
            "severity": 2,
            "description": "Fixed by removing text"
        },
        "404": {
            "severity": 2,
            "description": "Fixed by adding text"
        },
        "405": {
            "description": "There are no ATOM or HETATM lines in the PDB file"
        },
        "410": {
            "description": "No file loaded - can not convert coordinate file format"
        },
        "411": {
            "description": "Failed loading file - can not convert coordinate file format"
        },
        "412": {
            "description": "Can not overwrite existing file - can not convert coordinate file format"
        },
        "413": {
            "description": "Failed writing coordinate file"
        },
        "414": {
            "description": "Failed to identify coordinate file format"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "mustExist": False,
        "fromPreviousJob": False,
        "jobCombo": True,
        "mimeTypeName": 'chemical/x-pdb',
        "mimeTypeDescription": 'Model coordinates',
        "fileLabel": 'ensemble coordinates',
        "fileExtensions": ['pdb', 'cif', 'mmcif', 'ent'],
        "fileContentClassName": 'CPdbData',
        "isDirectory": False,
        "saveToDb": True,
        "requiredSubType": None,
        "requiredContentFlag": None,
        "guiLabel": 'Model ensemble',
        "toolTip": 'An ensemble of model coordinates in PDB or mmCIF format',
        "ifInfo": True,
        "ifAtomSelection": False,
        "downloadModes": [],
        "helpFile": 'model_data#ensemble_coordinate_files'
    },
    qualifiers_order=[
        'fileExtensions',
        'mimeTypeName',
        'mimeTypeDescription',
        'fileLabel',
        'allowUndefined',
        'mustExist',
        'fromPreviousJob',
        'jobCombo',
        'fileContentClassName',
        'isDirectory',
        'saveToDb',
        'requiredSubType',
        'requiredContentFlag'
    ],
    qualifiers_definition={
        "ifAtomSelection": {"type": bool, "description": "Atom selection option enabled"}
    },
    gui_label="CEnsemblePdbDataFile",
)
class CEnsemblePdbDataFile(CPdbDataFile):
    """A PDB coordinate file containing ensemble of structures as 'NMR' models"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "List shorter than required minimum length"
        },
        "102": {
            "description": "List longer than required maximum length"
        },
        "103": {
            "description": "Consecutive values in list fail comparison test"
        },
        "104": {
            "description": "Attempting to add object of wrong type"
        },
        "105": {
            "description": "Attempting to add object of correct type but wrong qualifiers"
        },
        "106": {
            "description": "Attempting to add data which does not satisfy the qualifiers for a list item"
        },
        "107": {
            "description": "Deleting item will reduce list below minimum length"
        },
        "108": {
            "description": "Adding item will extend list beyond maximum length"
        },
        "109": {
            "description": "Invalid item class"
        },
        "110": {
            "description": "etree (XML) list item of wrong type"
        },
        "112": {
            "description": "No list item object set for list"
        }
    },
    qualifiers={
        "listMinLength": 1
    },
    qualifiers_order=[
        'listMinLength',
        'listMaxLength',
        'listCompare'
    ],
    qualifiers_definition={
        "default": {"type": list},
        "listMaxLength": {"type": int, "description": "Inclusive maximum length of list"},
        "listMinLength": {"type": int, "description": "Inclusive minimum length of list"},
        "listCompare": {"type": int, "description": "If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method."}
    },
    gui_label="CEnsembleList",
)
class CEnsembleList(CList):
    """A list with all items of one CData sub-class"""
    pass


@cdata_class(
    attributes={
        "label": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.COneWord", tooltip="label attribute"),
        "number": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="number attribute"),
        "use": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CBoolean", tooltip="use attribute"),
        "pdbItemList": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CList", tooltip="pdbItemList attribute")
    },
    error_codes={
        "0": {
            "severity": 0,
            "description": "OK"
        },
        "1": {
            "severity": 1,
            "description": "Data has undefined value"
        },
        "2": {
            "severity": 3,
            "description": "Data has undefined value"
        },
        "3": {
            "severity": 2,
            "description": "Missing data"
        },
        "4": {
            "description": "Missing data"
        },
        "5": {
            "description": "Attempting to set data of wrong type"
        },
        "6": {
            "description": "Default value does not satisfy validity check"
        },
        "7": {
            "severity": 2,
            "description": "Unrecognised qualifier in data input"
        },
        "8": {
            "severity": 2,
            "description": "Attempting to get inaccessible attribute:"
        },
        "9": {
            "description": "Failed to get property"
        },
        "10": {
            "severity": 2,
            "description": "Attempting to set inaccessible attribute:"
        },
        "11": {
            "description": "Failed to set property:"
        },
        "12": {
            "description": "Undetermined error setting value from XML"
        },
        "13": {
            "description": "Unrecognised class name in qualifier"
        },
        "14": {
            "severity": 2,
            "description": "No object name when saving qualifiers to XML"
        },
        "15": {
            "description": "Error saving qualifier to XML"
        },
        "16": {
            "severity": 2,
            "description": "Unrecognised item in XML data file"
        },
        "17": {
            "description": "Attempting to set unrecognised qualifier"
        },
        "18": {
            "description": "Attempting to set qualifier with wrong type"
        },
        "19": {
            "description": "Attempting to set qualifier with wrong list item type"
        },
        "20": {
            "description": "Error creating a list/dict item object"
        },
        "21": {
            "description": "Unknown error setting qualifiers from Xml file"
        },
        "22": {
            "description": "Unknown error testing validity"
        },
        "23": {
            "description": "Error saving data object to XML"
        },
        "24": {
            "description": "Unable to test validity of default",
            "severity": 2
        },
        "300": {
            "description": "Compared objects are the same",
            "severity": 0
        },
        "315": {
            "description": "Both compared objects are null",
            "severity": 0
        },
        "301": {
            "description": "Unable to compare this class of data",
            "severity": 2
        },
        "302": {
            "description": "Other data has null value"
        },
        "303": {
            "description": "My data has null value"
        },
        "304": {
            "description": "Data has different values"
        }
    },
    qualifiers={
        "guiLabel": 'Ensemble',
        "allowUndefined": False
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CEnsemble",
)
class CEnsemble(CData):
    """An ensemble of models. Typically, this would be a set of related
PDB files, but models could also be xtal or EM maps. This should
be indicated by the types entry.
A single ensemble is a CList of structures."""
    pass


@cdata_class(
    error_codes={
        "201": {
            "description": "Word contains white space item"
        }
    },
    qualifiers={
        "onlyEnumerators": True,
        "enumerators": ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn']
    },
    qualifiers_order=[
        'minLength',
        'maxLength',
        'onlyEnumerators',
        'enumerators',
        'menuText',
        'allowedCharsCode'
    ],
    qualifiers_definition={
        "default": {"type": str},
        "maxLength": {"type": int, "description": "Maximum length of string"},
        "minLength": {"type": int, "description": "Minimum length of string"},
        "enumerators": {"type": list, "description": "A list of allowed or recommended values for string"},
        "menuText": {"type": list, "description": "A list of strings equivalent to the enumerators that will appear in the GUI"},
        "onlyEnumerators": {"type": bool, "description": "If this is true then the enumerators are obligatory - otherwise they are treated as recommended values"},
        "allowedCharsCode": {"type": int, "description": "Flag if the text is limited to set of allowed characters"}
    },
    gui_label="CElement",
)
class CElement(COneWord):
    """Chemical element """
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute")
    },
    error_codes={
        "201": {
            "description": "Error attempting to merge geometry files - no libcheck script"
        },
        "202": {
            "description": "Error attempting to merge geometry files - failed creating working directory"
        },
        "203": {
            "description": "Error attempting to merge geometry files - setting libcheck parameters"
        },
        "204": {
            "description": "Error attempting to merge geometry files - running libcheck"
        },
        "205": {
            "description": "Error attempting to merge geometry files - failed to run libcheck"
        }
    },
    qualifiers={
        "fileLabel": 'dictionary',
        "mimeTypeName": 'application/refmac-dictionary',
        "mimeTypeDescription": 'Geometry file',
        "guiLabel": 'Geometry dictionary',
        "toolTip": 'Idealised geometry of ligands for refinement',
        "fileExtensions": ['cif'],
        "fileContentClassName": 'CDictData',
        "helpFile": 'model_data#ligand_geometry'
    },
    qualifiers_order=[
        'fileExtensions',
        'mimeTypeName',
        'mimeTypeDescription',
        'fileLabel',
        'allowUndefined',
        'mustExist',
        'fromPreviousJob',
        'jobCombo',
        'fileContentClassName',
        'isDirectory',
        'saveToDb',
        'requiredSubType',
        'requiredContentFlag'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool, "description": "Flag if data file can be undefined at run time"},
        "mustExist": {"type": bool, "description": "Flag if data file must exist at run time"},
        "fromPreviousJob": {"type": bool, "description": "Flag if input data file can be inferred from preceeding jobs"},
        "jobCombo": {"type": bool, "description": "Flag if data widget should be a combo box "},
        "mimeTypeName": {"type": str, "description": ""},
        "mimeTypeDescription": {"type": str, "description": ""},
        "fileLabel": {"type": str, "description": "Label for file"},
        "fileExtensions": {"type": list, "listItemType": "<class 'str'>", "description": "A list of strings containing allowed file extensions (no dot)"},
        "fileContentClassName": {"type": str, "editable": "False", "description": "A string containing the name of a class which will hold the file contents"},
        "isDirectory": {"type": bool, "description": "Flag if the data is a directory"},
        "ifInfo": {"type": bool, "description": "Flag if gui widget should have info icon"},
        "saveToDb": {"type": bool, "description": "Save the name of this file in the database"},
        "requiredSubType": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed sub types"},
        "requiredContentFlag": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed content flags"}
    },
    gui_label="CDictDataFile",
)
class CDictDataFile(CDataFile):
    """A refmac dictionary file"""
    pass


@cdata_class(
    attributes={
        "monomerList": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CList", tooltip="monomerList attribute")
    },
    error_codes={
        "101": {
            "description": "Error opening MMCIF format file"
        },
        "102": {
            "description": "Error merging data - monomer already in geometry file"
        },
        "103": {
            "severity": 2,
            "description": "Warning merging data - overwriting geometry for monomer with same id"
        },
        "104": {
            "description": "Error reading geometry cif file - does not contain expected data"
        },
        "105": {
            "description": "Unknown error reading geometry file"
        },
        "106": {
            "description": "_chem_comp section not found in geometry file"
        },
        "110": {
            "description": "Attemting to delete unrecognised chem_comp.id"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CDictData",
)
class CDictData(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass


@cdata_class(
    attributes={
        "id": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.COneWord", tooltip="id attribute"),
        "three_letter_code": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.COneWord", tooltip="three_letter_code attribute"),
        "name": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="name attribute"),
        "group": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="group attribute"),
        "number_atoms_all": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="number_atoms_all attribute"),
        "number_atoms_nh": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="number_atoms_nh attribute"),
        "desc_level": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="desc_level attribute")
    },
    error_codes={
        "201": {
            "description": "Error reading monomer id and name"
        },
        "202": {
            "description": "Error writing monomer id and name"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CChemComp",
)
class CChemComp(CData):
    """Component of CDictDataFile contents"""
    pass


@cdata_class(
    attributes={
        "hitId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="hitId attribute"),
        "querySequence": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="querySequence attribute"),
        "hitSequence": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="hitSequence attribute")
    },
    error_codes={
        "0": {
            "severity": 0,
            "description": "OK"
        },
        "1": {
            "severity": 1,
            "description": "Data has undefined value"
        },
        "2": {
            "severity": 3,
            "description": "Data has undefined value"
        },
        "3": {
            "severity": 2,
            "description": "Missing data"
        },
        "4": {
            "description": "Missing data"
        },
        "5": {
            "description": "Attempting to set data of wrong type"
        },
        "6": {
            "description": "Default value does not satisfy validity check"
        },
        "7": {
            "severity": 2,
            "description": "Unrecognised qualifier in data input"
        },
        "8": {
            "severity": 2,
            "description": "Attempting to get inaccessible attribute:"
        },
        "9": {
            "description": "Failed to get property"
        },
        "10": {
            "severity": 2,
            "description": "Attempting to set inaccessible attribute:"
        },
        "11": {
            "description": "Failed to set property:"
        },
        "12": {
            "description": "Undetermined error setting value from XML"
        },
        "13": {
            "description": "Unrecognised class name in qualifier"
        },
        "14": {
            "severity": 2,
            "description": "No object name when saving qualifiers to XML"
        },
        "15": {
            "description": "Error saving qualifier to XML"
        },
        "16": {
            "severity": 2,
            "description": "Unrecognised item in XML data file"
        },
        "17": {
            "description": "Attempting to set unrecognised qualifier"
        },
        "18": {
            "description": "Attempting to set qualifier with wrong type"
        },
        "19": {
            "description": "Attempting to set qualifier with wrong list item type"
        },
        "20": {
            "description": "Error creating a list/dict item object"
        },
        "21": {
            "description": "Unknown error setting qualifiers from Xml file"
        },
        "22": {
            "description": "Unknown error testing validity"
        },
        "23": {
            "description": "Error saving data object to XML"
        },
        "24": {
            "description": "Unable to test validity of default",
            "severity": 2
        },
        "300": {
            "description": "Compared objects are the same",
            "severity": 0
        },
        "315": {
            "description": "Both compared objects are null",
            "severity": 0
        },
        "301": {
            "description": "Unable to compare this class of data",
            "severity": 2
        },
        "302": {
            "description": "Other data has null value"
        },
        "303": {
            "description": "My data has null value"
        },
        "304": {
            "description": "Data has different values"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CBlastItem",
)
class CBlastItem(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute")
    },
    error_codes={
        "101": {
            "description": "File does not exist"
        },
        "102": {
            "description": "No mime type for data file"
        },
        "103": {
            "description": "Attempting to set file content with inappropriate data"
        },
        "104": {
            "description": "There is no file content class specified for this type of file"
        },
        "105": {
            "description": "The file content class specified for this type of file can not be found"
        },
        "300": {
            "description": "Passed",
            "severity": 0
        },
        "305": {
            "description": "Neither original nor test file exists",
            "severity": 0
        },
        "306": {
            "description": "Original file does not exists"
        },
        "307": {
            "description": "Test file does not exist "
        },
        "308": {
            "description": "Files failed checksum comparison"
        },
        "309": {
            "description": "Files failed size comparison"
        },
        "310": {
            "description": "No comparison testing implemented for this file type",
            "severity": 2
        },
        "311": {
            "description": "Failed loading original file for comparison"
        },
        "312": {
            "description": "Failed loading test file for comparison"
        },
        "313": {
            "description": "Files failed simple text diff comparison"
        },
        "320": {
            "description": "Unrecognised error attempting to load file"
        }
    },
    qualifiers={
        "fileLabel": 'Blast sequence search',
        "mimeTypeName": 'application/Blast-alignments',
        "mimeTypeDescription": 'Blast sequence search results',
        "guiLabel": 'Blast results',
        "tooltip": 'Output from Blast search',
        "fileExtensions": ['bla', 'blast', 'xml'],
        "fileContentClassName": 'CBlastData',
        "helpFile": 'model_data#ali'
    },
    qualifiers_order=[
        'fileExtensions',
        'mimeTypeName',
        'mimeTypeDescription',
        'fileLabel',
        'allowUndefined',
        'mustExist',
        'fromPreviousJob',
        'jobCombo',
        'fileContentClassName',
        'isDirectory',
        'saveToDb',
        'requiredSubType',
        'requiredContentFlag'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool, "description": "Flag if data file can be undefined at run time"},
        "mustExist": {"type": bool, "description": "Flag if data file must exist at run time"},
        "fromPreviousJob": {"type": bool, "description": "Flag if input data file can be inferred from preceeding jobs"},
        "jobCombo": {"type": bool, "description": "Flag if data widget should be a combo box "},
        "mimeTypeName": {"type": str, "description": ""},
        "mimeTypeDescription": {"type": str, "description": ""},
        "fileLabel": {"type": str, "description": "Label for file"},
        "fileExtensions": {"type": list, "listItemType": "<class 'str'>", "description": "A list of strings containing allowed file extensions (no dot)"},
        "fileContentClassName": {"type": str, "editable": "False", "description": "A string containing the name of a class which will hold the file contents"},
        "isDirectory": {"type": bool, "description": "Flag if the data is a directory"},
        "ifInfo": {"type": bool, "description": "Flag if gui widget should have info icon"},
        "saveToDb": {"type": bool, "description": "Save the name of this file in the database"},
        "requiredSubType": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed sub types"},
        "requiredContentFlag": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed content flags"}
    },
    gui_label="CBlastDataFile",
)
class CBlastDataFile(CDataFile):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass


@cdata_class(
    attributes={
        "queryId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="queryId attribute"),
        "alignmentList": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CList", tooltip="alignmentList attribute")
    },
    error_codes={
        "201": {
            "description": "Failed reading blast file"
        },
        "202": {
            "description": "Blast file contains results of more than one query - only the first is read",
            "severity": 2
        },
        "203": {
            "description": "Failed parsing Blast file"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CBlastData",
)
class CBlastData(CDataFileContent):
    """Base class for classes holding file contents"""
    pass


@cdata_class(
    attributes={
        "text": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="text attribute")
    },
    error_codes={
        "0": {
            "severity": 0,
            "description": "OK"
        },
        "1": {
            "severity": 1,
            "description": "Data has undefined value"
        },
        "2": {
            "severity": 3,
            "description": "Data has undefined value"
        },
        "3": {
            "severity": 2,
            "description": "Missing data"
        },
        "4": {
            "description": "Missing data"
        },
        "5": {
            "description": "Attempting to set data of wrong type"
        },
        "6": {
            "description": "Default value does not satisfy validity check"
        },
        "7": {
            "severity": 2,
            "description": "Unrecognised qualifier in data input"
        },
        "8": {
            "severity": 2,
            "description": "Attempting to get inaccessible attribute:"
        },
        "9": {
            "description": "Failed to get property"
        },
        "10": {
            "severity": 2,
            "description": "Attempting to set inaccessible attribute:"
        },
        "11": {
            "description": "Failed to set property:"
        },
        "12": {
            "description": "Undetermined error setting value from XML"
        },
        "13": {
            "description": "Unrecognised class name in qualifier"
        },
        "14": {
            "severity": 2,
            "description": "No object name when saving qualifiers to XML"
        },
        "15": {
            "description": "Error saving qualifier to XML"
        },
        "16": {
            "severity": 2,
            "description": "Unrecognised item in XML data file"
        },
        "17": {
            "description": "Attempting to set unrecognised qualifier"
        },
        "18": {
            "description": "Attempting to set qualifier with wrong type"
        },
        "19": {
            "description": "Attempting to set qualifier with wrong list item type"
        },
        "20": {
            "description": "Error creating a list/dict item object"
        },
        "21": {
            "description": "Unknown error setting qualifiers from Xml file"
        },
        "22": {
            "description": "Unknown error testing validity"
        },
        "23": {
            "description": "Error saving data object to XML"
        },
        "24": {
            "description": "Unable to test validity of default",
            "severity": 2
        },
        "300": {
            "description": "Compared objects are the same",
            "severity": 0
        },
        "315": {
            "description": "Both compared objects are null",
            "severity": 0
        },
        "301": {
            "description": "Unable to compare this class of data",
            "severity": 2
        },
        "302": {
            "description": "Other data has null value"
        },
        "303": {
            "description": "My data has null value"
        },
        "304": {
            "description": "Data has different values"
        }
    },
    qualifiers={
        "pdbFileKey": ''
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "pdbFileKey": {"type": str, "description": "The key for a CPdbDataFile in the same CContainer"}
    },
    gui_label="CAtomSelection",
)
class CAtomSelection(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass


@cdata_class(
    attributes={
        "groupId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="groupId attribute"),
        "chainIds": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="chainIds attribute"),
        "firstRes": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="firstRes attribute"),
        "lastRes": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="lastRes attribute"),
        "atoms": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="atoms attribute"),
        "alt": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.COneWord", tooltip="alt attribute")
    },
    error_codes={
        "0": {
            "severity": 0,
            "description": "OK"
        },
        "1": {
            "severity": 1,
            "description": "Data has undefined value"
        },
        "2": {
            "severity": 3,
            "description": "Data has undefined value"
        },
        "3": {
            "severity": 2,
            "description": "Missing data"
        },
        "4": {
            "description": "Missing data"
        },
        "5": {
            "description": "Attempting to set data of wrong type"
        },
        "6": {
            "description": "Default value does not satisfy validity check"
        },
        "7": {
            "severity": 2,
            "description": "Unrecognised qualifier in data input"
        },
        "8": {
            "severity": 2,
            "description": "Attempting to get inaccessible attribute:"
        },
        "9": {
            "description": "Failed to get property"
        },
        "10": {
            "severity": 2,
            "description": "Attempting to set inaccessible attribute:"
        },
        "11": {
            "description": "Failed to set property:"
        },
        "12": {
            "description": "Undetermined error setting value from XML"
        },
        "13": {
            "description": "Unrecognised class name in qualifier"
        },
        "14": {
            "severity": 2,
            "description": "No object name when saving qualifiers to XML"
        },
        "15": {
            "description": "Error saving qualifier to XML"
        },
        "16": {
            "severity": 2,
            "description": "Unrecognised item in XML data file"
        },
        "17": {
            "description": "Attempting to set unrecognised qualifier"
        },
        "18": {
            "description": "Attempting to set qualifier with wrong type"
        },
        "19": {
            "description": "Attempting to set qualifier with wrong list item type"
        },
        "20": {
            "description": "Error creating a list/dict item object"
        },
        "21": {
            "description": "Unknown error setting qualifiers from Xml file"
        },
        "22": {
            "description": "Unknown error testing validity"
        },
        "23": {
            "description": "Error saving data object to XML"
        },
        "24": {
            "description": "Unable to test validity of default",
            "severity": 2
        },
        "300": {
            "description": "Compared objects are the same",
            "severity": 0
        },
        "315": {
            "description": "Both compared objects are null",
            "severity": 0
        },
        "301": {
            "description": "Unable to compare this class of data",
            "severity": 2
        },
        "302": {
            "description": "Other data has null value"
        },
        "303": {
            "description": "My data has null value"
        },
        "304": {
            "description": "Data has different values"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    contents_order=['groupId', 'chainIds',
                    'firstRes', 'lastRes', 'atoms', 'alt'],
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CAtomRefmacSelectionOccupancy",
)
class CAtomRefmacSelectionOccupancy(CData):
    """A residue range selection for occupancy groups"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "List shorter than required minimum length"
        },
        "102": {
            "description": "List longer than required maximum length"
        },
        "103": {
            "description": "Consecutive values in list fail comparison test"
        },
        "104": {
            "description": "Attempting to add object of wrong type"
        },
        "105": {
            "description": "Attempting to add object of correct type but wrong qualifiers"
        },
        "106": {
            "description": "Attempting to add data which does not satisfy the qualifiers for a list item"
        },
        "107": {
            "description": "Deleting item will reduce list below minimum length"
        },
        "108": {
            "description": "Adding item will extend list beyond maximum length"
        },
        "109": {
            "description": "Invalid item class"
        },
        "110": {
            "description": "etree (XML) list item of wrong type"
        },
        "112": {
            "description": "No list item object set for list"
        }
    },
    qualifiers={
        "listMinLength": 0
    },
    qualifiers_order=[
        'listMinLength',
        'listMaxLength',
        'listCompare'
    ],
    qualifiers_definition={
        "default": {"type": list},
        "listMaxLength": {"type": int, "description": "Inclusive maximum length of list"},
        "listMinLength": {"type": int, "description": "Inclusive minimum length of list"},
        "listCompare": {"type": int, "description": "If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method."}
    },
    gui_label="CAtomRefmacSelectionList",
)
class CAtomRefmacSelectionList(CList):
    """A list with all items of one CData sub-class"""
    pass


@cdata_class(
    attributes={
        "groupIds": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="groupIds attribute")
    },
    error_codes={
        "0": {
            "severity": 0,
            "description": "OK"
        },
        "1": {
            "severity": 1,
            "description": "Data has undefined value"
        },
        "2": {
            "severity": 3,
            "description": "Data has undefined value"
        },
        "3": {
            "severity": 2,
            "description": "Missing data"
        },
        "4": {
            "description": "Missing data"
        },
        "5": {
            "description": "Attempting to set data of wrong type"
        },
        "6": {
            "description": "Default value does not satisfy validity check"
        },
        "7": {
            "severity": 2,
            "description": "Unrecognised qualifier in data input"
        },
        "8": {
            "severity": 2,
            "description": "Attempting to get inaccessible attribute:"
        },
        "9": {
            "description": "Failed to get property"
        },
        "10": {
            "severity": 2,
            "description": "Attempting to set inaccessible attribute:"
        },
        "11": {
            "description": "Failed to set property:"
        },
        "12": {
            "description": "Undetermined error setting value from XML"
        },
        "13": {
            "description": "Unrecognised class name in qualifier"
        },
        "14": {
            "severity": 2,
            "description": "No object name when saving qualifiers to XML"
        },
        "15": {
            "description": "Error saving qualifier to XML"
        },
        "16": {
            "severity": 2,
            "description": "Unrecognised item in XML data file"
        },
        "17": {
            "description": "Attempting to set unrecognised qualifier"
        },
        "18": {
            "description": "Attempting to set qualifier with wrong type"
        },
        "19": {
            "description": "Attempting to set qualifier with wrong list item type"
        },
        "20": {
            "description": "Error creating a list/dict item object"
        },
        "21": {
            "description": "Unknown error setting qualifiers from Xml file"
        },
        "22": {
            "description": "Unknown error testing validity"
        },
        "23": {
            "description": "Error saving data object to XML"
        },
        "24": {
            "description": "Unable to test validity of default",
            "severity": 2
        },
        "300": {
            "description": "Compared objects are the same",
            "severity": 0
        },
        "315": {
            "description": "Both compared objects are null",
            "severity": 0
        },
        "301": {
            "description": "Unable to compare this class of data",
            "severity": 2
        },
        "302": {
            "description": "Other data has null value"
        },
        "303": {
            "description": "My data has null value"
        },
        "304": {
            "description": "Data has different values"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    contents_order=['groupIds'],
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CAtomRefmacSelectionGroups",
)
class CAtomRefmacSelectionGroups(CData):
    """A group selection for occupancy groups"""
    pass


@cdata_class(
    attributes={
        "groupId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="groupId attribute"),
        "chainId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.COneWord", tooltip="chainId attribute"),
        "firstRes": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="firstRes attribute"),
        "lastRes": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="lastRes attribute")
    },
    error_codes={
        "0": {
            "severity": 0,
            "description": "OK"
        },
        "1": {
            "severity": 1,
            "description": "Data has undefined value"
        },
        "2": {
            "severity": 3,
            "description": "Data has undefined value"
        },
        "3": {
            "severity": 2,
            "description": "Missing data"
        },
        "4": {
            "description": "Missing data"
        },
        "5": {
            "description": "Attempting to set data of wrong type"
        },
        "6": {
            "description": "Default value does not satisfy validity check"
        },
        "7": {
            "severity": 2,
            "description": "Unrecognised qualifier in data input"
        },
        "8": {
            "severity": 2,
            "description": "Attempting to get inaccessible attribute:"
        },
        "9": {
            "description": "Failed to get property"
        },
        "10": {
            "severity": 2,
            "description": "Attempting to set inaccessible attribute:"
        },
        "11": {
            "description": "Failed to set property:"
        },
        "12": {
            "description": "Undetermined error setting value from XML"
        },
        "13": {
            "description": "Unrecognised class name in qualifier"
        },
        "14": {
            "severity": 2,
            "description": "No object name when saving qualifiers to XML"
        },
        "15": {
            "description": "Error saving qualifier to XML"
        },
        "16": {
            "severity": 2,
            "description": "Unrecognised item in XML data file"
        },
        "17": {
            "description": "Attempting to set unrecognised qualifier"
        },
        "18": {
            "description": "Attempting to set qualifier with wrong type"
        },
        "19": {
            "description": "Attempting to set qualifier with wrong list item type"
        },
        "20": {
            "description": "Error creating a list/dict item object"
        },
        "21": {
            "description": "Unknown error setting qualifiers from Xml file"
        },
        "22": {
            "description": "Unknown error testing validity"
        },
        "23": {
            "description": "Error saving data object to XML"
        },
        "24": {
            "description": "Unable to test validity of default",
            "severity": 2
        },
        "300": {
            "description": "Compared objects are the same",
            "severity": 0
        },
        "315": {
            "description": "Both compared objects are null",
            "severity": 0
        },
        "301": {
            "description": "Unable to compare this class of data",
            "severity": 2
        },
        "302": {
            "description": "Other data has null value"
        },
        "303": {
            "description": "My data has null value"
        },
        "304": {
            "description": "Data has different values"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    contents_order=['groupId', 'chainId', 'firstRes', 'lastRes'],
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CAtomRefmacSelection",
)
class CAtomRefmacSelection(CData):
    """A residue range selection for rigid body groups"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute"),
        "selection": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CDict", tooltip="selection attribute")
    },
    error_codes={
        "1003": {
            "description": "XML does not have <ccp4i2> root node"
        },
        "1004": {
            "severity": 2,
            "description": "XML does not have <ccp4i2_header> section"
        },
        "1005": {
            "description": "XML does not have <ccp4i2_body> section"
        }
    },
    qualifiers={
        "mimeTypeName": 'application/CCP4-asu-content',
        "mimeTypeDescription": 'AU content',
        "fileExtensions": ['asu.xml'],
        "fileContentClassName": 'CAsuContent',
        "fileLabel": 'AU contents',
        "guiLabel": 'AU contents',
        "toolTip": 'A CCP4i2 file specifying AU contents',
        "helpFile": 'model_data#sequences',
        "saveToDb": True,
        "selectionMode": 0
    },
    contents_order=['selection'],
    qualifiers_order=[
        'autoLoadHeader'
    ],
    qualifiers_definition={
        "selectionMode": {"type": int, "description": "Chain selection options"}
    },
    gui_label="CAsuDataFile",
)
class CAsuDataFile(CI2XmlDataFile):
    """A reference to an XML file with CCP4i2 Header"""
    pass


@cdata_class(
    error_codes={
        "401": {
            "description": "Sequence the same as a sequence that is already loaded"
        },
        "402": {
            "description": "Sequence names are not unique: "
        }
    },
    qualifiers={
        "listMinLength": 0
    },
    qualifiers_order=[
        'listMinLength',
        'listMaxLength',
        'listCompare'
    ],
    qualifiers_definition={
        "default": {"type": list},
        "listMaxLength": {"type": int, "description": "Inclusive maximum length of list"},
        "listMinLength": {"type": int, "description": "Inclusive minimum length of list"},
        "listCompare": {"type": int, "description": "If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method."}
    },
    gui_label="CAsuContentSeqList",
)
class CAsuContentSeqList(CList):
    """A list with all items of one CData sub-class"""
    pass


@cdata_class(
    attributes={
        "sequence": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4ModelData.CSequenceString", tooltip="sequence attribute"),
        "nCopies": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="nCopies attribute"),
        "polymerType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="polymerType attribute"),
        "name": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="name attribute"),
        "description": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="description attribute"),
        "source": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CDataFile", tooltip="source attribute")
    },
    error_codes={
        "0": {
            "severity": 0,
            "description": "OK"
        },
        "1": {
            "severity": 1,
            "description": "Data has undefined value"
        },
        "2": {
            "severity": 3,
            "description": "Data has undefined value"
        },
        "3": {
            "severity": 2,
            "description": "Missing data"
        },
        "4": {
            "description": "Missing data"
        },
        "5": {
            "description": "Attempting to set data of wrong type"
        },
        "6": {
            "description": "Default value does not satisfy validity check"
        },
        "7": {
            "severity": 2,
            "description": "Unrecognised qualifier in data input"
        },
        "8": {
            "severity": 2,
            "description": "Attempting to get inaccessible attribute:"
        },
        "9": {
            "description": "Failed to get property"
        },
        "10": {
            "severity": 2,
            "description": "Attempting to set inaccessible attribute:"
        },
        "11": {
            "description": "Failed to set property:"
        },
        "12": {
            "description": "Undetermined error setting value from XML"
        },
        "13": {
            "description": "Unrecognised class name in qualifier"
        },
        "14": {
            "severity": 2,
            "description": "No object name when saving qualifiers to XML"
        },
        "15": {
            "description": "Error saving qualifier to XML"
        },
        "16": {
            "severity": 2,
            "description": "Unrecognised item in XML data file"
        },
        "17": {
            "description": "Attempting to set unrecognised qualifier"
        },
        "18": {
            "description": "Attempting to set qualifier with wrong type"
        },
        "19": {
            "description": "Attempting to set qualifier with wrong list item type"
        },
        "20": {
            "description": "Error creating a list/dict item object"
        },
        "21": {
            "description": "Unknown error setting qualifiers from Xml file"
        },
        "22": {
            "description": "Unknown error testing validity"
        },
        "23": {
            "description": "Error saving data object to XML"
        },
        "24": {
            "description": "Unable to test validity of default",
            "severity": 2
        },
        "300": {
            "description": "Compared objects are the same",
            "severity": 0
        },
        "315": {
            "description": "Both compared objects are null",
            "severity": 0
        },
        "301": {
            "description": "Unable to compare this class of data",
            "severity": 2
        },
        "302": {
            "description": "Other data has null value"
        },
        "303": {
            "description": "My data has null value"
        },
        "304": {
            "description": "Data has different values"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CAsuContentSeq",
)
class CAsuContentSeq(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass


@cdata_class(
    attributes={
        "seqList": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4ModelData.CAsuContentSeqList", tooltip="seqList attribute")
    },
    error_codes={
        "101": {
            "description": "Failed reading file - is it correct file type?"
        },
        "102": {
            "description": "Failed reading file - it is not AU contents file"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CAsuContent",
)
class CAsuContent(CDataFileContent):
    """Base class for classes holding file contents"""
    pass
