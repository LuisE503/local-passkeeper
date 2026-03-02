import json
import os
import base64
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel
from mnemonic import Mnemonic
from passkeeper.core import crypto

class Credential(BaseModel):
    id: str
    name: str
    username: str
    password_cipher: str
    nonce: str
    url: Optional[str] = None
    tags: List[str] = []

class VaultData(BaseModel):
    salt_b64: str
    dek_cipher_master_b64: str = ""
    dek_nonce_master_b64: str = ""
    dek_cipher_recovery_b64: str = ""
    dek_nonce_recovery_b64: str = ""
    
    # Old validation fields for backwards compatibility with vaults from Phase 1
    verification_b64: str = ""
    verification_nonce_b64: str = ""
    credentials: List[Credential] = []

class Vault:
    def __init__(self, master_password: str, vault_path: Path):
        self.master_password = master_password
        self.vault_path = vault_path
        self.salt = b""
        self.key = b""
        self.data = VaultData(salt_b64="", credentials=[])
        self.mnemo = Mnemonic("english")
        
    def generate_recovery_phrase(self) -> str:
        """Generates a secure 12-word BIP39 recovery phrase."""
        return self.mnemo.generate(strength=128)

    def initialize_new(self, recovery_phrase: Optional[str] = None):
        """Initializes a completely new vault with a random Data Encryption Key (DEK)."""
        self.salt = crypto.generate_salt()
        self.data.salt_b64 = base64.b64encode(self.salt).decode('utf-8')
        
        kek_master = crypto.derive_key(self.master_password, self.salt)
        
        if recovery_phrase:
            # 1. Generate random Data Encryption Key (DEK) for the credentials
            self.key = os.urandom(32) # AES-256 takes 32 bytes
            
            # 2. Encrypt DEK with the Master Password
            c_master, n_master = crypto.encrypt_bytes(self.key, kek_master)
            self.data.dek_cipher_master_b64 = base64.b64encode(c_master).decode('utf-8')
            self.data.dek_nonce_master_b64 = base64.b64encode(n_master).decode('utf-8')
            
            # 3. Encrypt DEK with the Recovery Phrase
            kek_recovery = crypto.derive_key(recovery_phrase, self.salt)
            c_rec, n_rec = crypto.encrypt_bytes(self.key, kek_recovery)
            self.data.dek_cipher_recovery_b64 = base64.b64encode(c_rec).decode('utf-8')
            self.data.dek_nonce_recovery_b64 = base64.b64encode(n_rec).decode('utf-8')
            
        else:
            # Backwards compatible initialization if no phrase is provided
            self.key = kek_master
            c, n = crypto.encrypt("passkeeper-magic", self.key)
            self.data.verification_b64 = c
            self.data.verification_nonce_b64 = n
            
        self.save()

    def load(self, provided_recovery_phrase: Optional[str] = None):
        """Loads an existing vault from disk. Extracts DEK via Master Password or Recovery Phrase."""
        if not self.vault_path.exists():
            raise FileNotFoundError("Vault file not found. Initialize first.")
            
        with open(self.vault_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            
        self.data = VaultData(**raw_data)
        self.salt = base64.b64decode(self.data.salt_b64)
        
        kek_master = crypto.derive_key(self.master_password, self.salt)
        valid_dek = None
        
        # 1. Is it a modern vault using DEK/KEK?
        if self.data.dek_cipher_master_b64 and self.data.dek_nonce_master_b64:
            # Normal login attempt (Master Password)
            if not provided_recovery_phrase:
                try:
                    c_master = base64.b64decode(self.data.dek_cipher_master_b64)
                    n_master = base64.b64decode(self.data.dek_nonce_master_b64)
                    valid_dek = crypto.decrypt_bytes(c_master, n_master, kek_master)
                except Exception:
                    pass
                    
            # Rescue attempt (Recovery Phrase and new Master Password)
            if not valid_dek and provided_recovery_phrase:
                kek_recovery = crypto.derive_key(provided_recovery_phrase, self.salt)
                try:
                    c_rec = base64.b64decode(self.data.dek_cipher_recovery_b64)
                    n_rec = base64.b64decode(self.data.dek_nonce_recovery_b64)
                    valid_dek = crypto.decrypt_bytes(c_rec, n_rec, kek_recovery)
                    
                    # If rescue successful, re-wrap the DEK using the NEW Master Password
                    c_new, n_new = crypto.encrypt_bytes(valid_dek, kek_master)
                    self.data.dek_cipher_master_b64 = base64.b64encode(c_new).decode('utf-8')
                    self.data.dek_nonce_master_b64 = base64.b64encode(n_new).decode('utf-8')
                    # Note: We do NOT re-generate the recovery DEK ciphertext, so the original 12 words still work.
                except Exception:
                    pass
                    
            if not valid_dek:
                 raise ValueError("Incorrect master password or invalid recovery phrase.")
            self.key = valid_dek
            
        # 2. Is it a legacy vault (Phase 1) without DEK?
        elif self.data.verification_b64 and self.data.verification_nonce_b64:
            try:
                dec = crypto.decrypt(self.data.verification_b64, self.data.verification_nonce_b64, kek_master)
                if dec == "passkeeper-magic":
                    valid_dek = kek_master
            except Exception:
                pass
                
            if not valid_dek:
                raise ValueError("Incorrect master password (legacy vault).")
            self.key = valid_dek
        else:
            raise ValueError("Corrupted Vault. No encryption signatures found.")

    def save(self):
        """Saves current vault state to disk."""
        self.vault_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.vault_path, "w", encoding="utf-8") as f:
            f.write(self.data.model_dump_json(indent=2))

    def add_credential(self, cred: Credential):
        self.data.credentials.append(cred)
        self.save()

    def list_credentials(self) -> List[Credential]:
        return self.data.credentials

    def encrypt_password(self, password: str) -> Tuple[str, str]:
        """Encrypts a generic password string returning cipher and nonce."""
        return crypto.encrypt(password, self.key)

    def decrypt_password(self, cipher: str, nonce: str) -> str:
        """Decrypts a stored password."""
        return crypto.decrypt(cipher, nonce, self.key)
