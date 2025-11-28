from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Store notes in memory (could be replaced with database)
notes_store = []
next_note_id = 1

# Path for persistent storage
NOTES_FILE = 'notes_data.json'


def load_notes():
    """Load notes from file if it exists"""
    global notes_store, next_note_id
    if os.path.exists(NOTES_FILE):
        try:
            with open(NOTES_FILE, 'r') as f:
                data = json.load(f)
                notes_store = data.get('notes', [])
                next_note_id = data.get('next_id', 1)
        except Exception:
            notes_store = []
            next_note_id = 1


def save_notes():
    """Save notes to file"""
    try:
        with open(NOTES_FILE, 'w') as f:
            json.dump({
                'notes': notes_store,
                'next_id': next_note_id
            }, f, indent=2)
    except Exception as e:
        print(f"Error saving notes: {e}")


@app.route('/notes/create', methods=['POST'])
def create_note():
    """
    Create and store a new note
    Expected JSON: { "text": "<note>" }
    Returns: { "id": <int>, "text": "<note>" }
    """
    global next_note_id
    
    # Check if request has JSON content
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Invalid JSON format"}), 400
    
    # Validate that 'text' field exists
    if data is None or 'text' not in data:
        return jsonify({"error": "Missing 'text' field in request"}), 400
    
    note_text = data.get('text')
    
    # Validate that note is not empty
    if not note_text or not note_text.strip():
        return jsonify({"error": "Note text cannot be empty"}), 400
    
    # Create the note
    note = {
        "id": next_note_id,
        "text": note_text
    }
    
    notes_store.append(note)
    next_note_id += 1
    
    # Save to file for persistence
    save_notes()
    
    return jsonify(note), 201


@app.route('/notes', methods=['GET'])
def get_notes():
    """
    Retrieve all notes (optional endpoint for testing)
    Returns: List of all notes
    """
    return jsonify(notes_store), 200


@app.route('/notes/delete/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """
    Delete a note by ID
    Returns: Success message or error
    """
    global notes_store
    
    # Find the note with the given ID
    note_index = None
    for i, note in enumerate(notes_store):
        if note['id'] == note_id:
            note_index = i
            break
    
    if note_index is None:
        return jsonify({"error": f"Note with id {note_id} not found"}), 404
    
    # Remove the note
    deleted_note = notes_store.pop(note_index)
    
    # Save to file for persistence
    save_notes()
    
    return jsonify({"message": "Note deleted successfully", "deleted_note": deleted_note}), 200


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "note-taking"}), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    # Load existing notes on startup
    load_notes()
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5001, debug=True)
