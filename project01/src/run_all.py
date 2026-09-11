import subprocess
import os

base = os.path.dirname(__file__)

task_inputs = {
    1: "1.0 2.0 3.0\n4.0 5.0 6.0\n",
    2: "1143411\n",
    4: "5\n",
    5: "-14.97\n",
    7: "3 4\n3 0 2 1\n6 4 8 5\n3 3 6 0\n",
    8: "10\n5\n3\n7\n3\n6\n3\n5\n2\n9\n4\n",
    9: "2 3.0\n5\n1.2\n-3\n",
    10: "5 48\n2023 100 14\n2020 18 347\n2023 10000000 34\n2023 1000 34\n2022 10 34\n",
}

task3_input = (
    "0 0 0 0 0 0 0 0 1 0\n"
    "0 1 1 1 0 0 0 1 1 1\n"
    "0 1 1 1 0 0 0 0 1 0\n"
    "0 1 1 1 0 0 0 0 0 0\n"
    "0 0 0 0 0 0 0 0 0 0\n"
    "0 1 1 0 0 1 1 0 0 0\n"
    "0 1 1 0 1 1 1 1 0 0\n"
    "0 0 0 0 1 1 1 1 0 0\n"
    "1 1 0 0 0 1 1 0 0 0\n"
    "1 1 0 0 0 0 0 0 0 0\n"
)

task6_input = '''{
  "list1": [
    {"title": "Titanic", "year": 1998},
    {"title": "Taxi 2", "year": 2000},
    {"title": "Avatar", "year": 2009}
  ],
  "list2": [
    {"title": "Terminator", "year": 1984},
    {"title": "Home Alone", "year": 1993},
    {"title": "Spider-Man", "year": 2002}
  ]
}
'''

for i in range(1, 11):
    print(f"{'='*40}")
    print(f"  TASK {i}")
    print(f"{'='*40}")

    path = os.path.join(base, f"exercise{i}", "task1.py")

    if i == 3:
        print("Input (input.txt):")
        print(task3_input)
        with open("input.txt", "w") as f:
            f.write(task3_input)
        result = subprocess.run(["python", path], capture_output=True, text=True)
        os.remove("input.txt")
    elif i == 6:
        print("Input (input.txt):")
        print(task6_input)
        with open("input.txt", "w") as f:
            f.write(task6_input)
        result = subprocess.run(["python", path], capture_output=True, text=True)
        os.remove("input.txt")
    else:
        print("Input:")
        print(task_inputs[i])
        result = subprocess.run(["python", path], input=task_inputs[i], capture_output=True, text=True)

    print("Output:")
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print("stderr:", result.stderr)
