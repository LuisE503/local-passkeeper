# 🔐 Local Passkeeper

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A secure, local-first password manager with a modern GUI and BIP39 Recovery Phrase.**

Local Passkeeper is a professional, open-source password manager designed for security-conscious users who want full control over their credentials. All data is stored locally and encrypted with industry-standard AES-256-GCM algorithms. No cloud sync—your passwords stay on your machine.

[English](../README.md) | [Español](docs/README.es.md) | [中文](README.zh-CN.md) | [Português](docs/README.pt.md) | [Français](docs/README.fr.md) | [Deutsch](docs/README.de.md) | [العربية](docs/README.ar.md) | [Русский](docs/README.ru.md) | [日本語](docs/README.ja.md) | [한국어](docs/README.ko.md)

## ✨ Features

- 🔒 **Military-grade encryption**: Data Encryption Keys (DEK) wrapped by AES-256-GCM.
- 🔑 **BIP39 Recovery Phrase**: 12-word recovery mnemonic if you ever forget your master password!
- 🖥️ **Modern GUI**: 1Password-style dark-themed Windows application written in Python & CustomTkinter.
- 🌐 **Multi-language**: 10 built-in languages.
- 📦 **Local-first**: No internet connection required. Your zero-knowledge vault is yours alone.
- 🤝 **100% Open Source**: Designed as a scalable base for contributors.

## 🚀 Quick Start (Windows)

We provide a ready-to-use executable file! No terminal required.

1. Locate `Passkeeper.exe` in the `dist/Passkeeper/` directory.
2. Double click the Application.
3. The Setup Wizard will guide you to create your Master Password and provide your 12-word Recovery Phrase. **Write it down safely!**

## 💻 Developer & Source Installation

If you want to run from source code (Python 3.9+ required):

```bash
git clone https://github.com/LuisE503/local-passkeeper.git
cd local-passkeeper

# Create virtual environment and install dependencies
python -m venv .venv
.venv\Scriptsctivate
pip install -e .
pip install customtkinter cryptography pydantic mnemonic pillow

# Run the app
passkeeper
```

### Compiling to .exe
```bash
pip install pyinstaller
python build_gui.py
```

## 🏗️ Architecture (DEK/KEK)

Our cryptographic model ensures absolute security while allowing recovery:
- Your `vault.json` holds an encrypted **Data Encryption Key (DEK)**.
- The DEK is independently wrapped twice: once by your Master Password (KEK) and once by your 12-word Recovery Phrase (KEK).
- This means you can unlock the DB using either your password OR your phrase without them conflicting.

## 🤝 Contributing
Contributions are welcome!

## 📄 License
MIT License.
