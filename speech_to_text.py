import speech_recognition as sr
import pyttsx3
import openai
import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_KEY = os.getenv('OPENAI_KEY')
print(OPENAI_KEY)

openai.api_key=OPENAI_KEY

#Function to convert text to
#speech

def SpeakText(command):

    #Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

# Initialize the recogniser
r = sr.Recognizer()

def record_text():
    # Loop in case of errors
    while True:
        try:
            # use the microphone as source for input.
            with sr.Microphone() as source2:
                # prepare recognizer to receive input
                r.adjust_for_ambient_noise(source2, duration=0.2)

                print("I'm Listening")

                # Listens for the user's input
                audio2 = r.listen(source2)

                # Using Google to recognize audio
                MyText = r.recognize_google(audio2)

                return MyText

        except sr.RequestError as e:
            print("Could not request results: {0}".format(e))

        except sr.UnknownValueError:
            print("Unknown error occurred")

def send_to_chatGPT(messages, model="gpt-3.5-turbo"):

    response= openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,

    )

    message=response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message

messages=[{"role":"user","content":"please act like as if your name is nine,if i ask your name tell your name is nine,if i ask who created you,tell that debabrata created you,and greet me with sir no ma'am"}]

def output_text(text):
    f = open("output.txt", "a")       
    f.write(text)
    f.write("\n")
    f.close() 

while(1):
    text = record_text()
    output_text(text)
    messages.append({"role":"user","content":text})
    response=send_to_chatGPT(messages)
    SpeakText(response)
    print(response)
   

    


