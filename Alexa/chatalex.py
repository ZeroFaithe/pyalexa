import pywhatkit
import wikipedia
import pyjokes
import speech_recognition as sr
from prompt_toolkit import prompt
from datetime import datetime
import time
import threading

user_name = input("\nAlexa: Hello! What's your name? ").strip()

hr = datetime.now().strftime("%H")
minute = datetime.now().strftime("%M")
date = datetime.now().strftime("%m/%d/%Y")

recognizer = sr.Recognizer()
mic = sr.Microphone()

# Threads :>
timer_thread = None
timer_event = threading.Event()


def listen_for_wake_word(wake_word="alexa"):
    print(f"\nAlexa: Try saying {wake_word} to record your command!")
    while True:
        with mic as source:
            audio = recognizer.listen(source, phrase_time_limit=3)
        try:
            text = recognizer.recognize_google(audio).lower()
            if wake_word in text:
                return
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print(f"API error: {e}")
            break


def listen_for_command():
    print("\nAlexa: Hm?\n")
    with mic as source:
        audio = recognizer.listen(source, phrase_time_limit=5)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Alexa: Sorry I could not understand the audio.")
        return "alexa"
    except sr.RequestError as e:
        print(f"API error: {e}")
        return ""


def get_command(user_name):
    user_typed = prompt(f"{user_name}: ").strip()

    if user_typed:
        return user_typed.lower()

    else:
        listen_for_wake_word("alexa")
        recognized_text = listen_for_command()

        if not recognized_text:
            print("No speech command detected, please try again.\n")
            return ""

        edited_command = prompt(f"{user_name}: ", default="alexa " + recognized_text)
        return edited_command.lower().strip()


def run_timer(duration, unit="minutes"):
    # Function to handle timer logic in a separate thread
    print(f"\nAlexa: Setting a timer for {duration} {unit}...\n")

    timer_event.clear()  # Reset the event

    # Convert minutes to seconds or retain seconds and wait
    if unit == "minutes":
        duration_in_seconds = duration * 60
    else:
        duration_in_seconds = duration

    for remaining in range(duration_in_seconds, 0, -1):
        if timer_event.is_set():
            time.sleep(1)
            print("\nAlexa: Timer was cancelled!")
            return True
        time.sleep(1)

    print(f"\nAlexa: Time's up! {user_name}, your timer of {duration} {unit} has expired!\n")
    return True


def cancel_timer():
    global timer_event
    timer_event.set()


