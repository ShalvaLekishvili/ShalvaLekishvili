# Installation / Upgrade Guide

This package is designed for the GitHub profile repository:

`ShalvaLekishvili/ShalvaLekishvili`

## Replace the current profile

1. Download and extract this package.
2. Open the existing `ShalvaLekishvili` profile repository.
3. Replace `README.md`.
4. Replace the `assets/` directory with the included `assets/`.
5. Add `.github/workflows/snake.yml`.
6. Commit and push to `main`.

Example:

```bash
git clone https://github.com/ShalvaLekishvili/ShalvaLekishvili.git
cd ShalvaLekishvili

# Copy the new README.md, assets/, and .github/ here.

git add README.md assets .github
git commit -m "Redesign profile as business-class security portfolio"
git push origin main
```

## Profile settings that should also be updated manually

Recommended GitHub profile bio:

`SOC Analyst (L2) | Detection Engineering | DFIR | Network Forensics | Security Automation`

Recommended pinned repositories, in this order:

1. SentinelForge
2. PacketScope
3. ShalvaLekishvili (profile repository)
4. E-olymp only if you want to retain programming-history context

Older repositories with vague or aggressive names should be archived, renamed, or clearly documented if you keep them public.

## Why this version is different

The previous profile was visually strong but tool-heavy. This redesign:

- centers verifiable engineering evidence;
- gives SentinelForge and PacketScope first-class placement;
- adds executive / business translation modules;
- reduces decorative cyber-noise;
- replaces "hacker identity first" with "security operator first";
- keeps technical depth without reading like a skills inventory;
- is designed to make sense to recruiters, SOC leads, engineering managers, and technical reviewers.

## Contribution snake

The workflow writes contribution SVGs to the `output` branch. After pushing:

1. Open **Actions**.
2. Run **Generate contribution snake** once manually.
3. Confirm the `output` branch is created.
4. The README will render the contribution graphic automatically.

## Final verification checklist

- README hero loads.
- All local SVGs render.
- SentinelForge and PacketScope links work.
- LinkedIn, TryHackMe, and portfolio links work.
- Snake workflow runs.
- Profile About/bio is updated.
- SentinelForge and PacketScope are pinned.
