import pandas as pd
import json
import csv

############## TO DO ################
# improve mappingdf

############## Start ################
# enter the name of the xlsform here:
form = 'xlsform.xlsx'
# give the output file a name:
result = 'output.json'

type_mapping = {}

with open('mappings/kobo121fieldtypes.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        if len(row) == 2:
            type_mapping[row[0]] = row[1]

mappingdf = pd.read_csv('mappings/kobo121fieldtypes.csv', delimiter='\t')

# Read the xlsform
df1 = pd.read_excel(form, sheet_name='survey')
df2 = pd.read_excel(form, sheet_name='choices')


# Create the JSON structure
data = {
    "published": True,
    "validation": False,
    "phase": "registrationValidation",
    "location": "Greece",
    "ngo": "Hellenic Red Cross Society",
    "titlePortal": {
        "en": "Cash in emergencies"
    },
    "titlePaApp": {
        "en": "Cash in emergencies"
    },
    "description": {
        "en": ""
    },
    "startDate": "2023-12-01T12:00:00.000Z",
    "endDate": "2024-12-01T12:00:00.000Z",
    "currency": "EUR",
    "distributionFrequency": "month",
    "distributionDuration": 3,
    "fixedTransferValue": 500,
    "paymentAmountMultiplierFormula": "",
    "financialServiceProviders": [
        {
        "fsp": "Commercial-bank-ethiopia"
        }
    ],
    "targetNrRegistrations": 1000,
    "tryWhatsAppFirst": False,
    "meetingDocuments": {
        "en": ""
    },
    "notifications": {
        "en": {
        "registered": "This is a message from Hellenic Red Cross.\n\nThank you for your registration. We will inform you later if you are included in this project or not."
        }
    },
    "phoneNumberPlaceholder": "+30 000 000 000",
    "programCustomAttributes": [],
    "programQuestions": [],
    "aboutProgram": {
        "en": "Cash in emergencies"
    },
    "fullnameNamingConvention": [
        "fullName"
    ],
    "languages": [
        "en"
    ],
    "enableMaxPayments": True
}

# Convert the first CSV data into the programQuestions format

for index, row in df1.iterrows():
    if row['type'].split()[0] in mappingdf['kobotype'].tolist():
        question = {
            "name": row['name'],
            "label": {
                "en": row['label']
            },
            "answerType": type_mapping[row['type'].split()[0]],
            "questionType": "standard",
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