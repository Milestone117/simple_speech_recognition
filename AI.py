import os
import time
from pdfminer.high_level import extract_text
import pygame
import speech_recognition as sr
import pyttsx3

# File Extensions Constants
PDF_EXT = '.pdf'
VIDEO_EXTS = ['.mp4', '.avi']

# Initialize Pygame for Video Playback
pygame.init()

# Initialize Speech Recognition
recognizer = sr.Recognizer()

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    print(voice.name)

def parse_document(file_path):
    # Extract text content from the document
    text = extract_text(file_path)
    # Process the extracted text as needed
    # ...
    print(f"Document parsed: {file_path}")
    print("Text Content:")
    print(text)


def play_video(file_path):
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Video Player")
    clock = pygame.time.Clock()

    video = pygame.movie.Movie(file_path)
    video_screen = pygame.Surface(video.get_size()).convert()
    video.set_display(video_screen)

    video.play()

    while video.get_busy():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                video.stop()
                pygame.quit()
                return

        screen.blit(video_screen, (0, 0))
        pygame.display.update()
        clock.tick(60)


def handle_user_input():
    while True:
        print("Please select an option:")
        print("1. Parse a document")
        print("2. Play a video")
        print("3. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            file_path = input("Enter the path to the document: ")
            file_extension = os.path.splitext(file_path)[1].lower()

            if file_extension == PDF_EXT:
                parse_document(file_path)
            else:
                print("Unsupported file format. Please provide a PDF document.")

        elif choice == '2':
            file_path = input("Enter the path to the video: ")
            file_extension = os.path.splitext(file_path)[1].lower()

            if file_extension in VIDEO_EXTS:
                play_video(file_path)
            else:
                print("Unsupported file format. Please provide an MP4 or AVI video.")

        elif choice == '3':
            print("Quitting the program...")
            break

        else:
            print("Invalid choice. Please try again.")


def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")

        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"Recognized speech: {text}")
        return text

    except sr.UnknownValueError:
        print("Unable to recognize speech.")
        return ""

    except sr.RequestError as e:
        print(f"Speech recognition error: {str(e)}")
        return ""


def speak(text):
    engine.say(text)
    engine.runAndWait()


def activate_assistant():
    print("Listening for wake-up phrase...")

    while True:
        text = recognize_speech()

        if "hi Liam" in text.lower():
            print("Assistant activated.")
            speak("How can I assist you?")
            handle_user_input()

        elif "thank you Liam" in text.lower():
            print("Assistant deactivated.")
            speak("You're welcome!")
            break


# Main Execution
activate_assistant()
