# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Currently supported versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Security Philosophy

Local Passkeeper is designed with security as the top priority:

- **Local-first**: No data sent to external servers by default
- **Strong encryption**: AES-256-GCM with Argon2id key derivation
- **Zero-knowledge**: Only you have access to your master password
- **Open source**: Transparent, auditable code
- **Minimal dependencies**: Reduced attack surface

## Threat Model

### What We Protect Against

- ✅ Unauthorized access to encrypted vaults
- ✅ Password database theft (encrypted at rest)
- ✅ Weak password usage
- ✅ Password reuse across services
- ✅ Memory dumps (passwords are zeroized)
- ✅ Brute-force attacks on master password

### What We Cannot Protect Against

- ❌ Compromised system (keyloggers, malware)
- ❌ Physical access to unlocked vault
- ❌ Lost/forgotten master password
- ❌ Social engineering attacks
- ❌ Rubber-hose cryptanalysis

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

### How to Report

1. **Email**: Send details to security@local-passkeeper.org (if available) or create a private security advisory on GitHub

2. **GitHub Security Advisory**: 
   - Go to the [Security tab](https://github.com/LuisE503/local-passkeeper/security)
   - Click "Report a vulnerability"
   - Fill in the details

### What to Include

- **Description**: Clear description of the vulnerability
- **Impact**: What an attacker could do
- **Reproduction**: Step-by-step instructions to reproduce
- **Affected versions**: Which versions are affected
- **Patches**: If you have a fix, include it

### Example Report

```
Subject: [SECURITY] Potential timing attack in password verification

Description:
The master password verification function may be vulnerable to timing 
attacks due to non-constant-time comparison.

Impact:
An attacker with local access could potentially determine password 
length through timing analysis.

Affected Versions:
0.1.0 - 0.1.5

Reproduction:
1. Create a vault with a known password
2. Try authentication with passwords of varying lengths
3. Measure response times
4. Observe correlation between response time and password length

Suggested Fix:
Use constant-time comparison from the `subtle` crate.
```

## Response Timeline

- **Initial Response**: Within 48 hours
- **Assessment**: Within 1 week
- **Fix Development**: Within 2 weeks (critical issues)
- **Public Disclosure**: After fix is deployed

## Security Updates

Security updates will be:
- Released as patch versions (e.g., 0.1.5 → 0.1.6)
- Announced in release notes
- Tagged with `security` label
- Published to GitHub Security Advisories

## Security Best Practices

### For Users

1. **Master Password**
   - Use a strong, unique master password
   - Minimum 16 characters recommended
   - Mix of uppercase, lowercase, numbers, symbols
   - Never share or write down
   - Use a passphrase: e.g., "correct-horse-battery-staple"

2. **Vault Protection**
   - Keep vault files secure (restrictive permissions)
   - Never commit vault files to version control
   - Create regular encrypted backups
   - Store backups in secure locations

3. **System Security**
   - Keep your OS and software updated
   - Use full-disk encryption
   - Use antivirus/antimalware software
   - Be cautious of suspicious programs
   - Lock your computer when away

4. **Regular Audits**
   - Run `passkeeper audit` regularly
   - Update weak passwords
   - Remove old/unused credentials
   - Check for password reuse

### For Developers

1. **Code Review**
   - All crypto code must be reviewed by security-conscious developers
   - Use established, well-tested crypto libraries
   - Never roll your own crypto

2. **Dependencies**
   - Regularly update dependencies
   - Run `cargo audit` in CI
   - Review dependency changes
   - Minimize dependency count

3. **Memory Safety**
   - Use `zeroize` for sensitive data
   - Avoid unnecessary copies of secrets
   - Clear sensitive data from memory ASAP
   - Use secure allocators when appropriate

4. **Testing**
   - Write security-focused tests
   - Test error conditions
   - Test boundary cases
   - Use fuzzing for input validation

## Known Security Considerations

### Current Implementation

1. **Master Password Storage**
   - Master password is never stored
   - Derived key is stored in memory only while vault is open
   - Memory is zeroized when vault is locked

2. **File Permissions**
   - Unix: Vault files set to 0600 (owner read/write only)
   - Windows: ACLs restrict access to current user

3. **Encryption**
   - AES-256-GCM: Authenticated encryption
   - Argon2id: Memory-hard key derivation
   - Random salts per vault (256 bits)
   - Random nonces per encryption (96 bits)

### Future Enhancements

- [ ] Support for hardware security keys (YubiKey, etc.)
- [ ] Optional two-factor authentication
- [ ] Encrypted clipboard with auto-clear
- [ ] Secure password sharing
- [ ] Audit logging

## Security Audits

We welcome security audits from the community:

- **Code Reviews**: Always appreciated
- **Pentesting**: Contact us first
- **Fuzzing**: Run fuzzing tools and report findings
- **Static Analysis**: Use tools like `cargo-geiger`

## Cryptographic Details

### Algorithms

- **Encryption**: AES-256-GCM (NIST approved, FIPS 140-2)
- **Key Derivation**: Argon2id (winner of Password Hashing Competition)
- **Random Generation**: OS-level CSPRNG via `rand` crate

### Parameters

```rust
// Argon2id parameters
iterations: 3        // Time cost
memory: 65536 KB     // Memory cost (64 MiB)
parallelism: 4       // Threads
salt: 32 bytes       // Random per-vault salt

// AES-256-GCM
key: 32 bytes        // Derived from master password
nonce: 12 bytes      // Random per-encryption
tag: 16 bytes        // Authentication tag
```

### Key Derivation Process

1. User enters master password
2. Retrieve vault's unique salt
3. Derive 256-bit key using Argon2id
4. Use derived key for AES-256-GCM encryption/decryption
5. Zeroize key from memory when done

## Compliance

- **GDPR**: No data collection, fully local
- **CCPA**: No personal data shared
- **SOC 2**: N/A (self-hosted solution)

## Responsible Disclosure

We follow responsible disclosure:

1. Researcher reports vulnerability privately
2. We confirm and assess the issue
3. We develop and test a fix
4. We release the fix
5. Public disclosure after users have time to update (typically 90 days)

## Bug Bounty

Currently, we do not have a formal bug bounty program. However, we deeply appreciate security research and will:

- Acknowledge contributors in release notes
- List researchers in a security hall of fame (with permission)
- Provide recognition in documentation

## Contact

- **Security Email**: security@local-passkeeper.org (if available)
- **GitHub Security Advisory**: [Report a vulnerability](https://github.com/LuisE503/local-passkeeper/security/advisories/new)
- **PGP Key**: [Available here] (if applicable)

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [Rust Security Guidelines](https://anssi-fr.github.io/rust-guide/)
- [Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

---

Thank you for helping keep Local Passkeeper secure! 🔒
