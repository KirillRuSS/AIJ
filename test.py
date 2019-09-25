import json
import config as c
import model

if __name__ == '__main__':
    file_name = c.DIR + "\\test_00.json"

    with open(file_name, encoding="utf8") as json_file:
        data = json.load(json_file)

        tasks = data['tasks']
        answers = model.take_exam(tasks)
        print(answers)
