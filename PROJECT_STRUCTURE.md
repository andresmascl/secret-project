# Project Structure

This document explains the folder and file structure of **Alekz**, an open‑source, local, Linux‑based voice assistant built on **Rhasspy** and **Playwright** to control a headful browser (with a real user session) and local applications.

The structure is intentionally modular, explicit, and scalable.

---

## Root Level

```
Alekz/
├── README.md
├── PROJECT_STRUCTURE.md
├── Makefile
├── main.py
├── vlc.py
├── assist/
└── browser/
```

### `README.md`
High‑level project overview: goals, supported platforms, how to run Alekz, and current scope.

### `PROJECT_STRUCTURE.md`
This document. Describes *why* each folder exists and what belongs in it.

### `Makefile`
Top‑level developer commands:
- setup / install dependencies
- run services
- run tests
- clean environments

### `main.py`
Optional global orchestrator.

Responsibilities:
- Start/stop sub‑systems (Rhasspy, browser controller)
- Route intents if a centralized controller is desired

This file may remain thin or even unused in early stages.

### `vlc.py`
Standalone local media controller.

Responsibilities:
- Control VLC via CLI / DBus
- Designed similarly to browser apps for future unification

---

## `assist/` — Voice Assistant Layer

```
assist/
└── rhasspy/
```

### `assist/rhasspy/`
Contains everything related to **Rhasspy**.

Responsibilities:
- Wake word detection ("Alezo")
- Speech‑to‑Text (STT)
- Intent extraction
- Forwarding structured intents to local services

Typical contents (not exhaustive):
- Rhasspy configuration
- Wake word models
- Intent definitions
- Environment variables

Rhasspy is treated as a *black box voice frontend*.

---

## `browser/` — Headful Browser Control (Playwright)

```
browser/
├── controllers
└── apps/
```

This layer is responsible for **controlling real browsers** using **Playwright**, always in **headful mode** with **persistent user profiles**.

### Controllers files (`brave`, `chrome`, `firefox`)

Each file in this folder represents a **browser adapter**.

Responsibilities:
- Launch the browser with the correct binary
- Use a persistent user profile (real session, cookies, logins)
- Expose a uniform control interface

Only browser‑specific code lives here.

---

## `browser/apps/` — Application‑Level Automation

```
browser/apps/
├── youtube.py
├── gmail.py
└── test/
```

Each file here represents a **website controller** that runs *inside* a browser.

These files are browser‑agnostic and operate on a Playwright `Page` object.

### `youtube.py`
YouTube automation logic.

Responsibilities:
- Open YouTube
- Search videos
- Play / pause
- Select results
- Navigate using keyboard or DOM

This is where voice intents ultimately land.

### `gmail.py`
Gmail automation logic.

Responsibilities:
- Open Gmail
- Read inbox state
- Open emails
- Future: send emails

---

## `browser/apps/test/` — Browser Automation Tests

```
browser/apps/test/
├── youtube_test.py
└── gmail.py
```

Automated tests for browser applications.

Responsibilities:
- Verify selectors still work
- Detect UI changes early
- Ensure Playwright flows remain valid

Tests are **headful by design**, matching real usage.

---

## Design Principles Reflected in the Structure

- **Clear separation of concerns**
  - Voice (Rhasspy)
  - Browser control
  - Application logic

- **Browser‑agnostic by design**
  - Apps don’t care whether they run in Brave, Chrome, or Firefox

- **Headful, real‑user automation**
  - No fake profiles
  - No stateless sessions

- **Testability**
  - Browser controlling logic is testable without voice input

- **Future extensibility**
  - New controllable sites go in `browser/apps/`