---
name: Optional P2P Sync
about: Implement end-to-end encrypted peer-to-peer vault synchronization
title: '[FEATURE] Optional P2P Sync'
labels: enhancement, sync, distributed
assignees: ''
---

## Description

Implement optional peer-to-peer (P2P) synchronization that allows users to sync their encrypted vaults across multiple devices without relying on a central server, maintaining the local-first and zero-knowledge principles.

## Motivation

Users with multiple devices (laptop, desktop, phone) want their passwords accessible everywhere, but:
- Don't want to rely on cloud providers
- Don't want to trust third parties with encrypted data
- Want to maintain local-first architecture
- Need offline access with eventual synchronization

## Proposed Solution

### Architecture: Hybrid P2P + Local Discovery

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│   Device A   │◄───────►│   Device B   │◄───────►│   Device C   │
│  (Laptop)    │  P2P    │  (Desktop)   │  P2P    │  (Phone)     │
└──────┬───────┘         └──────┬───────┘         └──────┬───────┘
       │                        │                        │
       │                        │                        │
       └────────────────────────┴────────────────────────┘
                         Local Network
                    (mDNS/Bonjour discovery)
```

### Sync Protocol

1. **Discovery**
   - Local network: mDNS/Bonjour
   - Internet: libp2p or custom relay (optional)
   - Manual: IP address + port

2. **Authentication**
   - Device pairing with QR code or code phrase
   - Public key exchange
   - Mutual TLS authentication

3. **Synchronization**
   - Merkle tree for efficient diff detection
   - Conflict resolution with timestamps
   - Incremental sync (only changed entries)
   - End-to-end encryption (vault stays encrypted)

4. **Conflict Resolution**
   - Latest timestamp wins (default)
   - Manual resolution for important conflicts
   - Keep both versions option
   - Tombstones for deletions

### CLI Commands

```bash
# Initialize sync capability
passkeeper sync init --vault my-vault.vault

# Enable sync on this device
passkeeper sync enable

# Pair a new device (generates pairing code)
passkeeper sync pair
> Pairing code: ALPHA-BRAVO-12345
> Scan QR code or enter code on other device

# Connect to paired device
passkeeper sync connect --code ALPHA-BRAVO-12345

# List paired devices
passkeeper sync devices
> Device ID          Name            Last Seen        Status
> abc123def456...   Laptop-Work     2 minutes ago    ✅ Online
> 789ghi012jkl...   Desktop-Home    1 hour ago       ⏸️  Offline

# Sync now (manual)
passkeeper sync now

# Auto-sync settings
passkeeper sync auto --enable --interval 5m

# Remove paired device
passkeeper sync unpair --device abc123def456

# Sync status
passkeeper sync status
> Auto-sync: Enabled (every 5 minutes)
> Last sync: 2 minutes ago
> Paired devices: 2 (1 online)
> Pending changes: 3 local, 1 remote
```

### Technology Stack

- **Discovery**: `mdns` or `zeroconf` crate for local network
- **P2P**: `libp2p` for decentralized networking
- **Encryption**: Additional layer on already-encrypted vault
- **Conflict Resolution**: CRDT or custom timestamp-based
- **Transport**: QUIC for modern, secure connections

## Implementation Plan

### Phase 1: Sync Infrastructure
- [ ] Add sync metadata to vault structure
- [ ] Implement device identity and key generation
- [ ] Create sync state tracking (versions, checksums)
- [ ] Implement Merkle tree for efficient diffing
- [ ] Add conflict detection logic

### Phase 2: Pairing & Discovery
- [ ] Device pairing with codes/QR
- [ ] mDNS discovery for local network
- [ ] Manual connection by IP:port
- [ ] Device management (list, unpair)

### Phase 3: Sync Protocol
- [ ] Implement sync message protocol
- [ ] Add transport layer (QUIC/TCP+TLS)
- [ ] Implement incremental sync
- [ ] Add conflict resolution strategies
- [ ] Progress reporting

### Phase 4: CLI Integration
- [ ] Add `sync` command group
- [ ] Implement manual sync
- [ ] Add auto-sync daemon
- [ ] Status and monitoring commands
- [ ] Configuration management

### Phase 5: Advanced Features
- [ ] Selective sync (exclude specific credentials)
- [ ] Sync history and rollback
- [ ] Bandwidth optimization
- [ ] NAT traversal for internet sync
- [ ] Mobile app integration

## Sync Workflow Example

```bash
# Device A (Laptop)
$ passkeeper sync init --vault work.vault
✅ Sync initialized for vault 'work.vault'
📱 Device ID: laptop-abc123

$ passkeeper sync pair
🔑 Pairing Code: TANGO-VICTOR-98765
📱 This code expires in 5 minutes
🎯 Scan QR code or enter on other device:
   ┌─────────────────────┐
   │  █ █ █  █████  █ █  │
   │  ███   ██ ██  ██ ██ │
   │  █  █ ███ ██ ███  █ │
   └─────────────────────┘

