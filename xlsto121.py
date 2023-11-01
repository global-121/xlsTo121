import pandas as pd
import json
import csv


############## TO DO ################
# phone number


############## Manual ################
# add column to xlsform called '121duplicatecheck' and set to true/false based on if you want to include it in the 121 duplicate check
# save xlsform in the same folder as 'xlsto121.py'
# enter the name of the xlsform here:
form = 'xlsform.xlsx'
# Change initial program setup under 'data'
# give the output file a name:
result = 'output.json'
# Run script
# post process: change phone number question to type 'tel'

# Define the mapping dictionary from the CSV
type_mapping = {}

with open('mappings/kobo121fieldtypes.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        if len(row) == 2:
            type_mapping[row[0]] = row[1]

# Read the xlsform
df1 = pd.read_excel(form, sheet_name='survey')
df2 = pd.read_excel(form, sheet_name='choices')


# Create the JSON structure
data = {
    "published": True,
    "validation": False,
    "phase": "registrationValidation",
    "location": "Ethiopia",
    "ngo": "ANE",
    "titlePortal": {
        "en": "DRA Joint Response 2023 Ethiopia - ANE"
    },
    "titlePaApp": {
        "en": "DRA Joint Response 2023 Ethiopia - ANE"
    },
    "description": {
        "en": ""
    },
    "startDate": "2023-08-01T12:00:00.000Z",
    "endDate": "2023-12-31T12:00:00.000Z",
    "currency": "ETB",
    "distributionFrequency": "month",
    "distributionDuration": 3,
    "fixedTransferValue": 7000,
    "paymentAmountMultiplierFormula": "",
    "financialServiceProviders": [
        {
        "fsp": "Commercial-bank-ethiopia"
        }
    ],
    "targetNrRegistrations": 250,
    "tryWhatsAppFirst": False,
    "meetingDocuments": {
        "en": ""
    },
    "notifications": {
        "en": {
        "registered": "This is a message from ANE.\n\nThank you for your registration. We will inform you later if you are included in this project or not."
        }
    },
    "phoneNumberPlaceholder": "+251 000 000 000",
    "programCustomAttributes": [],
    "programQuestions": [],
    "aboutProgram": {
        "en": "DRA Joint Response Ethiopia 2023 - ANE"
    },
    "fullnameNamingConvention": [
        "fullName"
    ],
    "languages": [
        "en",
        "et_AM"
    ],
    "enableMaxPayments": True
}

# Convert the first CSV data into the programQuestions format

for index, row in df1.iterrows():
    question = {
        "name": row['name'],
        "label": {
            "en": row['label']
        },
        "answerType": type_mapping[row['type'].split()[0]],
        "options": [],
        "scoring": {},
        "persistence": True,
        "pattern": "",
        "phases": [],
        "editableInPortal": True,
        "export": [
            "all-people-affected",
            "included",
            "selected-for-validation"
        ],
        "shortLabel": {
            "en": row['name'],
        },
        "duplicateCheck": row['121duplicatecheck'],
        "placeholder": ""
    }
    if type_mapping[row['type'].split()[0]] == 'dropdown':
        filtered_df = df2[df2['list_name'] == row['type'].split()[-1]]
        for index, row in filtered_df.iterrows():
            option = {
                "option": row['name'],
                "label": {
                    "en": row['label']
                }
            }
            question["options"].append(option)
    data["programQuestions"].append(question)


# Convert the data dictionary to JSON
output_json = json.dumps(data, indent=2)

# Write the JSON to a file
with open(result, 'w') as json_file:
    json_file.write(output_json)

print(f"JSON data has been written to {result}")