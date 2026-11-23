# Patient Records & ECG Session Tracker

A Python + SQLite CLI application that logs and queries arrhythmia classification
results from an embedded ECG monitoring system, built to connect
the biomedical embedded work with a database-backed software project.

## Setup

```bash
python3 db.py      # creates patient_tracker.db from schema.sql
python3 seed.py     # fills it with realistic fake data
python3 main.py      # run the app — login with doc1 / pass123
```

## Files

| File | Purpose |
|---|---|
| `schema.sql` | Table definitions, foreign keys, indexes |
| `db.py` | Connection helper — the only file that touches sqlite3 directly |
| `seed.py` | Generates fake doctors/patients/sessions/predictions |
| `crud.py` | Create/Read/Update/Delete functions |
| `queries.py` | The "insight" queries — JOINs, GROUP BY, window functions |
| `main.py` | CLI menu tying it all together |

## Schema

```
doctors (1) ──< patients (1) ──< ecg_sessions (1) ──< arrhythmia_predictions
```

A doctor treats many patients. A patient has many ECG sessions over time.
Each session produces a classification prediction. Splitting sessions and
predictions into separate tables (instead of one flat table) means a session
could have zero, one, or multiple predictions — e.g. if you re-ran the model.

## Concept map (read this after you've run it)

You said you want to build first and learn the concept names afterward —
here's the map from what you just ran to what it's officially called, in the
order it'll come up in a DSA/SQL interview.

| What the code does | What it's called | Where it lives |
|---|---|---|
| `WHERE name LIKE ?` | Filtering | `crud.search_patients_by_name` |
| `INSERT ... VALUES (?, ?, ?)` | Parameterized query (prevents SQL injection) | every function in `crud.py` |
| `patient_id INTEGER PRIMARY KEY` | Primary key | `schema.sql` |
| `FOREIGN KEY (doctor_id) REFERENCES doctors` | Foreign key / referential integrity | `schema.sql` |
| `CREATE INDEX ... ON patients(doctor_id)` | Indexing | `schema.sql` — speeds up JOINs/WHERE on that column |
| `JOIN patients p ON p.doctor_id = d.doctor_id` | Inner join | `queries.patients_per_doctor` |
| `LEFT JOIN ... WHERE s.session_id IS NULL` | Left join + anti-join pattern | `queries.patients_with_no_sessions` |
| `GROUP BY d.doctor_id` | Aggregation grouping | `queries.patients_per_doctor` |
| `HAVING COUNT(*) > 1` | Post-aggregation filter (different from WHERE) | `queries.most_common_classification_overall` |
| `ROW_NUMBER() OVER (ORDER BY s.session_date)` | Window function | `queries.arrhythmia_trend_per_patient` |
| `LAG(...) OVER (...)` | Window function — looks at the previous row | same |
| Splitting sessions/predictions into two tables | Normalization | schema design |
| One `db.py` used everywhere else | Separation of concerns / DB abstraction layer | project structure |

## Talking points for interviews

- "Why did you index `patient_id` on `ecg_sessions`?" → It's the column every
  history lookup filters and joins on.
- "Why two tables instead of one for sessions and predictions?" → A session is
  a raw recording event; a prediction is a model output tied to it — kept
  separate so a session could have zero or multiple predictions.
- "Walk me through your trickiest query." → The arrhythmia trend query: it
  numbers each patient's sessions chronologically with `ROW_NUMBER()` and
  compares each classification to the previous one with `LAG()`, so a doctor
  can see whether a patient's rhythm is worsening over time.

## Known simplifications (say these out loud if asked — don't get caught off guard)

- Passwords are stored in plain text — fine for a student CLI demo, not for
  production. In a real system you'd hash with something like bcrypt.
- No input validation on dates/numbers in the CLI — a real app would validate
  before hitting the database.
