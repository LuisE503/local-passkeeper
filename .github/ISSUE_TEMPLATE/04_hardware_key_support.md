---
name: Hardware Key Support
about: Add support for hardware security keys (YubiKey, FIDO2/WebAuthn)
title: '[FEATURE] Hardware Key Support'
labels: enhancement, security, hardware
assignees: ''
---

## Description

Implement support for hardware security keys (YubiKey, FIDO2/WebAuthn, U2F) as an additional authentication factor or as an alternative to traditional master passwords.

## Motivation

Hardware security keys provide:
- **Stronger authentication**: Physical possession required
- **Phishing resistance**: Cannot be stolen remotely
- **Convenience**: Tap to unlock (no typing)
- **Enterprise compliance**: Meets security standards
- **Protection**: Even if master password is compromised

## Proposed Solution

### Supported Keys

1. **YubiKey** (all models with FIDO2/U2F)
2. **Google Titan Security Key**
3. **Feitian ePass FIDO**
4. **Thetis FIDO U2F**
5. **Any FIDO2/WebAuthn compatible key**

### Authentication Modes

```rust
enum AuthMode {
    // Existing: master password only
    Password,                  
    
    // New modes:
    PasswordAndKey,            // 2FA: password + hardware key (most secure)
    KeyOnly,                   // Hardware key derives key (no password)
    PasswordOrKey,             // Either method works (flexible)
}
```

### Use Cases

#### 1. Two-Factor Authentication (2FA)

```bash
# Setup 2FA
$ passkeeper auth add-key --vault my-vault.vault
🔑 Insert security key and press its button...
✅ Security key registered: YubiKey 5 NFC (Serial: 12345678)
🔒 2FA enabled. Key will be required on next unlock.

# Unlock with 2FA
$ passkeeper open my-vault.vault
🔐 Enter master password: ********
🔑 Touch security key to continue...
✅ Vault unlocked
```

#### 2. Key-Only Authentication

```bash
# Create vault with hardware key only (no master password)
$ passkeeper init my-vault.vault --auth key-only
🔑 Insert security key...
✅ Vault created and encrypted with hardware key
⚠️  Warning: Losing this key means losing access to your vault!

# Unlock with key only
$ passkeeper open my-vault.vault
🔑 Touch security key...
✅ Vault unlocked
```

#### 3. Backup Keys

```bash
# Register multiple keys
$ passkeeper auth add-key --vault my-vault.vault --name "Primary Key"
✅ Primary Key registered

$ passkeeper auth add-key --vault my-vault.vault --name "Backup Key"
✅ Backup Key registered

$ passkeeper auth list-keys
🔑 Registered Security Keys:
   1. YubiKey 5 NFC    (Primary Key)   - Last used: 5 minutes ago
   2. YubiKey 5C       (Backup Key)    - Last used: Never

# Remove lost key
$ passkeeper auth remove-key --id 2
⚠️  This will revoke access for "Backup Key"
Continue? [y/N]: y
✅ Key removed
```

### Technical Architecture

```
┌─────────────────────────────────────────────┐
│               Passkeeper CLI                │
└────────────────┬────────────────────────────┘
                 │
      ┌──────────┴───────────┐
      │                      │
┌─────▼──────┐     ┌────────▼─────────┐
│  Password  │     │  Hardware Key    │
│  Auth      │     │  Auth (FIDO2)    │
└─────┬──────┘     └────────┬─────────┘
      │                     │
      │    ┌────────────────┘
      │    │
┌─────▼────▼──────┐
│   Key Derivation│
│   (Argon2id)    │
└────────┬─────────┘
         │
┌────────▼─────────┐
│  Vault Unlock    │
│  (AES-256-GCM)   │
└──────────────────┘
```

### Key Derivation with Hardware Key

