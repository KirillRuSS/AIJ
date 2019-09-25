import random
import config as c


def take_exam(tasks: dict) -> dict:
    """
    Дефолтный пример отверов на тест
    :param tasks: тест
    :return: ответы
    """
    random.seed(42)

    answers = {}

    for task in tasks:
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
                    'Внезапно, диаграммы связей, превозмогая сложившуюся непростую '
                    'экономическую ситуацию, подвергнуты целой серии независимых исследований. '
                    'Высокий уровень вовлечения представителей целевой'
                    'аудитории является четким доказательством простого факта: '
                    'высокое качество позиционных исследований обеспечивает'
                    'актуальность поэтапного и последовательного развития общества. '
                    'плановых заданий играет определяющее значение для модели развития. '
                    'Высокий уровень вовлечения представителей целевой'
                    'аудитории является четким доказательством простого факта: '
                    'граница обучения кадров однозначно фиксирует необходимость вывода текущих активов. '
                )

        else:
            raise RuntimeError('Unknown question type: {}'.format(question['type']))

        answers[task['id']] = answer

    return answers
