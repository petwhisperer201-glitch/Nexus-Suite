# NEXUS // MODULE SUITE

Nexus is a cross-platform behavioral utility suite for automated typing and game interaction. It mimics human behavior to avoid detection through randomized input patterns, dynamic fatigue models, and adaptive pausing matrices.

---

## 📦 MODULE OVERVIEW

This repository contains two variations of the engine depending on your specific use case:

1. **`NEXUS.pyw` (Full Suite):** Features a high-fidelity visual dashboard, remote version syncing, advanced human behavioral controls, and a fully automated Multi-Game Vision tool (supporting Kahoot, Blooket, and Gimkit).
2. **`Nexus light(typing mou...).py` (Light Module):** An ultra-compact, lightweight background engine focusing entirely on pure text automation with discrete preset triggers and an instant Overdrive (OVD) speed injection mode.

---

## 🎮 CONTROLS & SHORTCUT MAPS

The keyboard listening layout configures itself automatically based on your active operating system:

### 1. Full Engine (`NEXUS.pyw`)
| Action | 🪟 Windows | 🍏 macOS | 🐧 Linux |
| :--- | :--- | :--- | :--- |
| **Start Typing Engine** | `CTRL + ALT + V` | `CMD + SHIFT + V` | `CTRL + ALT + V` |
| **Hide / Show UI Window** | `ALT + C` | `CMD + SHIFT + H` | `ALT + C` |
| **Emergency Stop Engine** | `ESC` | `ESC` | `ESC` |

### 2. Light Engine (`Nexus light...`)
| Action | 🪟 Windows | 🍏 macOS | 🐧 Linux |
| :--- | :--- | :--- | :--- |
| **Start Typing Engine** | `CTRL + ALT + V` | `CMD + SHIFT + V` | `CTRL + ALT + V` |
| **Hide / Show Mini Window** | `F8` | `F8` | `F8` |
| **Emergency Stop Engine** | `ESC` | `ESC` | `ESC` |

---

## 🛠️ SETUP & SYSTEM DIRECTIONS

### Prerequisite Environments
* Python 3.8 or higher must be installed on your host system.
* Copy your target payload or text to your system clipboard before initializing the typing loops.

---

### Platform-Specific Operating Configurations

#### 🪟 Windows
* **Status:** 100% Fully Functional out-of-the-box.
* **Directions:** 1. Simply double-click `NEXUS.pyw` or the light variant script.
  2. The universal core bootstrap will instantly provision all local package environments (Pillow, PyAutoGUI, Pyperclip, Selenium, etc.) and handle High-DPI layout alignments automatically.

#### 🍏 macOS
* **Status:** Fully Functional (Requires Manual Privacy Authorization).
* **Directions:**
  1. Launch your target module variant directly from your Terminal application:
     ```bash
     python3 NEXUS.pyw
     # OR
     python3 "Nexus light(typing mou...).py"
     ```
  2. Because macOS utilizes sandbox tracking protection, global listener events and script injections will be blocked on the initial trigger.
  3. Authorize the operations manually by opening your computer's interface and navigating to:
     ```text
     System Settings ➔ Privacy & Security ➔ Accessibility
     ```
  4. Explicitly toggle the permission switches to green for your **Terminal** software (or script editor) and the local **Python execution binary**.

#### 🐧 Linux (Ubuntu, Debian, Mint, Fedora, etc.)
* **Status:** Requires Package Verification & X11 Session Adjustment.
* **Directions:**
  1. Linux distributions do not natively package graphic environments with basic interpreters. Run this command to fetch necessary graphical headers before launching the script:
     ```bash
     sudo apt update && sudo apt install python3-tk tk-dev libx11-dev -y
     ```
  2. **Crucial Wayland Security Blockade:** Modern Linux desktops default to an isolated display window engine called **Wayland**, which strictly isolates application windows and intentionally prevents tools like PyAutoGUI from sending keystrokes across applications.
  3. To bypass this, log out of your Linux account entirely. On the main login page, locate the gear/settings icon in the lower-right corner and explicitly switch your session profile to **Ubuntu on Xorg (X11)** or **X11 Session**.
  4. Once logged back into your new desktop environment, boot the application:
     ```bash
     python3 NEXUS.pyw
     ```

---

## 🍴 FORKING & CUSTOM EDITS
If you intend to copy, fork, or edit this project on your own GitHub account, please review the required structural parameters:
- **Review Code Notes:** Ensure you read and include the fork metadata headers provided inside the source files to maintain clear development lanes. You can find the exact block copy template in the `Fork Template.txt` file.
- **Maintain Core Attribution:** Keep the original copyright notices intact to properly credit the foundational layout.
- **Preserve Liability Shields:** Any custom branches must retain the "AS IS" operational clauses to protect both the original developers and individual fork maintainers from liability. Refer to the separate `LICENSE` file for the full open-source legal text.

## DISCLAIMER & LEGAL
Nexus is provided "as is" for educational, production simulation, and accessibility testing purposes only. 
- **The owner and development team are not responsible for any uses or misuses of this software suite.**
- The developers are not liable for any third-party account bans, academic integrity penalties, or unexpected platform flags resulting from automation tracking.
- Users assume total accountability for adhering to the specific Terms of Service governing any targeted external architectures or web clients.

## LICENSE
This project is licensed under the terms of the MIT License. Please see the separate `LICENSE` file in this repository for the full legal framework and operational definitions.

***
Created by petwhisperer201-glitch and The-Samri
