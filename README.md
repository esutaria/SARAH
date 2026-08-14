# S.A.R.A.H.

**Safety Assistant for Real-time Awareness and Hazard Detection**

S.A.R.A.H. is a prototype assistive system that combines computer vision, multimodal AI, speech recognition, and text-to-speech to help visually impaired users understand their surroundings.

The system continuously analyzes camera input for potential hazards while also supporting voice-activated environmental questions.

## Features

- Continuous camera-based hazard monitoring
- Detection of floor-level and head-level obstacles
- Spoken hazard alerts
- Voice-activated environmental questions
- Multimodal Gemini vision integration
- Conversational context across user interactions
- Concurrent speech recognition, AI inference, and text-to-speech

## Tech Stack

- Python
- OpenCV
- Google Gemini
- SpeechRecognition
- pyttsx3
- Multithreading

## Project Status

This repository contains a reconstructed version of the original S.A.R.A.H. research prototype.

The original system was developed using a borrowed ZED2 camera. Because the original hardware environment is no longer available, the reconstructed implementation has not been fully revalidated on the original device.

## Documentation

- [System Architecture](docs/architecture.md)
- [Limitations](docs/limitations.md)

## Future Work

Potential improvements include structured hazard detection outputs, depth-aware obstacle localization, improved concurrency handling, model confidence calibration, latency optimization, and systematic evaluation. The end goal is for S.A.R.A.H. to act as a cheaper, always available, extremely reliable alternative to a sighted guide.
