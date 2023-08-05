#!/usr/bin/env python3
"""
Validation rules
"""

from MarinegeoTemplateBuilder.construct import *
from MarinegeoTemplateBuilder.classes import Field
import datetime
import string
import warnings
import re


def validateList(field):
    """
    Validates items in a list. The items should be part of controlled vocabulary list which are Excel named ranges.
    The excel named range is set to be the same as the fieldName
    :param field: instance of the Field class
    :return: validator
    """
    validator = {
        "validate": "list",
        "error_type": field.warnLevel,
        "source": "={}".format(field.fieldName),
    }
    return validator


def validateFkey(field, allFields=Field.all):
    """
    Validates items from another column in the worksheet. The other column must be defined in the lookup field. The
    lookup field should follow the pattern of Sheet$fieldName where sheet is the worksheet where the column is
    located and fieldName is the name of the field to pull. The dropDownfkey() function uses the list of
    fields in the workbook (from the schemaFields) to locate the appropriate sheet/column letter to use to build
    the equation.

    Important: the lookup column must be defined before the validation rule gets set on the column. For example, it
    won't work if you are trying to lookup a column (Habitat$geoform) before the habitat sheet is created because
    the fields that belong to that sheet are not yet added to schemaFields.

    :param field: instance of the Field class
    :param allFields: list of all fields in the workbook.
    :return: validator
    """
    fsheet, fkey = field.lookup.split("$")
    eq = dropDownfkey(allFields, fsheet, fkey)
    validator = {
        "validate": "list",
        "error_type": field.warnLevel,
        "source": "{}".format(eq),
    }
    return validator


def validateDate(field=None):
    """
    Creates validation rule to check dates. Dates entered must be greater than 1/1/1900.
    :param field: None needed
    :return: validator
    """
    validator = {
        "validate": "date",
        "criteria": "greater than",
        "error_type": field.warnLevel,
        "minimum": datetime.date(1, 1, 1),
    }
    return validator


def validateTime(field=None):
    """
    Creates a validation ruleset to check that times are valid. Times must be between 00:00 and 23:59.
    :param field: None need
    :return: validator
    """
    validator = {
        "validate": "time",
        "criteria": "between",
        "minimum": datetime.time(0, 0),
        "error_type": field.warnLevel,
        "maximum": datetime.time(23, 59, 59),
    }
    return validator


def validateNumber(field):
    """
    Validation rule set to check that items entered into a column integers or decimals.
    :param field: instance of the Field class
    :return: validator
    """
    validator = {
        "validate": field.fieldType,
        "criteria": "greater than",
        "value": "-1e99",
        "error_type": field.warnLevel,
        "error_message": "{} must be a number.".format(field.fieldName),
    }
    return validator


def validateGreaterThan(field):
    """
    Validation rule set to check that items entered into a column are greater or equal to the minimum value set
    for the field (field.minValue). Works for both integers and decimals.
    :param field: instance of the Field class
    :return: validator
    """
    validator = {
        "validate": field.fieldType,
        "criteria": "greater than or equal to",
        "value": field.minValue,
        "error_type": field.warnLevel,
        "error_message": "{} must be greater than {}.".format(
            field.fieldType.capitalize(), field.minValue
        ),
    }
    return validator


def validateLessThan(field):
    """
    Validation rule set to check that items entered into a column are less or equal to the maximum value set
    for the field (field.maxValue). Works for both integers and decimals.
    :param field: instance of the Field class
    :return: validator
    """
    validator = {
        "validate": field.fieldType,
        "criteria": "less than or equal to",
        "value": field.maxValue,
        "error_type": field.warnLevel,
        "error_message": "{} must be less than {}.".format(
            field.fieldType.capitalize(), field.maxValue
        ),
    }
    return validator


def validateBetween(field):
    """
    Validation rule set to check that items entered into a column are between the minimum and maximum values for a
    field. Works for both integers and decimals. Min and max bound are inclusive.
    :param field: instance of the Field class
    :return: validator
    """
    validator = {
        "validate": field.fieldType,
        "criteria": "between",
        "minimum": field.minValue,
        "maximum": field.maxValue,
        "error_type": field.warnLevel,
        "error_message": "{} must be between {} and {}.".format(
            field.fieldType.capitalize(), field.minValue, field.maxValue
        ),
    }
    return validator


def selectValidator(field):
    """
    Selects the correct validator function using the fieldType attribute of the given field. New validators should
    be defined as a function and added as an additional item to conditional in this function.
    :param field: Field class instance where validation is going to be applied
    :return: validator function
    """
    if field.fieldType == "string":
        pass
    elif field.fieldType == "list":
        return validateList
    elif field.fieldType == "fkey":
        return validateFkey
    elif field.fieldType == "date":
        return validateDate
    elif field.fieldType == "time":
        return validateTime
    elif field.fieldType == "integer" or field.fieldType == "decimal":
        if field.minValue is None and field.maxValue is None:
            return validateNumber
        elif isfloat(field.minValue) and not isfloat(field.maxValue):
            return validateGreaterThan
        elif not isfloat(field.minValue) and isfloat(field.maxValue):
            return validateLessThan
        elif (
            isfloat(field.minValue)
            & isfloat(field.minValue)
            & (float(field.minValue) < float(field.maxValue))
        ):
            return validateBetween
        else:
            warnings.warn(
                "Unable to create a validator for {}. Check inputs.".format(
                    field.fieldName
                )
            )
            pass
    elif (
        field.fieldType == "equation"
    ):  # equations are not validated since they are formulas
        pass
    else:
        raise ValueError(
            "Unknown validator for {} .... field type is {}".format(
                field.fieldName, field.fieldType
            )
        )
    return


