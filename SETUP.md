# God Mode v5 — Installation

## Replace the profile repository

Copy the contents of this package into `ShalvaLekishvili/ShalvaLekishvili`.

```bash
git clone https://github.com/ShalvaLekishvili/ShalvaLekishvili.git
cd ShalvaLekishvili

# Copy README.md, assets/, config/, data/, scripts/, tests/, docs/,
# .github/, Makefile, SECURITY.md from this package.

git add .
git commit -m "feat(profile): deploy god-mode evidence portfolio v5"
git push origin main
```

## Before pushing

```bash
make all
```

Expected result:
- 4 unit tests pass;
- profile validation passes;
- dark/light generated SVGs exist;
- 10 TryHackMe IDs and 14 total credentials are present.

## After pushing

1. Open **Actions → Profile Intelligence Engine**.
2. Run **workflow_dispatch** once.
3. Confirm `data/live.json` is created and generated assets update.
4. Confirm the README's Live Portfolio Intelligence panel now says GitHub REST API instead of baseline.

## Recommended profile metadata

**Bio**

`SOC Analyst (L2) | Detection Engineering | DFIR | Threat Hunting | Network Forensics | Security Automation`

**Pinned repositories**

1. SentinelForge
2. PacketScope
3. ShalvaLekishvili
4. Only one additional repository that strengthens the engineering narrative

## Repository About panel

Your profile repository currently needs manual metadata. Recommended:

**Description**

`Evidence-first SOC, Detection Engineering and DFIR portfolio — self-updating public engineering intelligence.`

**Website**

`https://lekishvilishalva.netlify.app/`

**Topics**

`cybersecurity`, `soc`, `detection-engineering`, `dfir`, `threat-hunting`, `network-forensics`, `portfolio`, `security-automation`

## Social preview

Upload `assets/social-preview-v5.png` at:

**Settings → General → Social preview → Edit**

## Workflow permissions

The workflow requests `contents: write` in YAML. If repository policy blocks write access, open:

**Settings → Actions → General → Workflow permissions**

and allow the workflow token the needed write permission.

## Scheduled-workflow note

GitHub can automatically disable scheduled workflows in a public repository after 60 days with no repository activity. If that happens, re-enable the workflow in Actions and run it manually once.
