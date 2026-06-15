# Project 03 — Python_Bootcamp

**Summary:**  
In this project, you will learn how to create a web application in Python using Flask.

💡 [Click here](https://new.oprosso.net/p/4cb31ec3f47a4596bc758ea1861fb624) to share your feedback on this project. It’s anonymous and helps our team improve the learning experience. We recommend completing the survey right after finishing the project.

## Contents

  - [Chapter I](#chapter-i)
  - [Chapter II](#chapter-ii)
    - [General Information](#general-information)
    - [Topics to Study](#topics-to-study)
  - [Chapter III](#chapter-iii)
    - [Task 0. Project Setup](#task-0-project-setup)
    - [Task 1. Creating the Project Structure](#task-1-creating-the-project-structure)
    - [Task 2. Implementing the Domain Layer](#task-2-implementing-the-domain-layer)
    - [Task 3. Implementing the Datasource Layer](#task-3-implementing-the-datasource-layer)
    - [Task 4. Implementing the Web Layer](#task-4-implementing-the-web-layer)
    - [Task 5. Implementing the DI Layer](#task-5-implementing-the-di-layer)


## Chapter I

**Instructions**

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

A **web application** is a type of client-server application in which the client interacts with a web server via a browser. The logic of a web application is distributed between the server and the client. Data storage primarily occurs on the server, and information exchange takes place over the network.

**Flask** is one of the most popular Python frameworks for creating web applications. Its advantages include:

- **Ease of use**: Flask has a simple and intuitive syntax, making it ideal for beginner developers or those who prefer clear, straightforward code.
- **Good documentation**: Flask offers well-structured, clear documentation that simplifies getting started and troubleshooting.
- **Flexibility**: Flask provides a flexible and modular approach to web development, allowing you to select the necessary components and features for your project.
- **Support for RESTful APIs**: Flask provides convenient tools for developing RESTful APIs, including routing, data serialization, and request/response handling.
- **Good integration with other tools**: Flask easily integrates with popular Python libraries and tools, such as SQLAlchemy for database work and Jinja2 for templating.

These advantages make Flask an attractive choice for developers aiming to build fast, scalable, and maintainable web applications in Python.

### Topics to Study

- Web application,
- Flask for the backend,
- API,
- Minimax algorithm,
- MVC.

## Chapter III

## Project: Tic-Tac-Toe
The project is created once and used for all subsequent tasks.

### Task 0. Project Setup

In order to develop in Python, you will need to install the appropriate interpreter. It can be downloaded from the official website. Once installed, you can use the command line and/or various integrated development environments (IDEs) to work on projects.  

In this context, a project is a set of .py files containing Python code that can be run individually via the command `python filename.py` (or `python3`) or imported into a file commonly named `main.py`.  

In PyCharm, creating a project is straightforward. You just select the Python interpreter to use and specify the save path and project name. You can also create a virtual environment, which is useful for large projects with many dependencies, such as libraries and frameworks.

### Task 1. Creating the Project Structure

- Each layer should be a separate module.
- The project structure must include the following layers: **web**, **domain**, **datasource**, and **di**.
- The **web** layer must contain the following packages for client interaction: model, module, route, and mapper.
- The **domain** layer must include the model and service packages to implement business logic.
- The **datasource** layer must include the model, repository, and mapper packages for data handling (e.g., database operations).
- The **di** layer contains configurations for dependency injection.

### Task 2. Implementing the Domain Layer

- Define the game board model as an integer matrix.
- Define the current game model, which includes a UUID and the game board.
- Define a service interface with the following methods:
  - A method to determine the next move in the current game using the Minimax algorithm.
  - A method to validate the current game board (checking that previous moves have not been altered).
  - A method to check if the game has ended.
- Place models, interfaces, and implementations in separate files.

### Task 3. Implementing the Datasource Layer

- Implement a storage class for current games.
- Use thread-safe collections for storage.
- Define models for the game board and the current game.
- Implement mappers between the domain and data source models (domain<->datasource).
- Implement a repository to work with the storage class that includes the following methods:
  - A method to save the current game.
  - A method to retrieve the current game.
- Create a class that implements the service interface and accepts the repository as a parameter to work with the storage class.
- Place models, interfaces, and implementations in separate files.

### Task 4. Implementing the Web Layer

- Define models for the game board and the current game.
- Implement mappers between the domain and web models (domain<->web).
- Implement a Flask controller with a POST method, /game/{current_game_UUID}, that accepts a current game with a user-updated game board and returns a current game with a computer-updated game board.
- If an invalid game with an updated board is sent, return an error with a description.
- Support multiple games running simultaneously.
- Models, interfaces, and implementations should be in separate files.

### Task 5. Implementing the DI Layer

- Implement a Container class that defines the dependency graph.
- It must include at least:
  - A singleton storage class.
  - A repository for working with the storage class.
  - A service for working with the repository.