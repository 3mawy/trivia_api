# Full Stack API Final Project

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. 

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others. 

## Tasks

There are `TODO` comments throughout project. Start by reading the READMEs in:

1. [`./frontend/`](./frontend/README.md)
2. [`./backend/`](./backend/README.md)

We recommend following the instructions in those files in order. This order will look familiar from our prior work in the course.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository]() and [Clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom. 

## About the Stack

We started the full stack application for you. It is desiged with some key functional areas:

### Backend

The `./backend` directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in app.py to define your endpoints and can reference models.py for DB and SQLAlchemy setup. 

### Frontend

The `./frontend` directory contains a complete React frontend to consume the data from the Flask server. You will need to update the endpoints after you define them in the backend. Those areas are marked with TODO and can be searched for expediency. 

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. 

[View the README.md within ./frontend for more details.](./frontend/README.md)


# Trivia Api Reference

## Getting Started

- Local ENV, Hosted by default at http://127.0.0.1:5000/
- Authentication: No Authentication required yet

## Error Handling

Errors are returned as JSON objects in the following format:

    {
        "success": False,
        "error": 404,
        "messege": "Not Found"
    }

The Api will return three error types on failed requests:

- 400: Bad Request
- 404: Not Found
- 405: Not Allowed
- 422: Unprocessable Entity
- 500: Internal Server Error

## Api Endpoints

### GET '/categories'

- description
    - returns a list of available categories and a success value
    
- sample request: curl http://127.0.0.1:5000/categories
  
        {
          "categories": [
            {
              "id": 1, 
              "type": "Science"
            }, 
            {
              "id": 2, 
              "type": "Art"
            }
          ], 
          "success": true
        }


### GET '/questions'

- description
    - returns a list of questions, success value, total questions value, list of categories and the current category
    - the result is paginated with 10 questions a page, include a request argument of the page's number starting from 1 '?page=1'

- sample request: curl http://127.0.0.1:5000/questions
  
        {
          "categories": [
            {
              "id": 1, 
              "type": "Science"
            }, 
            {
              "id": 2, 
              "type": "Art"
            }
          ], 
          "current_category": "", 
          "questions": [
            {
              "answer": "Apollo 13", 
              "category": 5, 
              "difficulty": 4, 
              "id": 2, 
              "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
            }, 
            {
              "answer": "Tom Cruise", 
              "category": 5, 
              "difficulty": 4, 
              "id": 4, 
              "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
            }
          ], 
          "success": true, 
          "total_questions": 19
        }


### DELETE '/questions/<question_id>'

- description
    - deletes a question with a given ID if it exists, returns the id of the deleted question, success value, and a message
    
- sample request: curl -X DELETE http://127.0.0.1:5000/questions/2
  
        {
          "deleted": 2, 
          "message": "Question Deleted", 
          "success": true
        }


### POST '/questions'

- description
    - adds a new question to the database, returns the created question id, success value, and a message

- sample request: curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"question":"test question", "answer":"test answer", "difficulty":"2", "category":"2", }'
  
        {
          "created": 2, 
          "message": "Question Added", 
          "success": true
        }


### POST '/questions/search'

- description
    - returns a list of questions with matching searchTerm, success value, the current category, and total questions
    - the result is paginated with 10 questions a page, include a request argument of the page's number starting from 1 '?page=1'

- sample request: curl -X POST http://127.0.0.1:5000/questions/search -H "Content-Type: application/json" -d '{"searchTerm":"what" }'
  
        {
          "current_category": "", 
          "questions": [
            {
              "answer": "Muhammad Ali", 
              "category": 4, 
              "difficulty": 1, 
              "id": 9, 
              "question": "What boxer's original name is Cassius Clay?"
            }, 
            {
              "answer": "Apollo 13", 
              "category": 5, 
              "difficulty": 4, 
              "id": 2, 
              "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
            }, 
            {
              "answer": "Tom Cruise", 
              "category": 5, 
              "difficulty": 4, 
              "id": 4, 
              "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
            }, 
            {
              "answer": "Edward Scissorhands", 
              "category": 5, 
              "difficulty": 3, 
              "id": 6, 
              "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
            }, 
            {
              "answer": "Lake Victoria", 
              "category": 3, 
              "difficulty": 2, 
              "id": 13, 
              "question": "What is the largest lake in Africa?"
            }, 
        
          ], 
          "success": true, 
          "total_questions": 5
        }
        


### GET '/categories/<category_id>/questions'

- description
    - returns a list of questions filtered by category, success value, total questions value, list of categories and the current category
    - the result is paginated with 10 questions a page, include a request argument of the page's number starting from 1 '?page=1'

- sample request: curl http://127.0.0.1:5000/categories/2/questions
      
        {
          "current_category": 2, 
          "questions": [
            {
              "answer": "Escher", 
              "category": 2, 
              "difficulty": 1, 
              "id": 16, 
              "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
            }, 
            {
              "answer": "Mona Lisa", 
              "category": 2, 
              "difficulty": 3, 
              "id": 17, 
              "question": "La Giaconda is better known as what?"
            }, 
            {
              "answer": "One", 
              "category": 2, 
              "difficulty": 4, 
              "id": 18, 
              "question": "How many paintings did Van Gogh sell in his lifetime?"
            }, 
            {
              "answer": "Jackson Pollock", 
              "category": 2, 
              "difficulty": 2, 
              "id": 19, 
              "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
            }
          ], 
          "success": true, 
          "total_questions": 4
        }


### POST 'quizzes'

- description
    - takes a previous_questions attribute, and a quiz category ojb. 
    - returns a question object,  success value

- sample request: curl -X POST http://127.0.0.1:5000/quizzes  -H "Content-Type: application/json" -d '{"previous_questions":[], "quiz_category":{"type":"Geography","id":"2"}}'

        {
          "question": {
            "answer": "Escher", 
            "category": 2, 
            "difficulty": 1, 
            "id": 16, 
            "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
          }, 
          "success": true
        }


GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
