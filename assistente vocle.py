import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import time
import wolframalpha
import requests
import playsound
import os
from gtts import gTTS
import cv2

# Inizializiamo il microfono
r = sr.Recognizer()
mic = sr.Microphone( sample_rate=48000)
print(mic.list_microphone_names())
wikipedia.set_lang('it')


# funzione che converte da testo a parlato
def speak(text):
    print(text)
    tts = gTTS(text=text, lang='it')

    filename = "response.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)


# una volta riconosciuta la frase, elabora il comando
def parse_command(statement):
    if not statement:
        parse_command(take_command())

    print("Comando: " + statement)

    if 'wikipedia' in statement:
        # Usiamo le API di wikipedia per trarre informazioni su una questione
        try:
            speak('Cerco su Wikipedia...')
            statement = statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=2)
            speak("Secondo Wikipedia")
            for s in results.split("."):
                speak(s)
        except:
            playsound.playsound("non_ho_capito.mp3")
            print("Non ho capitoooo!")

    elif 'cerca' in statement:
        statement = statement.replace("cerca", "")
        webbrowser.open_new("https://www.google.it/search?q=" + statement)
        speak('Cerco su google' + statement)
        time.sleep(5)

    elif "ciao" in statement or "presentati" in statement:
        speak('Ciao. Sono l\'assistente vocale di Maipescion!')

    elif "arrivederci" in statement or "spegniti" in statement or "stop" in statement:
        speak('L\'assistente vocale di Maipescion si sta spegnendo. Ciao.')
        exit()

    elif 'apri youtube' in statement:
        webbrowser.open_new("https://www.youtube.com")
        speak("youtube è aperto")
        time.sleep(5)

    elif 'apri google' in statement:
        webbrowser.open_new("https://www.google.com")
        speak("Google chrome è aperto")
        time.sleep(5)

    elif 'apri gmail' in statement:
        webbrowser.open_new("https://www.gmail.com")
        speak("Gmail è aperto")
        time.sleep(5)

    elif "meteo" in statement:
        api_key = "8ef61edcf1c576d65d836254e11ea420"
        base_url = "https://api.openweathermap.org/data/2.5/weather?"
        speak("Di quale città desideri il meteo")
        city_name = take_command()
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        x = response.json()
        print("Cerco meteo in città: " + city_name)
        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"] - 273.15
            current_humidiy = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            speak(" La temperature in Celsius è di " +
                  str(f"{current_temperature:.2f}") + " \n gradi \n"
                                                      "\n La percenuale di temperatura è di  umidità " +
                  str(current_humidiy))


        else:
            speak(" Città non trovata ")



    elif 'ora' in statement:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sono le {strTime}")





    elif 'notizie' in statement:
        news = webbrowser.open_new("https://www.ilmattino.it")
        speak('Ecco le ultime notizie')
        time.sleep(6)

    elif 'scatta una foto' in statement:
        cam = cv2.VideoCapture(0)
        img_counter = 0
        while True:
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame")
                break
            cv2.imshow("test", frame)

            k = cv2.waitKey(1)
            if k % 256 == 27:

                print("Escape hit, closing...")
                break
            elif k % 256 == 32:

                img_name = "cattura{}.png".format(img_counter)
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                img_counter += 1

        cam.release()
        cv2.waitKey(1000)
        cv2.destroyAllWindows()

    elif 'calcola' in statement:
        speak('Posso risolvere calcoli matematici. Cosa devo calcolare?')
        try:
            question = take_command()
            app_id = "R2K75H-7ELALHR35X"
            client = wolframalpha.Client('R2K75H-7ELALHR35X')
            res = client.query(question)
            answer = next(res.results).text
            speak(answer)
            print(answer)
        except:
            playsound.playsound("non_ho_capito.mp3")
            print("Non ho capitoooo!")

    else:
        playsound.playsound("non_ho_capito.mp3")
        print("Non ho capitoooo!")

    parse_command(take_command())


# In ascolto per un comando vocale
def take_command():
    print("Sto ascoltando")
    try:
        with mic as source:
            audio = r.listen(source)
        return r.recognize_google(audio, language="it-IT").lower()
    except Exception as e:
        print(e)


parse_command(take_command())
