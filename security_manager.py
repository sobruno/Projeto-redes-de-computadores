import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class SecurityManager:
    def __init__(self, role):
        self.base_dir = role
        self.keys_dir = os.path.join(self.base_dir, "keys")
        os.makedirs(self.keys_dir, exist_ok=True)
        self.private_key, self.public_key = self._load_or_generate_keys()

    def _load_or_generate_keys(self):
        priv_path = os.path.join(self.keys_dir, "private.pem")
        pub_path = os.path.join(self.keys_dir, "public.pem")

        if os.path.exists(priv_path):
            with open(priv_path, "rb") as f:
                private_key = serialization.load_pem_private_key(f.read(), password=None)
            public_key = private_key.public_key()
        else:
            private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
            public_key = private_key.public_key()
            with open(priv_path, "wb") as f:
                f.write(private_key.private_bytes(
                    serialization.Encoding.PEM,
                    serialization.PrivateFormat.PKCS8,
                    serialization.NoEncryption()
                ))
            with open(pub_path, "wb") as f:
                f.write(public_key.public_bytes(
                    serialization.Encoding.PEM,
                    serialization.PublicFormat.SubjectPublicKeyInfo
                ))
        return private_key, public_key

    def public_bytes(self):
        return self.public_key.public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def fingerprint(self, pub_bytes=None):
        data = pub_bytes if pub_bytes else self.public_bytes()
        digest = hashes.Hash(hashes.SHA256())
        digest.update(data)
        return digest.finalize().hex()

    def encrypt_key(self, aes_key, target_pub_bytes):
        pub = serialization.load_pem_public_key(target_pub_bytes)
        return pub.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def decrypt_key(self, encrypted_key):
        return self.private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
