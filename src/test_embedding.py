from sentence_transformers import SentenceTransformer

print("Loading ML model... (this downloads the model the first time you run it)")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Our test sentence
sentence = "The bank's overall risk profile was stable."
print(f"\nSentence: '{sentence}'")

# Convert the English string into Math!
vector = model.encode(sentence)

print(f"\nThis sentence was converted into a vector with {len(vector)} numbers!")
print("Here are the first 5 numbers of that vector:")
print(vector[:5])
