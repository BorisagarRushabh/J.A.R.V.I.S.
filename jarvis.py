import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import pywhatkit as wk
import os
import cv2
import time
import pyautogui

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Choose the voice (0: Male, 1: Female)
engine.setProperty('rate', 160)  # Set speech rate

def speak(audio):
    """
    Converts the given text to speech and speaks it out loud.
    """
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    """
    Greets the user based on the time of day.
    """
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good morning !!")
    elif hour < 18:
        speak("Good afternoon !!")
    else:
        speak("Good evening !!")
    
    speak("At your service, sir. What can I do for you?")

def takecommand():
    """
    Listens to the user's command and returns it as a string.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query   

def search_wikipedia(query):
    """
    Searches Wikipedia for the given query and reads out the summary.
    """
    speak('Searching for it...')
    results = wikipedia.summary(query, sentences=2)
    speak("According to Wikipedia")
    print(results)
    speak(results)

def open_google():
    """
    Opens Google in the web browser.
    """
    speak("What should I search for?")
    query = takecommand().lower()
    webbrowser.open(f"https://www.google.com/search?q={query}")

def open_youtube():
    """
    Opens YouTube and plays a video based on user input.
    """
    speak("What would you like to watch?")
    query = takecommand().lower()
    wk.playonyt(query)

def open_camera():
    """
    Opens the webcam and displays the video feed.
    """
    cap = cv2.VideoCapture(0)
    while True:
        ret, img = cap.read()
        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) & 0xFF == 27:  # Esc key to exit
            break
    cap.release()
    cv2.destroyAllWindows()

def take_screenshot():
    """
    Takes a screenshot and saves it with a user-specified filename.
    """
    speak('Tell me a name for the file.')
    name = takecommand().lower()
    time.sleep(3)  # Wait for the user to get ready
    img = pyautogui.screenshot()
    img.save(f"{name}.png")
    speak("Screenshot saved")

def handle_command(query):
    """
    Handles the user's command by mapping it to the appropriate function.
    """
    commands = {
        'jarvis': lambda: speak("Yes sir"),
        'how are you': lambda: speak("I’m absolutely doing great, thanks for asking! How about you?"),
        'i am fine': lambda: speak("Glad to hear that!"),
        'what is': lambda query: search_wikipedia(query.replace("what is", "")),
        'who is': lambda query: search_wikipedia(query.replace("who is", "")),
        'just open google': lambda: webbrowser.open('https://www.google.com'),
        'open google': lambda: open_google(),
        'just open youtube': lambda: webbrowser.open('https://www.youtube.com'),
        'open youtube': lambda: open_youtube(),
        'search on youtube': lambda query: webbrowser.open(f"https://www.youtube.com/results?search_query={query.replace('search on youtube', '')}"),
        'close edge': lambda: os.system("taskkill /f /im msedge.exe"),
        'close chrome': lambda: os.system("taskkill /f /im chrome.exe"),
        'open command prompt': lambda: os.system("start cmd"),
        'shutdown the system': lambda: os.system("shutdown /s /t 5"),
        'restart the system': lambda: os.system("shutdown /r /t 5"),
        'lock the pc': lambda: os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0"),
        'open camera': lambda: open_camera(),
        'take screenshot': lambda: take_screenshot(),
        'open chrome': lambda: os.startfile('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'),
        'maximize this window': lambda: pyautogui.hotkey('alt', 'space') and pyautogui.press('x'),
        'google search': lambda query: pyautogui.hotkey('alt', 'd') and pyautogui.write(query.replace("google search", ""), 0.1) and pyautogui.press('enter'),
        'youtube search': lambda query: pyautogui.hotkey('alt', 'd') and time.sleep(1) and pyautogui.press('tab')*4 and pyautogui.write(query.replace("youtube search", ""), 0.1) and pyautogui.press('enter'),
        'open new window': lambda: pyautogui.hotkey('ctrl', 'n'),
        'open incognito window': lambda: pyautogui.hotkey('ctrl', 'shift', 'n'),
        'minimize this window': lambda: pyautogui.hotkey('alt', 'space') and pyautogui.press('n'),
        'open history': lambda: pyautogui.hotkey('ctrl', 'h'),
        'open downloads': lambda: pyautogui.hotkey('ctrl', 'j'),
        'previous tab': lambda: pyautogui.hotkey('ctrl', 'shift', 'tab'),
        'next tab': lambda: pyautogui.hotkey('ctrl', 'tab'),
        'close tab': lambda: pyautogui.hotkey('ctrl', 'w'),
        'close window': lambda: pyautogui.hotkey('ctrl', 'shift', 'w'),
        'clear browsing history': lambda: pyautogui.hotkey('ctrl', 'shift', 'delete')
    }

    for command, action in commands.items():
        if command in query:
            action()
            break
    else:
        speak("Sorry, I didn't understand that command.")

# Main program loop
if __name__ == "__main__":
    wishMe()
    while True:
        query = takecommand().lower()
        if query != "none":
            handle_command(query)
