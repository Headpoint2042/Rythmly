const API_BASE = "http://localhost:5000";

/**
 * Check if the backend server is reachable.
 * @returns {Promise<{status: string, timestamp: string}>}
 */
export async function healthCheck() {
  const res = await fetch(`${API_BASE}/api/health`);
  return res.json();
}

/**
 * Send rhythm session data for AI analysis.
 * @param {number} bpm - The BPM the user practiced at.
 * @param {number[]} timingOffsets - Timing deviations in ms (can be empty).
 * @returns {Promise<{success: boolean, message: string, suggestion: string, suggested_bpm: number, avg_offset_ms: number, threshold_ms: number}>}
 */
export async function analyzeSession(bpm, timingOffsets = []) {
  const res = await fetch(`${API_BASE}/api/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ bpm, timing_offsets: timingOffsets }),
  });
  return res.json();
}

/**
 * Save a practice session to the backend.
 * @param {{bpm: number, duration_seconds: number, avg_offset_ms?: number, success?: boolean}} session
 * @returns {Promise<Object>} The saved session with id and created_at.
 */
export async function saveSession(session) {
  const res = await fetch(`${API_BASE}/api/sessions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(session),
  });
  return res.json();
}

/**
 * Retrieve all past practice sessions.
 * @returns {Promise<Object[]>} Sessions sorted by most recent first.
 */
export async function getSessions() {
  const res = await fetch(`${API_BASE}/api/sessions`);
  return res.json();
}