def run_alexa():
    global timer_thread
    command = get_command(user_name)

    if not command.startswith("alexa"):
        print(
            "Null Entity from the Depths: Sorry, I don't understand your command. Please insert Alexa first to avoid disturbing my slumber.\n")
        return True

    if "alexa play" in command:
        song = command.replace("alexa play", "").strip()
        print("Alexa is Playing: " + song)
        pywhatkit.playonyt(song)
        return True

    elif "alexa hello" in command:
        print(f"Alexa: Hi {user_name}! ^ v ^")
        return True

    elif "alexa how are you doing" in command:
        print(f"Alexa: I am feeling wonderful right now!")
        return True

    elif "alexa help" in command:
        print("\nAlexa Commands:\n" \
              "what time is it - Asks Alexa for the time\n" \
              "what date is it - Asks Alexa for the date\n" \
              "play (music/video name) - Opens YouTube to play your input\n" \
              "who is (person name) - Outputs the summary of the person's biography\n" \
              "tell me a joke - Alexa tells you a bad joke!\n" \
              "calculate - Alexa calculates the basic expression you give\n" \
              "set a timer for (minutes/seconds) - Sets a timer\n" \
              "cancel timer - Cancels the timer\n" \
              "bye - Shuts down Alexa\n")
        return True

    elif "alexa what time is it" in command:
        if int(hr) > 12:
            h = int(hr) - 12
            print(f"It is {h}:{minute} PM\n")
        elif int(hr) == 0:
            h = int(hr) + 12
            print(f"It is {h}:{minute} AM\n")
        else:
            print(f"It is {hr}:{minute} AM\n")
        return True

    elif "alexa what date is it" in command:
        print(f"It is {date} today.\n")
        return True

    elif "alexa what is" in command:
        thing = command.replace("alexa what is", "").strip()
        results = wikipedia.search(thing)

        if not results:
            print("Sorry, I do not know what is ", thing, "\n")
            return True

        elif len(results) == 1:
            info = wikipedia.summary(results[0], sentences=2)
            print(info)
            return True

        else:
            print("\nHere are the results:")
            for i, result in enumerate(results, 1):
                print(f"{i}. {result}")

            choice = input("\nWhich one do you refer to? Pick a number (or press Enter to cancel): ").strip()

            if not choice: # Cancels if user presses Enter
                print("Cancelled.")
                return True

            try:
                choice_index = int(choice) - 1
                if 0 <= choice_index < len(results):
                    selected_title = results[choice_index]
                    info = wikipedia.summary(selected_title, sentences = 3, auto_suggest = False, redirect = True) # Turned off auto_suggest cuz it does not return exact result
                    print(f"\n{info}\n")
                    return True

                else:
                    print("Invalid choice number. \n")
                    return True

            except ValueError:
                print("Please enter a valid number. \n")
                return True

    elif "alexa who is" in command:
        person = command.replace("alexa who is", "").strip()
        results = wikipedia.search(person)

        if not results:
            print("Sorry, I do not know a person named:", person, "\n")
            return True

        elif len(results) == 1:
            info = wikipedia.summary(results[0], sentences=2)
            print(info)
            return True

        else:
            print("\nHere are the results:")
            for i, result in enumerate(results, 1):
                print(f"{i}. {result}")

            choice = input("\nWhich one do you refer to? Pick a number (or press Enter to cancel): ").strip()

            if not choice:  # Cancels if user presses Enter
                print("Cancelled.")
                return True

            try:
                choice_index = int(choice) - 1
                if 0 <= choice_index < len(results):
                    selected_title = results[choice_index]
                    info = wikipedia.summary(selected_title, sentences=3, auto_suggest=False, redirect=True)  # Turned off auto_suggest cuz it does not return exact result
                    print(f"\n{info}\n")
                    return True

                else:
                    print("Invalid choice number. \n")
                    return True

            except ValueError:
                print("Please enter a valid number. \n")
                return True

    elif "alexa tell me a joke" in command:
        joke = pyjokes.get_joke(language="en")
        print(f"{joke}\n")
        return True

    elif "alexa bye" in command:
        print(f"\nAlexa: Goodbye {user_name}! Feel free to use my services again!\n")
        return False

    elif "alexa calculate" in command:
        command = command.replace("alexa calculate ", "")
        calc = command.split()
        if len(calc) == 3:
            try:
                numb1 = float(calc[0])
                operator = calc[1]
                numb2 = float(calc[2])

                if operator == "+":
                    result = numb1 + numb2
                elif operator == "-":
                    result = numb1 - numb2
                elif operator == "*":
                    result = numb1 * numb2
                elif operator == "/":
                    result = numb1 / numb2
                else:
                    raise ValueError

                print(f"\nAlexa: The answer for {numb1} {operator} {numb2} is {result}\n")
                return True
            except:
                print("Please enter a valid expression. \n")

    elif "alexa set a timer for" in command:
        try:
            if "minutes" in command:
                minutes = int(command.replace("alexa set a timer for", "").strip().replace("minutes", "").strip())
                if timer_thread and timer_thread.is_alive():
                    print("Alexa: A timer is already running.")
                else:
                    timer_thread = threading.Thread(target=run_timer, args=(minutes, "minutes"))
                    timer_thread.start()
                return True

            elif "seconds" in command:
                seconds = int(command.replace("alexa set a timer for", "").strip().replace("seconds", "").strip())
                if timer_thread and timer_thread.is_alive():
                    print("Alexa: A timer is already running.")
                else:
                    timer_thread = threading.Thread(target=run_timer, args=(seconds, "seconds"))
                    timer_thread.start()
                return True

        except ValueError:
            print("Alexa: Sorry, I could not understand the timer duration.\n")
            return True

    elif "alexa cancel timer" in command:
        if timer_thread and timer_thread.is_alive():
            cancel_timer()
        else:
            print("Alexa: No timer is running to cancel.\n")
        return True

    else:
        print("Alexa: What do you mean by that?\n")
        return True


while True:
    if not run_alexa():
        break
