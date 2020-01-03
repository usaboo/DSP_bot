##Please Use your Initials of your name when Bot asks you for your name, as API understands US English accent##

import speech_recognition as sr  
import playsound    
from gtts import gTTS   # google text to speech
import os, sys, subprocess   
import wolframalpha 
import webbrowser  
from io import BytesIO
from io import StringIO
import pyaudio 
import struct 
import wave 
import tkinter as tk
import threading 


RATE        = 16000     
DURATION    = 5        
N = DURATION * RATE     
num = 1


def DSPBot_speaks(output):
    global num
    num +=1
    print("DSPBot : ", output)
    toSpeak = gTTS(text=output, lang='en-US', slow=False)
    file = str(num)+".mp3"
    toSpeak.save(file)
    playsound.playsound(file, True)
    os.remove(file)


def get_audio():
    r = sr.Recognizer()
    p = pyaudio.PyAudio()
    stream = p.open(format      = pyaudio.paInt16,
                channels    = 1,
                rate        = 16000,
                input       = True,
                output      = False )

    wf = wave.open('speak.wav', 'w')
    wf.setnchannels(1)      	# one channel (mono)
    wf.setsampwidth(2)      	# two bytes per sample (16 bits per sample)
    wf.setframerate(RATE)   # samples per second

    print('Speak Now..')
    for n in range(0, N):
        input_bytes = stream.read(1, exception_on_overflow = False)
        input_tuple = struct.unpack('h', input_bytes)
        x0 = input_tuple[0]
        output_value = x0
        output_bytes = struct.pack('h', output_value) 
        wf.writeframes(output_bytes)

    print('Stop.')
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    speaker = sr.AudioFile('speak.wav')
    with speaker as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio,language='en-US')
        print("You : ", text)
        return text
    except:
        DSPBot_speaks("Could not understand your audio, PLease try again!")
        os.remove('speak.wav')
        return 0

def browser(input):
    driver = webbrowser.get('safari')
    inp = input.lower()
    if 'youtube' in inp:
        DSPBot_speaks("Opening in youtube")
        query_list = inp.split()
        del(query_list[len(query_list)-1:len(query_list)-3:-1])
        query = query_list[1:]
        driver.open("http://www.youtube.com/results?search_query=" + '+'.join(query))
        return
    elif 'map' in inp or 'maps' in inp:
        DSPBot_speaks("Opening Maps")
        query_list = inp.split()
        del(query_list[len(query_list)-1:len(query_list)-3:-1])
        query = query_list[1:]
        driver.open("http://maps.google.com/?q=" + ' '.join(query))
        return
    else:
        if 'google' in input:
            DSPBot_speaks("Opening Google")
            query_list = inp.split()
            del(query_list[len(query_list)-1:len(query_list)-3:-1])
            query = query_list[1:]
            driver.open("https://www.google.com/search?q=" + '+'.join(query))
        else:
            DSPBot_speaks("Opening Browser")
            query_list = inp.split()
            del(query_list[len(query_list)-1:len(query_list)-3:-1])
            query = query_list[1:]
            driver.open("https://www.google.com/search?q=" + '+'.join(query))
        return


def exec_apps(input):
    if "chrome" in input:
        DSPBot_speaks("Google Chrome")
        if sys.platform == "win32":
            os.startfile('C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
        else:
            opener ="open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, "/Applications/Google Chrome.app/"])
        return
    elif "firefox" in input or "mozilla" in input:
        DSPBot_speaks("Opening Mozilla Firefox")
        if sys.platform == "win32":
            os.startfile('C:\Program Files\Mozilla Firefox\\firefox.exe')
        else:
            opener ="open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, "/Applications/Firefox.app/"])
        return
    elif "windows media player" in input:
        DSPBot_speaks("Opening Windows Media Player")
        os.startfile('C:\Program Files\Windows Media Player\wmplayer.exe')
        return
    elif "itunes" in input:
        DSPBot_speaks("Opening iTunes")
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, "/Applications/iTunes.app/"])
        return
    elif "recorder" in input:
        DSPBot_speaks("Opening Voice Recorder")
        recorder()        
    else:
        DSPBot_speaks("Application not Oppening, so there might be two possibilities:")
        DSPBot_speaks("Application not present in the System or Application Path is not correct!")
        return

