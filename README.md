# 📘 Telugu Document Writer Assistant

This README file consolidates all modules from the Telugu NLP project, including HMM-based and GRU-based sentence completion, spell checker, and grammar checker.

---

## Team & Contributions

| Name | Roll Number | Contribution |
| :--- | :--- | :--- |
| **Pappu Meghana** | S20230030400 | Sentence Completion using HMM N-gram Model |
| **Panuganti Bhanu** | S20230030399 | Sentence Completion — N-gram + GRU Reranker and Data cleaning |
| **MachiReddy Hemanth Sai**| S20230030389 | Spell Checker — Levenshtein + LSTM and Data collection |
| **Patnam Jahnavi** | S20230010181 | Telugu Grammar Checker and spell checker |

---

## Telugu Text Data Collection and Preprocessing

### Overview

This repository contains a complete **data collection and preprocessing pipeline** for building a high-quality **Telugu language corpus**.  
The dataset is created by combining **Wikipedia articles**, **web-scraped Telugu stories**, and a **Kaggle Telugu text corpus**, cleaned, tokenized, and merged into a unified format suitable for NLP applications such as **language modeling**, **spell correction**, or **translation**.

---

### Data Sources

| Source | Description | Output File |
|---------|--------------|--------------|
| **Wikipedia + Web Stories** | Combined dataset from Telugu Wikipedia pages and scraped Telugu stories | `merged_telugu_wikipedia_data.txt` |
| **Kaggle Dataset** | Telugu corpus from Kaggle (general text dataset) | `corpus.txt` |

Both data sources undergo independent cleaning, tokenization, and vocabulary generation before being merged into the final dataset.

---

### Processing Pipeline

| Step | Description | Script | Output |
|------|--------------|---------|---------|
| **1️⃣ Wikipedia + Web Story Scraping** | Fetches Telugu pages & stories | `0_scrape_wiki.py`, `3_web_scrapping.ipynb` | `merged_telugu_wikipedia_data.txt` |
| **2️⃣ Cleaning (Wiki + Web)** | Cleans merged Wikipedia and story data | `1_clean_wiki.py` | `final_cleaned_telugu_data_1.txt` |
| **3️⃣ Cleaning (Kaggle)** | Cleans Kaggle corpus data | `2_clean_corpus.py` | `final_cleaned_telugu_data_2.txt` |
| **4️⃣ Tokenization + Vocabulary (Wiki/Web)** | Tokenizes sentences & builds vocab | `4_tokenization_vocabulary_1.py` | `telugu_tokenized_sentences_1.json`, `telugu_vocabulary_1.txt` |
| **5️⃣ Tokenization + Vocabulary (Kaggle)** | Tokenizes sentences & builds vocab | `5_tokenization_vocabulary_2.py` | `telugu_tokenized_sentences_2.json`, `telugu_vocabulary_2.txt` |
| **6️⃣ Merge Final Corpus** | Merges both sources | `6_merge.py` | `final_cleaned_telugu_data.txt`, `telugu_vocabulary.txt`, `telugu_tokenized_sentences.json` |

---

### 1️⃣ Wikipedia and Web Story Scraping

#### Script: `0_scrape_wiki.py` & `3_web_scrapping.ipynb`
- Scrapes **Telugu Wikipedia articles** across hundreds of topics.
- Adds **web-scraped short stories** for narrative diversity.
- Deduplicates using SHA-256 hashing.
- All unique text stored in:
  ```
  merged_telugu_wikipedia_data.txt
  ```

**Example Output**
```
--- Content for Search Term: భారతదేశం ---
--- Start of unique page: భారతదేశ చరిత్ర ---
[Telugu text content...]
--- End of unique page: భారతదేశ చరిత్ర ---
```

---

### 2️⃣ Cleaning Stage

#### a) Wikipedia + Web Story Cleaning (`1_clean_wiki.py`)
- Cleans merged data from `merged_telugu_wikipedia_data.txt`.
- Removes:
  - Wikipedia markup, HTML tags, and metadata.
  - English/Hindi text, numbers, and symbols.
