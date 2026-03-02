# 🚀 Guía de Instalación - Local Passkeeper

Esta guía te ayudará a instalar y configurar Local Passkeeper desde cero.

## 📋 Requisitos Previos

### 1. Instalar Rust

Local Passkeeper está escrito en Rust, por lo que necesitas tener Rust instalado:

#### Windows

1. Descarga rustup desde: https://rustup.rs/
2. Ejecuta el instalador `rustup-init.exe`
3. Sigue las instrucciones (opción por defecto es recomendada)
4. Reinicia tu terminal después de la instalación

Verifica la instalación:
```powershell
rustc --version
cargo --version
```

#### Linux/macOS

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

Verifica la instalación:
```bash
rustc --version
cargo --version
```

### 2. Instalar Git (Opcional)

Si quieres clonar el repositorio:

- **Windows**: Descarga desde https://git-scm.com/download/win
- **Linux**: `sudo apt install git` (Ubuntu/Debian) o `sudo dnf install git` (Fedora)
- **macOS**: `brew install git` (requiere Homebrew)

## 📦 Métodos de Instalación

### Opción 1: Compilar desde Código Fuente (Recomendado)

#### Paso 1: Obtener el Código

```bash
# Clonar el repositorio
git clone https://github.com/LuisE503/local-passkeeper.git
cd local-passkeeper

# O descargar ZIP desde GitHub y extraer
```

#### Paso 2: Compilar el Proyecto

```bash
# Compilar en modo release (optimizado)
cargo build --release

# Los binarios estarán en: ./target/release/
```

#### Paso 3: Instalar Globalmente (Opcional)

```bash
# Instalar passkeeper en tu sistema
cargo install --path cli

# Ahora puedes usar 'passkeeper' desde cualquier ubicación
passkeeper --version
```

### Opción 2: Instalar Directamente desde Cargo (Cuando esté publicado)

```bash
cargo install passkeeper
```

### Opción 3: Usar Docker

#### Construir la Imagen

```bash
# Construir imagen de producción
docker build -t local-passkeeper .

# O usar docker-compose
docker-compose build
```

#### Usar la Imagen

```bash
# Ejecutar passkeeper en container
docker run -v $(pwd)/vaults:/data local-passkeeper --help

# Con docker-compose
docker-compose run passkeeper --help
```

## ✅ Verificación de la Instalación

### 1. Verificar que el Proyecto Compile

```bash
cd local-passkeeper
cargo build --all
```

Deberías ver algo como:
```
   Compiling passkeeper-core v0.1.0
   Compiling passkeeper-audit v0.1.0
   Compiling passkeeper v0.1.0
    Finished dev [unoptimized + debuginfo] target(s) in X.XXs
```

### 2. Ejecutar Tests

```bash
cargo test --all
```

Todos los tests deberían pasar:
```
test result: ok. XX passed; 0 failed; 0 ignored; 0 measured
```

### 3. Ejecutar el CLI

```bash
# Si instalaste globalmente
passkeeper --version

# O desde el directorio del proyecto
./target/release/passkeeper --version
```

Deberías ver:
```
passkeeper 0.1.0
```

## 🎯 Primeros Pasos

### 1. Crear tu Primera Bóveda

```bash
passkeeper init mi-passwords.vault
```

Te pedirá una contraseña maestra:
```
🔐 Crear Nueva Bóveda: mi-passwords.vault

Contraseña maestra: ************
Confirmar contraseña: ************

✅ Bóveda creada exitosamente!
```

### 2. Añadir tu Primera Credencial

```bash
passkeeper add --vault mi-passwords.vault
```

Sigue las indicaciones interactivas:
```
Título: GitHub
Usuario: mi-usuario
Contraseña: (deja vacío para generar)
¿Generar contraseña? [S/n]: s
URL: https://github.com
Notas: Cuenta personal de GitHub
Etiquetas (separadas por comas): trabajo,desarrollo

✅ Credencial añadida exitosamente!
```

### 3. Ver tus Credenciales

```bash
passkeeper list --vault mi-passwords.vault
```

### 4. Ejecutar Auditoría de Seguridad

```bash
passkeeper audit --vault mi-passwords.vault
```

## 🔧 Configuración Avanzada

### Crear Alias (Recomendado)

Para evitar escribir `--vault` cada vez:

#### Windows (PowerShell)

