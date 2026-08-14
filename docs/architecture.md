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
```
## Hazard Detection Pipeline

The application periodically captures an image from the camera and sends it to a multimodal model with instructions to identify potentially hazardous obstacles to a visually impaired user, including floor-level and head-level hazards.

Detected hazards are converted to spoken alerts.

## Voice Assistant Pipeline

Speech recognition runs concurrently with hazard monitoring.

When the user says the wake word "Sarah," the application captures the current camera frame and combines it with the user's spoken question. Gemini then generates a concise environment-aware response that is spoken back to the user.

## Concurrency

The prototype used Python threads to prevent speech recognition and text-to-speech from completely blocking environmental monitoring. The voice assistant feature is meant to override any hazards that are being stated when the user begins speaking to SARAH.

This was one of the major engineering challenges of the project because several asynchronous activities needed access to the same audio and camera resources.