- Keeps only valid Telugu Unicode (`U+0C00–U+0C7F`).
- Filters short or junk lines.
- Output:
  ```
  final_cleaned_telugu_data_1.txt
  ```

#### b) Kaggle Data Cleaning (`2_clean_corpus.py`)
- Cleans the Kaggle text file (`corpus.txt`) using identical rules.
- Removes non-Telugu content and short fragments.
- Output:
  ```
  final_cleaned_telugu_data_2.txt
  ```

---

### 3️⃣ Tokenization and Vocabulary Generation

#### a) Tokenization for Wikipedia/Web Data (`4_tokenization_vocabulary_1.py`)
#### b) Tokenization for Kaggle Data (`5_tokenization_vocabulary_2.py`)

Both scripts:
- Split text into sentences (`.` delimiter).
- Extract Telugu tokens using:
  ```
  [\u0C00-\u0C7F]+
  ```
- Build:
  - Sentence text file (`telugu_sentences_*.txt`)
  - Tokenized JSON (`telugu_tokenized_sentences_*.json`)
  - Vocabulary (`telugu_vocabulary_*.txt`)

**Example Output**
```
Saved 152,000 sentences to 'telugu_sentences_1.txt'
Saved 957,000 unique words to 'telugu_vocabulary_1.txt'
```

---

### 4️⃣ Final Merge (`6_merge.py`)

Combines both data sources into unified datasets.

| Input Files | Output File |
|--------------|--------------|
| `final_cleaned_telugu_data_1.txt`, `final_cleaned_telugu_data_2.txt` | `final_cleaned_telugu_data.txt` |
| `telugu_vocabulary_1.txt`, `telugu_vocabulary_2.txt` | `telugu_vocabulary.txt` |
| `telugu_tokenized_sentences_1.json`, `telugu_tokenized_sentences_2.json` | `telugu_tokenized_sentences.json` |

**Merge Features**
- Deduplicates using `set()` to avoid repeated sentences.
- Combines and sorts all unique vocabulary terms.
- Merges tokenized JSON files while preserving structure.

**Example Output**
```
Total sentences: 320,000 → final_cleaned_telugu_data.txt
Unique vocabulary: 959,857 → telugu_vocabulary.txt
Unique tokenized sentences: 1,036,856 → telugu_tokenized_sentences.json
```

---

### Directory Structure

```
📂 Telugu_Data_Preprocessing
 ┣ 📜 0_scrape_wiki.py
 ┣ 📜 1_clean_wiki.py
 ┣ 📜 2_clean_corpus.py
 ┣ 📜 3_web_scrapping.ipynb
 ┣ 📜 4_tokenization_vocabulary_1.py
 ┣ 📜 5_tokenization_vocabulary_2.py
 ┣ 📜 6_merge.py
 ┣ 📄 merged_telugu_wikipedia_data.txt
 ┣ 📄 corpus.txt
 ┣ 📄 final_cleaned_telugu_data_1.txt
 ┣ 📄 final_cleaned_telugu_data_2.txt
 ┣ 📄 final_cleaned_telugu_data.txt
 ┣ 📄 telugu_sentences_1.txt
 ┣ 📄 telugu_sentences_2.txt
 ┣ 📄 telugu_vocabulary_1.txt
 ┣ 📄 telugu_vocabulary_2.txt
 ┣ 📄 telugu_vocabulary.txt
 ┣ 📄 telugu_tokenized_sentences_1.json
 ┣ 📄 telugu_tokenized_sentences_2.json
 ┗ 📄 telugu_tokenized_sentences.json
```

---

### Dependencies

Install dependencies:
```bash
pip install wikipedia beautifulsoup4 requests tqdm regex
```

Most scripts use standard Python libraries:
- `re`, `json`, `hashlib`, `multiprocessing`, `os`, `time`

---

### Final Outputs

