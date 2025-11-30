import tenseal as ts
import pickle, os

def generate_keys():
    context = ts.context(
        ts.SCHEME_TYPE.BFV,
        poly_modulus_degree=8192,
        plain_modulus=1032193
    )
    context.generate_galois_keys()
    context.generate_relin_keys()

    os.makedirs("client/output", exist_ok=True)
    with open("client/output/context.seal", "wb") as f:
        f.write(context.serialize(save_secret_key=True))

    print("✅ Keys generated and saved in client/output/")

if __name__ == "__main__":
    generate_keys()
