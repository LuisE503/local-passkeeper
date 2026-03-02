---
name: Scheduled Security Audits
about: Implement automatic periodic security audits with notifications
title: '[FEATURE] Scheduled Security Audits'
labels: enhancement, security, automation
assignees: ''
---

## Description

Implement scheduled automatic security audits that run periodically in the background, analyze vault security, and notify users of issues like weak passwords, reused credentials, breached passwords, and expiring credentials.

## Motivation

Users often forget to manually check vault security. Proactive, automated audits help:
- **Catch weak passwords** before they're exploited
- **Detect breaches** via integration with Have I Been Pwned
- **Remind about old passwords** that should be rotated
- **Prevent password reuse** across critical accounts
- **Maintain security hygiene** without manual intervention

## Proposed Solution

### Features

1. **Scheduled Audits**
   - Run automatically on a schedule (daily, weekly, monthly)
   - Configurable audit frequency per vault
   - Runs in background without user interaction
   - Low resource usage

2. **Audit Types**
   - **Weak passwords**: Strength < threshold
   - **Reused passwords**: Same password used multiple times
   - **Old passwords**: Not changed in X days
   - **Breached passwords**: Check against HIBP API
   - **Missing 2FA**: Accounts that should have 2FA but don't
   - **Exposed metadata**: URLs, usernames in known breaches

3. **Notifications**
   - Desktop notifications (Windows/macOS/Linux)
   - Email reports (optional)
   - Terminal output on next CLI use
   - Audit reports saved to file
   - Dashboard summary

4. **Actions**
   - View detailed report
   - Update flagged credentials
   - Dismiss false positives
   - Schedule auto-updates (with caution)
   - Export audit logs

### CLI Commands

```bash
# Enable scheduled audits
passkeeper audit schedule enable --vault my-vault.vault --frequency daily

# Configure audit settings
passkeeper audit schedule config --vault my-vault.vault \
  --frequency weekly \
  --time "02:00" \
  --checks weak,reused,breached \
  --notify desktop,file

# Check schedule status
passkeeper audit schedule status

# Run manual audit now
passkeeper audit now --vault my-vault.vault

# View last audit report
passkeeper audit report --vault my-vault.vault [--last | --date 2024-01-20]

# List audit history
passkeeper audit history --vault my-vault.vault --limit 10

# Disable scheduled audits
passkeeper audit schedule disable --vault my-vault.vault

# Configure notifications
passkeeper audit notify config \
  --desktop \
  --email user@example.com \
  --threshold critical
```

### Configuration

```toml
# ~/.config/passkeeper/audit.toml

[audit]
enabled = true

[audit.schedule]
frequency = "daily"      # daily, weekly, monthly, custom
time = "02:00"          # Time to run (24-hour format)
custom_cron = ""        # Optional cron expression

[audit.checks]
weak_passwords = true
password_reuse = true
old_passwords = true
breached_passwords = true
missing_2fa = true
expiring_credentials = false

[audit.thresholds]
weak_password_score = 60          # Below this = weak
old_password_days = 365          # Older than this = should rotate
reuse_critical_domains = [       # Check reuse on critical sites
    "bank", "email", "work", "gov"
]

[audit.notifications]
desktop = true
email = false
email_address = ""
file = true
file_path = "~/.local/share/passkeeper/audit_reports/"
threshold = "warning"    # critical, warning, info

[audit.hibp]
enabled = true
api_key = ""            # Optional API key for faster checks
check_usernames = true
check_passwords = true  # Uses k-anonymity (safe)

[audit.reporting]
keep_history = 30       # Days to keep audit reports
detailed_logs = true
```

### Audit Report Format

