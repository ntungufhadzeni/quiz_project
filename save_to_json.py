import json

questions = [
    [{
        'ques_body': 'Do you have little interest or pleasure in doing things?',
        'A': 'Not at all',
        'B': 'Several days',
        'C': 'More than half the days',
        'D': 'Nearly every day'
    },
        {
            'ques_body': 'Are you feeling down, depressed, or hopeless?',
            'A': 'Not at all',
            'B': 'Several days',
            'C': 'More than half the days',
            'D': 'Nearly every day'
        },
        {
            'ques_body': 'Do you have trouble falling or staying asleep, or sleeping too much?',
            'A': 'Not at all',
            'B': 'Several days',
            'C': 'More than half the days',
            'D': 'Nearly every day'
        },
        {
            'ques_body': 'Are you feeling tired or having the little energy?',
            'A': 'Not at all',
            'B': 'Several days',
            'C': 'More than half the days',
            'D': 'Nearly every day'
        },
        {
            'ques_body': 'Do you have poor appetite or overeating?',
            'A': 'Not at all',
            'B': 'Several days',
            'C': 'More than half the days',
            'D': 'Nearly every day'
        },
        {
            'ques_body': 'Are you feeling bad about yourself?',
            'A': 'Not at all',
            'B': 'Several days',
            'C': 'More than half the days',
            'D': 'Nearly every day'
        },
        {
            'ques_body': 'Do you have trouble concentrating on things, such as reading the newspaper or watching TV?',
            'A': 'Not at all',
            'B': 'Several days',
            'C': 'More than half the days',
            'D': 'Nearly every day'
        },
        {
            'ques_body': 'Do you move or speak so slowly that other people could have noticed?',
            'A': 'Not at all',
            'B': 'Several days',
            'C': 'More than half the days',
            'D': 'Nearly every day'
        },
        {
            'ques_body': 'Are you having thoughts that you would be better off dead or of hurting yourself in some way?',
            'A': 'Not at all',
            'B': 'Several days',
            'C': 'More than half the days',
            'D': 'Nearly every day'
        }],
    [
        {
            'ques_body': 'Feeling nervous, anxious, or on edge',
            'A': 'Not at all',
            'B': 'Several days',
            'C': 'More than half the days',
            'D': 'Nearly every day'
        },
        {
            'ques_body': 'Not being able to stop or control worrying',
            'A': 'Not at all',
            'B': 'Several days',
            'C': 'More than half the days',
            'D': 'Nearly every day'
        },
        {
            'ques_body': 'Worrying too much about different things',
            'A': 'Not at all',
            'B': 'Several days',
            'C': 'More than half the days',
            'D': 'Nearly every day'
        },
        {
            'ques_body': 'Trouble relaxing',
            'A': 'Not at all',
            'B': 'Several days',
            'C': 'More than half the days',
            'D': 'Nearly every day'
        },
        {
            'ques_body': 'Being so restless that it is hard to sit still',
            'A': 'Not at all',
            'B': 'Several days',
            'C': 'More than half the days',
            'D': 'Nearly every day'
        },
        {
            'ques_body': 'Becoming easily annoyed or irritable',
            'A': 'Not at all',
            'B': 'Several days',
            'C': 'More than half the days',
            'D': 'Nearly every day'
        },
        {
            'ques_body': 'Feeling afraid, as if something awful might happen',
            'A': 'Not at all',
            'B': 'Several days',
            'C': 'More than half the days',
            'D': 'Nearly every day'
        }]

]

with open("data_file.json", "w") as write_file:
    json.dump(questions, write_file)

write_file.close()
