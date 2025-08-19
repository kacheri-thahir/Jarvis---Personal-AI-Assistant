import pyttsx3
import speech_recognition as sr
import random
import webbrowser
import datetime
import time
import pywhatkit as pwk
from winotify import Notification,audio
import pyautogui
from contacts import send_whatsapp_message
import wikipedia
import inflect




def speak(audio):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')   
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 160)
    engine.say(audio)
    engine.runAndWait()
    time.sleep(0.3)


def command():
    content = " "
    while content == " ":
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening....")
            r.adjust_for_ambient_noise(source, duration=3)
            try:
                audio = r.listen(source)
                print("processing...")
                content = r.recognize_google(audio, language='en-in')
                return content.lower()
            except Exception as e:
                print("Boss, can you repeat again...")
    return ""



def play_song_from_request(request):
    song_name = request.replace('play', '').strip()
    if not song_name:
        return speak("I can't hear. Can you repeat once again, boss?")
    
    speak(f"Playing {song_name}")
    try:
        pwk.playonyt(song_name)
    except Exception as e:
        speak("Something went wrong while playing.")
        print("Error:", e)



def main_process():
    speak("Hello sir, i am your personal assistent jarvis , How can i help you ?")
    while True:
        try:
            request = command().lower()
            print("Command received:", request)
            if not request:
                print("No command detected. Listening again...")
                continue

            if "hello jarvis" in request :
                speak("Hello sir, Welcome....")

            elif "play" in request:
                play_song_from_request(request)

            elif "time" in request:
                p=inflect.engine()  #engine to convert numbers to words
                now=datetime.datetime.now()
                h, m, am_pm= now.strftime('%I'), now.strftime('%M'), now.strftime('%p')
                minute_text = p.number_to_words(int(m)) if int(m) else "o'clock"
                speak(f"Boss, the time is {p.number_to_words(int(h))} {minute_text} {am_pm}")

               
            elif "date" in request :
                pres_date=datetime.datetime.now().strftime('%d %B %Y')
                speak(f"sir today date is"+str(pres_date))

            elif "new task" in request:
                task=request.replace("new task","").strip()
                if task!="":
                    speak("adding task"+task)
                    with open('tasks.txt','a') as f:
                        f.write(task+'\n')


            elif "speak task" in request:
                with open("tasks.txt",'r') as f:
                    speak("Boss, today task is " + f.read())


            elif "show work" in request:
                with open("tasks.txt",'r') as f:
                    tasks=f.read()
                toast = Notification(app_id="TASKS",title="TODAY TASKS",msg=tasks)
                toast.set_audio(audio.LoopingAlarm6, loop=False)
                toast.show()

            elif "send message" in request:
                send_whatsapp_message(request)
                
                
            elif "open" in request:
                query=request.replace("open","")
                speak("opening"+query)
                pyautogui.press('super')
                pyautogui.typewrite(query)
                time.sleep(1)
                pyautogui.press('enter')


            elif "search google" in request:
                request=request.replace("jarvis","")
                request=request.replace("search google","")
                speak("Searching about"+request)
                webbrowser.open("https://www.google.com/search?q="+request)


            elif "search wikipedia" in request:
                request=request.replace("jarvis","")
                request=request.replace("search wikipedia","")
                result=wikipedia.summary(request, sentences=2)
                print(result)
                speak(result)


            elif "exit" in request:
                speak("Bye sir, shutting down")
                break
            

        except Exception as e:
            print(f"Error:{e}")
            speak("Sorry Boss, I encountered an error. Please try again.")


        time.sleep(1)

if __name__ == "__main__":
    main_process()



