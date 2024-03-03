from guizero import App, Text, TextBox, PushButton, ListBox, Combo
import nltk
from nltk.corpus import wordnet as wn
from googletrans import Translator, constants
from deep_translator import GoogleTranslator
from pprint import pprint

app = App(title="Singapore", layout="grid")

nltk.download("punkt")
nltk.download("wordnet")
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()
questions = []
answers = []

def translate_text(text):
  translator = Translator()
  l = combo.value()
  translated_text = translator.translate(text, dest="de")
  return translated_text.text

file = open("question.txt", "r")
content = file.readlines ()

for row in content:
  data = row.strip().split("#")
  questions.append (data[0])
  answers.append (data[1])

oquestions = [stemmer.stem(question.lower()) for question in questions] 

def get_synonyms(word):
    synonyms = set()
    for synset in wn.synsets(word):
        for lemma in synset.lemmas():
            synonyms.add(lemma.name())
    return synonyms

def submit():
    user_input = input_box.value.lower().strip()

    if user_input in questions:
        answer_index = questions.index(user_input)
        listbox.append("You: " + user_input)
        listbox.append("Bot: " + translate_text(answers[answer_index]))
    else:
        user_input_stemmed = stemmer.stem(user_input)
        matches = []

        for q in oquestions:
            q_stemmed = stemmer.stem(q)
            match = sum(1 for word in user_input_stemmed.split() if word in q_stemmed)

            # Enhance matching by considering synonyms
            if match == 0:
                user_synonyms = set()
                for word in user_input_stemmed.split():
                    user_synonyms.update(get_synonyms(word))

                question_synonyms = set()
                for word in q_stemmed.split():
                    question_synonyms.update(get_synonyms(word))
                match = len(user_synonyms.intersection(question_synonyms))
            matches.append(match)

        maxMatch = max(matches)
        if maxMatch == 0:
            listbox.append("Bot: I'm sorry, I don't understand.")
        else:
            if matches.count(maxMatch) == 1:  # If only one match found
                answer_index = matches.index(maxMatch)
                listbox.append("You: " + user_input)
                t = str("Bot: " + answers[answer_index])
                tt = GoogleTranslator(source='auto', target='de').translate(t) 
                listbox.append(tt)
            else:  # If multiple matches found
                listbox.append("Bot: Did you mean...")
                for f, match in enumerate(matches):
                    if match == maxMatch:
                        listbox.append("Bot: " + questions[f])
    input_box.clear()
message_one = Text(app, text="Welcome to Singapore!", grid=[0, 0])
message_two = Text(app, text="How can I help you today?", grid=[0,2])
message_three = Text(app, text="Language:", grid=[1, 0])
combo = Combo(app, options=["English", "French", "German", "Japanese","Chinese"],grid=[1,1])
input_box = TextBox(app, "", width=40, grid=[0, 3])
submit_button = PushButton(app, text="Submit", command=submit, grid=[1, 3])
listbox = ListBox(app, items=[], grid=[0, 4], width=300, height=300)
app.display()
