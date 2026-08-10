# God Mode Profile Architecture

## Goal

The profile is designed as a small, evidence-backed publishing system rather than a static README full of badges.

## Layers

### 1. Human narrative
`README.md` explains role, operating philosophy, projects, business value, credentials, and reviewer routes.

### 2. Machine-readable source of truth
`config/portfolio.json` stores flagship definitions, claim verification rules, credentials, role, and API version.

### 3. Public intelligence collection
`scripts/profile_engine.py` calls GitHub's REST API for public metadata and project README content.

For each flagship it collects:
- repository description;
- primary language;
- license;
- star/fork counts;
- latest published release when available;
- last push timestamp;
- topics;
- README text for public-claim verification.

### 4. Claim verification
Selected portfolio claims are not simply copied into a metric card. Each has a regular expression that must be found in the source project's public README before the live intelligence panel reports it as verified.

Current claim set:
- SentinelForge: curated detections, EVTX ingestion, ATT&CK context;
- PacketScope: 48-test suite, PCAP/PCAPNG support, evidence slicing.

This is intentionally conservative. It verifies public documentation, not runtime correctness.

### 5. Generated presentation
The engine writes:
- `assets/generated/live-intelligence-dark.svg`
- `assets/generated/live-intelligence-light.svg`
- `assets/generated/credential-matrix-dark.svg`
- `assets/generated/credential-matrix-light.svg`
- `assets/generated/portfolio-manifest.json`

GitHub `<picture>` elements select a theme-specific asset.

### 6. Failure semantics
If live collection fails, the generator uses `data/baseline.json` and marks the output as baseline-backed. It does not silently label stale data as live.

### 7. Workflow hardening
`.github/workflows/profile-engine.yml`:
- uses `contents: write` only;
- uses a unique concurrency group;
- uses a timezone-aware Tbilisi schedule;
- pins reusable GitHub actions to full commit SHAs;
- runs tests before generation;
- validates generated output;
- commits only when generated files changed.

### 8. Supply-chain minimization
The profile engine intentionally uses only Python's standard library. The scheduled job does not run `pip install`.

## Why this is stronger than normal profile widgets

A normal GitHub profile often depends on multiple third-party image endpoints. Those endpoints can disappear, throttle, render inconsistently, or display opaque metrics. This design keeps the core evidence layer inside the profile repository and makes its generation logic reviewable.

## What not to automate

Do not automatically generate qualitative claims such as:
- "expert";
- "top 1%";
- "enterprise-grade";
- "production-ready";
- "zero false positives";
- "advanced" based on stars or commit count.

Those are interpretation claims and should require human review.
