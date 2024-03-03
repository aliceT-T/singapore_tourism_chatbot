from guizero import App, Text, TextBox, PushButton, ListBox
import nltk
from nltk.corpus import wordnet as wn
from googletrans import Translator

app = App(title="Singapore", layout="grid")

nltk.download("punkt")
nltk.download("wordnet")
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()

def translate_text(text):
  translator = Translator()
  translated_text = translator.translate(text, dest="ja")
  listbox.append(translate_text(user_input))
  return translated_text.text

questions = ["do i need to use an ez-link card to use public transportation?", 
             "what is the best place to eat in singapore?",
             "where can you get good bubble tea?",
             "are there any overrated places?"]
answers = ["yes", "laopasat", "playmade and koi!!", "yes... probably starbucks i don't really like it"]
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
        listbox.append(translate_text("Bot: " + answers[answer_index]))
        listbox.append("Bot: " + translate_text.answers[answer_index])
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
                listbox.append("Bot: " + answers[answer_index])
            else:  # If multiple matches found
                listbox.append("Bot: Did you mean...")
                for f, match in enumerate(matches):
                    if match == maxMatch:
                        listbox.append("Bot: " + questions[f])

message_one = Text(app, text="Welcome to Singapore!", grid=[0, 0])
message_two = Text(app, text="How can I help you today?", grid=[0, 1])
input_box = TextBox(app, "", width=40, grid=[0, 2])
submit_button = PushButton(app, text="Submit", command=submit, grid=[1, 2])
listbox = ListBox(app, items=[], grid=[0, 3], width=300, height=100)
app.display()