```bash
$ passkeeper audit report --last

╔══════════════════════════════════════════════════════════════╗
║          SECURITY AUDIT REPORT - January 20, 2024            ║
╚══════════════════════════════════════════════════════════════╝

Vault: my-vault.vault
Audit Date: 2024-01-20 02:00:15
Total Credentials: 247
Duration: 12.4 seconds

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 CRITICAL ISSUES: 5

  ⚠️  Breached Passwords (3)
      • linkedin.com - Password found in 2022 LinkedIn breach
      • oldsite.com - Password found in multiple breaches
      • forum.net - Password found in 2021 data leak
      
      Action: Change these passwords immediately!

  ⚠️  Weak Passwords (2)
      • test-account.com - Strength: 25/100 (Very Weak)
      • demo.org - Strength: 35/100 (Weak)
      
      Action: Generate and use strong passwords

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🟡 WARNINGS: 12

  ⚠️  Password Reuse (8 credentials)
      • "hunter2" used on: forum1.com, forum2.net, test.org
      • "Summer2020!" used on: shopping1.com, shopping2.com
      
      Action: Use unique passwords for each account

  ⚠️  Old Passwords (4 credentials)
      • bank.com - Last changed: 456 days ago
      • email.com - Last changed: 389 days ago
      
      Action: Consider rotating old passwords

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ GOOD PRACTICES: 230

  • 230 credentials with strong, unique passwords
  • 87 credentials with 2FA enabled
  • Average password age: 145 days
  • No other security issues detected

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 SECURITY SCORE

    Overall Score: 78/100  [████████████░░░░░░░░]
    
    - Strong Passwords:     ██████████████████░░ 93%
    - Unique Passwords:     ████████████░░░░░░░░ 67%
    - Up-to-date:           ███████████████░░░░░ 82%
    - No Breaches:          ████████████░░░░░░░░ 64%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 RECOMMENDATIONS

  1. Immediately change 3 breached passwords
  2. Update 2 weak passwords to stronger alternatives
  3. Create unique passwords for 8 reused credentials
  4. Consider rotating passwords older than 1 year
  5. Enable 2FA on critical accounts (bank, email, work)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next Actions:
  • View details: passkeeper audit report --last --detailed
  • Fix issues:   passkeeper update <service>
  • Next audit:   Daily at 02:00 (scheduled)

Report saved: ~/.local/share/passkeeper/audit_reports/2024-01-20.json
```

### Desktop Notification Example

```
┌─────────────────────────────────────────────┐
│ 🔐 Passkeeper Security Alert                │
├─────────────────────────────────────────────┤
│                                             │
│ Audit completed for: my-vault.vault         │
│                                             │
│ 🔴 5 Critical Issues                        │
│ 🟡 12 Warnings                              │
│                                             │
│ • 3 breached passwords detected             │
│ • 2 weak passwords found                    │
│ • 8 reused passwords                        │
│                                             │
│ [View Report] [Dismiss]                     │
└─────────────────────────────────────────────┘
```

## Implementation Plan

### Phase 1: Audit Engine Enhancement
- [ ] Extend existing audit module
- [ ] Add HIBP API integration (k-anonymity model)
- [ ] Implement breach checking for passwords
- [ ] Add username/email breach checking
- [ ] Implement 2FA detection heuristics
- [ ] Add historical tracking

### Phase 2: Scheduler
- [ ] Implement background daemon/service
- [ ] Add cron-like scheduling
- [ ] Persistent schedule storage
- [ ] Handle system sleep/wake
- [ ] Resource-friendly execution
- [ ] Lock file management (prevent concurrent runs)

### Phase 3: Notifications
- [ ] Desktop notifications (cross-platform)
- [ ] Email notifications (SMTP/API)
- [ ] File-based reports
- [ ] In-CLI notifications
- [ ] Notification preferences

### Phase 4: Reporting
- [ ] Enhanced report format
- [ ] Historical report storage
- [ ] Report comparison (trends)
- [ ] Export formats (JSON, HTML, PDF)
- [ ] Dashboard view

### Phase 5: CLI Integration
- [ ] `audit schedule` command group
- [ ] `audit report` command
- [ ] `audit history` command
- [ ] Configuration commands
- [ ] Interactive fixing workflow

### Phase 6: Platform Services
- [ ] Windows: Task Scheduler integration
- [ ] macOS: launchd integration
- [ ] Linux: systemd timer/cron
- [ ] Docker: cron job in container

## Technical Architecture

```
┌─────────────────────────────────────────────────────┐
│              Passkeeper Audit Scheduler             │
└───────────────────────┬─────────────────────────────┘
                        │
         ┌──────────────┴──────────────┐
         │                             │
┌────────▼──────────┐        ┌────────▼─────────┐
│  Scheduler Daemon │        │  Audit Engine    │
│  - Cron/Timer     │───────▶│  - Checks        │
│  - Background     │        │  - HIBP API      │
│  - Resource mgmt  │        │  - Scoring       │
└────────┬──────────┘        └────────┬─────────┘
         │                            │
         │                            │
┌────────▼──────────┐        ┌────────▼─────────┐
│  Notification     │        │  Report          │
│  Manager          │        │  Generator       │
│  - Desktop        │        │  - History       │
│  - Email          │        │  - Export        │
│  - File           │        │  - Statistics    │
└───────────────────┘        └──────────────────┘
```

## Have I Been Pwned Integration

