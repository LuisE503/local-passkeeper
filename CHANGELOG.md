# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned

- Browser extension integration (Chrome, Firefox, Edge)
- Import from popular password managers (1Password, LastPass, Bitwarden, KeePass)
- Optional P2P synchronization (end-to-end encrypted)
- Hardware security key support (YubiKey, FIDO2/WebAuthn)
- Scheduled automatic security audits with notifications
- Tauri-based GUI application
- Mobile applications (iOS/Android)
- TOTP/2FA code generation
- Secure password sharing
- Passkey/WebAuthn support

## [0.1.0] - 2026-02-28

### Added

#### Core Features
- **Vault Management**
  - Create and manage encrypted password vaults
  - AES-256-GCM encryption with authentication
  - Argon2id key derivation (3 iterations, 64 MiB memory cost)
  - Master password protection with zeroize for secure memory cleanup
  
- **Credential Operations**
  - Add new credentials with title, username, password, URL, notes, tags
  - Retrieve credentials by title or URL
  - Update existing credentials
  - Delete credentials with confirmation
  - List all credentials with filtering and sorting
  - Search across all fields (title, username, URL, notes, tags)
  - Tag management for organization
  - Favorite credentials for quick access
  
- **Password Management**
  - Generate strong random passwords (configurable length and complexity)
  - Configurable character sets (uppercase, lowercase, digits, symbols)
  - Password strength indicator
  - Copy passwords to clipboard with auto-clear (optional)
  
- **Security Audit**
  - Detect weak passwords (entropy analysis, pattern detection)
  - Find reused passwords across multiple credentials
  - Identify old passwords that should be rotated
  - Generate detailed audit reports with recommendations
  - Security scoring (0-100 scale)
  
- **Backup & Export**
  - Create encrypted backups of vaults
  - Export to JSON format
  - Import from JSON
  - Change master password
  
- **Statistics**
  - Display vault statistics (total credentials, by tag, favorites, weak passwords)
  - Password age distribution
  - Security health overview

#### CLI Interface
- **Commands Implemented**
  - `init` - Create new vault
  - `add` - Add credential
  - `get` - Retrieve credential
  - `list` - List all credentials
  - `update` - Update credential
  - `delete` - Delete credential
  - `search` - Search credentials
  - `audit` - Run security audit
  - `generate` - Generate password
  - `stats` - Show vault statistics
  - `backup` - Create encrypted backup
  - `export` - Export to JSON
  - `import` - Import from JSON
  - `change-master` - Change master password
  
- **User Experience**
  - Colored terminal output for better readability
  - Interactive password prompts (hidden input)
  - Table formatting for credential lists
  - Progress indicators
  - Clear error messages
  - Confirmation prompts for destructive operations

#### Security
- **Encryption**
  - AES-256-GCM (Galois/Counter Mode) for authenticated encryption
  - ChaCha20-Poly1305 as alternative cipher (ready for use)
  - 256-bit encryption keys
  - 96-bit random nonces (unique per encryption)
  - 128-bit authentication tags
  
- **Key Derivation**
  - Argon2id algorithm (winner of Password Hashing Competition)
  - 3 iterations (time cost)
  - 65,536 KB memory cost (64 MiB)
  - 4 parallel threads
  - Random 256-bit salt per vault
  
- **Memory Safety**
  - Passwords zeroized from memory after use
  - Rust's memory safety guarantees
  - No unsafe code blocks in core crypto
  
- **File Security**
  - Unix: 0600 permissions (owner read/write only)
  - Windows: ACLs restrict to current user
  - `.vault` files are encrypted blobs
  - No plaintext credential storage

#### Testing
- **Core Module Tests**
  - Encryption/decryption round-trip tests
  - Key derivation verification
  - Vault CRUD operation tests
  - Password generation tests
  - Search functionality tests
  - Tag and favorite tests
  - Error handling tests
  
