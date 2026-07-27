"""
seed.py
Populates the database with realistic fake data so the app isn't empty on demo day.
Run: python seed.py
"""

import random
from datetime import datetime, timedelta
from db import get_connection, init_db

FIRST_NAMES = ["Aarav", "Diya", "Kabir", "Meera", "Rohan", "Ananya", "Vikram",
               "Sneha", "Arjun", "Priya", "Karthik", "Lakshmi", "Nikhil", "Divya"]
LAST_NAMES = ["Sharma", "Iyer", "Reddy", "Nair", "Menon", "Rao", "Gupta",
              "Krishnan", "Pillai", "Verma"]
SPECIALIZATIONS = ["Cardiology", "General Medicine", "Internal Medicine"]
DEVICE_IDS = ["STM32-ECG-01", "STM32-ECG-02", "STM32-ECG-03"]
CLASSIFICATIONS = ["Normal", "AFib", "PVC", "Tachycardia", "Bradycardia"]


def random_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def random_date(start_year=1950, end_year=2005):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))


def seed():
    init_db()
    conn = get_connection()
    cur = conn.cursor()

    # Clear existing data (so you can re-run this safely while testing)
    for table in ["arrhythmia_predictions", "ecg_sessions", "patients", "doctors"]:
        cur.execute(f"DELETE FROM {table}")

    # --- Doctors ---
    doctor_ids = []
    for i in range(4):
        cur.execute(
            "INSERT INTO doctors (name, specialization, username, password) VALUES (?, ?, ?, ?)",
            (f"Dr. {random_name()}", random.choice(SPECIALIZATIONS), f"doc{i+1}", "pass123")
        )
        doctor_ids.append(cur.lastrowid)

    # --- Patients ---
    patient_ids = []
    for _ in range(20):
        cur.execute(
            "INSERT INTO patients (name, dob, gender, doctor_id) VALUES (?, ?, ?, ?)",
            (
                random_name(),
                random_date().strftime("%Y-%m-%d"),
                random.choice(["M", "F"]),
                random.choice(doctor_ids),
            )
        )
        patient_ids.append(cur.lastrowid)

    # --- ECG sessions + predictions ---
    for patient_id in patient_ids:
        num_sessions = random.randint(2, 5)
        session_date = datetime.now() - timedelta(days=random.randint(30, 200))
        for _ in range(num_sessions):
            session_date += timedelta(days=random.randint(5, 30))
            cur.execute(
                "INSERT INTO ecg_sessions (patient_id, session_date, device_id, duration_sec) "
                "VALUES (?, ?, ?, ?)",
                (patient_id, session_date.strftime("%Y-%m-%d %H:%M:%S"),
                 random.choice(DEVICE_IDS), random.randint(30, 300))
            )
            session_id = cur.lastrowid

            cur.execute(
                "INSERT INTO arrhythmia_predictions (session_id, classification, confidence, predicted_at) "
                "VALUES (?, ?, ?, ?)",
                (session_id, random.choice(CLASSIFICATIONS),
                 round(random.uniform(0.55, 0.99), 2),
                 session_date.strftime("%Y-%m-%d %H:%M:%S"))
            )

    conn.commit()
    conn.close()
    print(f"Seeded {len(doctor_ids)} doctors and {len(patient_ids)} patients with ECG sessions.")


if __name__ == "__main__":
    seed()
