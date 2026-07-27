"""
queries.py
The "insight" queries — these are what you point to when someone asks
"what makes this more than a CRUD app". Each function has a comment
naming the SQL concept it demonstrates, for your own reverse-learning.
"""

from db import get_connection


def patients_per_doctor():
    """Concept: JOIN + GROUP BY + COUNT"""
    conn = get_connection()
    rows = conn.execute("""
        SELECT d.name AS doctor, COUNT(p.patient_id) AS num_patients
        FROM doctors d
        LEFT JOIN patients p ON p.doctor_id = d.doctor_id
        GROUP BY d.doctor_id
        ORDER BY num_patients DESC
    """).fetchall()
    conn.close()
    return rows


def low_confidence_predictions(threshold=0.7):
    """Concept: WHERE filter + JOIN across 3 tables"""
    conn = get_connection()
    rows = conn.execute("""
        SELECT pt.name AS patient, s.session_date, ap.classification, ap.confidence
        FROM arrhythmia_predictions ap
        JOIN ecg_sessions s ON s.session_id = ap.session_id
        JOIN patients pt ON pt.patient_id = s.patient_id
        WHERE ap.confidence < ?
        ORDER BY ap.confidence ASC
    """, (threshold,)).fetchall()
    conn.close()
    return rows


def arrhythmia_trend_per_patient(patient_id):
    """
    Concept: WINDOW FUNCTION.
    ROW_NUMBER() numbers each patient's sessions in chronological order,
    so you can see how their classification changed session over session.
    This is the query to walk through in an interview.
    """
    conn = get_connection()
    rows = conn.execute("""
        SELECT
            ROW_NUMBER() OVER (ORDER BY s.session_date) AS session_no,
            s.session_date,
            ap.classification,
            ap.confidence,
            LAG(ap.classification) OVER (ORDER BY s.session_date) AS previous_classification
        FROM ecg_sessions s
        JOIN arrhythmia_predictions ap ON ap.session_id = s.session_id
        WHERE s.patient_id = ?
        ORDER BY s.session_date
    """, (patient_id,)).fetchall()
    conn.close()
    return rows


def most_common_classification_overall():
    """Concept: GROUP BY + HAVING"""
    conn = get_connection()
    rows = conn.execute("""
        SELECT classification, COUNT(*) AS occurrences
        FROM arrhythmia_predictions
        GROUP BY classification
        HAVING COUNT(*) > 1
        ORDER BY occurrences DESC
    """).fetchall()
    conn.close()
    return rows


def patients_with_no_sessions():
    """Concept: LEFT JOIN + IS NULL (find the 'missing' side of a join)"""
    conn = get_connection()
    rows = conn.execute("""
        SELECT p.name
        FROM patients p
        LEFT JOIN ecg_sessions s ON s.patient_id = p.patient_id
        WHERE s.session_id IS NULL
    """).fetchall()
    conn.close()
    return rows
