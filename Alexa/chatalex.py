import pywhatkit
import wikipedia
import pyjokes

def run_alexa():
    command = input("You: ").lower().strip()
    if not command.startswith("alexa"):
        print("Sorry, I don't understand your command.")
        return
    if "alexa play" in command:
        song = command.replace("alexa play", "").strip()
        print("Alexa is Playing: " + song)
        pywhatkit.playonyt(song)
    elif "alexa who is" in command:
        person = command.replace("alexa who is", "").strip()
        try:
            info = wikipedia.summary(person, 2)
            print(info)
        except:
            print("Sorry, I could not find any information about", person)
    elif "alexa tell me a joke" in command:
        joke = pyjokes.get_joke(language="en")
        print(joke)
    else:
        print("Alexa: Bruh")


print("Alexa: Hi! I am your chatbot assistant. Please your commands starting with my name, 'Alexa'")

while True:
    run_alexa()