# Device B (Desktop)
$ passkeeper sync connect --code TANGO-VICTOR-98765
🔍 Searching for device...
✅ Found device: laptop-abc123 (192.168.1.100)
🤝 Keys exchanged successfully
📦 Syncing vault...
   Downloaded: 127 credentials
   Conflicts: 0
✅ Sync complete!

# Later, on Device A
$ passkeeper add
# ... add new credential ...

$ passkeeper sync now
📤 Syncing with 1 device(s)...
✅ desktop-def456: 1 new credential sent
📥 Received: 0 updates
✅ Sync complete!
```

## Conflict Resolution Example

```bash
$ passkeeper sync now
⚠️  Conflicts detected:

Credential: github.com/myaccount
  Local:   Updated 2 minutes ago, password changed
  Remote:  Updated 5 minutes ago, username changed
  
Resolution options:
  1. Keep local version
  2. Keep remote version
  3. Merge both (keep username from remote, password from local)
  4. Review manually

Your choice [1-4]: 3
✅ Conflict resolved with merge

Sync Summary:
  ✅ Synced: 43 credentials
  ⚠️  Conflicts: 1 resolved
  📊 Bandwidth: 12.4 KB up, 8.7 KB down
```

## Security Considerations

### Encryption Layers

1. **Vault Encryption** (existing)
   - AES-256-GCM with Argon2id key derivation
   - Master password never transmitted

2. **Transport Encryption** (new)
   - TLS 1.3 or QUIC
   - Certificate pinning for paired devices
   - Perfect forward secrecy

3. **Additional Sync Encryption** (optional)
   - Separate sync key derived from master password
   - Protects against compromised transport

### Threat Model

✅ **Protected Against**:
- Network eavesdropping (TLS)
- Man-in-the-middle (certificate pinning)
- Unauthorized devices (pairing required)
- Replay attacks (nonce + timestamp)

⚠️ **Not Protected Against**:
- Compromised device (has vault access)
- Malicious paired device
- Physical device access

### Privacy

- 🔒 No metadata leakage (entry counts, titles encrypted)
- 🚫 No central server (true P2P)
- 👁️ No analytics or tracking
- 🏠 Local network preferred
- 🌐 Optional relay for internet (no data stored)

## Configuration

```toml
# ~/.config/passkeeper/sync.toml

[sync]
enabled = true
auto_sync = true
interval = "5m"
discovery = ["mdns", "manual"]

[sync.network]
listen_addr = "0.0.0.0:7878"
max_peers = 5
timeout = "30s"

[sync.security]
require_pairing = true
pairing_expiry = "5m"
sync_encryption = true

[sync.conflict]
resolution = "latest"  # latest, manual, keep-both
auto_resolve = true
```

## Benefits

- 🚀 Multi-device access without cloud
- 🔒 Maintains zero-knowledge architecture
- ⚡ Fast sync on local network
- 🌍 Works across internet (with relay)
- 💾 Still fully functional offline
- 🎯 Selective sync capability

## Alternatives Considered

1. **iCloud/Dropbox Sync**: Not private, requires cloud account
2. **Self-hosted Server**: Requires setup, not pure P2P
3. **Git-based Sync**: Complex, merge conflicts difficult
4. **Syncthing**: External dependency, less integrated

## Additional Context

### Similar Projects

- **Syncthing**: File sync inspiration
- **Resilio Sync**: P2P file sync
- **Magic Wormhole**: Device pairing
- **libp2p**: P2P networking library

### Research

- [CRDT for conflict resolution](https://crdt.tech/)
- [Merkle trees for sync](https://en.wikipedia.org/wiki/Merkle_tree)
- [Local-first software](https://www.inkandswitch.com/local-first/)

## Acceptance Criteria

- [ ] Devices can discover each other on local network
- [ ] Secure pairing with codes or QR
- [ ] Successfully syncs vaults between devices
- [ ] Handles conflicts gracefully
- [ ] Works offline (queues changes)
- [ ] Minimal bandwidth usage
- [ ] No data loss during sync
- [ ] Comprehensive testing (including network failures)
- [ ] Documentation with setup guide
- [ ] Security audit passed

## Dependencies

```toml
[dependencies]
libp2p = "0.53"           # P2P networking
mdns = "3.0"              # Local discovery
quinn = "0.10"            # QUIC protocol
qrcode = "0.13"           # QR code generation
tokio = "1.35"            # Async runtime
serde_cbor = "0.11"       # Binary serialization
```

---

**Labels**: `enhancement`, `sync`, `distributed`, `advanced`
**Estimated Effort**: 6-8 weeks
**Difficulty**: High
**Priority**: Medium (nice-to-have feature)
