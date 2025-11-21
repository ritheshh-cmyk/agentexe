import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

def generate_keys():
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # Serialize private key
    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Generate public key
    public_key = private_key.public_key()
    
    # Serialize public key
    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Write keys to files
    with open("server/private_key.pem", "wb") as f:
        f.write(pem_private)
    
    with open("server/public_key.pem", "wb") as f:
        f.write(pem_public)
        
    with open("client/public_key.pem", "wb") as f:
        f.write(pem_public)

    print("Keys generated successfully!")
    print("Server: private_key.pem, public_key.pem")
    print("Client: public_key.pem")

if __name__ == "__main__":
    generate_keys()