def keyLookup(listofFields, fsheet, fkey):
    """
    Hackish way to return the column letter from a list of fields for each sheet
    :param listofFields: list of all Field classes in workbook
    :param fsheet: the sheet name that will be connected
    :param fkey: the field name that will be connected with the foreign key
    :return: the column letter for the source of the foreign key
    """
    fattrib = [
        x.fieldName for x in listofFields if x.sheet == fsheet
    ]  # filters field list by selected sheet
    position = fattrib.index(fkey)
    letter = string.ascii_uppercase[position]  # gets the column letter for the position
    return letter


def dropDownfkey(listofFields, fsheet, fkey):
    """
    Builds an excel validation equation for another column in the workbook
    :param listofFields: list of all Field classes in workbook
    :param fsheet: the sheet name that will be connected
    :param fkey: fkey: the field name that will be connected with the foreign key
    :return: excel validation formula
    """
    letter = keyLookup(listofFields, fsheet, fkey)  # grab the column letter
    # example of the equation that ignores first row =OFFSET(Location!$B:$B, 1, 0, ROWS(Location!$B:$B)-1)
    eq = "=OFFSET({}!${}:${}, 1, 0, ROWS({}!${}:${})-1)".format(
        fsheet, letter, letter, fsheet, letter, letter
    )
    return eq


def createValidation(tab, col, field, maxRow=20000):
    """
    Applys the validation rule set to a set number of rows for the selected column (default is the first 20k rows)
    :param tab: the worksheet tab where the column is located
    :param col: the column number for the validation rule (zero indexed)
    :param field: instance of the Field class to build the validation rule set
    :return:
    """
    row = 0  # start row
    validator = selectValidator(field)

    if validator is not None:
        tab.data_validation(row + 1, col, maxRow, col, validator(field))
    return


def isfloat(value):
    """
    Checks if string can be converted to a float
    :param value: string to check
    :return: boolean
    """ ""
    try:
        float(value)
        return True
    except ValueError:
        return False
    except TypeError:
        return False


def buildEquation(field, listOfFields):
    """
    Replaces column names in the equation with the actual spreadsheet column letter
    :param field: field with the equation that is under the lookup attribute
    :param listOfFields: list of fields to use to exchange values
    :return: excel formula
    """

    colHash = {}  # empty dict to store results

    # Loop through the fields and add to dictionary of fieldname and the spreadsheet letter for each column
    for f in listOfFields:
        k = keyLookup(
            listOfFields, f.sheet, f.fieldName
        )  # lookup the letter for each column name
        colHash[f.fieldName] = k

    eq = field.lookup

    # look through columns and replace names with corresponding letters
    for key, value in colHash.items():
        eq = eq.replace(
            key, value + "{NUM}"
        )  # {NUM} is a placeholder for the row number

    return eq


def writeEquation(worksheet, field, listOfFields, cellFormat, maxRow=2000):
    """
    Loops through rows and writes equation by parsing fieldNames
    :param worksheet: the active sheet with the equation
    :param field: the field object
    :param listOfFields: list of all the field objects
    :param cellFormat: xlsxwriter cell format
    :param maxRow: number of rows to apply the formula
    :return:
    """

    # lookup destination letter for equation
    d = keyLookup(listOfFields, field.sheet, field.fieldName)

    eq = buildEquation(field, listOfFields)

    for rownum in range(2, maxRow):
        req = eq.format(NUM=rownum)
        hidden = hideEQ(req)
        worksheet.write_formula(
            "{DESTLETTER}{NUM}".format(DESTLETTER=d, NUM=rownum), hidden, cellFormat
        )

    pass


def hideEQ(eq):
    """
    Will "hide" the equation when input values are not filled out. The default behaviour is that the equation shows up
    as a zero. This function will take the equation and wrap it in a conditional to return a empty string if there
    are not values in the input cells
    :param eq:
    :return:
    """

    # goal =IF(OR(B8="", C8=""), "", B8+C8)
    eqNoSign = eq[1:]  # remove the equal sign from the start of the string

    # all cells that make up the equation inputs
    inputs = re.findall("\w+\d+", eq)

    orConditionals = ""

    for cell in inputs:
        cellStr = cell + '="",'
        orConditionals += cellStr

    newEQ = '=IF(OR({orCond}), "", {equation})'.format(
        orCond=orConditionals, equation=eqNoSign
    )

    return newEQ