| File | Description |
|------|--------------|
| `final_cleaned_telugu_data.txt` | Final merged and cleaned Telugu corpus |
| `telugu_vocabulary.txt` | Combined vocabulary from all sources |
| `telugu_tokenized_sentences.json` | Tokenized sentence dataset |
| `*_1.*` | Processed files for Wikipedia + Web Story data |
| `*_2.*` | Processed files for Kaggle corpus data |

---

### Future Work

- Automate the full pipeline into a single execution script.  
- Integrate Indic NLP tools for sentence segmentation and POS tagging.  
- Expand scraping sources for greater linguistic variety.  

---

## Sentence Completion using HMM N-gram Model

### Overview

This module implements a trigram (3-gram) Hidden Markov Model for Telugu language modeling. The model supports next-word prediction, sentence completion, and perplexity evaluation. I have used add-one (Laplace) smoothing and a backoff strategy to make predictions more robust.

---

### Model Architecture

#### Bigram Model (BigramHMM)

- **Order:** 2-gram (bigram)
- **Context:** Uses 1 previous word
- **Smoothing:** Add-one (Laplace)
- **Formula:** P(w₂|w₁) = (count(w₁→w₂) + 1) / (count(w₁) + |V|)

#### Trigram Model (HMMNGramModel)

- **Order:** 3-gram (trigram)
- **Context:** Uses 2 previous words
- **Smoothing:** Add-one (Laplace)
- **Special Tokens:** `<s>` (start), `</s>` (end)
- **Backoff Strategy:** Trigram → Bigram
- **Formula:** P(word|context) = (count(context, word) + 1) / (count(context) + |V|)

---

### Dataset

#### Required Files

```
telugu_tokenized_sentences_final.json  # Contains 1,036,856 tokenized sentences
telugu_vocabulary_final.txt            # Contains 959,857 unique vocabulary words
```

### How to Run

#### 1. Setup and Dependencies

```python
import re
import math
import json
from collections import defaultdict, Counter
import pickle
```

All dependencies are from Python's standard library, so no additional installation is needed.

#### 2. Load Training Data

```python
# Load tokenized sentences
with open('telugu_tokenized_sentences_final.json', 'r', encoding='utf-8') as f:
    tokenized_sentences = json.load(f)

# Load vocabulary
with open('telugu_vocabulary_final.txt', 'r', encoding='utf-8') as f:
    vocab = {line.strip() for line in f if line.strip()}

print(f"Loaded {len(tokenized_sentences)} sentences and {len(vocab)} vocab words.")
```

#### 3. Train the Model

```python
from hmm_ngram_model import HMMNGramModel

# Initialize trigram model
model = HMMNGramModel(n=3)

# Train on large dataset
model.train(tokenized_sentences, vocab=vocab)

# Calculate perplexity
perplexity = model.perplexity(tokenized_sentences)
print(f"Perplexity: {perplexity}")
```

#### 4. Use the Model

##### Next-Word Prediction

```python
word = "సూర్య"
predictions = model.predict_next([word], top_k=3)
print(f"Predictions: {predictions}")
# Output: [('చంద్ర', 6.25e-06), ('చంద్రులు', 4.17e-06), ('భరత్', 4.17e-06)]
```

##### Sentence Completion

```python
seed = "వాణిజ్యం"
completed_sentence = model.complete_sentence(seed, max_len=20)
print(f"Completed: {completed_sentence}")
#Completed: వాణిజ్యం సంస్కృతి వృద్ధి చెందేందుకు అనుమతించింది
```

---

### Running the Jupyter Notebook

#### Open the Notebook

```bash
jupyter notebook SentenceCompletion_HMM_Integration.ipynb
```

#### Notebook Sections

1. **Data Loading & Tokenization** (Cells 1-4)
2. **Bigram Model Implementation** (Cells 5-12)
3. **HMM N-gram Integration** (Cells 13-17)
4. **Final Testing on Large Dataset** (Cells 18-29)
---

### Example Results

#### Model Performance

```
Training Data: 1,036,856 sentences
Vocabulary Size: 959,857 words
Perplexity: 2.532
```

#### Sample Predictions

