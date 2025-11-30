import json, tenseal as ts, base64, os

def load_context():
    with open("client/output/context.seal", "rb") as f:
        return ts.context_from(f.read())

def decrypt_results():
    context = load_context()
    data = json.load(open("cloud/encrypted_results.json"))
    results = {}

    for doc, enc_str in data.items():
        enc_bytes = base64.b64decode(enc_str.encode("utf-8"))
        enc_score = ts.bfv_vector_from(context, enc_bytes)
        score = enc_score.decrypt()[0]
        results[doc] = score

    os.makedirs("results", exist_ok=True)
    with open("results/result_1.json", "w") as f:
        json.dump(results, f, indent=2)

    print("🔓 Results decrypted in results/result_1.json")
    print("📄 Results:", results)

if __name__ == "__main__":
    decrypt_results()
