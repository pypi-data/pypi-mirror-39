# dry run to create template to check inputs
from MarinegeoTemplateBuilder.classes import Field, Vocab
import logging
import re
from MarinegeoTemplateBuilder.validators import isfloat


def check_vocab(fieldsList, vocabTerms=None):
    """
    checks all vocab objects in a list to see if they are valid
    :param fieldsList: list of Field() objects
    :param vocabTerms: list of Vocab() objects
    :return:
    """
    if vocabTerms is not None:
        for vocab in vocabTerms:

            # vocab destination
            checkerNoneVocab(vocab, "fieldName")
            checkerSymbolsVocab(vocab, "fieldName")
            checkerVocabDestinationExist(
                vocab, fieldsList
            )  # check that the field actually exists

            # code
            checkerNoneVocab(vocab, "code")
            checkerSymbolsVocab(vocab, "code")

            # definitions
            checkerNoneVocab(vocab, "definition")

    pass


def check_fields(fieldsList, vocabList=None):
    """
    Checks all field objects in a list to see if they are valid
    :param fieldsList: List of Field() object
    :return: nothing - warnings and errors are logged
    """
    for field in fieldsList:

        # check that sheet is defined and doesn't contain bad values
        checkerNone(field, "sheet")
        checkerSymbols(field, "sheet")

        # check that sheet name is not reserved
        checkSheetNotReserved(field)

        # check that fieldName is defined and doesn't contain bad values
        checkerNone(field, "fieldName")
        checkerSymbols(field, "fieldName")

        # check that field definition is defined
        checkerNone(field, "fieldDefinition")

        # check that fileType is defined and valid
        checkerNone(field, "fieldType")
        checkerAllowedValues(
            field,
            "fieldType",
            [
                "string",
                "date",
                "list",
                "integer",
                "decimal",
                "time",
                "fkey",
                "equation",
            ],
        )

        # check format string for time date fields?

        # check that the lookup value exists?
        if field.fieldType == "fkey":
            checkerNone(field, "lookup")
            checkerFkey(field, fieldsList)

        # unit - PASS

        # check that min and max values are numbers
        if field.fieldType in ["integer", "decimal"]:
            if field.minValue is not None:
                checkerNumber(field, "minValue")
            if field.maxValue is not None:
                checkerNumber(field, "maxValue")

        # check that the given column warnLevel are in the allowed list
        checkerAllowedValues(field, "warnLevel", ["warning", "stop", "information"])

        # check that each fieldType list has at least one vocab term
        if field.fieldType == "list" and vocabList is not None:
            checkerVocabDestinationExist(field, vocabList)

        # TODO check that DATE OR TIME has string format defined

    pass


def checkerNone(fieldObj, attribute):
    """
    logs a warning if the field attribute value is none
    :param fieldObj: Field() object to test
    :param attribute: String of the attribute to check
    :return:
    """
    value = getattr(fieldObj, attribute)  # get attribute value
    if value is None:
        logging.warning(
            "{} {} - {} is None.".format(fieldObj.sheet, fieldObj.fieldName, attribute)
        )
    pass


def checkerAllowedValues(fieldObj, attribute, allowedValues):
    """
    logs a warning if the field attribute value is not in the list of allowed values
    :param fieldObj: Field() object to test
    :param attribute: String of the attribute to check
    :param allowedValues: list of allowed values for attribute
    :return:
    """
    value = getattr(fieldObj, attribute)  # get attribute value
    if value not in allowedValues:
        logging.warning(
            "{} {} - {} not valid. Must be in {}.".format(
                fieldObj.sheet, fieldObj.fieldName, attribute, allowedValues
            )
        )
    pass


