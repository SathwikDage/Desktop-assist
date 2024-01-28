import pyttsx3
import speech_recognition as sr
from googlesearch import search
from bs4 import BeautifulSoup
import requests
import json

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def wish():
    speak("Hello Sir, how can I help you")

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    while True:
        print("Please say something....")
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Please say something....")
                speak("Please say something")
                audio = r.listen(source, timeout=10)
                text = r.recognize_google(audio)
                print(f"Recognized text: {text.lower()}")
                return text.lower()
        except sr.UnknownValueError:
            print("Cannot understand audio")
            speak("Sorry, I couldn't understand. Please try again.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            speak("There was an error. Please try again later.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            speak("An unexpected error occurred. Please try again.")

def takeSpeechInput():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak something:")
        speak("Speak something")
        audio_data = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio_data).lower()
        return query
    except sr.UnknownValueError:
        print("Sorry, could not understand the audio. Please try again.")
        speak("Sorry, could not understand the audio. Please try again.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        speak("There was an error. Please try again later.")
        return None

def getWeatherInfo():
    r = sr.Recognizer()
    speak("Which city?")
    with sr.Microphone() as source:
        print("Talk")
        audio_text = r.listen(source)
        print("Time over, thanks")
        try:
            print("Text: "+r.recognize_google(audio_text))
            city = r.recognize_google(audio_text)
        except:
            print("Sorry, I did not get that")

    url = f"https://api.weatherapi.com/v1/current.json?key=218f94ca3d394715be4172515242701&q={city}"
    response = requests.get(url)
    weather_data = json.loads(response.text)
    temperature = weather_data["current"]["temp_c"]
    humidity = weather_data["current"]["humidity"]
    speak(f"The current temperature in {city} is {temperature} degrees celsius and {humidity} humidity")

def readTopSearchResults(query, num_results=5):
    query = f"list of {query}"
    speak(f"Searching for {query} on Google")
    results = list(search(query, sleep_interval=4, num_results=num_results))

    if results:
        for i, result in enumerate(results, start=1):
            try:
                page = requests.get(result)
                soup = BeautifulSoup(page.content, 'html.parser')
                paragraphs = [p.text for p in soup.find_all('p')]
                for paragraph in paragraphs:
                    sentences = paragraph.split('. ')
                    if len(sentences) > 5:
                        text = '. '.join(sentences[:5]) + '.'
                        break
                else:
                    continue
                speak(f"Result {i}: {text}")
            except Exception as e:
                print(f"Error reading result {i}: {e}")
                speak(f"Error reading result {i}")

if __name__ == "__main__":
    wish()
    speak("Is this working?")
    command = takeCommand().lower()
    print(f"You said: {command}")

    while True:
        if "weather" in command:
            getWeatherInfo()
        elif "search" in command:
            search_query = takeSpeechInput()
            if search_query:
                readTopSearchResults(search_query, num_results=5)
        else:
            speak("Sorry, I didn't understand that command. Please try again.")
        
        command = takeCommand().lower()
