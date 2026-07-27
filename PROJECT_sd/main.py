"""
main.py
The CLI menu that ties everything together. Run: python main.py
"""

from datetime import datetime
from db import get_connection, init_db
import crud
import queries


def login():
    print("\n--- Doctor Login ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    conn = get_connection()
    row = conn.execute(
        "SELECT doctor_id, name FROM doctors WHERE username = ? AND password = ?",
        (username, password)
    ).fetchone()
    conn.close()
    if row:
        print(f"\nWelcome, {row['name']}.")
        return row["doctor_id"]
    print("Invalid login. (Try doc1 / pass123 from seed data.)")
    return None


def print_rows(rows, headers):
    if not rows:
        print("  (no results)")
        return
    print("  " + " | ".join(headers))
    for r in rows:
        print("  " + " | ".join(str(v) for v in r))


def menu():
    while True:
        print("""
--- Patient Tracker ---
1. Add patient
2. Log ECG session (+ optional prediction)
3. View patient history
4. Search patient by name
5. Patients per doctor (insight)
6. Low-confidence predictions (insight)
7. Arrhythmia trend for a patient (window function insight)
8. Patients with no sessions yet (insight)
0. Exit
""")
        choice = input("Choose: ").strip()

        if choice == "1":
            name = input("Patient name: ")
            dob = input("DOB (YYYY-MM-DD): ")
            gender = input("Gender (M/F): ")
            doctor_id = input("Doctor ID: ")
            pid = crud.add_patient(name, dob, gender, doctor_id)
            print(f"Added patient #{pid}")

        elif choice == "2":
            patient_id = input("Patient ID: ")
            device_id = input("Device ID (e.g. STM32-ECG-01): ")
            duration = input("Duration (sec): ")
            classification = input("Classification (blank to skip): ") or None
            confidence = input("Confidence 0-1 (blank to skip): ") or None
            sid = crud.log_ecg_session(
                patient_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                device_id, int(duration), classification,
                float(confidence) if confidence else None
            )
            print(f"Logged session #{sid}")

        elif choice == "3":
            patient_id = input("Patient ID: ")
            rows = crud.get_patient_history(patient_id)
            print_rows(rows, ["session_id", "date", "device", "duration", "classification", "confidence"])

        elif choice == "4":
            keyword = input("Name contains: ")
            rows = crud.search_patients_by_name(keyword)
            print_rows(rows, ["id", "name", "dob", "gender"])

        elif choice == "5":
            print_rows(queries.patients_per_doctor(), ["doctor", "num_patients"])

        elif choice == "6":
            rows = queries.low_confidence_predictions(0.7)
            print_rows(rows, ["patient", "date", "classification", "confidence"])

        elif choice == "7":
            patient_id = input("Patient ID: ")
            rows = queries.arrhythmia_trend_per_patient(patient_id)
            print_rows(rows, ["session_no", "date", "classification", "confidence", "previous"])

        elif choice == "8":
            print_rows(queries.patients_with_no_sessions(), ["name"])

        elif choice == "0":
            print("Bye.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    init_db()
    print("Database ready. (Run seed.py first if this is your first time.)")
    doctor_id = login()
    if doctor_id:
        menu()
