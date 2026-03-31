import random
from datetime import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

# In-memory session store
sessions = []


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})


@app.route("/api/analyze", methods=["POST"])
def analyze():
    """Analyze a rhythm session and return AI feedback.

    Expects JSON body:
        bpm (int): The BPM the user was practicing at.
        timing_offsets (list[float]): Deviation from perfect beat in ms for each tap.

    Returns JSON:
        success (bool): Whether the performance was acceptable.
        message (str): Feedback message for the user.
        suggestion (str): "increase" | "decrease" | "maintain"
        suggested_bpm (int): The recommended next BPM.
    """
    data = request.get_json()
    if not data or "bpm" not in data:
        return jsonify({"error": "Missing required field: bpm"}), 400

    bpm = data["bpm"]
    timing_offsets = data.get("timing_offsets", [])

    if timing_offsets:
        avg_offset = sum(abs(t) for t in timing_offsets) / len(timing_offsets)
    else:
        # Simulate timing accuracy when no real data is provided
        avg_offset = random.uniform(5, 120)

    # Threshold logic: lower BPM should be easier to hit accurately
    threshold = max(30, 80 - (bpm - 60) * 0.3)

    if avg_offset <= threshold:
        success = True
        suggestion = "increase"
        suggested_bpm = bpm + 10
        message = (
            f"Great job! Your average timing offset was {avg_offset:.1f}ms, "
            f"which is within the acceptable range. "
            f"I would recommend increasing the BPM to {suggested_bpm}."
        )
    else:
        success = False
        suggestion = "decrease"
        suggested_bpm = max(20, bpm - 10)
        message = (
            f"Your average timing offset was {avg_offset:.1f}ms, "
            f"which is above the target of {threshold:.0f}ms. "
            f"I would recommend practicing at {suggested_bpm} BPM first."
        )

    return jsonify({
        "success": success,
        "message": message,
        "suggestion": suggestion,
        "suggested_bpm": suggested_bpm,
        "avg_offset_ms": round(avg_offset, 1),
        "threshold_ms": round(threshold, 1),
    })


@app.route("/api/sessions", methods=["POST"])
def create_session():
    """Save a practice session.

    Expects JSON body:
        bpm (int): BPM practiced at.
        duration_seconds (float): How long the session lasted.
        avg_offset_ms (float, optional): Average timing offset.
        success (bool, optional): Whether AI analysis passed.
    """
    data = request.get_json()
    if not data or "bpm" not in data:
        return jsonify({"error": "Missing required field: bpm"}), 400

    session = {
        "id": len(sessions) + 1,
        "bpm": data["bpm"],
        "duration_seconds": data.get("duration_seconds", 0),
        "avg_offset_ms": data.get("avg_offset_ms"),
        "success": data.get("success"),
        "created_at": datetime.now().isoformat(),
    }
    sessions.append(session)

    return jsonify(session), 201


@app.route("/api/sessions", methods=["GET"])
def get_sessions():
    """Retrieve all practice sessions, most recent first."""
    return jsonify(sorted(sessions, key=lambda s: s["created_at"], reverse=True))


if __name__ == "__main__":
    app.run(debug=True)
