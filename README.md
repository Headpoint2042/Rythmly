# Rythmly

A rhythm training application that helps musicians practice tempo accuracy with a built-in metronome and AI-powered feedback. Built as a Hi-Fi prototype for HCI Module 6 at university.

## Tech Stack

- **Frontend**: Vue 3, Tailwind CSS 3, Web Audio API
- **Backend**: Flask, Flask-CORS

## Setup

### Frontend

```bash
cd frontend
npm install
```

### Backend

```bash
cd backend
pip install -r requirements.txt
```

Or install manually:

```bash
pip install Flask Flask-CORS
```

## Running

Start both servers in separate terminals:

```bash
# Terminal 1 - Frontend (http://localhost:8080)
cd frontend
npm run serve

# Terminal 2 - Backend (http://localhost:5000)
cd backend
python app.py
```

## Project Structure

```
Rythmly/
├── frontend/
│   └── src/
│       ├── main.js                         # Vue app entry point
│       ├── App.vue                         # Root component, state management
│       ├── api.js                          # Backend API client
│       ├── styles.css                      # Tailwind CSS imports
│       └── components/
│           ├── ButtonsBPMComponent.vue     # Metronome with BPM controls
│           ├── AIFeedbackComponent.vue     # AI recording toggle
│           └── PopupComponent.vue          # Feedback modal dialog
└── backend/
    ├── app.py                              # Flask API server
    └── requirements.txt                    # Python dependencies
```

## API Endpoints

| Method | Endpoint         | Description                                          |
|--------|------------------|------------------------------------------------------|
| GET    | `/api/health`    | Health check, returns server status and timestamp    |
| POST   | `/api/analyze`   | Analyze rhythm session, returns feedback + BPM advice|
| POST   | `/api/sessions`  | Save a practice session                              |
| GET    | `/api/sessions`  | Retrieve all past sessions (most recent first)       |

### POST `/api/analyze`

Request body:

```json
{
  "bpm": 120,
  "timing_offsets": [12.5, -8.3, 15.1, -3.2]
}
```

Response:

```json
{
  "success": true,
  "message": "Great job! Your average timing offset was 9.8ms...",
  "suggestion": "increase",
  "suggested_bpm": 130,
  "avg_offset_ms": 9.8,
  "threshold_ms": 62.0
}
```

### POST `/api/sessions`

Request body:

```json
{
  "bpm": 120,
  "duration_seconds": 30,
  "avg_offset_ms": 9.8,
  "success": true
}
```