| Input Word | Top Prediction | Completed Sentence |
|------------|----------------|-------------------|
| పన్నెండున్నరకి | తన (2.08e-06) | పన్నెండున్నరకి తన ఫ్లాట్ కి తాళం వేసి వుంది |
| సూర్య | చంద్ర (6.25e-06) | సూర్య చంద్ర కు భూలోకమ్మ చెప్పిన మాటలు గుర్తొచ్చాయి |
| చదువు | పూర్తి (6.25e-06) | చదువు పూర్తి అయింది |
| రాము | పెద్దగా (3.13e-06) | రాము పెద్దగా నవ్వుకుంటూ తుర్రున బయటకు పరుగెత్తింది |
| సైనికులు | క్రమశిక్షణకి (2.08e-06) | సైనికులు క్రమశిక్షణకి అలవాటుపడినవారు కాబట్టి... |
| వాణిజ్యం | సంస్కృతి (2.08e-06) | వాణిజ్యం సంస్కృతి వృద్ధి చెందేందుకు అనుమతించింది |
| ఇల్లు | కూడా (9.37e-06) | ఇల్లు కూడా అమ్మి అప్పులన్నీ తీర్చేశాడు |
| పరిశుభ్రత | విషయంలో (2.08e-06) | పరిశుభ్రత విషయంలో శ్రద్ధ తీసుకోవడం లేదేమోనని... |

---

### Key Functions

#### HMMNGramModel Class

| Method | Description | Parameters |
|--------|-------------|------------|
| `train(sentences, vocab)` | Trains the model on tokenized sentences | `sentences`: list, `vocab`: set |
| `predict_next(context, top_k)` | Predicts next words with probabilities | `context`: str/list, `top_k`: int |
| `complete_sentence(seed, max_len)` | Generates a complete sentence | `seed`: str, `max_len`: int |
| `perplexity(test_sentences)` | Calculates model perplexity | `test_sentences`: list |
| `get_probability(context, word)` | Gets P(word\|context) | `context`: tuple, `word`: str |
| `tokenize_telugu_sentence(sentence)` | Tokenizes Telugu text | `sentence`: str |

---


---

# Sentence Completion — N-gram + GRU Reranker

This module implements a **Telugu sentence completion system** using a **trigram N-gram model** combined with a **GRU-based deep learning reranker**.  
It is designed for efficient sentence continuation using a large tokenized corpus while balancing fluency and contextual relevance.

---

## Overview

### Pipeline Summary
1. **N-gram model (Trigram + Unigram):**
   - Learns token probabilities from the Telugu corpus.
   - Generates top candidate next-words for a given context.
   - Computes unigram and trigram probabilities for use by reranker.

2. **GRU Reranker:**
   - Encodes the context sequence and scores candidate tokens.
   - Uses features: GRU-encoded context, candidate embedding, and n-gram + unigram log-probabilities.
   - Trained with binary classification to prefer true continuations.

3. **Sentence Completion:**
   - Combines N-gram predictions with GRU scores.
   - Uses repetition penalties, sampling temperature, and fluency heuristics.
   - Produces step-by-step completions with interpretive logs.

---

## File Structure

| File | Description |
|------|--------------|
| `10 SentenceCompletion_Ngram_GRU.ipynb` | Main notebook containing all code chunks (1–9). |
| `telugu_tokenized_sentences.json` | Tokenized Telugu sentences (list of token lists). |
| `telugu_vocabulary.txt` | Optional vocabulary file (one word per line). |
| `gru_reranker.pt` | Trained GRU reranker model checkpoint. |

---

## Configuration (`CONFIG` block)

| Key | Meaning | Default |
|-----|----------|----------|
| `tokenized_json` | Path to tokenized Telugu corpus. | `"telugu_tokenized_sentences.json"` |
| `vocab_txt` | Optional vocab file path. | `"telugu_vocabulary.txt"` |
| `ngram_n` | N-gram order (3 = trigram). | `3` |
| `train_samples` | Number of sampled contexts for reranker training. | `20000` |
| `top_k` | Number of candidate words per context. | `12` |
| `negs_per_pos` | Negative samples per positive. | `2` |
| `vocab_size` | Vocabulary size limit for embedding. | `30000` |
| `embed_dim`, `hidden_size` | Embedding & GRU hidden dimensions. | `256` |
| `batch_size` | Training batch size. | `64` |
| `epochs` | Training epochs. | `5` |
| `lr` | Learning rate. | `1e-3` |
| `device` | `"cpu"` or `"cuda"` (if GPU available). | `"cpu"` |

