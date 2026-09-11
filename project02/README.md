# Project 02 — Python_Bootcamp

**Summary:**  
In this project, you'll practice using object-oriented, procedural, and multiparadigm approaches in Python — and you'll also write code that follows the functional programming paradigm.

💡 Click here to share your feedback on this project. It's anonymous and helps us make the learning experience better. We recommend filling out the survey right after completing the project.

## Contents

  - [Chapter I](#chapter-i)
    - [Instructions](#instructions)
  - [Chapter II](#chapter-ii)
    - [General Information](#general-information)
  - [Chapter III](#chapter-iii)
    - [Task 1. Exam](#task-1-exam)
    - [Task 2. Image Downloader](#task-2-image-downloader)

## Chapter I

### Instructions

How to learn at “School 21”:

- Here, you’ll find a unique learning experience with a lot of freedom. You’re given a task and left to find your own way to solve it, using whatever resources work best for you — whether that’s the Internet or AI tools like GigaChat. Just be mindful of information quality: verify, think critically, analyze, and compare.
- Peer-to-peer (P2P) learning is the exchange of knowledge and experience with peers, where everyone acts as both mentor and student. This approach allows you to gain a deeper understanding of the material by learning from one another.
- Feel free to ask for help: around you are peers who are also navigating this path for the first time. Share your own experience and ideas with others.  Join Rocket.Chat to stay updated with the latest community announcements. 
- Your learning is meaningless if you just copy someone else’s solutions. When receiving help from others, always make sure you fully understand the “why”, “how”, and “purpose” behind the solution. Don’t be afraid to make mistakes. 
- Does the task seem impossible? Take a break, get some fresh air and clear your mind — this has helped many people. Maybe after that, the solution will come to you naturally.
- The learning process is just as important as the result. It’s not just about completing the task — it’s about understanding HOW to solve it. 

How to work with the project:

- Before starting, clone the project from GitLab into a repository with the same name.
- All files should be created inside the _src/_ folder of the cloned repository.
- After cloning the project, create a _develop_ branch and do all your development there. Then, push the _develop_ branch to GitLab.
- Your directory should not contain any files other than those specified in the assignments.

## Chapter II

### General Information

Topics to explore:

- **OOP (Object-Oriented Programming)** — a programming paradigm that structures and organizes code as objects that interact with each other.
- **Procedural approach** — a programming style in which tasks are broken down into small procedures or functions.
- **Functional paradigm** — focuses on defining and applying functions that transform data without altering the original values.
- **Multiparadigm approach** — combining multiple programming paradigms within a single program.
- **Differences from C and C++** — syntax, dynamic typing, memory management, and built-in libraries.
- **Asynchronous / parallel programming** — techniques for running multiple tasks simultaneously.

## Chapter III

**Important!** Each task must be organized as a separate project.   
For example: `T01/src/exercise0`, `T01/src/exercise1`, ..., `T01/src/exerciseN-1`, where **N** is the total number of tasks.  
If one task builds upon the previous one, simply copy the previous project into the new directory and continue development from there.

Be sure to follow the instructions for the tasks specified in the materials.

### Task 1. Exam

Students are lining up to take an exam. Several examiners are working simultaneously. All students wait in a single, shared queue. As soon as an examiner becomes available, the next student in line goes in for their exam.

Thirty seconds after an exam begins, each examiner is permitted to take a lunch break. They finish the current session, after which they refuse new students for a random duration between 12 and 18 seconds.

The exam process works as follows:  
Each student is asked three questions from a question bank. For each question, the student randomly selects a word from the question as their answer. Statistically, boys tend to choose words closer to the beginning of the question, while girls tend to choose words closer to the end. The probabilities follow a golden ratio distribution. For example, in response to the question "There is a table", a boy would answer "There" with probability `**a = 1/F**`, "is" with probability `**b = (1–a)/F**`, and "table" with probability `**c = 1–a–b**`, where `**F ≈ 1.618...**` (for a 4-word question, `**c = (1–a–b)/F**`, and so on). A girl answering the same question would choose "table" with probability `**a**`, "is" with `**b**`, and "There" with `**c**`.

Since examiners do not know the correct answer in advance, they follow the same approach and randomly select words from the question. Multiple correct answers are allowed. After selecting one answer, the examiner has a 1/3 chance of selecting another answer and continues this process until all the words in the question have been selected as correct or the examiner stops.

Once the student has answered, the examiner decides whether the student passed the exam. There is a 1/8 chance that the examiner is in a bad mood (in which case the student automatically fails), a 1/4 chance that the examiner is in a good mood (in which case the student automatically passes), and a 5/8 chance that the examiner is in a neutral mood. In that case, the outcome depends on performance: the student passes if they answered more questions correctly than incorrectly.

The exam's duration depends on the length of the examiner's name. For example, an examiner named **Stepan** (6 letters) would conduct exams lasting between 5 and 7 seconds (a random float in that range).

You need to simulate the exam process.

When the program starts:

- The list of examiners is read from the `examiners.txt` file.
- The list of students who arrived early and formed a queue is read from `students.txt`.
- The question bank is read from the `questions.txt` file.

The exam then begins.

Each examiner conducts exams on a separate process.

During execution, the console must display up-to-date exam information, including:

1. **Table of Students** with two columns: "Student" and "Status".
    - The status can be one of the following: "In Queue", "Passed", or "Failed". The table must be sorted by status: first, students in the queue in the order they’ll be examined; second, those who passed; and third, those who failed.
2. **Table of Examiners** with five columns: "Examiner", "Current Student", "Total Students", "Failed", and "Work Time".
    - When an examiner is on a break or has finished for the day, display "-" in the "Current student" column.
3. A separate line showing the number of students still in the queue out of the total.
4. A separate line displaying the time since the exam started.

This information should be updated in place, not printed as new lines.

**When the exam ends and program stops, display:**

1. **Table of Students** with two columns: "Student" and "Status".
    - Status is now only "Passed" or "Failed". The table is sorted with "Passed" first and "Failed" last.
2. **Table of Examiners** with four columns: "Examiner", "Total Students", "Failed", and "Work Time".
3. A separate line showing the total time from the start to the finish of the exam.
4. A separate line listing top-performing students (those who passed the exam the fastest), separated by commas.
5. A separate line listing top examiners (those with the lowest failure rate among their students), comma-separated.
6. A separate line listing students to be expelled — these are the students who failed and finished earlier than other students who also failed.
7. A separate line listing the best questions, separated by commas. A question is considered the best if the highest number of students answered it correctly.
8. A separate line with the exam result summary. The exam is considered successful if **more than 85%** of students pass.

**Input**

| examiners.txt |
| --- |
| Stepan M<br>Darya F<br>Mikhail M |

| students.txt |
| --- |
| Petr M<br>Sergey M<br>Varvara F<br><br>Ivan M<br>Ekaterina F<br>Alexandra F<br>Aleksey M |

| questions.txt |
| --- |
| There is a table<br>A man is a dog’s friend<br>Solar eclipses affect people<br>Programming is an interesting activity |

**Output**

During exam

```
+------------+----------+
| Student    |  Status  |
+------------+----------+
| Aleksey    | In queue |
| Petr       |  Passed  |
| Ivan       |  Passed  |
| Ekaterina  |  Passed  |
| Sergey     |  Failed  |
| Varvara    |  Failed  |
| Alexandra  |  Failed  |
+------------+----------+

+-------------+-----------------+-----------------+---------+--------------+
| Examiner    | Current student | Total students  | Failed  | Work time    |
+-------------+-----------------+-----------------+---------+--------------+
| Stepan      | Aleksey         |        1        |    0    |    12.31     |
| Darya       | -               |        3        |    2    |    12.14     |
| Mikhail     | -               |        2        |    1    |     7.21     |
+-------------+-----------------+-----------------+---------+--------------+

Remaining in queue: 1 out of 7
Time since exam started: 12.31

```

After exam

```
+------------+----------+
| Student    |  Status  |
+------------+----------+
| Petr       |  Passed  |
| Ivan       |  Passed  |
| Ekaterina  |  Passed  |
| Sergey     |  Failed  |
| Varvara    |  Failed  |
| Alexandra  |  Failed  |
| Aleksey    |  Failed  |
+------------+----------+

+-------------+-----------------+---------+--------------+
| Examiner    | Total students  | Failed  | Work time    |
+-------------+-----------------+---------+--------------+
| Stepan      |        2        |    1    |    12.35     |
| Darya       |        3        |    2    |    12.14     |
| Mikhail     |        2        |    1    |     7.21     |
+-------------+-----------------+---------+--------------+

Time from exam start to finish: 12.35  
Top-performing students: Ivan  
Top examiners: Stepan, Mikhail  
Students to be expelled: Varvara  
Best questions: There is a table, A man is a dog’s friend  
Result: Exam failed
```

### Task 2. Image Downloader
Write a link handler that prompts the user to enter an image URL and downloads the image asynchronously. Ask the user for the next URL immediately after they enter the previous one. Continue doing so until they enter an empty line. If not all images have been downloaded by that point, display a message and wait for all downloads to finish before terminating the program.

Do not terminate the program immediately if any error occurs. Instead, store the status for summary output at the end.  
At the beginning, the user must specify where to save the downloaded images.   
If the specified path is invalid or the program does not have write access to it, prompt the user to enter a different path.

Before exiting, display a summary of successful and failed downloads.

**Input**

```
./img
https://images2.pics4learning.com/catalog/s/swamp_15.jpg
https://bad-link-no-website-here.strange/img.png
https://images2.pics4learning.com/catalog/p/parrot.jpg

```

**Output**

Summary of successful and unsuccessful downloads

```
+----------------------------------------------------------+--------+
| Link                                                     | Status |
+----------------------------------------------------------+--------+
| https://images2.pics4learning.com/catalog/s/swamp_15.jpg | Success|
| https://bad-link-no-website-here.strange/img.png         | Error  |
| https://images2.pics4learning.com/catalog/p/parrot.jpg   | Success|
+----------------------------------------------------------+--------+
```