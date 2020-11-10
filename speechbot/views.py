from django.shortcuts import render

# Import essential libraries and packages needed in the project


import nltk
import numpy as np
import pyttsx3
import speech_recognition as sr
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import json
r=sr.Recognizer()

from miscellaneous.emailsending import emailconfirmation
from speechbot.forms import UserDetailsForm


# Load and open json file containing intents used for training data
data_file = open('./models/intents.json').read()
data = json.loads(data_file)


# Load trained model
from keras.models import load_model
model = load_model('./models/chatbot_model.h5')


# Extracting Data
word = []
classes = []
word_and_tag = []
l = []
whole_data =[]
for intents in data['intents']:
    for pattern in intents['patterns']:

        words = nltk.word_tokenize(pattern)
        word.extend(words)
        word_and_tag.append((words, intents['tag']))

        if intents['tag'] not in classes:
            classes.append(intents['tag'])

word = [lemmatizer.lemmatize(w.lower()) for w in word]
word = sorted(list(set(word)))
classes = sorted(list(set(classes)))


# Function for predicting probability of input words belonging to particular class
def predict_prob(input_data, word):
    in_data = nltk.word_tokenize(input_data)
    in_data = [lemmatizer.lemmatize(word.lower()) for word in in_data]
    bag_p = [0] * len(word)
    for in_d in in_data:
        for i, w in enumerate(word):
            if w == in_d:
                bag_p[i] = 1

    return (np.array(bag_p))



# Function for predicting response with respect to given pattern

def responsefun(lis, word, classes):

    resultant = model.predict(np.array([predict_prob(lis, word)]))[0]

    res_index = np.argmax(resultant)
    classes = classes[res_index]
    response = ''
    for i in data['intents']:

        if i["tag"] == classes:
            response = i["responses"]
            break
    return response


# Function to convert text to speech
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()



# Function to convert speech to text
def listen(t):
    with sr.Microphone() as source:
        audio = r.listen(source, phrase_time_limit=t, timeout=2)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            print("\nBot : \nSorry, I didn't get it\n")

        except sr.RequestError:
            print("\nBot : \nSorry, service is down at this moment\n")
    return voice_data




# Index function
def index(request):
    listenfun = "1"
    if request.method == "POST" and 'b2' in request.POST:

        userText = request.POST["msg"]
        mydata = responsefun(str(userText), word, classes)
        mydata = mydata[0]
        speak(mydata)
        whole_data.append(userText)

        return render(request, 'index.html', {"mydata": mydata, "userText": userText,"listenfun":listenfun})




    if request.method=="POST" and 'b1' in request.POST:
        lis=listen(10)
        lis=lis.lower()
        if lis!="":
            global l
            l.append(lis)
        if lis!="":
            if lis=="hello" or lis=="hello hello":
                mydata = responsefun(str(lis), word, classes)
                speak("Perfect let’s move ahead")
                speak(mydata)
                mydata = "Perfect let’s move ahead \n" + mydata[0]
                userText = lis

                return render(request, 'index.html', {"mydata": mydata, "userText": userText,"listenfun":listenfun})

            elif lis=="yes":

                listt= l[-2]
                print(listt)


                if 'for' in listt:
                    aphlist = []
                    li = list(listt.split(" "))


                    for i in range(0, len(li)):
                        if i == 2 or i == 5:
                            aphlist.append(li[i])

                    print(aphlist)
                    listt = aphlist[0][0] + aphlist[1][0]



                whole_data.append(listt)
                if len(whole_data) ==1:

                    userText = listt
                    mydata="Is it your first name or last name?"
                    speak(mydata)
                    return render(request, 'index.html', {"mydata": mydata, "userText": userText,"listenfun":listenfun})
                if len(whole_data) == 3:
                    userText = listt
                    mydata="Is it your first name or last name?"
                    speak(mydata)
                    return render(request, 'index.html', {"mydata": mydata, "userText": userText,"listenfun":listenfun})


                mydata = responsefun(str(listt), word, classes)
                speak("Perfect let’s move ahead")
                speak(mydata)
                mydata1=mydata
                mydata ="Perfect let’s move ahead \n" + mydata[0]
                userText=listt
                if mydata1==["May I know your email"]:
                    email="1"
                    return render(request, 'index.html', {"mydata": mydata, "userText": userText ,"email":email})


                return render(request, 'index.html', {"mydata": mydata, "userText": userText,"listenfun":listenfun})
            elif lis=="no":
                speak("Can you please repeat a bit slowly")
                mydata = "Can you please repeat a bit slowly"
                userText = lis
                return render(request, 'index.html', {"mydata": mydata, "userText": userText,"listenfun":listenfun})
            elif lis=="bye":
                mydata = "Your name is "+ whole_data[0]+ " " + whole_data[2]+" age is "+whole_data[4]+" gender is "+whole_data[5]+" email is "+whole_data[6]+" address is "+whole_data[7]+" state code is "+whole_data[8]
                speak(mydata)
                userText = lis
                emailconfirmation(whole_data[0],whole_data[6])
                form = UserDetailsForm(request.POST)
                f = form.save(commit=False)
                f.firstname =whole_data[0]
                f.lastname = whole_data[2]
                f.age= whole_data[4]
                f.gender=whole_data[5]
                f.email=whole_data[6]
                f.address=whole_data[7]
                f.statecode=whole_data[8]
                f.save()
                return render(request, 'index.html', {"mydata": mydata, "userText": userText,"listenfun":listenfun})

            else:


                userText=lis
                mydata = "I heard " + lis + " is it correct say yes or no"
                speak(mydata)

                return render(request, 'index.html',  {"mydata": mydata,"userText":userText,"listenfun":listenfun})
        else:
            mydata="Please Speak Again"
            return render(request, 'index.html', {"mydata": mydata,"listenfun":listenfun})

    return render(request,'index.html',{"listenfun":listenfun})