---

## How to Run

**Setup and Dependencies**
```python
import os
import json
import math
import random
import pickle
import time
from collections import defaultdict, Counter
from tqdm import tqdm
import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
```

1. **Prepare Data**
   - Place `telugu_tokenized_sentences.json` in the working directory.
   - Optionally include `telugu_vocabulary.txt`.

2. **Train N-gram Model**
   ```python
   ngram = NGramModel(n=3)
   ngram.train(corpus)
   ```

3. **Generate Training Pairs**
   ```python
   pairs = sample_training_pairs_optimized(corpus, ngram, CONFIG["train_samples"],
                                           CONFIG["top_k"], CONFIG["negs_per_pos"])
   ```

4. **Train GRU Reranker**
   ```python
   model = GRUReranker(vocab_size, emb_dim=CONFIG["embed_dim"], hidden=CONFIG["hidden_size"]).to(device)
   # Run CHUNK 8: training loop
   ```

5. **Save Model**
   ```python
   torch.save({
       "model_state": model.state_dict(),
       "word2idx": word2idx,
       "idx2word": idx2word
   }, "gru_reranker.pt")
   ```

6. **Inference**
   ```python
   complete_sentence_gru_fluent("నేను పుస్తకం", ngram, model, word2idx, idx2word, "cpu")
   ```

---

## Example Output

```
Prefix tokens: ['నేను', 'పుస్తకం']

Step 1 — context: నేను పుస్తకం
   తెరిచి             -> 0.2723
   చదువుకుంటున్నాను   -> 0.1357
   ...
Selected (best): తెరిచి

...
Completed sentence (joined): నేను పుస్తకం తెరిచి పేజీలు తిప్పి చూశాడు అనుమానంగా
```

---

## Tips

- Use **streaming datasets** for large corpora to save memory.
- Increase `max_ctx_len` (default 4) for better contextual understanding.
- To improve fluency:
  - Enable temperature sampling (`sample_T=0.8`).
  - Apply unigram boost (`alpha=0.15`).
  - Use cumulative repetition penalty (`0.85`).

---

## Model Checkpoints

- **`gru_reranker.pt`** — PyTorch checkpoint with:
  - `model_state`: GRU weights
  - `word2idx`, `idx2word`: vocabulary maps

Load example:
```python
ckpt = torch.load("gru_reranker.pt", map_location="cpu")
model = GRUReranker(len(ckpt["word2idx"]))
model.load_state_dict(ckpt["model_state"])
model.eval()
```

---

## Evaluation Metrics

- **Perplexity (N-gram)**: Measures language model quality.
- **Top-1 accuracy (Reranker)**: Evaluated on 5% held-out validation pairs.

---

## Dependencies

```bash
pip install torch numpy tqdm
```

---

## License

MIT License — free to use, modify, and distribute for research and educational purposes.


---

## Telugu Spell Correction using Seq2Seq + Hybrid Model

### Overview

This module implements a **character-level sequence-to-sequence (Seq2Seq)** model with **Luong attention** for **Telugu word spell correction**.  
It combines a **deep learning approach** (Bidirectional LSTM Encoder–Decoder) with a **rule-based Levenshtein distance mechanism**, forming a **hybrid correction system**.  
The model corrects noisy or misspelled Telugu words and enhances performance through **beam search decoding** and **confidence-based hybrid re-ranking**.

---

### Model Architecture

#### Seq2Seq Model (Encoder–Decoder with Attention)

