#!/usr/bin/env python3
"""
Template Builder Python Classes
"""


class Field:
    """
    Fields are the columns that are added to the workbook. Each field must have a destination (sheet), header
    name (fieldName), description (fieldDefinition) and the attribute type defined (fieldType).

    The allowed fieldType options are:
        string - general format cells with no restrictions.
        date - Excel date format with validation. Dates and times must have the formatString defined.
        list - Validation from another column in the spreadsheet. Source must be defined in the lookup variable.
        integer - validation of integers only. Maybe constrained using minValue and maxValue.
        decimal - validation of numbers. May be constrained using minValue and maxValue.

    Dates and times field types should have the date format defined as the formatString. Some examples include
    YYYY-MM-DD for dates and HH:MM for hours/minutes. See Excel Format Cells dialogue for help.

    List items should be loaded as Vocab instances.

    Integers and decimals fields can be limited to a certain range using the min and max values. The min and max values
    are inclusive.

    """

    # list of all the fields to write to the schema tab
    all = []

    def __init__(
        self,
        sheet=None,
        fieldName=None,
        fieldDefinition=None,
        fieldType="string",
        formatString=None,
        lookup=None,
        unit=None,
        minValue=None,
        maxValue=None,
        warnLevel="warning",
    ):
        self.all.append(self)  # add item to the list of all fields
        self.sheet = sheet
        self.fieldName = fieldName
        self.fieldDefinition = fieldDefinition
        self.fieldType = fieldType
        self.formatString = formatString
        self.lookup = lookup
        self.unit = unit
        self.minValue = minValue
        self.maxValue = maxValue
        self.warnLevel = warnLevel

    # @property
    # def fieldtype(self):
    #     return self._fieldType
    #
    # # limits fieldType to predefined options only
    # @fieldtype.setter
    # def fieldtype(self, value):
    #     acceptableTypes = ['string', 'date', 'list', 'integer', 'decimal', 'time']
    #     if value not in acceptableTypes:
    #         raise ValueError("Unknown fieldType: {}. Valid fieldType include {}".format(value, acceptableTypes))
    #     self._fieldType = value

    # # limits warnLevel to predefined options only
    # @fieldtype.setter
    # def warningType(self, value):
    #     acceptableTypes = ['warning', 'stop', 'information']
    #     if value not in acceptableTypes:
    #         raise ValueError("Unknown warning level: {}. Valid warnings must be one of {}".format(value, acceptableTypes))
    #     self._warnLevel = value


class Vocab:
    """
    Controlled vocabulary for fields. The controlled vocabulary is used for populating validation drop down menus.

    Each vocabulary term must have the destination field (fieldName) and the term/code itself (code). It is also
    best practice to include a definition for each code.
    """

    # list of all the Vocab terms to write to the vocab tab
    all = []

    def __init__(self, fieldName=None, code=None, definition=None):
        self.all.append(self)  # add item to the list of all vocab terms
        self.fieldName = fieldName
        self.code = code
        self.definition = definition

    def __repr__(self):
        return "(fieldName: {}, code: {}, definition: {})".format(
            self.fieldName, self.code, self.definition
        )