```rust
// Challenge-response with hardware key
fn derive_key_with_hardware(
    password: Option<&str>,      // Optional password
    hardware_key: &Device,       // Physical key
    salt: &[u8],                 // Vault salt
) -> Result<[u8; 32]> {
    // Generate challenge
    let challenge = generate_challenge(salt);
    
    // Get response from hardware key
    let response = hardware_key.sign(challenge)?;
    
    // Combine with password if present
    let key_material = match password {
        Some(pwd) => {
            // 2FA mode: combine both
            let pwd_derived = argon2id_derive(pwd, salt)?;
            combine_keys(&pwd_derived, &response)
        },
        None => {
            // Key-only mode: use hardware response
            response
        }
    };
    
    // Final key derivation
    Ok(key_material)
}
```

## Implementation Plan

### Phase 1: FIDO2 Integration
- [ ] Research and select FIDO2 library (`ctap-hid-ffi` or `fido-device`)
- [ ] Implement device detection and enumeration
- [ ] Implement challenge-response authentication
- [ ] Add key registration flow
- [ ] Test with multiple key types

### Phase 2: Vault Integration
- [ ] Extend vault metadata to store key info
- [ ] Implement key derivation with hardware
- [ ] Add support for multiple registered keys
- [ ] Implement key revocation
- [ ] Add migration path from password-only

### Phase 3: CLI Commands
- [ ] `passkeeper auth init` - Setup authentication method
- [ ] `passkeeper auth add-key` - Register new key
- [ ] `passkeeper auth list-keys` - Show registered keys
- [ ] `passkeeper auth remove-key` - Revoke key
- [ ] `passkeeper auth test-key` - Test key without unlocking
- [ ] Update all existing commands to support hardware auth

### Phase 4: User Experience
- [ ] Clear prompts and instructions
- [ ] Timeout handling (key not inserted)
- [ ] Multiple key support (try each)
- [ ] Fallback mechanisms
- [ ] Progress indicators

### Phase 5: Security & Testing
- [ ] Security audit of implementation
- [ ] Test with various key types
- [ ] Test attack scenarios
- [ ] Backup and recovery testing
- [ ] Documentation and best practices

## CLI Commands Reference

```bash
# Initialize 2FA
passkeeper auth add-key --vault my-vault.vault [--name NAME]

# List registered keys
passkeeper auth list-keys --vault my-vault.vault

# Remove a key
passkeeper auth remove-key --vault my-vault.vault --key-id ID

# Change auth mode
passkeeper auth set-mode --vault my-vault.vault --mode [password|key|both|either]

# Test key without unlocking
passkeeper auth test-key --vault my-vault.vault

# Backup key data (for disaster recovery)
passkeeper auth backup --vault my-vault.vault --output backup.json

# Emergency password reset (requires all registered keys)
passkeeper auth reset-password --vault my-vault.vault
```

## Security Considerations

### Advantages

✅ **Physical Security**: Key must be possessed
✅ **Phishing Resistant**: Cannot be phished remotely
✅ **Strong Cryptography**: ECDSA, Ed25519
✅ **Tamper Resistant**: Keys stored in secure element
✅ **Backup Support**: Multiple keys can be registered
✅ **Audit Trail**: Track which key was used when

### Risks and Mitigations

⚠️ **Lost Key**: 
- Mitigation: Support multiple registered keys
- Recommendation: Register backup key

⚠️ **Key Theft**:
- Mitigation: Require password + key (2FA mode)
- Some keys support PIN protection

⚠️ **USB Port Access**:
- Risk: Someone could use inserted key
- Mitigation: Auto-lock after timeout, require button press

### Threat Model

| Attack Vector           | Password Only | Password + Key | Key Only |
|------------------------|---------------|----------------|----------|
| Remote password theft  | ❌ Vulnerable | ✅ Protected   | ✅ N/A   |
| Phishing               | ❌ Vulnerable | ✅ Protected   | ✅ Protected |
| Keylogger              | ❌ Vulnerable | ⚠️ Partial     | ✅ Protected |
| Stolen key             | ✅ N/A        | ⚠️ Partial     | ❌ Vulnerable |
| Stolen key + password  | ✅ N/A        | ❌ Vulnerable  | ✅ N/A   |

**Recommendation**: Use **Password + Key** (2FA) for best security.

## Configuration