Añade a tu perfil de PowerShell (`$PROFILE`):
```powershell
function pk { passkeeper --vault "C:\ruta\a\tu\vault.vault" $args }
```

Luego usa:
```powershell
pk list
pk add
pk audit
```

#### Linux/macOS (Bash/Zsh)

Añade a tu `~/.bashrc` o `~/.zshrc`:
```bash
alias pk='passkeeper --vault ~/mis-passwords.vault'
```

Luego usa:
```bash
pk list
pk add
pk audit
```

### Variable de Entorno

Establece la variable `PASSKEEPER_VAULT`:

#### Windows (PowerShell)

```powershell
# Sesión actual
$env:PASSKEEPER_VAULT = "C:\ruta\a\tu\vault.vault"

# Permanente (usuario)
[System.Environment]::SetEnvironmentVariable('PASSKEEPER_VAULT', 'C:\ruta\a\tu\vault.vault', 'User')
```

#### Linux/macOS

```bash
# Añadir a ~/.bashrc o ~/.zshrc
export PASSKEEPER_VAULT=~/mi-passwords.vault
```

Ahora puedes usar:
```bash
passkeeper list
passkeeper add
```

## 🐛 Solución de Problemas

### Error: "cargo: command not found"

- **Causa**: Rust no está instalado o no está en el PATH
- **Solución**: Instala Rust siguiendo los pasos de arriba y reinicia tu terminal

### Error: "linker 'cc' not found"

- **Linux**: Instala build essentials: `sudo apt install build-essential`
- **macOS**: Instala Xcode Command Line Tools: `xcode-select --install`
- **Windows**: Instala Visual Studio Build Tools desde https://visualstudio.microsoft.com/downloads/

### Error: "openssl-sys" compilation failed

**Windows**: Necesitas OpenSSL. Dos opciones:

1. Instalar OpenSSL precompilado:
   ```powershell
   # Usando Chocolatey
   choco install openssl
   
   # O descargar desde: https://slproweb.com/products/Win32OpenSSL.html
   ```

2. Usar características alternativas (más fácil):
   ```bash
   cargo build --release --no-default-features
   ```

**Linux**:
```bash
# Ubuntu/Debian
sudo apt install pkg-config libssl-dev

# Fedora
sudo dnf install pkgconf openssl-devel
```

**macOS**:
```bash
brew install openssl
```

### El Proyecto no Compila

1. Verifica que tienes la versión correcta de Rust:
   ```bash
   rustc --version
   # Debe ser 1.75.0 o superior
   ```

2. Actualiza Rust:
   ```bash
   rustup update
   ```

3. Limpia y reconstruye:
   ```bash
   cargo clean
   cargo build --release
   ```

### Los Tests Fallan

1. Asegúrate de estar en el directorio del proyecto
2. Ejecuta los tests con más información:
   ```bash
   cargo test --all -- --nocapture
   ```

3. Si un test específico falla, ejecuta solo ese test:
   ```bash
   cargo test nombre_del_test -- --nocapture
   ```

## 📚 Siguientes Pasos

Una vez instalado:

1. **Lee el [QUICKSTART.md](QUICKSTART.md)** para comenzar a usar passkeeper
2. **Consulta el [README.md](README.md)** para documentación completa
3. **Explora [examples/](examples/)** para ejemplos de uso
4. **Lee [SECURITY.md](SECURITY.md)** para entender la seguridad del sistema

## 🆘 Obtener Ayuda

Si tienes problemas:

1. **Documentación**: Lee la documentación completa en [docs/](docs/)
2. **Issues**: Busca o crea un issue en GitHub
3. **Discussions**: Participa en GitHub Discussions
4. **Help Command**: Usa `passkeeper --help` para ayuda del CLI

## 🔄 Actualización

Para actualizar a la última versión:

```bash
# Si instalaste con cargo install
cargo install passkeeper --force

# Si compilaste desde fuente
cd local-passkeeper
git pull
cargo build --release
cargo install --path cli --force
```

## 🎉 ¡Listo!

Ahora tienes Local Passkeeper instalado y listo para usar. ¡Disfruta de una gestión de contraseñas segura y local!

---

**Importante**: Recuerda que tu contraseña maestra es la clave de tu bóveda. Si la pierdes, tus datos no podrán recuperarse. ¡Manténla segura!

Para más ayuda, visita: https://github.com/LuisE503/local-passkeeper
