#!/usr/bin/env python3
"""
Loads attribute fields and vocabulary from csv files into templatebuilder class instances.
"""

from MarinegeoTemplateBuilder import classes
import pandas as pd
import chardet
import sys

if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

# generic loading functions to turn data from csv files or pandas data frames into python class objects
def loadCSV(csv, classType):
    """
    Loads items from a csv as as a pandas dataframe
    :param csv: path to a csv file
    :param classType: class instance type to load data into
    :return: a list of templatebuilder class instances
    """
    # check the csv file encoding
    with open(csv, "rb") as r:
        rawdata = r.read()
        encoding = chardet.detect(rawdata)[
            "encoding"
        ]  # guess the right encoding using chardet

    # load as a pandas dataframe
    df = pd.read_csv(csv, encoding=encoding)

    rows = loadDF(df, classType)

    return rows


def loadDF(df, classType):
    """
    Load items from a pandas dataframe as python objects
    :param df: pandas dataframe
    :param classType: class instance type to load data into
    :return: a list of templatebuilder class instances
    """

    # check that header matches the expected values
    if sorted(list(df)) != sorted(classParams(classType)):
        print("Expected: {}".format(sorted(classParams(classType))))
        print("Got: {}".format(sorted(list(df))))
        raise ValueError(
            "Input file is not properly formatted. Unknown items in the header."
        )

    # replace all NaNs with Nones
    df = df.where((pd.notnull(df)), None)

    # dataframe to dictionary of records
    dicts = df.to_dict(orient="records")

    # loop over dictionaries and unpack items
    rows = [classType(**d) for d in dicts]

    return rows


# function that determine the input type (csv file, dataframe or list of python objects) and
# loads the data using the appropriate data loader
def loadSwitcher(userInput, classType):
    """
    Checks the input type provided by the user and parses the data using the appropriate loader
    :param userInput: path to csv file, pandas data frame or list of python objects
    :param classType: desired class type
    :return: list of python objects of the selected type
    """

    if isinstance(userInput, list):
        if checkListObjects(userInput, classType):
            objects = userInput
        else:
            raise ValueError("Unknown List. Expected a list of objects")
    elif isinstance(userInput, pd.DataFrame):
        objects = loadDF(userInput, classType)
    elif userInput.endswith(".csv"):
        objects = loadCSV(userInput, classType)
    else:
        raise ValueError("Unknown input type.")
    return objects


def checkListObjects(listOfObjects, expectedClass):
    """
    Checks to see if all items in a list are instances of the expected class
    :param listOfObjects: list of objects to test
    :param expectedClass: the Class of the objects
    :return: boolean
    """
    check = all(isinstance(x, expectedClass) for x in listOfObjects)
    return check


def classParams(classType):
    """
    Gets a list of default parameters created with init to check to see if input matches the selected class
    :param classType: desired class type
    :return: list of fields for selected Class
    """

    # create an example instance for pulling all the required fields
    example = classType()
    requiredFields = list(example.__dict__.keys())

    # clear the example instances
    classType.all.pop()

    return requiredFields


def clearClassLists(classType):
    """
    Cleans up the Field or Vocab all list by deleting all existing instances
    :return:
    """
    # clear the list of instances
    del classType.all[:]
    return


def createExampleCSV(text, filename="example.csv"):
    """
    Creates a csv file from a text string. Primarily used for unittests.
    :param text: text string with commas seperating vars and new lines
    :param filename: output name for the file
    :return: filename
    """
    s = StringIO(text)

    with open(filename, "w") as f:
        for line in s:
            f.write(line)
    return filename
