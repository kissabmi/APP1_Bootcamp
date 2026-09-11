import multiprocessing as mp
import os
import random
import time
from dataclasses import dataclass
from math import sqrt
from queue import Empty

PHI = (1 + sqrt(5)) / 2

IN_QUEUE = 'In Queue'
PASSED = 'Passed'
FAILED = 'Failed'


@dataclass
class Person:
    name: str
    gender: str

    def is_boy(self):
        return self.gender.upper() in ('M', 'М')


def read_people(path):
    people = []

    with open(path, encoding='utf-8') as file:
        for line in file:
            parts = line.split()

            if not parts:
                continue

            if len(parts) != 2:
                raise ValueError(f'bad line in {path}: {line!r}')

            people.append(Person(parts[0], parts[1]))

    return people


def read_questions(path):
    with open(path, encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]


def golden_weights(count):
    weights = []
    rest = 1.0

    for _ in range(count - 1):
        weight = rest / PHI
        weights.append(weight)
        rest -= weight

    weights.append(rest)
    return weights


def choose_word(words, is_boy):
    words = list(words)

    if not is_boy:
        words.reverse()

    return random.choices(words, weights=golden_weights(len(words)), k=1)[0]


def choose_correct_words(question, examiner):
    words_left = question.split()
    correct_words = set()

    while words_left:
        word = choose_word(words_left, examiner.is_boy())
        correct_words.add(word)
        words_left.remove(word)

        if random.random() > 1 / 3:
            break

    return correct_words


def ask_questions(student, examiner, questions):
    correct_count = 0
    correct_questions = []

    for question in random.sample(questions, 3):
        answer = choose_word(question.split(), student.is_boy())
        correct_answers = choose_correct_words(question, examiner)

        if answer in correct_answers:
            correct_count += 1
            correct_questions.append(question)

    return correct_count, correct_questions


def decide_result(correct_count):
    mood = random.random()

    if mood < 1 / 8:
        return False

    if mood < 3 / 8:
        return True

    return correct_count > 1


def make_table(headers, rows):
    widths = [len(str(header)) for header in headers]

    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))

    border = '+' + '+'.join('-' * (width + 2) for width in widths) + '+'
    header = '|' + '|'.join(
        f' {str(headers[i]).center(widths[i])} '
        for i in range(len(headers))
    ) + '|'

    lines = [border, header, border]

    for row in rows:
        line = '|' + '|'.join(
            f' {str(row[i]).ljust(widths[i])} '
            for i in range(len(row))
        ) + '|'
        lines.append(line)

    lines.append(border)
    return '\n'.join(lines)


def take_exam(student, examiner, questions):
    correct_count, correct_questions = ask_questions(student, examiner, questions)
    passed = decide_result(correct_count)

    duration = random.uniform(
        max(1, len(examiner.name) - 1),
        len(examiner.name) + 1
    )

    time.sleep(duration)
    return passed, duration, correct_questions


def examiner_process(examiner, queue, state, lock, questions):
    random.seed(time.time() + os.getpid())

    total = 0
    failed = 0
    work_time = 0.0
    had_lunch = False

    while True:
        if not had_lunch and time.time() - state['start_time'] >= 30:
            time.sleep(random.uniform(12, 18))
            had_lunch = True

        try:
            student = queue.get_nowait()
        except Empty:
            if state['finished'] >= state['total_students']:
                break

            time.sleep(0.1)
            continue

        with lock:
            state['current'][examiner.name] = student.name
            state['in_queue'] -= 1

        passed, duration, correct_questions = take_exam(student, examiner, questions)

        total += 1
        failed += int(not passed)
        work_time += duration

        with lock:
            state['status'][student.name] = PASSED if passed else FAILED
            state['finish_time'][student.name] = time.time() - state['start_time']
            state['exam_time'][student.name] = duration

            state['current'][examiner.name] = '-'
            state['exam_total'][examiner.name] = total
            state['exam_failed'][examiner.name] = failed
            state['work_time'][examiner.name] = work_time

            for question in correct_questions:
                state['question_score'][question] += 1

            state['finished'] += 1


def student_rows(state, final=False):
    order = list(state['students'])
    priority = {PASSED: 0, FAILED: 1} if final else {
        IN_QUEUE: 0,
        PASSED: 1,
        FAILED: 2,
    }

    names = sorted(
        order,
        key=lambda name: (
            priority.get(state['status'].get(name, IN_QUEUE), 0),
            order.index(name)
        )
    )

    return [
        (name, state['status'].get(name, IN_QUEUE))
        for name in names
    ]


