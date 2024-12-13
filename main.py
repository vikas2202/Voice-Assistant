import speech_recognition as sr
import pyttsx3
import requests
from datetime import datetime
import time

# Initialize the speech recognition and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Set up the text-to-speech engine properties
engine.setProperty("rate", 150)  # Speed of speech
engine.setProperty("volume", 1)  # Volume level

# Function to speak a given text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen and recognize voice input
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=15)
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Can you repeat?")
            return ""
        except sr.RequestError:
            speak("Sorry, there seems to be a problem with the speech recognition service.")
            return ""

# Function to check the weather
def get_weather(city):
    api_key = " http://api.weatherapi.com/v1"  # Replace with your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response.get("cod") != 200:
        speak("Sorry, I couldn't fetch the weather details. Please try again.")
        return
    weather = response["weather"][0]["description"]
    temp = response["main"]["temp"]
    speak(f"The current weather in {city} is {weather} with a temperature of {temp} degrees Celsius.")

# Function to read the news
def get_news():
    api_key = "https://newsapi.org/v2/everything?q=tesla&from=2024-11-10&sortBy=publishedAt&apiKey=API_KEY"  # Replace with your NewsAPI key
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url).json()
    if response.get("status") != "ok":
        speak("Sorry, I couldn't fetch the news. Please try again.")
        return
    articles = response.get("articles", [])[:5]
    if not articles:
        speak("I couldn't find any news at the moment.")
    else:
        speak("Here are the top headlines:")
        for i, article in enumerate(articles):
            speak(f"Headline {i+1}: {article['title']}")

# Function to set a reminder
def set_reminder(reminder_time, message):
    try:
        reminder_time = datetime.strptime(reminder_time, "%H:%M")
        speak(f"Reminder set for {reminder_time.strftime('%I:%M %p')}. I'll notify you.")
        while True:
            now = datetime.now()
            if now.hour == reminder_time.hour and now.minute == reminder_time.minute:
                speak(f"Reminder: {message}")
                break
            time.sleep(10)
    except ValueError:
        speak("Sorry, I couldn't understand the time format. Please try again.")

# Main function to process user commands
def main():
    speak("Hello! I'm your personal assistant. How can I help you today?")
    while True:
        command = listen()
        if "weather" in command:
            speak("Sure. Which city's weather would you like to know?")
            city = listen()
            if city:
                get_weather(city)
        elif "news" in command:
            get_news()
        elif "reminder" in command:
            speak("What time should I set the reminder for? Please say it in 24-hour format, like 14:30.")
            reminder_time = listen()
            speak("What should I remind you about?")
            message = listen()
            if reminder_time and message:
                set_reminder(reminder_time, message)
        elif "exit" in command or "quit" in command:
            speak("Goodbye! Have a great day.")
            break
        else:
            speak("Sorry, I didn't understand that. Please try again.")

# Run the assistant
if __name__ == "__main__":
    main()
