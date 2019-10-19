import random
from collections import defaultdict

import numpy as np

from solvers import solver19, solver0
from utils import *
from solvers import *

import traceback




class CuttingEdgeStrongGeneralAI(object):

    def __init__(self, train_path='public_set/train'):
        self.train_path = train_path
        self.classifier = classifier.Solver()
        solver_classes = [
            solver1,
            solver2,
            solver3,
            solver4,
            solver0,
            solver6,
            solver7,
            solver0,
            solver9,
            solver10,
            solver10,
            solver10,
            solver13,
            solver14,
            solver15,
            solver16,
            solver19,
            solver19,
            solver19,
            solver19,
            solver21,
            solver22,
            solver23,
            solver24,
            solver25,
            solver26
        ]
        self.solvers = self.solver_loading(solver_classes)
        self.clf_fitting()

    def solver_loading(self, solver_classes):
        _solver19 = solver19.Solver()
        _solver19.load()

        solvers = []
        for i, solver_class in enumerate(solver_classes):
            solver_index = i + 1
            train_tasks = load_tasks(self.train_path, task_num=solver_index)
            solver_path = os.path.join("data", "models", "solver{}.pkl".format(solver_index))

            if str(solver_classes[solver_index-1].Solver)=="<class 'solvers.solver19.Solver'>":
                solvers.append(_solver19)
                continue
            else:
                solver = solver_class.Solver()

            if os.path.exists(solver_path):
                print("Loading Solver {}".format(solver_index))
                solver.load(solver_path)
            else:
                print("Fitting Solver {}...".format(solver_index))
                try:
                    solver = solver_class.Solver()
                    solver.fit(train_tasks)
                    solver.save(solver_path)
                except Exception as e:
                    print('Exception during fitting: {}'.format(e))
            print("Solver {} is ready!\n".format(solver_index))
            solvers.append(solver)
        #solvers[18].predict_from_model(None) #!!!
        return solvers

    def clf_fitting(self):
        tasks = []
        for filename in os.listdir(self.train_path):
            if filename.endswith(".json"):
                data = read_config(os.path.join(self.train_path, filename))
                tasks.append(data)
        print("Fitting Classifier...")
        self.classifier.fit(tasks)
        print("Classifier is ready!")
        return self

    def not_so_strong_task_solver(self, task):
        question = task['question']
        if question['type'] == 'choice':
            # pick a random answer
            choice = random.choice(question['choices'])
            answer = choice['id']
        elif question['type'] == 'multiple_choice':
            # pick a random number of random choices
            min_choices = question.get('min_choices', 1)
            max_choices = question.get('max_choices', len(question['choices']))
            n_choices = random.randint(min_choices, max_choices)
            random.shuffle(question['choices'])
            answer = [
                choice['id']
                for choice in question['choices'][:n_choices]
            ]
        elif question['type'] == 'matching':
            # match choices at random
            random.shuffle(question['choices'])
            answer = {
                left['id']: choice['id']
                for left, choice in zip(question['left'], question['choices'])
            }
        elif question['type'] == 'text':
            if question.get('restriction') == 'word':
                # pick a random word from the text
                words = [word for word in task['text'].split() if len(word) > 1]
                answer = random.choice(words)

            else:
                # random text generated with https://fish-text.ru
                answer = (
                    'Для современного мира реализация намеченных плановых заданий позволяет '
                    'выполнить важные задания по разработке новых принципов формирования '
                    'материально-технической и кадровой базы. Господа, реализация намеченных '
                    'плановых заданий играет определяющее значение для модели развития. '
                    'Сложно сказать, почему сделанные на базе интернет-аналитики выводы призывают '
                    'нас к новым свершениям, которые, в свою очередь, должны быть в равной степени '
                    'предоставлены сами себе. Ясность нашей позиции очевидна: базовый вектор '
                    'развития однозначно фиксирует необходимость существующих финансовых и '
                    'административных условий.'
                )

        else:
            raise RuntimeError('Unknown question type: {}'.format(question['type']))

        return answer

    def take_exam(self, exam):
        answers = {}
        # pprint.pprint(exam)
        if "tasks" in exam:
            variant = exam["tasks"]
            if isinstance(variant, dict):
                if "tasks" in variant.keys():
                    variant = variant["tasks"]
        else:
            variant = exam
        task_number = self.classifier.predict(variant)
        #task_number = task_number*0+19
        print("Classifier results: ", task_number)
        for i, task in enumerate(variant):
            task_id = task['id']
            task_index, task_type = i + 1, task["question"]["type"]
            try:
                #if task_number[i] >= 16 or task_number[i] <= 20:
                prediction = self.solvers[task_number[i] - 1].predict_from_model(task)
                #else:
                #    prediction = ""

                print("Prediction " + str(task_number[i]) + ": ", prediction)
            except Exception as e:
                print(traceback.format_exc())
                prediction = self.not_so_strong_task_solver(task)
            if isinstance(prediction, np.ndarray):
                prediction = list(prediction)
            answers[task_id] = prediction
        return answers

