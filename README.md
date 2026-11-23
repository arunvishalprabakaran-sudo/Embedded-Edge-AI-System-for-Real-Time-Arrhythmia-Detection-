Drone Based ECG Arrhythmia Assessment System Using Edge AI

## Project Overview

This project focuses on developing an AI-powered ECG Arrhythmia Assessment System by integrating electronic hardware, embedded systems and machine learning.

The system uses an ADS1292R ECG acquisition module interfaced with a Raspberry Pi 4 to acquire ECG signals. The acquired signals are processed using digital signal processing techniques and classified using machine learning models deployed on the Raspberry Pi.

The system provides ECG waveform visualization, cardiac rhythm classification and shockability assessment through a graphical user interface.

## Hardware Components

| Component | Purpose |
|---|---|
| Raspberry Pi 4 | Main processing and control unit |
| ADS1292R | ECG signal acquisition and analog front-end |
| ECG Electrodes | Acquiring electrical cardiac signals |
| Display | Visualizing ECG waveform and classification results |
| Bluetooth Speaker | Providing voice instructions and announcements |
| Power Supply | Supplying power to the system |

## Software and Technologies

- Python
- Embedded Linux (Raspberry Pi OS)
- NumPy and SciPy
- ONNX Runtime
- Machine Learning
- Digital Signal Processing
- Tkinter GUI
- SPI Communication
- Raspberry Pi GPIO
- Pytest

## Hardware Implementation

- Interfaced the ADS1292R ECG front-end with Raspberry Pi 4 using SPI communication.
- Configured GPIO pins for sensor control and data acquisition.
- Acquired ECG signals through the ECG electrodes.
- Integrated a display for real-time system interaction.
- Integrated Bluetooth audio output for voice assistance.

## Software Implementation

- Developed Python modules for ECG acquisition and signal processing.
- Implemented digital filtering to reduce baseline wander and power-line interference.
- Developed signal quality assessment and feature extraction modules.
- Integrated trained machine learning models using ONNX Runtime.
- Developed a graphical user interface using Tkinter.
- Implemented voice-based instructions and classification announcements.

## System Working

1. ECG electrodes capture the electrical activity of the heart.
2. ADS1292R acquires and converts the ECG signal into digital data.
3. Raspberry Pi receives the acquired signal through SPI communication.
4. The software performs filtering and preprocessing.
5. The processed ECG signal is passed to the machine learning pipeline.
6. AI models classify the cardiac rhythm and assess shockability.
7. The ECG waveform and classification results are displayed on the interface.
8. Voice assistance provides instructions and announces the results.

## Machine Learning Models

Three ONNX models are integrated into the system:

| Model | Function |
|---|---|
| Shockability Classifier | Identifies shockable and non-shockable rhythms |
| Arrhythmia Classifier | Performs multiclass ECG rhythm classification |
| VF/VT Classifier | Distinguishes Ventricular Fibrillation and Ventricular Tachycardia |

## System Workflow

```text
       ECG Electrodes
              |
              v
         ADS1292R
        ECG Sensor
              |
          SPI Interface
              |
              v
        Raspberry Pi 4
              |
       ECG Signal Processing
              |
       Signal Preprocessing
              |
       Feature Extraction
              |
       Machine Learning
              |
       Rhythm Classification
              |
       Shockability Assessment
              |
       +------+------+
       |             |
       v             v
   ECG Display    Voice Output
       |
       v
  Classification Result
```

## Key Features

- Hardware and software integration.
- ECG signal acquisition using ADS1292R.
- SPI-based sensor interfacing.
- Digital signal filtering and preprocessing.
- AI-based ECG rhythm classification.
- Shockable and non-shockable rhythm assessment.
- Raspberry Pi-based edge AI processing.
- Graphical ECG visualization.
- Voice-assisted user interaction.
- Local processing without cloud dependency.

## Applications

- Academic research in biomedical instrumentation.
- Embedded AI-based ECG monitoring.
- Edge computing in healthcare applications.
- Experimental cardiac rhythm assessment systems.

## Future Enhancements

- Integration with drone-based remote monitoring systems.
- Wireless ECG data transmission.
- Improved classification using advanced deep learning models.
- Integration with additional biomedical sensors.
- Optimization for portable embedded medical monitoring platforms.

## Disclaimer

This project is an academic research prototype developed for educational purposes. It is not a certified medical device and must not be used as a replacement for professional medical diagnosis or treatment.

## Author

**Electronics and Instrumentation Engineering**

Hardware | Embedded Systems | Signal Processing | Edge AI | Machine Learning
