import json

add_questions = [
    {
        'q': 'Have you previously diagnosed with a mental illness?',
        'add': [
            'Bipolar Disorder',
            'Depression',
            'Anxiety',
            'Psychotic',
            'Substance Use'
        ]
    },
    {
        'q': 'Anyone diagnosed with mental illness in your family?',
        'add': [
            'Both parents',
            'Single Parent',
            'Sibling',
            'Relative',
            'Grandparents'
        ]
    },
    {
        'q': 'Have you ever felt you should cut down on your drinking?',
        'add': [
            'Once',
            'Very often'
        ]
    },
    {
        'q': 'Have people annoyed you by criticizing your drinking?',
        'add': [
            'Once',
            'Very often'
        ]
    },
    {
        'q': 'Have you been diagnosed with a medical problem?',
        'add': [
            'Diabetes',
            'Asthma',
            'Hypertension',
            'HIV',
            'Stroke',
            'Thyroid disease',
            'Epilepsy',
            'Head Injury',
            'COVID-19',
            'Meningitis'
        ]
    },
    {
        'q': 'Did you experience any traumatic events as a child?',
        'add': [
            'Physical',
            'Sexual',
            'Emotional',
            'Neglect',
            'Death of parents/caregiver',
            'Natural disaster'
        ]
    },
    {
        'q': 'Have you experienced any traumatic events as an adult?',
        'add': [
            'Physical',
            'Sexual',
            'Emotional',
            'Neglect',
            'Death of parents/caregiver',
            'Natural disaster'
        ]
    }

]

with open("add_data_file.json", "w") as write_file:
    json.dump(add_questions, write_file)

write_file.close()
