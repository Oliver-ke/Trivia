# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

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