- **Encoder:** Bidirectional LSTM  
- **Decoder:** LSTM with Attention mechanism  
- **Embedding Dimension:** 64  
- **Latent Dimension:** 128  
- **Attention Type:** Luong-style global attention  
- **Regularization:** Dropout + Layer Normalization  
- **Optimizer:** Adam (learning rate = 3e-4, clipnorm = 1.0)  
- **Loss Function:** Sparse categorical cross-entropy  

**Equation (simplified):**  
For each output token y_t,  
P(y_t | y_{<t}, x) = softmax(W_c [h_t; c_t])  
where c_t is the context vector computed via attention over encoder outputs.

---

### Hybrid Correction Module (Levenshtein + Seq2Seq Confidence)

- **Candidate Generation:** Filters top candidates using Levenshtein distance.  
- **Confidence Scoring:** Uses the trained Seq2Seq model to compute prediction confidence.  
- **Hybrid Decision:** Selects the candidate with the highest model confidence; if none found, falls back to beam search output.  

**Distance Metric:**  
d(a, b) = min edit distance between strings a, b

---

### Dataset

#### Required File

```
telugu_word_correction_pairs.json  # Contains noisy → correct Telugu word pairs
```

Each record is a dictionary with two keys:
```json
{
  "input": "భారదేతశం",
  "target": "భారతదేశం"
}
```

#### Data Split
| Dataset | Size | Description |
|----------|------|-------------|
| Training | 30,000 pairs | Model fitting |
| Validation | 10,000 pairs | Early stopping & tuning |
| Testing | 5,000 pairs | Evaluation accuracy |

---

### How to Run

#### 1. Setup and Dependencies

```python
import os, json, random, numpy as np, tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense, Embedding, Bidirectional, Attention, Concatenate, Dropout
from tqdm import tqdm
```

If not already installed:
```bash
pip install tensorflow numpy tqdm
```

#### 2. Load Dataset

```python
with open('telugu_word_correction_pairs.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Loaded {len(data)} word pairs.")
```

#### 3. Train the Model

```python
# Define and compile model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train
history = model.fit(train_dataset,
                    validation_data=val_dataset,
                    epochs=10,
                    batch_size=128)
```

The model automatically saves the best checkpoint and final weights in:
```
saved_models/
 ┣ seq2seq_best.keras
 ┗ seq2seq_final.keras
```

#### 4. Use the Model

##### a) Greedy & Beam Search Predictions

```python
test_word = "భారదేతశం"

greedy_pred = beam_search_predict(model, test_word, beam_width=1)
beam_pred = beam_search_predict(model, test_word, beam_width=3)

print("Greedy:", greedy_pred)
print("Beam Search:", beam_pred)
```

##### b) Hybrid Correction

```python
hybrid_pred = hybrid.correct_word(test_word, max_suggestions=3, max_distance=1)
print("Hybrid Correction:", hybrid_pred)
```

---

### Example Results

#### Sample Predictions

| Noisy Input | Target | Greedy Seq2Seq | Beam Search (w=3) | Hybrid (Levenshtein + DL) |
|--------------|---------|----------------|-------------------|----------------------------|
| భారదేతశం | భారతదేశం | భారదేటం | భారతదేశం | భారతదేశం |
| ముహూర్త్ | ముహూర్తం | ముహూర్తం | ముహూర్తం | ముహూర్తం |
| ప్రవేశమ్ | ప్రవేశం | ప్రవేశం | ప్రవేశం | ప్రవేశం |
| సూర్య | సూర్యుడు | సూర్య | సూర్యుడు | సూర్యుడు |

#### Accuracy Comparison
| Method | Accuracy (N=50) |
|--------|----------------|
| Greedy Seq2Seq | 82.0% |
| Beam Search | 86.0% |
| **Hybrid Model** | **92.0%** |

---

### Running the Jupyter Notebook

#### Open the Notebook

```bash
jupyter notebook SpellChecker_Levenshtein_LSTM.ipynb
```

#### Notebook Sections

1. **Dataset Loading & Preprocessing** (Cells 1–5)  
2. **Vocabulary Encoding** (Cells 6–8)  
3. **Model Construction (Encoder–Decoder + Attention)** (Cells 9–18)  
4. **Training with EarlyStopping and Checkpointing** (Cells 19–25)  
5. **Beam Search Decoder Implementation** (Cells 26–30)  
6. **Hybrid Spell Checker Integration** (Cells 31–40)  
7. **Evaluation and Testing** (Cells 41–50)  

