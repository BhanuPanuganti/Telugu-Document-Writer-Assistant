import re
import math
import json
import os
from collections import defaultdict, Counter
import pickle

class HMMNGramModel:
    def __init__(self, n=3):
        self.n = n
        self.ngram_counts = defaultdict(Counter)
        self.context_counts = Counter()
        self.vocab = set()
        self.trained = False

    def tokenize_telugu_sentence(self, sentence):
        return [w for w in sentence.split() if re.match(r'[\u0C00-\u0C7F]+', w)]

    def train(self, sentences, vocab=None):
        self.ngram_counts = defaultdict(Counter)
        self.context_counts = Counter()
        self.vocab = set() if vocab is None else vocab.copy()

        # Convert raw sentences to token lists if needed
        if sentences and isinstance(sentences[0], str):
            tokenized_sentences = [self.tokenize_telugu_sentence(s) for s in sentences]
        else:
            tokenized_sentences = sentences

        for tokens in tokenized_sentences:
            tokens = ["<s>"] * (self.n - 1) + tokens + ["</s>"]

            for i in range(len(tokens) - self.n + 1):
                context = tuple(tokens[i:i + self.n - 1])
                next_word = tokens[i + self.n - 1]

                if vocab is None:
                    self.vocab.add(next_word)

                self.ngram_counts[context][next_word] += 1
                self.context_counts[context] += 1

        self.vocab.update(["<s>", "</s>"])
        self.trained = True

    def get_probability(self, context, word):
        context_size = self.n - 1
        current_context = tuple(
            context[-context_size:]
            if len(context) >= context_size
            else ["<s>"] * (context_size - len(context)) + context
        )

        vocab_size = len(self.vocab)
        count_word = self.ngram_counts.get(current_context, {}).get(word, 0)
        count_context = self.context_counts.get(current_context, 0)
        denominator = count_context + vocab_size

        if denominator > 0:
            return (count_word + 1) / denominator
        else:
            return 1 / vocab_size

    def predict_next(self, context, top_k=3):
        if isinstance(context, str):
            context = self.tokenize_telugu_sentence(context)

        context_size = self.n - 1
        current_context = tuple(
            ["<s>"] * max(0, context_size - len(context)) + context[-context_size:]
        )

        if current_context in self.context_counts:
            probs = {}
            for word in self.vocab:
                if word not in ['<s>']:
                    probs[word] = self.get_probability(current_context, word)

            return sorted(probs.items(), key=lambda x: x[1], reverse=True)[:top_k]

        # Backoff
        if self.n > 2 and len(current_context) > 1:
            return self.predict_next(context[-1], top_k)

 
        word_freq = Counter()
        for cxt in self.context_counts:
            word_freq.update(self.ngram_counts[cxt])

        total = sum(word_freq.values())
        return [(word, count / total) for word, count in word_freq.most_common(top_k)
                if word not in ['<s>', '</s>']]

    def complete_sentence(self, seed_words, max_len=20):
        if isinstance(seed_words, str):
            sentence = self.tokenize_telugu_sentence(seed_words)
        else:
            sentence = seed_words.copy()

        generated_words = set(sentence)

        for _ in range(max_len):
            next_word_pred = self.predict_next(sentence, top_k=1)
            if not next_word_pred:
                break

            next_word = next_word_pred[0][0]
            if next_word == "</s>":
                break

            if next_word in generated_words:
                if len(next_word) > 2:
                    break
                elif sentence.count(next_word) >= 2:
                    break

            sentence.append(next_word)
            generated_words.add(next_word)

        return " ".join(sentence)

    def perplexity(self, test_sentences):
        if not self.trained:
            return float("inf")

        total_log_prob = 0
        total_words = 0

        for sentence in test_sentences:
            if isinstance(sentence, str):
                tokens = self.tokenize_telugu_sentence(sentence)
            else:
                tokens = sentence

            tokens = ["<s>"] * (self.n - 1) + tokens + ["</s>"]

            for i in range(self.n - 1, len(tokens)):
                context = tokens[i - self.n + 1:i]
                word = tokens[i]

                prob = self.get_probability(context, word)
                total_log_prob += -math.log(max(prob, 1e-10))
                total_words += 1

        return math.log(total_log_prob / total_words) if total_words > 0 else float("inf")



    def save_model(self, path):
        
        with open(path, "wb") as f:
            pickle.dump({
                "n": self.n,
                "ngram_counts": self.ngram_counts,
                "context_counts": self.context_counts,
                "vocab": self.vocab
            }, f)


    def load_model(self, path):
        with open(path, "rb") as f:
            data = pickle.load(f)

        self.n = data["n"]
        self.ngram_counts = data["ngram_counts"]
        self.context_counts = data["context_counts"]
        self.vocab = data["vocab"]
        self.trained = True


        print(f"Model loaded from {path}")



def load_training_data(sentences_path, vocab_path):
    with open(sentences_path, 'r', encoding='utf-8') as f:
        tokenized_sentences = json.load(f)

    with open(vocab_path, 'r', encoding='utf-8') as f:
        vocab = {line.strip() for line in f if line.strip()}

    print(f"Loaded {len(tokenized_sentences)} sentences and {len(vocab)} vocab words.")
    return tokenized_sentences, vocab


def load_or_train(model, sentences, vocab, model_path="hmm_ngram_model.pkl"):
    if os.path.exists(model_path):
        print("Existing model found. Loading...")
        model.load_model(model_path)
    else:
        print("No saved model. Training...")
        model.train(sentences, vocab)
        model.save_model(model_path)
    return model


if __name__ == "__main__":

    tokenized_sentences, vocab = load_training_data(
        'telugu_tokenized_sentences.json',
        'telugu_vocabulary.txt'
    )

    
    model = HMMNGramModel(n=3)

    model = load_or_train(
        model,
        tokenized_sentences,
        vocab,
        model_path="hmm_ngram_model.pkl"
    )


    print("Perplexity:", model.perplexity(tokenized_sentences))

    test_words = [
        "పన్నెండున్నరకి", "సూర్య", "చదువు", "రాము",
        "సైనికులు", "వాణిజ్యం", "ఇల్లు",
        "మాట వింటూనే", "పరిశుభ్రత", "ఆమె"
    ]

    for word in test_words:
        print("----------------------------------------")
        print(f"Word: {word}")
        print("Prediction:", model.predict_next([word]))
        print("Completion:", model.complete_sentence(word))
