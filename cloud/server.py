import json, tenseal as ts, base64, sys

def load_context():
    with open("client/output/context.seal", "rb") as f:
        return ts.context_from(f.read())

def load_encrypted_index():
    data = json.load(open("cloud/encrypted_index.json"))
    return data["vocab"], data["index"]

def search_encrypted(keyword):
    vocab, enc_index = load_encrypted_index()
    context = load_context()

    if keyword not in vocab:
        print("❌ Keyword not in vocabulary.")
        return

    query_vec = [1 if w == keyword else 0 for w in vocab]
    enc_query = ts.bfv_vector(context, query_vec)

    results = {}
    for doc, enc_bytes_str in enc_index.items():
        enc_bytes = base64.b64decode(enc_bytes_str.encode("utf-8"))
        enc_vec = ts.bfv_vector_from(context, enc_bytes)
        enc_score = enc_vec.dot(enc_query)
        results[doc] = base64.b64encode(enc_score.serialize()).decode("utf-8")

    with open("cloud/encrypted_results.json", "w") as f:
        json.dump(results, f)

    print(f"✅ Encrypted results computed for '{keyword}'.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        keyword = sys.argv[1].strip().lower()
    else:
        keyword = input("Enter the keyword to search: ").strip().lower()
    search_encrypted(keyword)
