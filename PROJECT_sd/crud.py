"""
crud.py
Basic Create / Read / Update / Delete operations.
Every query uses '?' placeholders instead of f-strings — this is called a
parameterized query. It's the standard defense against SQL injection, and
mentioning it in an interview is a free point.
"""

from db import get_connection


# ---------- CREATE ----------

def add_doctor(name, specialization, username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO doctors (name, specialization, username, password) VALUES (?, ?, ?, ?)",
        (name, specialization, username, password)
    )
    conn.commit()
    doctor_id = cur.lastrowid
    conn.close()
    return doctor_id


def add_patient(name, dob, gender, doctor_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO patients (name, dob, gender, doctor_id) VALUES (?, ?, ?, ?)",
        (name, dob, gender, doctor_id)
    )
    conn.commit()
    patient_id = cur.lastrowid
    conn.close()
    return patient_id


def log_ecg_session(patient_id, session_date, device_id, duration_sec,
                     classification=None, confidence=None):
    """Logs a session, and optionally a linked prediction in the same call."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO ecg_sessions (patient_id, session_date, device_id, duration_sec) "
        "VALUES (?, ?, ?, ?)",
        (patient_id, session_date, device_id, duration_sec)
    )
    session_id = cur.lastrowid

    if classification:
        cur.execute(
            "INSERT INTO arrhythmia_predictions (session_id, classification, confidence, predicted_at) "
            "VALUES (?, ?, ?, ?)",
            (session_id, classification, confidence, session_date)
        )

    conn.commit()
    conn.close()
    return session_id


# ---------- READ ----------

def list_patients():
    conn = get_connection()
    rows = conn.execute("SELECT patient_id, name, dob, gender FROM patients ORDER BY name").fetchall()
    conn.close()
    return rows


def get_patient_history(patient_id):
    """All sessions + predictions for one patient, most recent first."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT s.session_id, s.session_date, s.device_id, s.duration_sec,
               p.classification, p.confidence
        FROM ecg_sessions s
        LEFT JOIN arrhythmia_predictions p ON p.session_id = s.session_id
        WHERE s.patient_id = ?
        ORDER BY s.session_date DESC
    """, (patient_id,)).fetchall()
    conn.close()
    return rows


def search_patients_by_name(keyword):
    conn = get_connection()
    rows = conn.execute(
        "SELECT patient_id, name, dob, gender FROM patients WHERE name LIKE ?",
        (f"%{keyword}%",)
    ).fetchall()
    conn.close()
    return rows


# ---------- UPDATE ----------

def update_patient_doctor(patient_id, new_doctor_id):
    conn = get_connection()
    conn.execute("UPDATE patients SET doctor_id = ? WHERE patient_id = ?", (new_doctor_id, patient_id))
    conn.commit()
    conn.close()


# ---------- DELETE ----------

def delete_patient(patient_id):
    """Deletes a patient and everything downstream (sessions, predictions)."""
    conn = get_connection()
    cur = conn.cursor()
    session_ids = [r[0] for r in cur.execute(
        "SELECT session_id FROM ecg_sessions WHERE patient_id = ?", (patient_id,)
    ).fetchall()]
    for sid in session_ids:
        cur.execute("DELETE FROM arrhythmia_predictions WHERE session_id = ?", (sid,))
    cur.execute("DELETE FROM ecg_sessions WHERE patient_id = ?", (patient_id,))
    cur.execute("DELETE FROM patients WHERE patient_id = ?", (patient_id,))
    conn.commit()
    conn.close()