def checkerSymbols(fieldObj, attribute, illegalSymbols="[@_!#$%^&*()<>?/\|}{~:]"):
    """
    logs an error if the attribute value contains an illegal symbol
    :param fieldObj: Field() object to test
    :param attribute: String of the attribute to check
    :param illegalSymbols: String containing all the illegal symbols to check
    :return:
    """
    value = getattr(fieldObj, attribute)  # get attribute value

    # https://www.geeksforgeeks.org/python-program-check-string-contains-special-character/
    regex = re.compile(illegalSymbols)

    if regex.search(str(value)) != None:
        logging.error(
            "{} {} - {} is not valid. {} contains illegal symbols.".format(
                fieldObj.sheet, fieldObj.fieldName, attribute, value
            )
        )
    pass


def checkerNumber(fieldObj, attribute):
    """
    logs an error if the attribute value is not a number
    :param fieldObj: Field() object to test
    :param attribute: String of the attribute to check
    :return:
    """
    value = getattr(fieldObj, attribute)  # get attribute value

    if not isfloat(value):
        logging.error(
            "{} {} - {} is not valid. Must be a number.".format(
                fieldObj.sheet, fieldObj.fieldName, attribute, value
            )
        )

    pass


def checkerFkey(fieldObj, objList):
    """
    logs an error if the foreign key destination does not exist
    :param fieldObj: Field() object that is a foreign key to test
    :param objList: List of all the Field objects in the workbook
    :return:
    """
    value = getattr(fieldObj, "lookup")  # get attribute value

    # pull out the lookup destination sheet and fieldName
    dest_sheet, dest_field = value.split("$")

    # list comp over objList to find matches
    match = [
        x for x in objList if (x.sheet == dest_sheet and x.fieldName == dest_field)
    ]

    if len(match) == 0:
        logging.error(
            "{} {} - {} is not valid. {} does not exist.".format(
                fieldObj.sheet, fieldObj.fieldName, "Foreign Key", value
            )
        )
    pass


def checkerNoneVocab(vocabObj, attribute):
    """
    logs a warning if the field attribute value is none
    :param vocabObj: vocab() object to test
    :param attribute: String of the attribute to check
    :return:
    """
    value = getattr(vocabObj, attribute)  # get attribute value
    if value is None:
        logging.warning(
            "Vocabulary {} {} is None.".format(vocabObj.fieldName, attribute)
        )
    pass


def checkerSymbolsVocab(vocabObj, attribute, illegalSymbols="[@_!#$%^&*()<>?/\|}{~:]"):
    """
    logs an error if the attribute value contains an illegal symbol
    :param vocabObj: vocab() object to test
    :param attribute: String of the attribute to check
    :param illegalSymbols: String containing all the illegal symbols to check
    :return:
    """
    value = getattr(vocabObj, attribute)  # get attribute value

    # https://www.geeksforgeeks.org/python-program-check-string-contains-special-character/
    regex = re.compile(illegalSymbols)

    if regex.search(str(value)) != None:
        logging.error(
            "Vocabulary {} - {} is not valid. {} contains illegal symbols.".format(
                vocabObj.fieldName, attribute, value
            )
        )
    pass


def checkerVocabDestinationExist(Obj, List):
    """
    Checks that the vocab destination actually exists
    :param Obj: object to test
    :param List: list of objects to try to match
    :return:
    """
    value = getattr(Obj, "fieldName")  # get attribute value

    # list comp over fieldList to find matches
    match = [x for x in List if x.fieldName == value]

    if len(match) == 0:
        logging.error("Vocabulary destination missing for fieldName {}.".format(value))
    pass


def checkSheetNotReserved(Obj, reserved=["Metadata", "Schema", "Vocab"]):
    """
    Checks if the field's sheet parameter is reserved and shouldn't be used since they are internally generated
    :param Obj: Field object to test
    :param reserved: list of reserved sheet names that shouldn't be used.
    :return:
    """
    value = getattr(Obj, "sheet")  # get attribute value

    if value in reserved:
        logging.error(
            "{} uses a reserved sheet name that is used internally.".format(
                Obj.fieldName
            )
        )
    pass
