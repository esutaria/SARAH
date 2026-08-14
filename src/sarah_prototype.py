"""
S.A.R.A.H.
Safety Assistant for Real-time Awareness and Hazard Detection

Reconstructed prototype based on the original research implementation.

The original prototype combined:
- camera-based environmental analysis
- multimodal Gemini inference
- continuous hazard alerts
- voice-activated environmental questions
- text-to-speech output

This reconstructed version may differ from the final hardware-tested
implementation because the original source repository and ZED2 hardware
environment are no longer available.
"""

import os
import time
import threading

import cv2
import pyttsx3
import speech_recognition as sr
from google import genai
from google.genai import types


# ---------------------------------------------------------------------------
# Gemini configuration
# ---------------------------------------------------------------------------

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    raise EnvironmentError(
        "GEMINI_API_KEY environment variable is not set."
    )

# The original prototype used separate clients for hazard detection and
# conversational assistance. Both now use the same securely stored API key.
hazard_client = genai.Client(api_key=API_KEY)
voice_client = genai.Client(api_key=API_KEY)


# ---------------------------------------------------------------------------
# Camera setup
# ---------------------------------------------------------------------------

camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)

if not camera.isOpened():
    print("Error: Unable to access the camera.")
    raise SystemExit

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

ret, frame = camera.read()

if ret:
    h, w, _ = frame.shape

    # The original ZED2 prototype used one half of the stereo image.
    left_image = cv2.flip(frame[:, : w // 2], 1)
    cv2.imshow("Live Feed", left_image)


# ---------------------------------------------------------------------------
# Speech setup
# ---------------------------------------------------------------------------

recognizer = sr.Recognizer()

engine = pyttsx3.init()
hazard_engine = pyttsx3.init()

voices = engine.getProperty("voices")

if voices:
    engine.setProperty("voice", voices[0].id)

    if len(voices) > 1:
        hazard_engine.setProperty("voice", voices[1].id)

engine.setProperty("rate", 200)
hazard_engine.setProperty("rate", 150)


# ---------------------------------------------------------------------------
# Runtime state
# ---------------------------------------------------------------------------

speaking = True
run = True

exit_words = ["exit", "stop", "quit", "bye", "goodbye"]
full_exit_phrase = "done"
wake_word = "sarah"

conversation_context = {}


# ---------------------------------------------------------------------------
# Camera helpers
# ---------------------------------------------------------------------------

def image_from_camera():
    """
    Capture the current camera frame and return it as JPEG bytes.

    The original ZED2 setup exposed a stereo frame, so this prototype uses
    the left half of the captured image.
    """

    ret, frame = camera.read()

    if not ret:
        print("Error: Unable to read from camera.")
        return None

    h, w, _ = frame.shape
    left_image = frame[:, : w // 2]

    cv2.imshow("Live Feed", left_image)

    success, encoded_image = cv2.imencode(".jpg", left_image)

    if not success:
        print("Error: Could not encode frame.")
        return None

    return encoded_image.tobytes()


# ---------------------------------------------------------------------------
# Conversational assistant
# ---------------------------------------------------------------------------

def get_response(user_input, image_bytes):
    """
    Ask Gemini to answer a user's spoken question using the current camera
    frame and limited conversational context.
    """

    print("Starting conversational request.")

    try:
        prompt = (
            f"Previous context: {conversation_context}. "
            "Keep your response concise and answer questions for a visually "
            f"impaired person: {user_input}"
        )

        response = voice_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                prompt,
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type="image/jpeg",
                ),
            ],
        )

        return response.text

    except Exception as exc:
        print(f"Error in get_response: {exc}")
        return "I encountered an error processing your request."


# ---------------------------------------------------------------------------
# Text-to-speech
# ---------------------------------------------------------------------------

def run_speech():
    """
    Run conversational text-to-speech.

    A separate thread allows the main application to avoid blocking
    indefinitely if the speech engine hangs.
    """

    try:
        engine.runAndWait()

    except Exception as exc:
        print(f"Speech engine error: {exc}")


# ---------------------------------------------------------------------------
# Speech recognition
# ---------------------------------------------------------------------------

