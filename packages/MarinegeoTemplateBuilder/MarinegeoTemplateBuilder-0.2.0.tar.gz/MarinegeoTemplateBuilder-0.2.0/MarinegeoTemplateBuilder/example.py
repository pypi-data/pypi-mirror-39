# Example of creating an Excel template using the MarinegeoTemplateBuilder package
import MarinegeoTemplateBuilder
from MarinegeoTemplateBuilder.classes import Field, Vocab
import datetime

# some values to prefill for the metadata section
metadataValues = {
    "Title": "MarineGEO Template Builder Workbook Demo",
    "Abstract": "This example illustrates all the configurable options for adding columns with validation to a workbook"
                " using the MarineGEO Template Builder package.",
    "ContactPerson": "Firstname Lastname",
    "EmailAddress": "first.last@example.com",
    "People": "Person One; Person Two; Person Three",
    "DataEntryBy": "Firstname Lastname",
    "DataEntryDate": datetime.datetime.today().strftime('%Y-%m-%d'),
    "Notes": "For Demonstration Use Only!",
    "ProtocolVersion":"The version number of the protocol used."

}

# columns to add to the workbook as a list of Field()'s
fields = [
    # Dropdown list lookup from controlled vocabulary
    Field(sheet="Location", fieldName="site", fieldDefinition="site abbreviation", fieldType="list"),

    # String data field
    Field(sheet="Location", fieldName="locationID", fieldDefinition="unique code for sampling location"),

    # On new sheet create a foreign key to the location ID on the location sheet
    Field(sheet="Data", fieldName="locationID", fieldDefinition="foreign key for sampling location", fieldType="fkey", lookup="Location$locationID"),

    # Date field in the format of YEAR-MONTH-DAY (YYYY-MM-DD)
    Field(sheet="Data", fieldName="date", fieldDefinition="Date Collected", fieldType="date", formatString="YYYY-MM-DD"),

    # Time field in the format of HH:MM
    Field(sheet="Data", fieldName="time", fieldDefinition="Time Collected", fieldType="time", formatString="HH:MM"),

    # Another dropdown list that contains controlled vocabulary
    Field(sheet="Data", fieldName="type", fieldDefinition="Type collected", fieldType="list"),

    # A field that must contain positive integers
    Field(sheet="Data", fieldName="posNum", fieldDefinition="Positive numbers only", fieldType="integer", minValue=0),

    # A field for decimals between -5.5 and 99.9
    Field(sheet="Data", fieldName="decimal", fieldDefinition="decimal", fieldType="decimal", minValue=-5.5, maxValue=99.9),

    # Calculated field that multiplys the PosNum by the Decimal
    Field(sheet="Data", fieldName="multiply", fieldDefinition="PosNum times Decimal", fieldType="equation", lookup="=posNum * decimal"),

]

# Load the vocab for the controlled vocab fields
vocab = [
    Vocab(fieldName="site", code="A", definition="site a"),
    Vocab(fieldName="site", code="B", definition="site B"),
    Vocab(fieldName="type", code="Red", definition="site B"),
    Vocab(fieldName="type", code="Blue", definition="site B")

]

# create the example template
MarinegeoTemplateBuilder.main(
    "TestTemplate_v0.0.1.xlsx",
    fields,
    vocab,
    branding="DEFAULT",
    metadataValues=metadataValues,
    dryrun=False,
)
