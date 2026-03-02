# 🔐 Local Passkeeper

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Un administrador de contraseñas local seguro con GUI moderna y Frase de Rescate BIP39.**

Local Passkeeper es un gestor de contraseñas de código abierto diseñado para usuarios conscientes de su seguridad que desean un control total sobre sus credenciales. Todos los datos se almacenan localmente y se cifran con algoritmos estándar de la industria (AES-256-GCM). Sin sincronización en la nube: sus contraseñas permanecen en su máquina.

[English](../README.md) | [Español](README.es.md) | [中文](README.zh-CN.md) | [Português](README.pt.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [العربية](README.ar.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

## ✨ Características

- 🔒 **Cifrado de grado militar**: Claves de cifrado de datos (DEK) protegidas por AES-256-GCM.
- 🔑 **Frase de recuperación BIP39**: ¡Recuperación mnemotécnica de 12 palabras de emergencia!
- 🖥️ **GUI Moderna**: Aplicación de Windows con tema oscuro al estilo 1Password en Python.
- 🌐 **Multi-idioma**: 10 idiomas incorporados.
- 📦 **Local-first**: No necesita Internet. La bóveda es únicamente tuya.
- 🤝 **Código abierto**: Diseñado como base o portafolio.

## 🚀 Inicio Rápido (Windows)

1. Localiza el archivo `Passkeeper.exe` en la carpeta `dist/Passkeeper/`.
2. Haz doble clic en la aplicación.
3. El Asistente Visual te guiará para crear una contraseña maestra y te dará 12 palabras secretas. **¡Anótalas en un cuaderno!**

## 💻 Desarrolladores y Código Fuente

Instalación con Python 3.9+:

```bash
git clone https://github.com/LuisE503/local-passkeeper.git
cd local-passkeeper
python -m venv .venv
.venv\Scriptsctivate
pip install -e .
pip install customtkinter cryptography pydantic mnemonic pillow

passkeeper
```

## 🏗️ Arquitectura de Criptografía (DEK/KEK)
Su archivo `vault.json` almacena una Llave de Encriptación de Datos (DEK). 
Esta DEK interna está envuelta independientemente por dos matrices matemáticas: tú Contraseña Maestra o tú Frase de Recuperación. 

## 📄 Licencia
MIT License.
