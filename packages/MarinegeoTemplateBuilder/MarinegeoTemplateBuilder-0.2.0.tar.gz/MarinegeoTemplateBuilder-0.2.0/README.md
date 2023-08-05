[![Build Status](https://travis-ci.org/MarineGEO/MarineGEO-template-builder.svg?branch=master)](https://travis-ci.org/MarineGEO/MarineGEO-template-builder)

# MarineGEO Template Builder

Python package to create standardized data entry templates for the [Marine Global Earth Observatory (MarineGEO) Network](http://marinegeo.si.edu). This package is a wrapper around [xlsxwriter](https://xlsxwriter.readthedocs.io/) and creates Excel workbooks with built-in validation and metadata. Templates are created using a list of fields defined by the user to use as columns in the workbook. Each field has several attributes that can be set to control what type of values are allowed and provide control over data input validation.  


## Installation

The `MarinegeoTemplateBuilder` package can be installed from [PyPi](https://pypi.org/project/MarinegeoTemplateBuilder/) using pip.


```python
pip install MarinegeoTemplateBuilder
```

### Requirements

 - Python 2.7+
 - [xlsxwriter](https://xlsxwriter.readthedocs.io/)

## Example

Simple example of a creating a workbook with a single sheet with two columns.

```python
# Example of creating an Excel template using the MarinegeoTemplateBuilder package
from MarinegeoTemplateBuilder import *

# create the example template
main("Example.xlsx", fields=[Field(sheet="sheet1", fieldName="ColA", fieldDefinition="Column A"),
    Field(sheet="sheet1", fieldName="ColB", fieldDefinition="Column B")], title="Test Template")

```

![Example of MarinegeoTemplateBuilder Workbook](docs/simple_example.gif)

## Metadata Configuration

### Metadata sheet

Each workbook has a sheet called Metadata that is used to store information about the project. This sheet is automatically generated for all workbooks using a default set of metadata fields. Options for configuring the metadata sheet are set using the parameters in `MarinegeoTemplateBuilder.main()`.

Default metadata fields
  - Title
  - Abstract
  - ContactPerson
  - EmailAddress
  - People
  - DataEntryBy
  - DataEntryDate
  - Notes
  - ProtocolVersion
  - TemplateVersion
  - WorkbookBuildInfo (populated automatically)

#### Custom Metadata fields
 
Custom metadata fields can be used by passing in a list of field objects to metadataList in `MarinegeoTemplateBuilder.main(metadataList=[])`. This will override the default metadata field options 

```python
custom_metadata = [
    Field(
        sheet="Metadata",
        fieldName="Custom 1",
        fieldDefinition="Custom Metadata Field 1",
    ),
    Field(
        sheet="Metadata",
        fieldName="Custom 2",
        fieldDefinition="Custom Metadata Field 2",
    )]


# custom metadata
main(..., metadataList=custom_metadata)
```
 
![custom metadata example](docs/customMetadata.png)


#### Prefilling Metadata

Metadata elements can be preset so default values are set when the workbook is created. This is accomplished by passing a python dictionary of values using the metadata fieldnames as the keys to `metadataValues`.

```python
metadataValues = {
    "TemplateVersion": "v0.0.1",
    "ProtocolVersion": "v0.0.1",
    "Title": "Please Enter Title Here",
}
```

#### Branding Logo

The user can change the branding image at the top of the metadata sheet by passing an image to MarinegeoTemplateBuilder.main(..., branding='path/to/img'). If no image is provided, the default is to just have a blank space at the top of the sheet. To use the MarineGEO logo that is provided in the package, just pass `"DEFAULT"` as the parameter option. 

 Note: The layout was designed primarily for the MarineGEO logo, so you may need to lay around with the size of the image to properly display it on the sheet.
 

![default metadata page annotated](docs/metadata_annotated_default.png)

 
### Field Configuration

Each template will have custom columns that may be split across several sheets in the workbook. This is controlled by creating a list of columns (Fields) to add to the workbook. Fields are the columns that are added to the workbook. Each field must have a destination (`sheet`), column header name (`fieldName`), description (`fieldDefinition`) and the attribute type defined (`fieldType`). Certain special fieldTypes will have additional options that can be set to control formats and allowed values. 

#### Supported Field Types

 - string: general format cells with no restrictions.
 - date: Excel date format with validation. Dates must have the `formatString` defined.
 - date: Excel time format with validation. Times must have the `formatString` defined.
 - list: Validation from another column in the spreadsheet. Source must be defined in the `lookup` variable.
 - equation: Calculated field from other columns. Equation must be defined in the `lookup` variable.
 - integer: validation of integers only. Maybe constrained using minValue and maxValue.
 - decimal: validation of numbers. May be constrained using minValue and maxValue.
 - fkey: Dropdown list from another column (foreign key) in the workbook. 


##### Strings

Field type `string` is for general format cells that have no restrictions. There is no validation rules built in - all values will be allowed in the cells. This should be the default fieldType for all fields that do no fit under the other special field types.

##### Dates

Field type `date` is for columns that contain date fields. Excel will provide validation on the cells to ensure that the user inputs are valid dates. To work properly, the field must have the `formatString` defined to control the format of the date/time string.  Some examples include YYYY-MM-DD for dates and HH:MM for hours/minutes. See [Excel Format Cells](https://support.microsoft.com/en-us/help/264372/how-to-control-and-understand-settings-in-the-format-cells-dialog-box) for help.


##### Times

Field type `time` is for columns that contain time fields. Excel will provide validation on the cells to ensure that the user inputs are valid times. To work properly, the field must have the `formatString` defined to control the format of the date/time string.  Some examples include YYYY-MM-DD for dates and HH:MM for hours/minutes. See [Excel Format Cells](https://support.microsoft.com/en-us/help/264372/how-to-control-and-understand-settings-in-the-format-cells-dialog-box) for help.


##### Lists

Field type `list` items are dropdown menus that contain controlled vocabulary for the field. Vocabulary terms should be loaded as `Vocab()` instances. See vocabulary section for more information. 

##### Integers

Integer fields can be set using the fieldType `integer`. Integer fields can be limited to a certain range by setting the min or max values. The min and max limits are inclusive. For example, if you want a column to only contain positive integers that are less or equal to three use `minValue = 1, maxValue = 3`.  If the min and max limits are not set, the column will just validate that the input is an integer. 

##### Decimals

Decimial fields can be set using the fieldType `decimal`. Decimal fields are very similiar to integer fields but accept all number. The range of acceptable values can be set using the min and max values for the field. For example, if a column needs to only contain positive numbers then set the validation to `minValue=0`. If the min and max limits are not set, the column will just validate that the input is an number.

##### Foreign Keys

Foregin keys are references to columns in other sheets. This special field type is set using a fieldType of `fkey` with a special value pointing to the other column in `lookup`. The lookup value needs to be in the format of `sheet$columnName`.

##### Equations

Calculated fields are a very special columns. The field type needs to be set as `equation` and the formula needs to be writen in the `lookup` attribute using the column fieldNames. Equations start with an equals sign and use the field names (the column names get swapped internally with the excel column letter values). Equations can only reference the columns on the active sheet and cannot calculate cells on different rows. Example of having a sum column that adds to columns together - `"=column1 + column2"`. By default, all calculated fields are locked and unable to edited and appear grayed out. Note: use equations sparingly, the implementation is finicky and fills the speadsheet with lots of null values.

#### Warn Levels

The validation error level for each field can be set to 'stop', 'warning', or 'information'. See [xlsxwriter error_type](https://xlsxwriter.readthedocs.io/working_with_data_validation.html) for more info. 

#### Loading fields
 
Fields can be loaded from a csv file, dataframe or list of `Field()` objects. 

```
sheet,fieldName,fieldDefinition,fieldType,formatString,loopup,unit,minValue,maxValue,warnLevel
Location,site,MarineGEO site abbreviation,list,,,,,,
Location,locationID,Unique code for each sampling location,string,,,,,,
Location,locality,Local or common name of the sampling location,string,,,,,,
Cover,locationID,Foreign key to the locationID defined on the Location sheet,fkey,,Location$locationID,,,,
Cover,transectNumber,"Transect Number",integer,,,dimensionless,1,3,
Cover,stopNumber,"Stop number along transect",integer,,,dimensionless,1,5,
```

```python
from MarinegeoTemplateBuilder.classes import Field

attributes = [

    Field(sheet="Location", fieldName="site", fieldDefinition="MarineGEO site abbreviation",fieldType="list"),
    Field(sheet="Location", fieldName="locationID",fieldDefinition="Unique code for each sampling location",fieldType="string"),
    Field(sheet="Location", fieldName="locality",fieldDefinition="Local or common name of the sampling location",fieldType="string"),
    Field(sheet="Cover",fieldName="locationID",fieldDefination="Foreign key to the locationID defined on the Location sheet",fieldType="fkey",lookup="Location$locationID"),
    Field(sheet="Cover",fieldName="transectNumber",fieldDefination="Transect Number",fieldType="integer",unit="dimensionless",minValue=1,maxValue=3),
    Field(sheet="Cover",fieldName="stopNumber",fieldDefinition="Stop number along transect",fieldType="integer",unit="dimensionless",minValue=1,maxValue=5)
]

```

### Controlled Vocabulary

Vocabulary are the terms that are used in the dropdown menus. The vocabulary can be set using two different methods. Each vocab term must have the destination fieldName, the code and the definition. All the terms will be added to the Vocab tab in the workbook.

Controlled vocabulary for fields. The controlled vocabulary is used for populating validation drop down menus.

Each vocabulary term must have the destination field (fieldName) and the term/code itself (code). It is also best practice to include a definition for each code.

Note: the destination `fieldName` for the vocabulary must match the `fieldName` for the vocabulary and be set as a `fieldType` of `"list"`.

#### Load vocabulary terms 

Vocabulary terms can be loaded from a csv, dataframe or a list of `Vocab()` class instances.

```
fieldName,code,definition
percentCover,<5%,Less than 5%
percentCover,10%,Between 5-10%
percentCover,15%,Between 10-15%
```
```python
from MarinegeoTemplateBuilder.classes import Vocab

vocabulary = [
    Vocab(fieldName="percentCover",code="<5%",definition="Less than 5%"),
    Vocab(fieldName="percentCover",code="10%",definition="Between 5-10%"),
    Vocab(fieldName="percentCover",code="15%",definition="Between 10-15%")
]

```


## Full example

```python
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
```

![Full MarineGEO template builder example](docs/full_example.gif)