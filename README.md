A Natural Language Processing (NLP) pipeline for processing large Arabic text corpora, including tokenization, stop word removal, dictionary verification, stemming, lemmatization, named entity recognition (NER), and the creation of word/sequence matrices for predictive text applications.

## Features

- Merges thousands of text files into a single corpus.
- Tokenizes Arabic text and removes stop words.
- Verifies tokens against a custom Arabic dictionary.
- Applies stemming and lemmatization.
- Performs Named Entity Recognition (NER) using Farasa.
- Saves vocabulary and generates word and sequence matrices for next-word/sequence prediction.
- Provides a Flask API endpoint for sequence prediction.
- Includes a simple web interface for user interaction.

## Requirements

- Python 3.8+
- [NLTK](https://www.nltk.org/)
- [Farasa Segmenter & NER](https://github.com/mawdoo3/farasa)
- Flask
- flask-cors

Install dependencies:
```sh
pip install nltk flask flask-cors farasa
```

## Usage

### 1. Prepare Data

Place your raw `.txt` files in the Sports directory.

### 2. Run the NLP Pipeline

Process the corpus and generate vocabulary and matrices:
```sh
python pp.py
```

### 3. Start the Flask API

Serve the prediction API and web interface:
```sh
python appp.py
```
Visit [http://localhost:5000](http://localhost:5000) in your browser.

### 4. Predict Next Sequences

Use the web interface or send a POST request to `/predict` with a JSON body:
```json
{ "word": "YOUR_ARABIC_WORD" }
```

## Output Files

- vocabulaire.txt: Filtered vocabulary (named entities).
- word_matrix.json: Next-word prediction matrix.
- sequence_matrix.json: Next-sequence prediction matrix.

- Ensure dictt.txt and `stop_arabic.txt` are present and properly formatted.
- Farasa requires Java; see [Farasa documentation](https://github.com/mawdoo3/farasa) for setup.
- For large corpora, adjust the number of files processed in pp.py as needed.

## License

This project is for educational and research purposes.
