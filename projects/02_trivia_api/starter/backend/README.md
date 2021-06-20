# Backend - Full Stack Trivia API

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks
These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.


2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.


3. Create an endpoint to handle GET requests for all available categories.


4. Create an endpoint to DELETE question using a question ID.


5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.


6. Create a POST endpoint to get questions based on category.


7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.


8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.


9. Create error handlers for all expected errors including 400, 404, 422 and 500.



## API Endpoints

GET '/questions?page=${integer}'
GET '/categories'
DELETE '/questions/${question_id}'
POST '/questions'
POST '/questions/search'
GET '/categories/<int:category_id>/questions'
POST '/quizzes'

```js
GET '/questions?page=${integer}'
- Fetches a paginated list of all questions , the total number of questions, a dictionary of all categories, and the current category.
- Request Arguments: http query argument 'page' that must be an integer value
- Returns: Object with a list of at most 10 questions , the total number of questions, a dictionary of all categories in which the keys are the ids and the value is the corresponding type of the category, and the current category which is always set to None.
    {
      'questions':[
          {
            'id': 1000
            'question': 'Which mythological woman was said to have a face that launched 1000 ships? ',
            'answer': Helen of Troy,
            'category': 4,
            'difficulty': 3
          }, ...],
      'total questions': 500
      'categories':{
          '1': "Science",
          '2': "Art",
          '3': "Geography",
          '4': "History",
          '5': "Entertainment",
          '6': "Sports"
          },
      'current_category': None
    }
```

```js
GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: Object with a single key, categories, that contains a object of id: category_string key:value pairs.
    {
      '1' : "Science",
      '2' : "Art",
      '3' : "Geography",
      '4' : "History",
      '5' : "Entertainment",
      '6' : "Sports"
    }
```

```js
DELETE '/questions/${question_id}'
- Deletes question from the database based on its id
- Request Argument: Integer value for question_id
- Returns: Object indicating the deletion was successful and the question id of the deleted question
    {
      'success': True
      'deleted_question_id': 1
    }
```

```js
POST '/questions'
- Adds a new question to the database
- Request Body: object with values for question, answer, category, and difficulty
    {
      'question': 'What is my name?',
      'answer': 'You will never know O_0'
      'category': 4,
      'difficulty': 5
    }
- Returns: Object indicating the deletion was successful and the question id of the created question
    {
      'success': True
      'new_question_id': 1
    }
```

```js
POST '/questions/search'
- Searches for questions that contain a passed search term as a substring
- Request Body: object with key value pair for the search term and the input string
    {searchTerm: 'example string'}
- Returns: Object with a list of questions matching the search term, the total number of questions that match, and the current category which is always set to None
    {
      'questions':[
          {
            'id': 1000
            'question': 'Which mythological woman is said to have a face that launched 1000 ships? ',
            'answer': Helen of Troy,
            'category': 4,
            'difficulty': 2
          }, ...]
      'total_questions': 5
      'current_category': None
    }
```

```js
GET '/categories/${category_id}/questions'
- Fetches a list of questions corresponding to a given category
- Request Argument: Integer value for category_id
- Returns: Object with a list of all questions in the given category, the total number of questions regardless of category, and the current category type.
    {
      'questions':[
          {
            'id': 10
            'question': 'Which Argentinian soccer player has won the Ballon D'or Award the most amount of times? ',
            'answer': 'Lionel Messi',
            'category': 6,
            'difficulty: 2
          }, ...]
      'total_questions': 500
      'current_category': 'Sports'
    }
```

```js
POST '/quizzes'
- Fetches a new, randomly selected question that has not yet been asked in the quiz
- Request Body: Object with a list of the ids of the previous questions asked in the quiz, and a dictionary with the information of the category of the quiz
    {
      'previous_questions': [1, 3, 5, 7],
      'quiz_category': {
          'type': 'Entertainment',
          'id': 5
          }
    }
- Returns: Object containing the data for the next question in the quiz
    {
      question: {
        'id': 34
        'question': 'Which famous reality star married Kanye West?',
        'answer': 'Kim Kardashian',
        'category': 5,
        'difficulty': 3}
    }
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