- **Audit Module Tests**
  - Weak password detection tests
  - Password reuse detection
  - Old password identification
  - Audit scoring tests
  - False positive checks

#### DevOps
- **Docker Support**
  - Production Dockerfile (multi-stage build)
  - Development Dockerfile with tools
  - Docker Compose configuration
  - Build scripts
  
- **GitHub Actions**
  - CI workflow (build, test, clippy, formatting)
  - Release workflow (cross-platform binaries)
  - Security audit workflow (cargo-audit, clippy security)
  - Documentation workflow (build and deploy docs)
  
- **Code Quality**
  - Rustfmt configuration
  - Clippy lints enabled
  - Cargo.toml workspace organization

#### Documentation
- **README Files**
  - English (main README.md)
  - Spanish (docs/README.es.md)
  - Chinese Simplified (docs/README.zh-CN.md)
  - Portuguese (docs/README.pt.md)
  - French (docs/README.fr.md)
  - German (docs/README.de.md)
  - Arabic (docs/README.ar.md)
  - Russian (docs/README.ru.md)
  - Japanese (docs/README.ja.md)
  - Korean (docs/README.ko.md)
  
- **Project Documentation**
  - CONTRIBUTING.md - Contribution guidelines
  - SECURITY.md - Security policy and vulnerability reporting
  - LICENSE - MIT License
  - CHANGELOG.md - This file
  
- **Examples**
  - Basic usage shell script
  - Advanced workflow shell script
  - Programmatic API usage example
  - Sample vault with test data
  
- **Issue Templates**
  - Browser Extension Integration (#1)
  - Import from Password Managers (#2)
  - Optional P2P Sync (#3)
  - Hardware Key Support (#4)
  - Scheduled Security Audits (#5)
  - Bug Report template
  - GitHub issue configuration

#### Architecture
- **Cargo Workspace**
  - `core` - Core library with encryption, storage, and vault logic
  - `cli` - Command-line interface application
  - `audit` - Security auditing module
  
- **Dependencies**
  - `aes-gcm 0.10` - AES-256-GCM encryption
  - `argon2 0.5` - Key derivation
  - `clap 4.5` - CLI framework
  - `serde 1.0` - Serialization
  - `uuid 1.10` - Unique identifiers
  - `chrono 0.4` - Date/time handling
  - `ring 0.17` - Additional cryptography
  - `base64 0.21` - Encoding
  - `zeroize 1.7` - Secure memory clearing
  - `rpassword 7.3` - Password prompting
  - `colored 2.1` - Terminal colors
  - `dialoguer 0.11` - Interactive prompts
  - `tabled 0.15` - Table formatting
  - `thiserror 1.0` - Error handling

### Security

- ✅ All cryptographic operations use industry-standard algorithms
- ✅ No plaintext password storage
- ✅ Memory is zeroized after use
- ✅ File permissions restrict vault access
- ✅ Test coverage for security-critical code
- ✅ No unsafe Rust in crypto code
- ✅ Dependencies audited with cargo-audit

### Known Limitations

- Master password cannot be recovered if forgotten
- No built-in cloud sync (local-first by design)
- CLI only (GUI planned for future release)
- Single-user vaults (no sharing yet)
- No hardware key support yet
- No TOTP/2FA code generation
- Manual audit required (automatic scheduling planned)

## [0.0.1] - 2024-01-15 (Initial Commit)

### Added
- Project structure initialization
- Basic Cargo workspace setup
- Initial README

---

## Release Types

- **Major version** (X.0.0): Breaking changes, major new features
- **Minor version** (0.X.0): New features, backwards compatible
- **Patch version** (0.0.X): Bug fixes, performance improvements

## Links

- [Repository](https://github.com/LuisE503/local-passkeeper)
- [Issues](https://github.com/LuisE503/local-passkeeper/issues)
- [Releases](https://github.com/LuisE503/local-passkeeper/releases)
- [Discussions](https://github.com/LuisE503/local-passkeeper/discussions)
