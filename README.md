# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

## Starting Project

### Pre-requisites and Local Development

Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file.

To run the application run the following commands:

```

export FLASK_APP=flaskr

export FLASK_ENV=development

flask run

```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration.

#### Frontend

From the frontend folder, run the following commands to start the client:

```

npm install // only once to install dependencies

npm start

```

By default, the frontend will run on localhost:3000.

## API documentation

### Base URL: start app locally on localhost:5000/api

### Endpoints

`GET /categories`

- Fetches question categories
- Request argument: NONE
- Returns an object containing the following

```
{
  "success": True,
  "categories": {
    '1': "History",
    '2': "Science"
  },
}
```

`GET /questions?page=1`

- Fetches a paginated list of questions, page query is optional and defaults to 1
- Request argument: None
- Returns an object containing the following

```
{
  "success": true,
  "questions": [
    {
      'id': 1,
      'question': What is Africa,
      'answer': continent,
      'category': 1,
      'difficulty': 1
    }
  ],
  "total_questions": 1,
  "categories": {
    '1': "History",
    '2': "Science"
  },
  "current_category": "All",
}
```

`DELETE /question/<question_id>`

- Delete a question by question id
- Request Argument: Node
- Returns an object with the following properties

```
{
   "success": true,
    "questions": [
      {
      'id': 1,
      'question': What is Africa,
      'answer': continent,
      'category': 1,
      'difficulty': 1
    }
    ],
    "total_questions": 0,
    "categories": {
      '1': "History",
      '2': "Science"
    },
    "current_category": "All",
}

```

`POST \questions`

- Post a new question
- Request argument:

```
{
  question: <String>
  answer: <String>
  category: <category_id>
  difficulty: <Number 1 - 4>
}
```

- Returns an object with the following parameters example

```
{
   "success": true,
    "questions": [
      'id': 1,
      'question': What is Africa,
      'answer': continent,
      'category': 1,
      'difficulty': 1
    ],
    "total_questions": 1,
    "categories": {
      '1': "History",
      '2': "Science"
    },
    "current_category": "All",
}
```

`POST /questions/search`

- Search for questions by keyword
- Request argument:

```
{
  searchTerm: <String>
}
```

- Return an object with search result

```
{
    "success": true,
    "questions": [
      'id': 1,
      'question': What is Africa,
      'answer': continent,
      'category': 1,
      'difficulty': 1
    ],
    "total_questions": 1,
    "current_category": "All",
}
```

`GET /categories/<int:category_id>/questions`

- Fetches questions for a given category id
- Request argument: None
- Returns:

```
{
  "success": true,
    "questions": [
      'id': 1,
      'question': What is Africa,
      'answer': continent,
      'category': 1,
      'difficulty': 1
    ],
    "total_questions": 1,
    "current_category": "All",
}
```

`POST /quizzes`

- Fetches random quest questions
- Request argument:

```
{
  "previous_questions": <array of previous questions>
  "quiz_category": <optional category>
}
```

- Returns an object with the following example parameters

```
{
  "success": true,
  "question": What is the name of the longest river
}
```