def recognize_speech():
    """
    Continuously listen for the S.A.R.A.H. wake word.

    When detected, capture the current environment and send both the image
    and spoken input to Gemini.
    """

    global speaking, run

    with sr.Microphone() as source:
        print("Listening for 'Sarah'...")

        while run:
            try:
                audio = recognizer.listen(source, timeout=1)
                text = recognizer.recognize_google(audio)

                print(f"You said: {text}")

                normalized_text = text.lower()

                if "sarah" in normalized_text or "sara" in normalized_text:
                    print("Wake word detected.")

                    speaking = False

                    image_bytes = image_from_camera()

                    if image_bytes is None:
                        continue

                    response_from_gemini = get_response(
                        text,
                        image_bytes,
                    )

                    print(f"SARAH: {response_from_gemini}")

                    # The original implementation manually stopped an
                    # existing speech loop before beginning a new response.
                    if engine._inLoop:
                        engine.endLoop()

                    engine.say(response_from_gemini)

                    words = response_from_gemini.split()
                    num_words = max(len(words), 1)

                    speech_thread = threading.Thread(
                        target=run_speech,
                        daemon=True,
                    )

                    speech_thread.start()

                    # Approximation used in the original prototype to prevent
                    # speech synthesis from hanging indefinitely.
                    timeout = 160 / num_words

                    print(f"Speech timeout set to {timeout:.2f} seconds.")

                    speech_thread.join(timeout=timeout)

                    conversation_context["last_user_input"] = text
                    conversation_context["last_gemini_response"] = (
                        response_from_gemini
                    )

                    speaking = True

                    print("Finished speaking.")

                if full_exit_phrase in normalized_text:
                    print("Stopping program.")

                    speaking = False
                    run = False
                    break

            except sr.WaitTimeoutError:
                pass

            except sr.UnknownValueError:
                print("Could not understand audio.")

            except sr.RequestError as exc:
                print(
                    "Could not request results from Google Speech "
                    f"Recognition service: {exc}"
                )


# ---------------------------------------------------------------------------
# Hazard detection
# ---------------------------------------------------------------------------

def hazard_api_call(image_bytes):
    """
    Send the current camera frame to Gemini for environmental hazard analysis.
    """

    try:
        print("Running hazard analysis.")

        response = hazard_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                (
                    "Very concisely describe hazards and obstacles for a "
                    "visually impaired person in this image. Head-level and "
                    "floor-level obstacles should definitely be included. "
                    "Also say where they are in relation to the user who is "
                    "holding the camera. Just say 'no hazards' if you don't "
                    "see any hazardous ones."
                ),
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type="image/jpeg",
                ),
            ],
        )

        return response

    except Exception as exc:
        return exc


def speak_hazard():
    """
    Capture the environment, detect hazards, and announce them aloud.
    """

    global speaking

    image_bytes = image_from_camera()

    if not image_bytes:
        return

    response = hazard_api_call(image_bytes)

    if isinstance(response, Exception):
        print(f"Hazard analysis error: {response}")
        return

    hazard_message = response.text.strip()

    print(f"Hazard analysis: {hazard_message}")

    if (
        not hazard_message
        or "no hazards" in hazard_message.lower()
        or "none" in hazard_message.lower()
    ):
        return

    words = hazard_message.split()

    if not speaking:
        return

    hazard_engine.say("Hazard Alert")

    print(f"Hazard alert: {hazard_message}")

    for word in words:
        if hazard_engine._inLoop:
            hazard_engine.endLoop()

        if not speaking:
            return

        hazard_engine.say(word)

        hazard_thread = threading.Thread(
            target=hazard_engine.runAndWait,
            daemon=True,
        )

        hazard_thread.start()

        # Approximate timeout preserved from the recovered prototype.
        hazard_thread.join(timeout=len(word) * 0.1)


# ---------------------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------------------

def main():
    global run

    speech_thread = threading.Thread(
        target=recognize_speech,
        daemon=True,
    )

    speech_thread.start()

    try:
        while run:
            speak_hazard()

            # Continuously scan the environment approximately every 2 seconds.
            time.sleep(2)

            # Allows the OpenCV preview window to update.
            cv2.waitKey(1)

    except KeyboardInterrupt:
        print("Program interrupted.")

    finally:
        run = False

        camera.release()
        cv2.destroyAllWindows()

        print("Program finished.")


if __name__ == "__main__":
    main()
