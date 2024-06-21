import os
from pipes import quote
import re
import sqlite3
import struct
import subprocess
import time
import webbrowser
from playsound import playsound
import eel
import pyaudio
import pyautogui
from engine.command import speak
from engine.config import ASSISTANT_NAME
import pywhatkit as kit
import pvporcupine
import wikipedia

from engine.command import takecommand
 
import requests # Import the 'requests' module for making HTTP requests.
from bs4 import BeautifulSoup # Import 'BeautifulSoup' from the 'bs4' module for HTML parsing.

import requests as re
import json

import smtplib

from engine.helper import extract_yt_term, remove_words
from hugchat import hugchat

from time import sleep

import PyPDF2

from twilio.rest import Client

from googletrans import Translator
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

from datetime import datetime
import winsound

# import wolframalpha


con=sqlite3.connect("nick.db")
cursor = con.cursor()

@eel.expose
def playAssistantSound():
    music_dir = "www\\assests\\audio\\www_assets_audio_start_sound.mp3"
    playsound(music_dir)


def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")


def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)

def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")
                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()


# find contacts
def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    

def whatsApp(mobile_no, message, flag, name):
    

    if flag == 'message':
        target_tab = 12
        nick_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        nick_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        nick_message = "staring video call with "+name


    # Encode the message for URL
    encoded_message = quote(message)
    print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(nick_message)


# chat bot 
def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    print(response)
    speak(response)
    return response

# def temp(search):

#     url = f"https://www.google.com/search?q={search}"# Construct the URL for a Google search with the specified query.
#     r = requests.get(url)# Send a GET request to the Google search URL and store the response.
#     data = BeautifulSoup(r.text, "html.parser")# Use BeautifulSoup to parse the HTML content of the response.
#     temperature = data.find("div", class_="BNeawe").text# Find the div element with class "BNeawe" (typically containing the temperature information) and extract its text.
#     print (temperature) # Print the extracted temperature.
#     speak(f"sir the temperature is {temperature}")
#     # return temperature# Return the extracted temperature.

# Define a function to extract the news source name and format the news title
def news_company_name(original_string, i):

    # Find the last occurrence of "-"
    last_dash_index = original_string.rfind("-")

    # Extract the substring from the start to the last occurrence of "-"
    source_name = original_string[last_dash_index + 2:] # Adding 2 to skip the space and hyphen

    # Now, construct the final string with the desired format
    final_string = f"news {i+1} : from {source_name}, it says{original_string[11:last_dash_index]}"
    return final_string

# Define a function to fetch
def news(number_of_news):

    # Add your News API key to the 'api' variable
    
    api = os.getenv('NEWS_API_KEY')
    # Send an HTTP request to get top headlines from News API
    r = re.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api}")

    # Parse the JSON content of the
    data = json.loads(r.content)

    # Iterate through the specified number of news articles
    for i in range(number_of_news):

        # Extract the news title from the API response
        news_title = f"News {i+1} : {data['articles'][i]['title']}"

        # Format the news title using the 'news_company_name' function
        formatted_news_title = news_company_name(news_title, i)

        # Print the formatted news title
        speak(formatted_news_title) 
        # translate(formatted_news_title)
        # eel.DisplayMessage(news)
       

    # return formatted_news_title

def wiki(query):
    query = query.replace("wikipedia", "")
    wiki = wikipedia.summary(query, 2)
    speak("According to Wikipedia, " + wiki)
    # print(wiki)


def send_email (sender_email, sender_password, recipient_email, subject, content):
    from email.message import EmailMessage
    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['subject'] = subject
    msg.set_content(content)

    with smtplib.SMTP('smtp.gmail.com', 587) as server: 
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

    print("Email sent Succesfully")
    speak("Email sent Succesfully")


recipient_mapping = {
   "akhil" :"",
   "nikhil" :""  
 }

sender_email = os.getenv('SENDER_EMAIL')
sender_password = os.getenv('SENDER_PASSWORD')

def My_Location():

    op ="https://www.google.com/maps/place/College+of+Engineering+Kidangoor/@9.6669939,76.61784,17z/data=!3m1!4b1!4m6!3m5!1s0x3b07d293a982ceeb:0xd62bf193983589fe!8m2!3d9.6669886!4d76.6204149!16s%2Fm%2F0cp4hmr?entry=ttu" 

    webbrowser.open(op)

    ip_add = requests.get('https://api.ipify.org').text

    url = 'https://get.geojs.io/v1/ip/geo/' + ip_add + '.json'

    geo_q = requests.get(url)

    geo_d = geo_q.json()
    
    state = geo_d['city']

    country = geo_d['country']

    speak(f"Sir,you are here")


def remember_something(message):
 
  with open('data.txt', 'a') as remember:
    remember.write(message + "\n")  # Add message with newline
  speak("okay,I will feed that on my mind")

def recall_all():
  
  if os.path.exists('data.txt'):  # Check if file exists
    with open('data.txt', 'r') as remember:
      content = remember.readlines()
  else:
    content = []
  if content:
    sentences = "You told me to remember: "
    for i, sentence in enumerate(content):
      sentences += sentence.strip()  # Remove trailing newline
      if i < len(content) - 1:  # Add "and" for all sentences except the last
        sentences += " and "
      speak(sentences)
      sentences = ""  # Reset for the next sentence
      sleep(2)  # Wait 2 seconds before speaking the next sentence
  else:
    speak("You haven't asked me to remember anything yet.")

