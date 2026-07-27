# End-to-End ECG Monitoring & Cardiac Event Tracking System

Real-time ECG acquisition and arrhythmia classification on an STM32N6 edge
NPU, paired with a Python/SQLite backend for logging and trend analysis of
classification results.

## Overview

This project combines embedded signal acquisition, on-device deep learning,
and a lightweight database backend into a single pipeline:

1. **Acquisition** — ECG signal captured via the ADS1292R analog front-end.
2. **On-device inference** — A 5-class 1D-CNN classifies heartbeat type in
   real time on the STM32N6's Neural-ART NPU.
3. **Emergency detection** — A parallel Pan-Tompkins + logistic regression
   pipeline flags ventricular tachycardia/fibrillation (VT/VF) with low
   latency.
4. **Logging & tracking** — A Python/SQLite backend stores every session and
   prediction, so trends per patient can be queried over time.

## Key Results

| Component | Method | Dataset | Accuracy |
|---|---|---|---|
| Heartbeat classification | 5-class 1D-CNN, INT8-quantized | MIT-BIH Arrhythmia | 96% |
| VT/VF emergency detection | Pan-Tompkins R-peak detection + logistic regression (spectral entropy features) | CinC 2015 ICU Alarm | 96% |

## Architecture

```
ADS1292R (ECG front-end)
        │
        ▼
STM32N6 microcontroller
   ├── Pan-Tompkins R-peak detection ──► Logistic Regression VT/VF classifier
   └── 1D-CNN (INT8, Neural-ART NPU) ──► 5-class heartbeat classification
        │
        ▼
Python/SQLite backend
   ├── Patients, Doctors, ECG Sessions, Arrhythmia Predictions
   └── Indexed joins + window functions (ROW_NUMBER, LAG) for per-patient trend analysis
```

## Tech Stack

- **Hardware:** ADS1292R ECG AFE, STM32N6 (Neural-ART NPU)
- **ML tooling:** ST Edge AI Core, X-CUBE-AI, INT8 quantization
- **Signal processing:** Pan-Tompkins R-peak detection, spectral entropy features
- **Backend:** Python, SQLite (parameterized queries, indexed FK joins, window functions)

## Repository Structure

```
├── firmware/           # STM32N6 embedded application
├── model/              # 1D-CNN training + quantization scripts
├── vt_vf_classifier/    # Pan-Tompkins + logistic regression pipeline
├── patient_tracker/     # Python/SQLite backend (schema, CRUD, insight queries)
│   ├── schema.sql
│   ├── db.py
│   ├── seed.py
│   ├── crud.py
│   ├── queries.py
│   └── main.py
└── README.md
```

## Getting Started (patient_tracker backend)

```bash
cd patient_tracker
python3 db.py      # create the database from schema.sql
python3 seed.py     # populate with sample data
python3 main.py      # run the CLI (login: doc1 / pass123)
```

## Datasets

- [MIT-BIH Arrhythmia Database](https://physionet.org/content/mitdb/) — heartbeat classification
- [CinC Challenge 2015 — ICU Cardiac Arrhythmia Alarms](https://physionet.org/content/challenge-2015/) — VT/VF detection

## Future Work

- Extend the backend with a lightweight REST API (FastAPI) for remote access.
- Add over-the-air model update support for the deployed NPU model.
- Expand the classifier to detect additional arrhythmia classes.

## License

MIT
