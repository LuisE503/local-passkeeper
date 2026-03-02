import os
import base64
from typing import Tuple
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

def derive_key(password: str, salt: bytes) -> bytes:
    """Derives a strong 256-bit encryption key from a password using Scrypt."""
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1,
    )
    return kdf.derive(password.encode())

def encrypt(data: str, key: bytes) -> Tuple[str, str]:
    """Encrypts plaintext data using AES-256-GCM. Returns (ciphertext, nonce) encoded in base64."""
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # Recommended 96-bit nonce for GCM
    
    ciphertext = aesgcm.encrypt(nonce, data.encode('utf-8'), None)
    
    return base64.b64encode(ciphertext).decode('utf-8'), base64.b64encode(nonce).decode('utf-8')

def decrypt(ciphertext_b64: str, nonce_b64: str, key: bytes) -> str:
    """Decrypts base64 AES-GCM ciphertext using the given key and nonce."""
    aesgcm = AESGCM(key)
    ciphertext = base64.b64decode(ciphertext_b64)
    nonce = base64.b64decode(nonce_b64)
    
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode('utf-8')

def encrypt_bytes(data: bytes, key: bytes) -> Tuple[bytes, bytes]:
    """Encrypts raw bytes using AES-256-GCM. Returns (ciphertext, nonce)."""
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, data, None)
    return ciphertext, nonce

def decrypt_bytes(ciphertext: bytes, nonce: bytes, key: bytes) -> bytes:
    """Decrypts raw bytes using AES-256-GCM."""
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None)

def generate_salt() -> bytes:
    """Generates a random 16-byte salt."""
    return os.urandom(16)
