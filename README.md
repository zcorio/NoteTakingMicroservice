# Note Taking Microservice

A Flask-based JSON microservice for creating and storing text notes.

## Features

- Create and store text notes via REST API
- JSON request/response format
- Persistent storage (notes saved to file)
- Input validation with appropriate error responses
- Integration-ready for Flask web applications

## Installation

Install dependencies:
```python
pip install -r requirements.txt
```

## Running the Microservice

Start the server by running `app.py`. The service will run on `http://localhost:5001`

## API Endpoints

### Create Note

**Endpoint:** `POST /notes/create`

**Request Format:**
```json
{
  "text": "<note>"
}
```

**Success Response (201):**
```json
{
  "id": 1,
  "text": "<note>"
}
```

**Error Responses (400):**
- Invalid JSON format
- Missing 'text' field
- Empty note text

**Example using Python requests:**
```python
import requests

response = requests.post(
    'http://localhost:5001/notes/create',
    json={'text': 'Remember to buy groceries'}
)
print(response.json())  # {'id': 1, 'text': 'Remember to buy groceries'}
```

### Get All Notes (Optional)

**Endpoint:** `GET /notes`

Returns all stored notes.

### Health Check

**Endpoint:** `GET /health`

Check if the service is running.

## Integration with Flask Dashboard

From your Flask dashboard, send POST requests to create notes:

```python
import requests

def create_note(note_text):
    response = requests.post(
        'http://localhost:5001/notes/create',
        json={'text': note_text}
    )
    
    if response.status_code == 201:
        return response.json()  # {'id': <int>, 'text': '<note>'}
    else:
        return {'error': response.json()}
```

## Error Handling

The service returns HTTP 400 status code with JSON error messages for:
- Invalid JSON format
- Missing 'text' field
- Empty or whitespace-only notes

## Data Storage

Notes are persisted in `notes_data.json` file for durability across service restarts.

## Acceptance Criteria Compliance

✅ **Requirement 1:** Given the user has entered a note in the dashboard form, when the dashboard sends a POST request to `/notes/create` with JSON `{ "text": "<note>" }`, then the microservice stores the note and returns `{ "id": <int>, "text": "<note>" }`.

✅ **Requirement 2:** Given the microservice receives invalid JSON or an empty note, when the request is processed, then the microservice returns a JSON error with status code 400.