### k-Anonymity Model (Privacy-Preserving)

```rust
async fn check_password_breach(password: &str) -> Result<bool> {
    // SHA-1 hash of password
    let hash = sha1(password);
    
    // Send only first 5 characters to API (k-anonymity)
    let prefix = &hash[0..5];
    let suffix = &hash[5..];
    
    // Query HIBP API
    let response = reqwest::get(
        format!("https://api.pwnedpasswords.com/range/{}", prefix)
    ).await?;
    
    // Check if suffix appears in response
    let breached = response.text().await?
        .lines()
        .any(|line| line.starts_with(&suffix.to_uppercase()));
    
    Ok(breached)
}
```

**Privacy**: Only first 5 characters of hash sent to API. Password never leaves device in plaintext.

## Daemon Implementation

### Linux (systemd timer)

```ini
# ~/.config/systemd/user/passkeeper-audit.service
[Unit]
Description=Passkeeper Security Audit
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/passkeeper audit run-scheduled
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
```

```ini
# ~/.config/systemd/user/passkeeper-audit.timer
[Unit]
Description=Run Passkeeper security audits daily

[Timer]
OnCalendar=daily
OnCalendar=02:00
Persistent=true

[Install]
WantedBy=timers.target
```

### macOS (launchd)

```xml
<!-- ~/Library/LaunchAgents/com.passkeeper.audit.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "...">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.passkeeper.audit</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/passkeeper</string>
        <string>audit</string>
        <string>run-scheduled</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>2</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/tmp/passkeeper-audit.log</string>
</dict>
</plist>
```

## Security & Privacy Considerations

✅ **Privacy Protected**:
- HIBP k-anonymity: only 5 chars of hash sent
- No passwords leave device
- No telemetry or tracking
- Audit reports stored locally

✅ **Secure**:
- Vault remains encrypted
- No credentials in logs
- Secure API communication (TLS)
- Rate limiting to prevent abuse

⚠️ **Considerations**:
- HIBP API requires internet access
- May have false positives
- Historical breach data may be incomplete

## Dependencies

```toml
[dependencies]
# Existing dependencies
# ...

# New dependencies for scheduling
tokio = { version = "1.35", features = ["full"] }
tokio-cron-scheduler = "0.9"         # Cron scheduling
chrono = "0.4"                       # Already in use

# Notifications
notify-rust = "4.10"                 # Desktop notifications (cross-platform)
lettre = "0.11"                      # Email notifications

# HIBP API
reqwest = { version = "0.11", features = ["json"] }
sha1 = "0.10"                        # SHA-1 for HIBP

# Report generation
comfy-table = "7.1"                  # Better table formatting
serde_json = "1.0"                   # JSON reports
```

## Benefits

- 🛡️ Proactive security without user action
- 📊 Trend analysis over time
- 🔔 Immediate breach notifications
- 📅 Regular security check-ins
- 🎯 Actionable recommendations
- 📈 Security score tracking

## Alternatives Considered

1. **Manual audits only**: Easy to forget
2. **Cloud-based service**: Privacy concerns
3. **Always-on monitoring**: Resource intensive

## Use Cases

### 1. Personal User

```bash
# Enable daily audits at 2 AM
$ passkeeper audit schedule enable --daily --time 02:00

Wake up to notification:
  "🔴 3 breached passwords detected in your vault!"
  
Fix issues immediately.
```

### 2. Family Plan

```bash
# Audit multiple vaults
$ passkeeper audit schedule enable --vault family.vault --notify email --email parent@example.com

Weekly email report showing security status of family vault.
```

### 3. Team/Enterprise

```bash
# Strict security requirements
$ passkeeper audit schedule enable \
  --vault work.vault \
  --frequency daily \
  --checks all \
  --threshold critical \
  --email security@company.com

Daily reports to security team for compliance.
```

## Acceptance Criteria

- [ ] Audits run automatically on schedule
- [ ] HIBP integration works with k-anonymity
- [ ] Desktop notifications appear correctly
- [ ] Email notifications work (when configured)
- [ ] Reports saved to file system
- [ ] Historical reports viewable
- [ ] Configurable audit frequency
- [ ] Low resource usage when running
- [ ] Works on Windows, macOS, and Linux
- [ ] Handles offline/no-internet gracefully
- [ ] Comprehensive documentation
- [ ] Privacy audit passed (no PII sent to external services)

---

**Labels**: `enhancement`, `security`, `automation`, `high-priority`
**Estimated Effort**: 3-4 weeks
**Difficulty**: Medium
**Priority**: High
