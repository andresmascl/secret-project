# Contributing to Alekz

Thanks for your interest in contributing to **Alekz**.

Alekz is a **local-first, developer-focused voice assistant**. Contributions are welcome, but the project intentionally prioritizes **clarity, control, and correctness** over convenience or mass appeal.

Please read this document before opening issues or pull requests.

---

## Project Philosophy (Read This First)

Before contributing, understand these non-negotiable principles:

1. **Local-first**
   - Core functionality must work without cloud dependencies.

2. **User-owned sessions**
   - Browser automation must use *real, persistent user profiles*.
   - No fake accounts, no ephemeral containers by default.

3. **Headful over headless**
   - Visibility and debuggability are preferred over speed.

4. **Explicit > Magical**
   - Avoid hidden behavior, background magic, or excessive abstraction.

5. **Composable architecture**
   - Voice, browser control, and application logic must remain decoupled.

If a proposed change violates any of these, it will likely be rejected.

---

## What Kind of Contributions Are Welcome

### ✅ Encouraged

- New **browser apps** (e.g. Spotify Web, Reddit, Jira)
- Improvements to existing apps (YouTube, Gmail)
- Additional browser controllers (Chromium-based variants)
- Bug fixes in Playwright automation
- Selector stability improvements
- Documentation improvements
- Tests that reflect real-world usage

---

## Repository Structure (High Level)

- `assist/` → Voice & intent extraction (Rhasspy)
- `browser/controllers/` → Browser-specific adapters
- `browser/apps/` → Website automation logic
- `browser/apps/test/` → Headful Playwright tests

If you add new functionality, put it in the *correct layer*.

---

## Development Environment

### Requirements

- Linux (primary target)
- Python 3.10+
- One supported browser installed (Brave, Chrome, or Firefox)
- A microphone (for voice testing)

---

## Coding Guidelines

### General

- Keep code **simple and readable**
- Avoid over-engineering
- Prefer plain Python over clever abstractions
- Explicit imports and names

### Browser Apps

- Must be **browser-agnostic**
- Must accept a Playwright `Page`
- Must not launch or manage the browser directly
- Must fail loudly when selectors break

### Browser Controllers

- One controller per browser
- No app-specific logic allowed
- Responsible only for launching and managing browser context

### Rhasspy Integration

- Treat Rhasspy as a black box
- Do not hard-code assumptions about STT or intent engines

---

## Tests

- Tests are **headful by design**
- Tests should reflect real user flows
- Do not mock browser behavior unless strictly necessary
- Prefer end-to-end verification over unit tests

Run tests using the Makefile targets (when available).

---

## Commit & PR Guidelines

### Commits

- Use clear, descriptive commit messages
- One logical change per commit

Example:
```
browser/apps: improve YouTube search selector stability
```

### Pull Requests

- Describe *what* changed and *why*
- Reference related issues if applicable
- Keep PRs focused and reviewable

Large refactors without discussion are discouraged.

---

## Issues

When opening an issue, include:

- OS and browser used
- Steps to reproduce
- Expected vs actual behavior
- Screenshots or recordings (for browser issues)

Vague issues may be closed without action.

---

## Code of Conduct

Be respectful.
Assume good intent.
This is a technical project, not a social network.

---

## Final Note

Alekz is intentionally opinionated.

If you disagree with its constraints, you are encouraged to fork it.
That is not failure — that is open source working as intended.