def examiner_rows(state, final=False):
    rows = []

    for name in state['examiners']:
        total = state['exam_total'].get(name, 0)
        failed = state['exam_failed'].get(name, 0)
        work_time = f"{state['work_time'].get(name, 0.0):.2f}"

        if final:
            rows.append((name, total, failed, work_time))
        else:
            current = state['current'].get(name, '-')
            rows.append((name, current, total, failed, work_time))

    return rows


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_live(state):
    clear_screen()

    print(make_table(['Student', 'Status'], student_rows(state)))
    print()
    print(make_table(
        ['Examiner', 'Текущий студент', 'total', 'Завали', 'Work Time'],
        examiner_rows(state)
    ))
    print()

    print(f"осталось в очереди: {state['in_queue']} из {state['total_students']}")
    print(f"время с момента начала экзамена: {time.time() - state['start_time']:.2f}")


def names_with_min(items):
    if not items:
        return ['-']

    best_value = min(value for _, value in items)

    return [
        name
        for name, value in items
        if abs(value - best_value) < 0.01
    ]


def get_top_students(state):
    items = []

    for name in state['students']:
        if state['status'].get(name) == PASSED:
            items.append((name, state['exam_time'][name]))

    return names_with_min(items)


def get_top_examiners(state):
    items = []

    for name in state['examiners']:
        total = state['exam_total'].get(name, 0)

        if total > 0:
            fail_rate = state['exam_failed'].get(name, 0) / total
            items.append((name, fail_rate))

    return names_with_min(items)


def get_students_to_expel(state):
    items = []

    for name in state['students']:
        if state['status'].get(name) == FAILED:
            items.append((name, state['finish_time'][name]))

    return names_with_min(items)


def get_best_questions(state):
    scores = dict(state['question_score'])

    if not scores:
        return ['-']

    best_score = max(scores.values())

    return [
        question
        for question, score in scores.items()
        if score == best_score
    ]


def show_final(state):
    clear_screen()

    print(make_table(['Student', 'Status'], student_rows(state, final=True)))
    print()
    print(make_table(
        ['Examiner', 'Total Students', 'Завалил', 'Work Time'],
        examiner_rows(state, final=True)
    ))
    print()

    passed_count = sum(
        1
        for name in state['students']
        if state['status'].get(name) == PASSED
    )

    print(f"Время с момента начала экзамена и до момента и его завершения: {time.time() - state['start_time']:.2f}")
    print(f"Лучшие студенты: {', '.join(get_top_students(state))}")
    print(f"Лучшие экзаменаторы: {', '.join(get_top_examiners(state))}")
    print(f"Студенты к отчислению: {', '.join(get_students_to_expel(state))}")
    print(f"Лучшие вопросы: {', '.join(get_best_questions(state))}")

    result = 'passed' if passed_count / state['total_students'] > 0.85 else 'failed'
    print(f'Result exam {result}')


def create_state(manager, students, examiners, questions):
    state = manager.dict()

    state['students'] = [student.name for student in students]
    state['examiners'] = [examiner.name for examiner in examiners]

    state['status'] = manager.dict({
        student.name: IN_QUEUE
        for student in students
    })

    state['current'] = manager.dict({
        examiner.name: '-'
        for examiner in examiners
    })

    state['exam_total'] = manager.dict({
        examiner.name: 0
        for examiner in examiners
    })

    state['exam_failed'] = manager.dict({
        examiner.name: 0
        for examiner in examiners
    })

    state['work_time'] = manager.dict({
        examiner.name: 0.0
        for examiner in examiners
    })

    state['question_score'] = manager.dict({
        question: 0
        for question in questions
    })

    state['finish_time'] = manager.dict()
    state['exam_time'] = manager.dict()

    state['total_students'] = len(students)
    state['in_queue'] = len(students)
    state['finished'] = 0
    state['start_time'] = time.time()

    return state


def main():
    folder = os.path.dirname(os.path.abspath(__file__))

    try:
        students = read_people(os.path.join(folder, 'students.txt'))
        examiners = read_people(os.path.join(folder, 'examiners.txt'))
        questions = read_questions(os.path.join(folder, 'questions.txt'))
    except (OSError, ValueError) as error:
        print(f'Input error: {error}')
        return

    if not students or not examiners or len(questions) < 3:
        print('error check students.txt, examiners.txt and questions.txt')
        return

    manager = mp.Manager()
    state = create_state(manager, students, examiners, questions)
    lock = manager.Lock()

    queue = mp.Queue()

    for student in students:
        queue.put(student)

    processes = []

    for examiner in examiners:
        process = mp.Process(
            target=examiner_process,
            args=(examiner, queue, state, lock, questions)
        )

        process.start()
        processes.append(process)

    try:
        while state['finished'] < state['total_students']:
            show_live(state)
            time.sleep(0.3)
    except KeyboardInterrupt:
        for process in processes:
            process.terminate()

        return

    for process in processes:
        process.join()

    show_final(state)


if __name__ == '__main__':
    main()
