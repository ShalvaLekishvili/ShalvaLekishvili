# Deep Research Notes — August 2026

This portfolio design was aligned to current GitHub platform behavior and security guidance.

## GitHub platform references

- Profile README management: `https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme`
- README behavior / relative image paths: `https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes`
- Social preview configuration: `https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview`
- GitHub Actions workflow syntax and timezone-aware schedules: `https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions`
- GitHub Actions secure-use reference: `https://docs.github.com/en/actions/reference/security/secure-use`
- REST API overview / current version: `https://docs.github.com/en/rest?apiVersion=2026-03-10`
- Repository statistics API: `https://docs.github.com/en/rest/metrics/statistics?apiVersion=2026-03-10`
- Releases API: `https://docs.github.com/v3/repos/releases`
- Dependabot options: `https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference`

## Findings applied to v5

1. GitHub supports profile READMEs and relative local assets, so core presentation assets can remain repository-controlled.
2. GitHub supports light/dark responsive images through `<picture>` patterns.
3. Scheduled Actions can use IANA time zones; v5 uses `Asia/Tbilisi`.
4. GitHub recommends full-length commit SHA pinning for immutable action references.
5. Token permissions should be minimized; the refresh job uses repository-content write permission because it commits generated assets.
6. GitHub REST API is versioned; v5 sends `X-GitHub-Api-Version: 2026-03-10`.
7. Social preview images are repository-configurable, so a dedicated 1280×640 image is included.

## Live portfolio audit findings

At research time the public profile repository had no repository-level description, website, or topics in its About panel. Those should be added manually because README design cannot replace repository metadata.

SentinelForge publicly documents v0.2.0, Windows EVTX ingestion, Wazuh/Sysmon normalization, 12 curated defensive detections, IOC extraction, process graph correlation, ATT&CK coverage, API/CLI, CI, and a hardened container baseline.

PacketScope publicly documents PCAP/PCAPNG analysis, protocol metadata, behavioral detections, evidence slicing, analyst state, privacy boundaries, FastAPI/CLI, MIT licensing, and a 48-test suite.
