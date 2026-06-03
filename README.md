# NEXUS // MODULE SUITE

Nexus is a cross-platform behavioral utility suite designed for automated typing simulation and live game client interaction. It leverages programmatic delay profiles, randomized user-fatigue matrices, and headless visual matching layers to smooth input tracks across target environments.

---

## MODULE OVERVIEW

This repository partitions core mechanics into three specific, decoupled script variations depending on your workspace footprint or automation objective:

1. **`NEXUS.pyw` (Full Core Suite):** Features the high-fidelity graphical Matrix-rain dashboard, live repository update sync patches, sliders for customized human pacing, and the unified vision tab system containing automated bypass tools for Kahoot and Blooket sessions.
2. **`Nexus light(Typing Moudle).pwy` (Standalone Typing):** An ultra-compact, stripped-down desktop injector focused purely on text streaming automation. Features discrete WPM modifier hotkeys and an integrated instant Overdrive (OVD) layout switch.
3. **`Nexus light(Kahoot Module).pyw` (Standalone Kahoot Engine):** A minimalist standalone web-automation node built exclusively to target live game structures. It strips out all typing code strings, tracking browser selectors directly via standard Selenium frameworks, and includes a localized error-percentage calibration matrix.

---

## CONTROLS & SHORTCUT MAPS

System shortcut behaviors automatically map based on host platform parameters:

### 1. Full Master Suite (`NEXUS.pyw`)
| Action | Windows | macOS | Linux |
| :--- | :--- | :--- | :--- |
| **Start Behavioral Typing** | `CTRL + ALT + V` | `CMD + SHIFT + V` | `CTRL + ALT + V` |
| **Toggle Suite Window Visibility** | `ALT + C` | `CMD + SHIFT + H` | `ALT + C` |
| **Emergency Kill Typing Thread** | `ESC` | `ESC` | `ESC` |

### 2. Standalone Typing Engine (`Nexus light(Typing Moudle).pwy`)
| Action | Windows | macOS | Linux |
| :--- | :--- | :--- | :--- |
| **Inject Clipboard String** | `CTRL + ALT + V` | `CMD + SHIFT + V` | `CTRL + ALT + V` |
| **Toggle Mini Overlay View** | `F8` | `F8` | `F8` |
| **Emergency Halt Automation** | `ESC` | `ESC` | `ESC` |

### 3. Standalone Kahoot Node (`Nexus light(Kahoot Module).pyw`)
| Action | Windows | macOS | Linux |
| :--- | :--- | :--- | :--- |
| **Launch Web Driver Frame** | Click `LAUNCH ENGINE` GUI Button | Click `LAUNCH ENGINE` GUI Button | Click `LAUNCH ENGINE` GUI Button |
| **Toggle Window Visibility Matrix** | `F8` | `F8` | `F8` |
| **Emergency Close & Driver Kill** | `ESC` | `ESC` | `ESC` |

---

## SETUP & SYSTEM DIRECTIONS

### Prerequisite Environments
* Python 3.8 (or higher) is mandatory for core system compilation.
* For the typing engines, copy target payload texts directly to the clipboard before execution. 
* For the Kahoot vision modules, a valid, unobstructed internet connection is required to coordinate with the API decisions and internal web drivers.

---

### Platform-Specific Operating Configurations

#### Windows
* **Status:** 100% Fully Functional with high-DPI platform scaling adjustments out of the box.
* **Directions:** Direct execution by double-clicking the specified script module target. The bootstrap pipeline automatically pulls missing environment attachments (`Pillow`, `pyautogui`, `pyperclip`, `pynput`, `requests`, `selenium`, `webdriver-manager`, `pygetwindow`, `pystray`) into local user paths cleanly and quietly.

#### macOS
* **Status:** Fully Functional (Requires Manual Accessibility Entitlements).
* **Directions:**
  1. Boot your selected automation component directly using your terminal console framework:
     ```bash
     python3 NEXUS.pyw
     # OR
     python3 "Nexus light(Kahoot Module).pyw"
     ```
  2. Because macOS isolates input-monitoring permissions, background event handlers and hotkey hooks are restricted during initialization.
  3. Approve execution access by pointing your computer’s workspace preferences to:
     ```text
     System Settings ➔ Privacy & Security ➔ Accessibility
     ```
  4. Ensure permissions are toggled to active for your targeting **Terminal** application instance and the base **Python application binary**.

#### Linux (Ubuntu, Debian, Mint, Fedora, etc.)
* **Status:** Requires Frame Buffer Prerequisites & X11 Workspace Switch.
* **Directions:**
  1. Linux server configurations lack embedded graphical framework wrappers. Deploy structural window dependencies using your native package manager before script launch:
     ```bash
     sudo apt update && sudo apt install python3-tk tk-dev libx11-dev -y
     ```
  2. **Wayland Display Restrictions:** Modern distribution default desktop engines (Wayland) purposefully separate processing structures, blocking libraries like `pyautogui` or `pynput` from dispatching virtual keystrokes across decoupled app layers.
  3. To bypass this, log out of your current session profile. Before re-entering your user credentials, locate the gear icon in the lower corner of the display manager and explicitly modify the target profile setting to **Ubuntu on Xorg** or **X11 Session**.
  4. Once initialized into your new graphic environment session, execute:
     ```bash
     python3 NEXUS.pyw
     ```

---

## FORKING & CUSTOM EDITS
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
