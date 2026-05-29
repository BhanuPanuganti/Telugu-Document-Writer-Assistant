import random
import string
import json
import os

# --- Configuration Constants ---
TELUGU_CHARS = "అఆఇఈఉఊఋఎఏఐఒఓఔకఖగఘఙచఛజఝఞటఠడఢణతథదధనపఫబభమయరఱలళవశషసహఁంః"
ALL_CHARS = string.ascii_lowercase + " " + TELUGU_CHARS

# --- Data Generation Functions ---

def load_vocabulary(filename="telugu_vocabulary.txt"):
    """Loads vocabulary from file. Creates dummy if not found."""
    if not os.path.exists(filename):
        print(f"Warning: '{filename}' not found. Creating dummy vocabulary file.")
        dummy_words = [
            "అందరూ", "కంప్యూటరు", "తెలుగు", "మాటలు", "ప్రపంచము", 
            "సాహిత్యం", "కృషి", "విద్యార్థి", "పరీక్ష", "విజ్ఞానం"
        ]
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write('\n'.join(dummy_words))
            print(f"Created dummy file with {len(dummy_words)} words.")
        except IOError as e:
            print(f"Error creating dummy file: {e}")
            return dummy_words

    try:
        with open(filename, "r", encoding="utf-8") as f:
            vocab_words = [w.strip().replace(" ", "") for w in f if w.strip()]
    except Exception as e:
        print(f"Error reading vocabulary file: {e}")
        return []
    
    # Remove duplicates and very short words
    vocab_words = [w for w in list(set(vocab_words)) if len(w) >= 3]
    return vocab_words

def make_typo(word):
    """Generates a single typo (edit distance 1) in a word."""
    if len(word) < 3:
        return word
    
    typo_type = random.choice(['delete', 'insert', 'swap', 'replace'])
    
    if typo_type == 'delete':
        i = random.randint(0, len(word) - 1)
        return word[:i] + word[i+1:]
        
    elif typo_type == 'insert':
        i = random.randint(0, len(word))
        char = random.choices(
            population=list(TELUGU_CHARS + string.ascii_lowercase + " "),
            weights=[0.7]*len(TELUGU_CHARS) + [0.3/27]*27, k=1
        )[0]
        return word[:i] + char + word[i:]
        
    elif typo_type == 'swap' and len(word) >= 2:
        i = random.randint(0, len(word) - 2)
        return word[:i] + word[i+1] + word[i] + word[i+2:]
        
    elif typo_type == 'replace':
        i = random.randint(0, len(word) - 1)
        char = random.choices(
            population=list(TELUGU_CHARS + string.ascii_lowercase + " "),
            weights=[0.7]*len(TELUGU_CHARS) + [0.3/27]*27, k=1
        )[0]
        return word[:i] + char + word[i+1:]
    
    return word

def generate_batch(vocab_words, start_idx, end_idx, typo_multiplier=5):
    """Generates a batch of training pairs from start_idx to end_idx."""
    batch_pairs = []
    seen_pairs = set() 

    for w in vocab_words[start_idx:end_idx]:
        batch_pairs.append({"input": w, "target": w})
        seen_pairs.add((w, w))

        typos_generated = 0
        attempts = 0
        max_attempts = typo_multiplier * 3  

        while typos_generated < typo_multiplier and attempts < max_attempts:
            attempts += 1
            typo_word = make_typo(w)
            if typo_word != w and (typo_word, w) not in seen_pairs:
                batch_pairs.append({"input": typo_word, "target": w})
                seen_pairs.add((typo_word, w))
                typos_generated += 1

    random.shuffle(batch_pairs)
    return batch_pairs


def save_data_in_batches(vocab_words, filename="telugu_word_correction_pairs.json", batch_size=10000, typo_multiplier=5):
    """Generates training pairs and writes them to JSON file in batches."""
    if os.path.exists(filename):
        print(f"⚠ Warning: '{filename}' exists and will be overwritten.")
    
    total_words = len(vocab_words)
    print(f"Total words: {total_words}, Batch size: {batch_size}")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("[\n")
        first_item = True
        
        for start in range(0, total_words, batch_size):
            end = min(start + batch_size, total_words)
            batch = generate_batch(vocab_words, start, end, typo_multiplier)
            
            for pair in batch:
                if not first_item:
                    f.write(",\n")
                json.dump(pair, f, ensure_ascii=False)
                first_item = False
            print(f" Batch {start // batch_size + 1} written ({end-start} words).")
        
        f.write("\n]")  
    print(f"\n All batches written to '{filename}' successfully.")


if __name__ == "__main__":
    VOCAB_FILENAME = "telugu_vocabulary.txt"
    OUTPUT_FILENAME = "telugu_word_correction_pairs.json"
    TYPO_MULTIPLIER = 4
    BATCH_SIZE = 5000 

    vocab_words = load_vocabulary(VOCAB_FILENAME)
    
    if not vocab_words:
        print("Fatal Error: Vocabulary is empty. Cannot generate data.")
        exit(1)
    else:
        print(f"Total Unique Words Loaded: {len(vocab_words)}")
    
    save_data_in_batches(vocab_words, filename=OUTPUT_FILENAME, batch_size=BATCH_SIZE, typo_multiplier=TYPO_MULTIPLIER)

    print("\nFirst 5 Sample Pairs:")
    with open(OUTPUT_FILENAME, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for pair in data[:5]:
            print(f"Input: '{pair['input']}' -> Target: '{pair['target']}'")
