import os
import nltk
from nltk import pos_tag, ne_chunk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from nltk.tokenize import wordpunct_tokenize
import json
from collections import defaultdict, Counter
from flask import Flask, request, jsonify
import random
from flask import render_template
from flask import send_from_directory
from flask_cors import CORS


 

nltk.download('punkt')  # Download the necessary data for tokenization
nltk.download('stopwords')  # Download the list of stopwords for different languages, including Arabic
nltk.download('wordnet')  # Download WordNet, necessary for English lemmatization
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
repertoire_source = r"C:\Users\DELL\Desktop\Sports"
fichier_sortie = "fusion_resultat.txt"
fichiers_a_fusionner = sorted(os.listdir(repertoire_source))[:6000]
chemin_sortie = os.path.join(repertoire_source, fichier_sortie)

with open(chemin_sortie, 'w', encoding='utf-8') as fichier_sortie:
    for fichier in fichiers_a_fusionner:
        chemin_fichier = os.path.join(repertoire_source, fichier)
        with open(chemin_fichier, 'r', encoding='utf-8') as fichier_source:
            contenu = fichier_source.read()
            fichier_sortie.write(contenu)
            fichier_sortie.write('\n')

print(f"The merging of the files is complete. The result is saved in {chemin_sortie}.")

# Tokenization of words
with open(chemin_sortie, 'r', encoding='utf-8') as fichier_sortie:
    contenu_sortie = fichier_sortie.read()
    mots_fusionnes = word_tokenize(contenu_sortie)

# Removing stop words using the list of Arabic stopwords
stop_words_arabe = set(stopwords.words('arabic'))
mots_diff_stopwords = [mot for mot in mots_fusionnes if mot.lower() not in stop_words_arabe]

# Load the Arabic dictionary
with open(r'C:\Users\DELL\Desktop\FINALNLP\dictt.txt', 'r', encoding='utf-8') as f:
    arabic_dictionary = set(line.strip() for line in f)

# Dictionary verification
verified_words = [word for word in mots_diff_stopwords if word in arabic_dictionary]

# Stemming of words
arabic_stemmer = SnowballStemmer("arabic")
mots_stemmes = [arabic_stemmer.stem(mot) for mot in verified_words]

# Lemmatization of words (in English)
lemmatizer = WordNetLemmatizer()
mots_lemmatizes = [lemmatizer.lemmatize(mot) for mot in verified_words]

# Result file after removing stop words, dictionary verification, stemming and lemmatization
fichier_resultat_lem = "resultat_lem.txt"
chemin_resultat_lem = os.path.join(repertoire_source, fichier_resultat_lem)

with open(chemin_resultat_lem, 'w', encoding='utf-8') as fichier_resultat_lem:
    fichier_resultat_lem.write(' '.join(mots_lemmatizes))

print(f"The words after removing stop words, dictionary verification, stemming and lemmatization have been saved in {chemin_resultat_lem}.")
# Apply NER
ner_words = ne_chunk(pos_tag(wordpunct_tokenize(' '.join(verified_words))))

# Print named entities
for named_entity in ner_words:
    if hasattr(named_entity, 'label'):
        print(named_entity.label(), ' '.join(c[0] for c in named_entity))


# Create a dictionary to hold the words and their next words
word_dict = defaultdict(Counter)

# Loop over the words and add the next word to the dictionary
for i in range(len(verified_words) - 1):
    word_dict[verified_words[i]][verified_words[i + 1]] += 1

# Keep only the top 3 next words for each word
for word, next_words in word_dict.items():
    word_dict[word] = dict(next_words.most_common(3))

# Save the dictionary as a JSON file
with open('word_matrix.json', 'w', encoding='utf-8') as f:
    json.dump(word_dict, f, ensure_ascii=False, indent=4)

print("The word matrix has been saved in word_matrix.json.") 






app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')




@app.route('/predict', methods=['POST'])
def predict():
    # Load the word matrix
    with open('word_matrix.json', 'r', encoding='utf-8') as f:
        word_dict = json.load(f)
    data = request.get_json()
    input_word = data['word']
    next_words = word_dict.get(input_word, {})
    if not next_words:
        return jsonify({'error': 'Word not found in dictionary'}), 400
    # Select a random word from the predicted words
    predicted_word = random.choice(list(next_words.keys()))
    return jsonify({'predicted_word': predicted_word})


if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)


