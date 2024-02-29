from tkinter import Listbox
from guizero import *
import nltk
app = App(title="Singapore", layout="grid")

def submit():
  questions = ["Do I need to buy an ez-link card to use public transport?","What mrt lines should I take to get to the orchard?","What is the minimum amount to top up my ez-link?","What line should I take to get to Marina Bay sands?","Are there mrt stations in the malls?","Can I eat or drink in the trains and buses?"] #stemmed questions in here
  answers = []#answers go here
  matches = []
  originalQ = []#original questions go here

  nltk.download("punkt")
  from nltk.stem.lancaster import LancasterStemmer

  stemmer = LancasterStemmer()

  file = open("question.txt","r")
  data =[]
  for row in file:
    data = row.strip().split("#")
    questions.append(data[0].lower())
   #append questions and answers here.
    words = data[0].split(" ")
    q = ""
    for word in words:
      q += stemmer.stem(word).lower()+" "
    questions.append(q[0:-1])
  file.close()
  word = str(input)
  words = word.lower().strip().split(" ")

  import string 
  nltk.download("punkt")
  from nltk.stem import PorterStemmer
  from nltk.tokenize import word_tokenize
  stemmer = PorterStemmer()
  from nltk.stem import WordNetLemmatizer
  nltk.download("wordnet")
  nltk.download("omw - 1.4")
  wnl = WordNetLemmatizer()
  example_words = ["program","programing","programer","programs","programers"]

  print("{0:20}{1:20}".format("--Word--","--Lemma--"))
  for word in example_words:
    print ("{0:20}{1:20}".format(word,wnl.lemmatize(word,pos="v")))

  print (" ")

  wnl =WordNetLemmatizer()
  example_sentence = "Python programmers often tend to like programming in python because it's like english. We call people who program in python pythonistas. Typing type"

  example_sentence_no_punct = example_sentence.translate(str.maketrans("","",string.punctuation))

  word_tokens = word_tokenize(example_sentence_no_punct)

  print("{0:20}{1:20}".format("--Word--","--Lemma--"))
  for word in word_tokens:
    print ("{0:20}{1:20}".format(word,wnl.lemmatize(word,pos="v")))


message_one = Text(app, text="Welcome to Singapore!", grid=[0, 0])
message_one = Text(app, text="How can I help you today?", grid=[0, 1])
input = TextBox(app, "", height=400, width=37, grid=[0, 2])
button = PushButton(app, text="Submit", command = submit, grid=[0,3])
listbox = ListBox(app, items=[], grid=[0,4],height=300, width=300)
app.display()
