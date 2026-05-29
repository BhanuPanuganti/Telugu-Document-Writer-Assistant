import json

#  Merge cleaned data

cleaned_files = ["final_cleaned_telugu_data_1.txt", "final_cleaned_telugu_data_2.txt"]
cleaned = set()

for file in cleaned_files:
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            word = line.strip()
            if word:
                cleaned.add(word)

with open("final_cleaned_telugu_data.txt", "w", encoding="utf-8") as f:
    for word in sorted(cleaned):
        f.write(word + "\n")

print(f"Total sentences: {len(cleaned):,} → final_cleaned_telugu_data.txt")


# Merge vocabulary files

voc_files = ["telugu_vocabulary_1.txt", "telugu_vocabulary_2.txt"]
vocabulary = set()

for file in voc_files:
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            word = line.strip()
            if word:
                vocabulary.add(word)

with open("telugu_vocabulary.txt", "w", encoding="utf-8") as f:
    for word in sorted(vocabulary):
        f.write(word + "\n")

print(f"Unique vocabulary: {len(vocabulary):,} → telugu_vocabulary.txt")


#  Merge tokenized JSON files

tok_files = ["telugu_tokenized_sentences_1.json", "telugu_tokenized_sentences_2.json"]
tokens_seen = set()
unique_tokenized_sentences = []

for file in tok_files:
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
        for tok_list in data:
            tok_tuple = tuple(tok_list)
            if tok_tuple not in tokens_seen:
                tokens_seen.add(tok_tuple)
                unique_tokenized_sentences.append(tok_list)

with open("telugu_tokenized_sentences.json", "w", encoding="utf-8") as f:
    json.dump(unique_tokenized_sentences, f, ensure_ascii=False, indent= 2)

print(f"Unique tokenized sentences: {len(unique_tokenized_sentences):,} → telugu_tokenized_sentences.json")