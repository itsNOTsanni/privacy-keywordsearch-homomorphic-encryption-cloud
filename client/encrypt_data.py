import os, json, tenseal as ts, base64

def load_context():
    with open("client/output/context.seal", "rb") as f:
        return ts.context_from(f.read())

def tokenize(text):
    return text.lower().replace('.', '').split()

def build_encrypted_index():
    context = load_context()
    vocab = []
    docs_enc = {}

    # Build vocabulary
    for fname in os.listdir("client/data"):
        text = open(f"client/data/{fname}").read()
        vocab.extend(tokenize(text))
    vocab = sorted(list(set(vocab)))
    print("📘 Vocabulary:", vocab)

    # Encrypt document vectors
    for fname in os.listdir("client/data"):
        text = open(f"client/data/{fname}").read()
        tokens = tokenize(text)
        bitvector = [1 if word in tokens else 0 for word in vocab]
        enc_vec = ts.bfv_vector(context, bitvector)
        docs_enc[fname] = base64.b64encode(enc_vec.serialize()).decode("utf-8")

    os.makedirs("cloud", exist_ok=True)
    with open("cloud/encrypted_index.json", "w") as f:
        json.dump({"vocab": vocab, "index": docs_enc}, f)

    print("✅ Encrypted index uploaded to cloud!")

if __name__ == "__main__":
    build_encrypted_index()
