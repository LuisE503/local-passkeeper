# 🚀 Quick Start Guide - Local Passkeeper

Get started with Local Passkeeper in 5 minutes!

## Prerequisites

- **Rust**: Version 1.75 or later
- **Cargo**: Comes with Rust
- **Git**: For cloning (optional)

## Installation

### Option 1: Build from Source

```bash
# Navigate to project directory
cd c:\Users\Usuario\Desktop\PX\Administrador_contraseñas

# Build the project
cargo build --release

# Binary will be at: ./target/release/passkeeper.exe
```

### Option 2: Install with Cargo (after publishing)

```bash
cargo install passkeeper
```

### Option 3: Use Docker

```bash
# Build Docker image
docker-compose build

# Run passkeeper in container
docker-compose run passkeeper --help
```

## First Steps

### 1. Create Your First Vault

```bash
passkeeper init my-passwords.vault
```

You'll be prompted to create a master password. Choose a strong password!

```
Enter master password: ************
Confirm password: ************
✅ Vault created: my-passwords.vault
```

### 2. Add Your First Credential

```bash
passkeeper add --vault my-passwords.vault
```

Follow the interactive prompts:

```
Title: GitHub
Username: myusername
Password: (leave empty to generate) 
Generate password? [Y/n]: y
URL: https://github.com
Notes: Personal GitHub account
Tags (comma-separated): work,development
Mark as favorite? [y/N]: y

✅ Credential added successfully!
```

### 3. Retrieve a Credential

```bash
passkeeper get --vault my-passwords.vault --title GitHub
```

Output:

```
╭──────────────────────────────────╮
│ GitHub                    ⭐     │
├──────────────────────────────────┤
│ Username: myusername             │
│ Password: ••••••••••••••••••••   │
│ URL: https://github.com          │
│ Tags: work, development          │
│ Created: 2024-01-20 10:30:15     │
╰──────────────────────────────────╯

[Copy Password] [Copy Username] [Edit] [Delete]
```

### 4. List All Credentials

```bash
passkeeper list --vault my-passwords.vault
```

### 5. Run Security Audit

```bash
passkeeper audit --vault my-passwords.vault
```

Output:

```
╔══════════════════════════════════════════════════════════════╗
║                    SECURITY AUDIT REPORT                      ║
╚══════════════════════════════════════════════════════════════╝

Total Credentials: 1
Strong Passwords: 1 (100%)
Weak Passwords: 0
Reused Passwords: 0

Overall Security Score: 100/100 ████████████████████ 

✅ Excellent! Your vault is secure.
```

## Common Commands

### Generate a Strong Password

```bash
passkeeper generate --length 24 --symbols
```

### Search Credentials

```bash
passkeeper search --vault my-passwords.vault --query "github"
```

### Update a Credential

```bash
passkeeper update --vault my-passwords.vault --title "GitHub"
```

### Create Backup

```bash
passkeeper backup --vault my-passwords.vault --output backup.vault.enc
```

### View Statistics

```bash
passkeeper stats --vault my-passwords.vault
```

### Export to JSON

```bash
passkeeper export --vault my-passwords.vault --output export.json
```

## Essential Tips

### 💡 Master Password

- **Choose wisely**: This password cannot be recovered if forgotten
- **Minimum 12 characters** recommended
- **Use a passphrase**: e.g., "correct-horse-battery-staple"
- **Never share** your master password

### 💡 Backup Your Vault

```bash
# Create encrypted backup regularly
passkeeper backup --vault my-passwords.vault --output ~/backups/passwords-$(date +%Y%m%d).enc
```

### 💡 Security Best Practices

- Run `passkeeper audit` regularly
- Update weak passwords immediately
- Use unique passwords for each service
- Enable 2FA on accounts when available
- Keep vault file secure (not in cloud folders without encryption)

### 💡 Tags for Organization

```bash
# Use tags to organize credentials
--tags work,email            # Work email
--tags personal,social       # Social media
--tags banking,critical      # Banking
--tags development,github    # Development tools
```

### 💡 Command Shortcuts

```bash
# Set alias in your shell profile
alias pk='passkeeper --vault my-passwords.vault'

# Now you can use:
pk add
pk get --title GitHub
pk list
pk audit
```

## Keyboard Shortcuts (CLI)

- `Ctrl+C`: Cancel operation
- `Ctrl+D`: Exit interactive prompt
- `Tab`: Auto-complete (in some terminals)
- `↑/↓`: Navigate command history

## Example Workflow

```bash
# Morning routine: Access your passwords
pk open my-passwords.vault

# Add new account
pk add
# ... interactive prompts ...

# Search for credentials
pk search --query "amazon"

# Get specific credential
pk get --title "Amazon"

# Run weekly security audit
pk audit

# Update weak password
pk update --title "OldSite"

# Create backup before changes
pk backup --output ~/backups/weekly-backup.enc

# View statistics
pk stats
```

## Troubleshooting

### Problem: "Vault file not found"

**Solution**: Specify the full path to your vault file:

```bash
passkeeper add --vault C:\Users\Usuario\Documents\my-vault.vault
```

### Problem: "Invalid master password"

**Solution**: Make sure you're entering the correct master password. There's no recovery if forgotten!

### Problem: "Permission denied"

**Solution**: Vault files are locked to your user account. Make sure you have read/write permissions.

### Problem: Commands not found

**Solution**: Add Cargo bin to your PATH:

```bash
# Windows (PowerShell)
$env:PATH += ";$HOME\.cargo\bin"

# Linux/macOS
export PATH="$HOME/.cargo/bin:$PATH"
```

## Next Steps

### 📚 Learn More

- Read the full [README](README.md)
- Check [examples/](examples/) for more usage scenarios
- Read [SECURITY.md](SECURITY.md) for security details

### 🤝 Contribute

- Read [CONTRIBUTING.md](CONTRIBUTING.md)
- Check open issues on GitHub
- Submit feature requests
- Report bugs

### 🔒 Stay Secure

- Enable scheduled audits (coming soon)
- Consider hardware key support (roadmap)
- Set up automatic backups
- Read security best practices

## Get Help

- **Command help**: `passkeeper --help`
- **Command-specific help**: `passkeeper add --help`
- **Documentation**: See [README.md](README.md)
- **Issues**: https://github.com/LuisE503/local-passkeeper/issues
- **Discussions**: https://github.com/LuisE503/local-passkeeper/discussions

---

**Ready to secure your passwords?** 🔐

```bash
passkeeper init my-secure-vault.vault
```

Happy password managing! 🎉
