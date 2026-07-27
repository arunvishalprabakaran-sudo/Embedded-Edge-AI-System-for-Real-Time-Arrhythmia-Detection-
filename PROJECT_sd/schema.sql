-- schema.sql
-- Patient Records & ECG Session Tracker
-- Run this once to create the database structure.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS doctors (
    doctor_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    specialization  TEXT,
    username        TEXT UNIQUE NOT NULL,
    password        TEXT NOT NULL   -- plain text ok for a student project; mention in README you know this isn't production-safe
);

CREATE TABLE IF NOT EXISTS patients (
    patient_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    dob             DATE,
    gender          TEXT,
    doctor_id       INTEGER,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

CREATE TABLE IF NOT EXISTS ecg_sessions (
    session_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id      INTEGER NOT NULL,
    session_date    DATETIME NOT NULL,
    device_id       TEXT,
    duration_sec    INTEGER,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);

CREATE TABLE IF NOT EXISTS arrhythmia_predictions (
    prediction_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id      INTEGER NOT NULL,
    classification  TEXT NOT NULL,   -- e.g. 'Normal', 'AFib', 'PVC', 'Tachycardia'
    confidence      REAL,
    predicted_at    DATETIME NOT NULL,
    FOREIGN KEY (session_id) REFERENCES ecg_sessions(session_id)
);

-- Indexes: speed up the lookups the app actually does (patient history search,
-- and joining sessions -> predictions). This is also a real interview talking point:
-- "I indexed patient_id and session_id because those are my most common JOIN/WHERE columns."
CREATE INDEX IF NOT EXISTS idx_patients_doctor ON patients(doctor_id);
CREATE INDEX IF NOT EXISTS idx_sessions_patient ON ecg_sessions(patient_id);
CREATE INDEX IF NOT EXISTS idx_predictions_session ON arrhythmia_predictions(session_id);
