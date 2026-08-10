# Security policy

This repository is a public profile and portfolio automation system. It intentionally processes only public GitHub repository metadata and public README content.

## Automation hardening

- GitHub Actions are pinned to full commit SHAs.
- Workflow token permission is limited to `contents: write` because generated assets are committed back to this repository.
- No `pull_request_target` or untrusted-code workflow is used.
- The profile engine uses Python standard library only and has no runtime package dependency.
- Public project claims are verified against project READMEs before being rendered as verified evidence.

Report an issue privately through an appropriate contact channel if you discover a security concern in the automation.
