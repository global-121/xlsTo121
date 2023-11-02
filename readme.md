# Script to generate 121 programs from an xlsx form

This script, xlsto121.py, is a Python tool designed to convert an XLSForm file into a JSON structure compatible with the 121 Service.

## Purpose

The script automates the conversion process of an XLSForm into a JSON structure that can be used in the 121 Service platform for managing humanitarian projects. It extracts survey questions and choice options from the XLSForm, maps them to specific question types, and generates a JSON file that can be imported into the 121 Service.

## Prerequisites

Before using this script, ensure that you have the following:

- Python 3 installed on your system.

Required Python libraries: pandas, json, csv. You can install these libraries using pip:

```bash
pip install pandas jsonlib
```

## Script Usage

### Configuration

Before running the script, there are a few manual steps and configurations you need to perform:

1. Update 'xlsform.xlsx' File

   Set the form variable in the script to the name of your XLSForm file, which should be placed in the same folder as the script.

2. Add a '121duplicatecheck' Column

   In your XLSForm, make sure to add a column called '121duplicatecheck' and set it to true or false based on whether you want to include it in the 121 duplicate check. This step is important for data validation in the 121 Service platform.

3. Change the type of the (primary) phone number question

   Change the type of the (primary) phone number question to `tel` in the Excel file

4. Customize Initial Program Setup

   You can customize the initial program setup under the 'data' dictionary within the script to match your specific project details. Update values like project title, currency, distribution details, and other project-specific information.

```python
data = {
    # ...
    "titlePortal": {
        "en": "Cash in emergencies"
    },
    "titlePaApp": {
        "en": "Cash in emergencies"
    },
    # Update other fields as needed
    # ...
}
```

## Running the Script

Once you have completed the configurations and manual steps, you can run the script. It will read your XLSForm, process the data, and generate a JSON output.

To run the script, open a terminal or command prompt, navigate to the directory containing the script and your XLSForm file, and execute the following command: `python xlsto121.py`

The script will convert the XLSForm to a JSON file named 'output.json'.

## Post-Processing

After running the script, you may need to perform further customizing the generated JSON file to match specific project requirements.

## Create program in 121

Use the body of `output.json` in the `/api/programs` endpoint of your desired 121 instance to create the program.