```toml
# vault metadata (example)
[auth]
mode = "password_and_key"  # password | key_only | password_and_key | password_or_key

[[auth.keys]]
id = "abc123def456..."
name = "YubiKey 5 NFC"
added = "2024-01-15T10:30:00Z"
last_used = "2024-01-20T15:45:00Z"
credential_id = "base64_encoded_id..."
public_key = "base64_encoded_pubkey..."

[[auth.keys]]
id = "789ghi012jkl..."
name = "Backup Key"
added = "2024-01-15T10:35:00Z"
last_used = null
credential_id = "base64_encoded_id..."
public_key = "base64_encoded_pubkey..."
```

## User Experience Examples

### Setup Wizard

```bash
$ passkeeper init secure-vault.vault --with-hardware-key

🔐 Create New Vault: secure-vault.vault
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: Choose Authentication Method
  1. Master password only (traditional)
  2. Hardware key only (no password needed)
  3. Password + Hardware key (2FA - recommended) ⭐
  
Your choice [1-3]: 3

Step 2: Set Master Password
  Enter master password: ************
  Confirm password: ************
  ✅ Password strength: Strong (92/100)

Step 3: Register Hardware Key
  🔑 Please insert your security key and press its button...
  
  ⏳ Waiting for key...
  
  ✅ Detected: YubiKey 5 NFC (Serial: 12345678)
  
  Register another backup key? [y/N]: y
  
  🔑 Insert backup key...
  ✅ Detected: YubiKey 5C (Serial: 87654321)
  
  Register another backup key? [y/N]: n

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Vault created successfully!

Summary:
  📁 Vault: secure-vault.vault
  🔐 Authentication: Password + Hardware Key (2FA)
  🔑 Registered Keys: 2
     - YubiKey 5 NFC (Primary)
     - YubiKey 5C (Backup)
  
⚠️  Important:
  • Keep backup key in secure location
  • Losing all keys means losing vault access
  • Write down recovery information
```

## Dependencies

```toml
[dependencies]
# FIDO2/WebAuthn support
authenticator = "0.4"       # Firefox's FIDO library
ctap-hid-ffi = "3.5"        # Low-level CTAP/FIDO2
webauthn-rs = "0.4"         # WebAuthn server library

# Or alternative:
yubico-manager = "0.11"     # YubiKey-specific (if targeting YubiKey only)

# USB device handling
rusb = "0.9"                # USB library
```

## Compatibility

| Key Type            | FIDO2 | U2F | OTP | Status |
|--------------------|-------|-----|-----|---------|
| YubiKey 5 Series   | ✅    | ✅  | ✅  | Full    |
| YubiKey 4 Series   | ❌    | ✅  | ✅  | Limited |
| Google Titan       | ✅    | ✅  | ❌  | Full    |
| Feitian            | ✅    | ✅  | ❌  | Full    |
| Thetis             | ✅    | ✅  | ❌  | Full    |
| SoloKeys           | ✅    | ✅  | ❌  | Full    |

## Alternatives Considered

1. **PIV/Smart Cards**: More complex, less user-friendly
2. **Biometrics**: Platform-specific, privacy concerns
3. **Mobile Authenticator**: Network dependency
4. **TPM**: Not portable across devices

## Resources

- [FIDO2 Specification](https://fidoalliance.org/specs/fido-v2.0-ps-20190130/fido-client-to-authenticator-protocol-v2.0-ps-20190130.html)
- [WebAuthn Guide](https://webauthn.guide/)
- [YubiKey Developer](https://developers.yubico.com/)
- [CTAP Protocol](https://fidoalliance.org/specs/fido-v2.0-id-20180227/fido-client-to-authenticator-protocol-v2.0-id-20180227.html)

## Acceptance Criteria

- [ ] Detect and communicate with FIDO2/U2F keys
- [ ] Register multiple hardware keys
- [ ] Unlock vault with hardware key
- [ ] Support 2FA (password + key)
- [ ] Support key-only mode
- [ ] Key revocation works correctly
- [ ] Clear error messages for all failure cases
- [ ] Works with at least YubiKey, Google Titan, and SoloKeys
- [ ] Comprehensive documentation
- [ ] Security audit passed

---

**Labels**: `enhancement`, `security`, `hardware`, `advanced`
**Estimated Effort**: 4-5 weeks
**Difficulty**: High
**Priority**: Medium