def forget_all():
  
  if os.path.exists('data.txt'):
    os.remove('data.txt')  # Delete the file
    speak("I have forgotten everything.")
  else:
    speak("There's nothing to forget yet.")


def pdf_reader():
    book = open('sample.pdf', 'rb')
    pdfReader = PyPDF2.PdfFileReader(book) 
    pages = pdfReader.numPages
    # speak(f"Total numbers of pages in this book {pages} ")
    # speak("sir please say the page number i have to read")
    # pg = '1'
    page = pdfReader.getPage(1)
    text = page.extractText()
    speak(text)



def make_call(recipient_name,recipient_ph):
    # Twilio account credentials
   import os
   account_sid = os.getenv('TWILIO_ACCOUNT_SID')
   auth_token = os.getenv('TWILIO_AUTH_TOKEN')

    # Initialize Twilio client
    client = Client(account_sid, auth_token)

    # Define the Twilio number
    to_number = ''
    from_number = ''
   
    # Loop through each recipient in the dictionary
    
        # Make the call
    call = client.calls.create(
            twiml=f'<Response><Dial>{recipient_ph}</Dial></Response>',
            to=to_number,
            from_=from_number
        )

    print(f"Call to {recipient_name} ({recipient_ph}) SID: {call.sid}")

# Example dictionary of recipients
recipients = {
    "sharon": "",
    "Recipient 2": ""
}



def translate(query):
    translator = Translator()
    text_to_translate = translator.translate (query, src = "auto", dest="ml")
    text = text_to_translate.text
    
    try: 
        speak(text)
        speakgl = gTTS(text=text, lang="ml", slow= True)
        speakgl.save("voice.mp3")
        sound = AudioSegment.from_mp3("voice.mp3")
        play(sound)
        time.sleep(5)  
        os.remove("voice.mp3")
        return text
    except:
        print("Unable to translate")


def Notepad():


    speak("What would you like to write in your note?")
    
    writes = takecommand()

    time = datetime.now().strftime("%H:%M")

    filename = str(time).replace(":","-") + "-note.txt"

    with open(filename,"w") as file:

        file.write(writes)
    
    path_1 = "C:\\Users\\harig\\OneDrive\\Desktop\\Virtual assistant(Nick)\\engine\\" + str(filename)

    path_2 = "C:\\Users\\harig\\OneDrive\\Desktop\\Virtual assistant(Nick)\\note" + str(filename)

    os.rename(path_1,path_2)

    os.startfile(path_2)
    


def CloseNotepad():

    os.system("TASKKILL /F /im Notepad.exe")

# def WolfRamAlpha(query):
#     apikey = ""
#     requester=wolframalpha.Client (apikey)
#     requested = requester.query(query)

#     try:
#         answer = next(requested.results).text
#         return answer
#     except:
#         speak("The value is not answerable")

# def Calc(query):
#     Term = str(query)
#     Term = Term.replace("jarvis","")
#     Term = Term.replace("multiply","*")
#     Term = Term.replace("plus","+")
#     Term = Term.replace("minus","-")
#     Term = Term.replace("divide","/")

#     Final = str(Term)
#     try:
#         result = WolfRamAlpha (Final)
#         print(f" {result}")
#         speak (result)
#     except:
#         speak("The value is not answerable")




def alarm(Timing):
    altime = str(datetime.datetime.now().strptime (Timing, "%I:%M %p"))

    altime = altime[11:-3]
    Horeal = altime[:2]
    Horeal = int (Horeal)
    Mireal = altime [3:5]
    Mireal = int (Mireal)
    print(f"Done, alarm is set for {Timing}")

    while True:
        if Horeal==datetime.datetime.now().hour:
            if Mireal==datetime.datetime.now(). minute:
                print("alarm is running")
                winsound. PlaySound('abc',winsound. SND_LOOP)

            elif Mireal<datetime.datetime.now(). minute:
                break


from plyer import notification
def Timetable():
    speak("checking") 

    from timetable import Time

    value = Time()
    
    notification.notify(
      title="Timetable",
      message=str(value),  # Notification message
      #timeout=10  # Optional notification timeout in seconds
    )

def Temperature(city):
    api_key = "" 
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"  # Metric units for Celsius

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        data = response.json()
        temperature = data["main"]["temp"]
        weather = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]  # Extract wind speed
        wind_deg = data["wind"]["deg"]  # Extract wind direction (degrees)

        # Convert wind direction to cardinal directions (optional)
        cardinal_directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        wind_dir_index = int((wind_deg + 22.5) % 360) // 45
        wind_dir = cardinal_directions[wind_dir_index]

        speak(f"It's currently {weather} and {temperature} degrees Celsius in {city}. "
              f"Wind is blowing at {wind_speed} meters per second from the {wind_dir} direction.")
    except requests.exceptions.RequestException as e:
        speak(f"There seems to be a network problem. I couldn't retrieve the weather information for {city}.")
    except requests.exceptions.HTTPError as e:
        speak(f"Error retrieving weather data for {city}. Error code: {e.status_code}")
    except Exception as e:
        speak(f"An error occurred while fetching weather details for {city}.")