def recorder(): 
    
    class App():
        chunk = 1024 
        sample_format = pyaudio.paInt16 
        channels = 1
        fs = 44100  
    
        frames = []  
        def __init__(self, master):
            self.isrecording = False
            self.button1 = tk.Button(main, text='START',command=self.startrecording)
            self.button2 = tk.Button(main, text='STOP',command=self.stoprecording)      

            self.button1.pack(side = tk.TOP, fill = tk.X)
            self.button2.pack(side = tk.BOTTOM, fill = tk.X)

        def startrecording(self):
            self.p = pyaudio.PyAudio()  
            self.stream = self.p.open(format=self.sample_format,channels=self.channels,rate=self.fs,frames_per_buffer=self.chunk,input=True)
            self.isrecording = True
        
            print('Start Recording')
            t = threading.Thread(target=self.record)
            t.start()

        def stoprecording(self):
            self.isrecording = False
            print('recording complete')
            self.filename=input('the filename?')
            self.filename = self.filename+".wav"
            wf = wave.open(self.filename, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.sample_format))
            wf.setframerate(self.fs)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            main.destroy()
        def record(self):
       
            while self.isrecording:
                data = self.stream.read(self.chunk)
                self.frames.append(data)

    main = tk.Tk()
    main.title('Recorder')
    main.geometry('200x50')
    app = App(main)
    main.mainloop()

def input_audio(input):
    try:
        if "hey there" in input or "hello there" in input:
            speak = '''Hello There! This is you Assistant, DSP Bot!
                I can do the following tasks for you.
                1. Play a song on YouTube
                2. Open Maps and search for a location
                3. Do calculations
                4. Check the time
                Else search the web for you.'''
            DSPBot_speaks(speak)
            return
        elif "what are you" in input:
            speak = "I am a Python Application."
            DSPBot_speaks(speak)
            return
        elif "who made you" in input:
            speak = "PB, HB and US built this Application"
            assistant_speaks(speak)
            DSPBot_speaks(speak)
            return
        elif "calculate" in input.lower():
            app_id= "E88JGJ-GK9K5LY7UR"
            client = wolframalpha.Client(app_id)
            ind = input.lower().split().index('calculate')
            query = input.split()[ind + 1:]
            res = client.query(' '.join(query))
            answer = next(res.results).text
            DSPBot_speaks("The answer is " + answer)
            return
        elif 'open' in input:
            exec_apps(input.lower())
            return
        elif 'play' or 'search' in input:                                 
            browser(input.lower())
            return
        elif 'time' in input:
            client = wolframalpha.Client('E88JGJ-GK9K5LY7UR')
            res = client.query('time now')
            assistant_speaks(next(res.results).text)
        else:
            DSPBot_speaks("May I search the web for you?")
            ans = get_audio()
            if 'yes' in str(ans) or 'yeah' in str(ans):
                search_web(input)
            else:
                return
    except Exception as exe:
        print(exe)
        DSPBot_speaks("I am not sure if I can understand the audio. May I search the web for you?")
        answer = get_audio()
        if 'yes' in str(answer):
            search_web(input)


if __name__ == "__main__":
    DSPBot_speaks("Hi, May I Know Your Name?")
    initials = get_audio()
    if initials == 0:
        sys.exit()
    else:
        DSPBot_speaks("Hello, " + initials.upper() + '.')
        while(1):
            DSPBot_speaks("Go Ahead, How can I help?")
            text = get_audio()
            if text == 0:
                continue
            if "exit" in str(text) or "bye" in str(text):        #Say: "Exit" or "Bye" to stop the execution.
                DSPBot_speaks("See you next time, "+ initials.upper() +'.')
                break
            input_audio(text)


