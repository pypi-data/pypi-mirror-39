# loads data into a workbook

from MarinegeoTemplateBuilder.classes import Vocab, Field
from MarinegeoTemplateBuilder.validators import keyLookup
import random
import datetime
import json


def fillColumn(tabs, listFields, column, values):
    """
    Fills a column in the workbook with a list of values starting at row 2
    :param tabs: dictionary containing the workbook's sheets
    :param listFields: a list of fields - needed to lookup the column's index
    :param column: the Field() object for the column
    :param values: list of items to fill the column
    :return:
    """

    # lookup column letter
    col = keyLookup(listFields, column.sheet, column.fieldName)

    # write the list of values to the columns starting below the header
    tabs[column.sheet].write_column("{column}2".format(column=col), values)

    pass


def fillValues(listFields, listVocab, tabs, values=None):
    """
    Fills values into a xlxswriter workbook sheet
    :param listFields: the list of Field objects already added to the workbook
    :param listVocab: list of vocab terms for any fields with controlled vocabulary
    :param tabs: dictionary of all the sheets in the workbook
    :param values: "RANDOM" fills 20 rows with random values or a dictionary (key = fieldName, values = list of values)
    :return:
    """

    d = {}  # empty dictionary for storing random values generated for fkey

    # loop through all the fields in the
    for f in listFields:

        # when the seedValues are set to random, generate some random values and write to the sheet
        if values == "RANDOM":
            print("Filling {}${} with random values".format(f.sheet, f.fieldName))

            # foreign keys are tricky, they depend on values from another column
            if f.fieldType == "fkey":
                terms = d.get(
                    f.lookup
                )  # for foreign keys the list of terms is the values already written to the col
            else:
                terms = (
                    listVocab
                )  # all other list lookup use the controlled vocab provided by the user.

            # get a list of 20 random values that fit within the given field type and limits
            randomValues = [getRandom(f, terms) for i in range(20)]

            d[
                f.sheet + "$" + f.fieldName
            ] = (
                randomValues
            )  # set the dict to the field name and random values for potential fkey lookups

            # write the values to speadsheet for the given column
            fillColumn(tabs, listFields, f, randomValues)

        elif isinstance(values, dict):
            # TODO this potentially will break if multiple fields in spreadsheet have same names
            v = values.get(
                f.fieldName
            )  # pull the values for the fieldName from the dict

            # if values are provided for the field, seed the rows with the data
            if v is not None:
                print("Filling {}${} with seeded values.".format(f.sheet, f.fieldName))
                fillColumn(tabs, listFields, f, v)  # write the values to the speedsheet
        else:
            pass

    pass


def getRandom(field, terms=None):
    """
    Random value switcher
    :param field: Field() instance
    :param terms: List of potential choices to use
    :return: a random value that fits within the field's type and limits
    """
    if field.fieldType == "integer":
        r = randomInteger(field)
    elif field.fieldType == "decimal":
        r = randomDecimal(field)
    elif field.fieldType == "date":
        r = randomDate()
    elif field.fieldType == "time":
        r = randomDate()
    elif field.fieldType == "list" and terms is not None:
        r = randomVocab(field, terms)
    elif field.fieldType == "fkey" and terms is not None:
        r = random.choice(terms)
    elif field.fieldType == "string":
        r = randomWord()
    else:
        r = None
    return r


def randomInteger(field):
    """
    Takes a field object and returns a random integer within the min and max allowed values
    :param field: Integer field object()
    :return: random integer between the min and max values if provided (else between -100 and 100)
    """
    if field.minValue is None:
        field.minValue = -100  # set lower limit to -100 if value not provided

    if field.maxValue is None:
        field.maxValue = 100  # set upper limit to 100 if value not provided

    rint = random.randint(field.minValue, field.maxValue)  # random integer

    return rint


def randomDecimal(field):
    """
    Takes a field object and returns a random decimal within the min and max allowed values
    :param field: field object() that is of fieldType decimal
    :return: random decimal between the min and max values if provided (else between -100 and 100)
    """
    if field.minValue is None:
        field.minValue = -100  # set lower limit to -100 if value not provided

    if field.maxValue is None:
        field.maxValue = 100  # set upper limit to 100 if value not provided

    rdecimal = random.uniform(field.minValue, field.maxValue)  # random integer

    return round(rdecimal, 2)


def randomVocab(field, vocab):
    """
    Select a random vocab term from a list of Vocab objects
    :param field: the Field object instance
    :param vocab: the list of Vocab terms
    :return: random item from the list of vocab terms
    """

    listCodes = [
        x.code for x in vocab if x.fieldName == field.fieldName
    ]  # filter vocab object to match the selected field

    ritem = random.choice(listCodes)

    return str(ritem)


def randomDate():
    """
    Generate a random date that is within the last year starting from 2018-11-30
    :return: random datetime object
    """
    now = datetime.datetime(2018, 11, 30, 9)
    randomTS = now - datetime.timedelta(seconds=random.randint(0, 60 * 60 * 34 * 365))
    return randomTS




def randomWord():
    """
    Select a random word from a list
    :return:
    """
    with open('words.json') as f:
        words = json.load(f)['data']

    w = random.choice(words)
    return w

