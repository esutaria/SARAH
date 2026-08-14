# System Architecture

S.A.R.A.H. combines continuous environmental monitoring with an on-demand multimodal voice assistant.

## High-Level Flow

```text
Camera
  |
  v
OpenCV Frame Capture
  |
  +----------------------+
  |                      |
  v                      v
Hazard Detection     Voice Assistant
  |                      |
  v                      v
Gemini Vision        Gemini Vision
  |                      |
  v                      v
Hazard Alert         Contextual Answer
  |                      |
  +----------+-----------+
             |
             v
        Text-to-Speech
             |
             v
            User