---

### Example Outputs

```
Noisy : భారదేతశం
Target: భారతదేశం
Greedy Seq2Seq → భారదేటం
Beam Search (width=3) → భారతదేశం
Hybrid (Levenshtein + DL) → భారతదేశం
------------------------------------------------------------
Hybrid Accuracy (N=50): 92.00%
Beam Search Accuracy (N=50): 86.00%
```

---

### Key Classes and Functions

#### HybridSpellChecker

| Method | Description | Parameters |
|--------|-------------|-------------|
| `correct_word(noisy_word, max_suggestions, max_distance)` | Performs hybrid correction using Levenshtein + Seq2Seq | `noisy_word`: str |
| `candidates_by_levenshtein(noisy_word)` | Generates nearby word candidates | `max_suggestions`, `max_distance` |
| `seq2seq_confidence(enc_seq, candidate)` | Computes Seq2Seq-based confidence score | `enc_seq`: encoded tensor |
| `levenshtein(a, b)` | Computes edit distance between words | `a`, `b`: str |

#### beam_search_predict

| Parameter | Description |
|------------|-------------|
| `beam_width` | Number of candidate beams to keep |
| `length_penalty` | Controls sequence length bias |
| `max_repeat` | Avoids character repetition |
| **Returns:** Predicted corrected word |

---

### Model Performance

```
Training Data: 30,000 word pairs
Validation Data: 10,000 pairs
Embedding Dim: 64
Latent Dim: 128
Final Validation Accuracy: ~79%
Hybrid Evaluation Accuracy: ~84%
```

---

### Environment

| Library | Version |
|----------|----------|
| Python | 3.11.x |
| TensorFlow | 2.20.0 |
| Keras | 3.12.0 |
| NumPy | 2.2.6 |
| tqdm | 4.67.1 |
| pandas | 2.2.2 |
| matplotlib | 3.9.2 |
| OS | Windows 10 (64-bit) |

---

### Future Work

- Integrate Transformer-based models (e.g., T5, mBART).  
- Collect real-world noisy Telugu text for data augmentation.  
- Extend correction to sentence-level context using contextual embeddings.

---

### Author

**Hemanth (S20230030389)**  
*Deep Learning & NLP Project — Telugu Spell Correction using Seq2Seq + Hybrid Model*  
Developed using **TensorFlow 2.20** and **Jupyter Notebook**.  


---

# Telugu Grammar Checker

A rule-based NLP system that detects grammatical errors in **Telugu sentences** — including subject–verb agreement, tense consistency, and double negations.

---

## Features

- Detects **grammar inconsistencies** using linguistic rules  
- Combines **Stanza** (for POS tagging & dependency parsing) with **custom rules**  
- Checks for:
  - Subject–verb agreement  
  - Tense consistency  
  - gender mismatch
  - Case/postposition errors  
  - Negation conflicts

---

## How to Run

Ensure dependencies are installed and the Stanza Telugu model is downloaded.

Open the Jupyter notebook telugu_grammar_checker.ipynb

Execute the cells or script.

Provide a Telugu sentence in the last cell

The system prints whether the sentence is correct or lists grammar error(s) with explanations.


## Example Outputs

✓ Sentence Correct: నేను ఆపిల్ తిన్నాను

✖ Sentence: నేను ఆపిల్ తిన్నాము
 - Subject–verb number mismatch (నేను vs తిన్నాము)

✓ Sentence Correct: మేము ఆపిల్ తిన్నాము

✓ Sentence Correct: వారు వస్తున్నారు

✖ Sentence: ఆమె తిన్నాడు
 - Gender disagreement between ఆమె and తిన్నాడు

✓ Sentence Correct: ఆపిల్ ను తినాను

✖ Sentence: నేను తినలేదు లేదు
 - Double negatives: తినలేదు లేదు

---

