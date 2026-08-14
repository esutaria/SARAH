# S.A.R.A.H.

### Safety Assistant for Real-time Awareness and Hazard Detection

A multimodal AI assistive system combining real-time environmental
hazard detection with a voice-controlled visual assistant for people
with visual impairments.

## 🎥 Demo

[![Watch the S.A.R.A.H. Prototype Demo](https://img.youtube.com/vi/WMObGMByjl4/maxresdefault.jpg)](https://youtu.be/WMObGMByjl4)

**[▶ Watch the full S.A.R.A.H. prototype demo on YouTube →](https://youtu.be/WMObGMByjl4)**

## The Problem

White canes are inexpensive and reliable mobility aids, but cannot
detect many hazards above ground level and provide limited information
about a user's surrounding environment. Thus the preferred assistance form 
for the visually impaired community is sighted guides, but they can be 
difficult to have around 24/7 and very expensive to hire.

S.A.R.A.H. explores whether a visual-language model can augment a
traditional white cane by providing in one system the two capabilities that 
give sighted guides the biggest advantage:

1. Proactive hazard detection
2. On-demand environmental assistance

## How It Works

Camera → OpenCV → Gemini 2.0 Flash
                     ↓
              ┌──────────────┐
              │              │
        Hazard Monitor   Voice Assistant
              │              │
              └──────┬───────┘
                     ↓
                Text-to-Speech

The hazard pipeline periodically analyzes the user's surroundings and
announces relevant obstacles.

When the user says "Sarah," the conversational pipeline receives
priority, captures the current camera frame, and answers questions
about the environment.

## Engineering Challenge: Managing Competing Audio

One of the largest implementation challenges was allowing an
on-demand voice query to interrupt continuous hazard announcements.

The prototype uses concurrent speech recognition and environmental
monitoring, with explicit control over text-to-speech execution so
user questions can take priority over background hazard detection.

## Evaluation

The prototype was evaluated through a preliminary three-person pilot
study across indoor and outdoor environments.

Evaluation categories included:

- Head-level hazards
- Body-level hazards
- Floor-level hazards
- Landmark identification
- Environmental Q&A
- Text reading
- False positives
- False negatives

The system received scores of at least 4/5 across hazard-detection
categories. False positives emerged as the primary area requiring
future improvement.

> This was a small exploratory pilot and did not include visually
> impaired participants. Results should not be interpreted as a
> clinical or safety validation.

## Tech Stack

Python · OpenCV · Gemini 2.0 Flash · SpeechRecognition · pyttsx3 ·
Multithreading

## Research

S.A.R.A.H. was developed as part of an independent research project
with mentorship from Dr. Nakul Gopalan, an assistant professor at
Arizona State University's School of Computing and Augmented Intelligence.

The project included literature review, system design, implementation,
prompt engineering, prototype testing, and evaluation.

## Future Work

- Reduce unnecessary hazard alerts
- Add depth-aware spatial reasoning
- Personalize alerts based on user preferences
- Move inference onto portable hardware
- Add offline functionality
- Conduct accessibility testing with visually impaired participants
