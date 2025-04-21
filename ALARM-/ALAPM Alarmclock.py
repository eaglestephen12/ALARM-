# alarm with voice command for dismiss and snooze

import time
import datetime
import pygame
import sys
import itertools
import os
from colorama import init, Fore, Back, Style
import speech_recognition as sr

# Initialize colorama
init(autoreset=True)

# === BANNER AND LOADING ANIMATION ===

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}
 █████╗ ██╗      █████╗ ██████╗ ███╗   ███╗
██╔══██╗██║     ██╔══██╗██╔══██╗████╗ ████║
███████║██║     ███████║██████╔╝██╔████╔██║
██╔══██║██║     ██╔══██║██╔═══╝ ██║╚██╔╝██║
██║  ██║███████╗██║  ██║██║     ██║ ╚═╝ ██║
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚═╝

           {Fore.YELLOW}THE ULTIMATE PYTHON ALARM
    """
    print(banner)
    print(Fore.LIGHTWHITE_EX + "⏳ Preparing the wake-up magic...\n")

def animate_loading(duration=5):
    spinner = itertools.cycle([Fore.GREEN + '|', Fore.YELLOW + '/', Fore.MAGENTA + '-', Fore.CYAN + '\\'])
    start_time = time.time()
    while time.time() - start_time < duration:
        sys.stdout.write(Fore.LIGHTBLUE_EX + f"\rStarting in {int(duration - (time.time() - start_time))}s " + next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
    print(Fore.GREEN + "\n🚀 Ready to wake you up in style!\n")
    time.sleep(1)
    clear_screen()

def listen_for_command():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print(Fore.LIGHTBLUE_EX + "🎙️ Listening for your command... (say 'snooze' or 'dismiss')")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print(Fore.YELLOW + f"👂 You said: {command}")
        return command
    except sr.UnknownValueError:
        print(Fore.RED + "🤔 Didn't catch that. Please type instead.")
        return None
    except sr.RequestError:
        print(Fore.RED + "⚠️ Voice service unavailable. Please type instead.")
        return None

# Run banner and animation
clear_screen()
show_banner()
animate_loading()

# === ALARM SETUP ===

# Get user input for the alarm
print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "Set your alarm below ⏰")
alarm_hour = int(input(Fore.LIGHTGREEN_EX + "Enter hour (1–12): "))
alarm_minute = int(input(Fore.LIGHTGREEN_EX + "Enter minute (0–59): "))
alarm_period = input(Fore.LIGHTGREEN_EX + "AM/PM: ").strip().upper()

# Convert to 24-hour format if needed
if alarm_period == "PM" and alarm_hour != 12:
    alarm_hour += 12
elif alarm_period == "AM" and alarm_hour == 12:
    alarm_hour = 0

print(Fore.YELLOW + f"\n✅ Alarm set for {alarm_hour:02d}:{alarm_minute:02d} ({alarm_period})\n")

# === ALARM LOOP ===
while True:
    now = datetime.datetime.now()
    current_hour = now.hour
    current_minute = now.minute

    print(Fore.LIGHTBLACK_EX + f"⏱️  Checking time... {current_hour:02d}:{current_minute:02d}", end='\r')

    if current_hour == alarm_hour and current_minute == alarm_minute:
        print(Fore.RED + Style.BRIGHT + "\n⏰ WAKE UP! ALARM RINGING...\n")

        # Play the alarm sound
        pygame.mixer.init()
        pygame.mixer.music.load(r"C:\Users\STEPHEN MBURU\Downloads\alarm.mp3")  # Replace with your file path
        pygame.mixer.music.play()

        # Wait for the music to finish or snooze
        while pygame.mixer.music.get_busy():
            time.sleep(1)
        pygame.mixer.music.stop()

        # === NEW: VOICE COMMAND SECTION ===
        print(Fore.CYAN + "\n🔁 Press [Enter] to dismiss, type 'snooze' or say it out loud.")

        voice_command = listen_for_command()

        if voice_command in ["snooze", "dismiss"]:
            user_choice = voice_command
        else:
            user_choice = input("👉 ").strip().lower()

        if user_choice == "snooze":
            snooze_time = datetime.datetime.now() + datetime.timedelta(minutes=5)
            alarm_hour = snooze_time.hour
            alarm_minute = snooze_time.minute
            print(Fore.YELLOW + f"\n😴 Snoozed! Next ring at {alarm_hour:02d}:{alarm_minute:02d}\n")
            continue
        else:
            print(Fore.GREEN + "\n✅ Alarm dismissed. Have a great day!\n")
            break

    time.sleep(30)
