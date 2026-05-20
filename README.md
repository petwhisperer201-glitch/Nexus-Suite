# NEXUS // MODULE SUITE

Nexus is a cross-platform behavioral utility suite for automated typing and game interaction. It mimics human behavior to avoid detection through randomized input patterns, dynamic fatigue models, and adaptive pausing matrices.

## KEY FEATURES
- **Human Typing:** Simulates behavioral fatigue, variable pauses, and localized adjacent-key typos.
- **Focus Control:** Automatically pauses typing if the target window loses focus (Windows natively).
- **Universal Bootstrap:** Detects the host architecture and installs required platform-specific Python libraries on first launch.
- **Cross-Platform Compliance:** Dynamically formats window boundaries, driver settings, and operational parameters for seamless cross-OS execution.

---

## CONTROLS & SHORTCUTS

The keyboard listening module adapts dynamically depending on your active operating system environment:

| Action | Windows |  macOS | Linux |
| :--- | :--- | :--- | :--- |
| **Start Typing Engine** | `CTRL + ALT + V` | `CMD + SHIFT + V` | `CTRL + ALT + V` |
| **Hide / Show UI Window** | `ALT + C` | `CMD + SHIFT + H` | `ALT + C` |
| **Emergency Stop Engine** | `ESC` | `ESC` | `ESC` |

---

## SETUP & REQUIREMENTS

### 1. Prerequisite Environments
* Python 3.8 or higher must be installed on your machine.
* Ensure your clipboard contains the text or payload you wish to automate before triggering the engine.

### 2. Platform-Specific Configurations

#### Windows
* **Status:** 100% Fully Functional out-of-the-box.
* **Steps:** 1. Download `NEXUS.pyw`.
  2. Double-click to run. The primary initialization layer will automatically handle High-DPI display adjustments and allocate package architectures.

#### macOS
* **Status:** Fully Functional (Requires System Security Configuration).
* **Steps:**
  1. Open your Terminal and launch the file using: `python3 NEXUS.pyw`
  2. Because macOS isolates background automation, the system will block global keyboard and mouse triggers on first use.
  3. You **must** manually grant accessibility permissions by navigating to:
     System Settings -> Privacy & Security -> Accessibility
  4. Toggle the switch to explicitly allow your **Terminal app** (or IDE) and the **Python binary** to control your computer.

#### Linux (Ubuntu, Debian, Mint, Fedora, etc.)
* **Status:** Requires Package Installation & X11 Display Engine configuration.
* **Steps:**
  1. Linux distributions do not ship with basic graphic wrapper packages. Before launching the script, open your terminal and install the underlying developmental headers:
     ```bash
     sudo apt update && sudo apt install python3-tk tk-dev libx11-dev -y
     ```
  2. **Crucial Security Restriction:** Modern Linux distributions default to a secure display server called **Wayland**, which strictly bans background software from logging keys or injecting clicks into external windows. 
  3. To bypass this barrier, log completely out of your Linux user profile. On the login screen, click the small gear/settings icon in the bottom corner and change your active session from **Ubuntu/Wayland** to **Ubuntu on Xorg (X11)**.
  4. Once logged back into an X11 session, execute the utility: `python3 NEXUS.pyw`

---

## FORKING & CUSTOM EDITS
If you intend to copy, fork, or edit this project on your own GitHub account, please review the required structural parameters:
- **Review Code Notes:** Ensure you read and include the fork metadata headers provided inside the source files to maintain clear development lanes. You can find the exact block copy template in the `Fork Template` file.
- **Maintain Core Attribution:** Keep the original copyright notices intact to properly credit the foundational layout.
- **Preserve Liability Shields:** Any custom branches must retain the "AS IS" operational clauses to protect both the original developers and individual fork maintainers from liability. Refer to the separate `LICENSE` file for the full open-source legal text.

## DISCLAIMER & LEGAL
Nexus is provided "as is" for educational and productivity purposes only. 
- **The owner and his team are not responsible for any uses or misuses of this software.**
- The developer is not responsible for any account bans, academic penalties, or consequences resulting from the use of this tool.
- Users are responsible for complying with the Terms of Service of any third-party platforms used in conjunction with this software.
- This tool does not bypass hardware-level security, anti-cheat barriers, or encrypted root-level kernel tracking modules.

## LICENSE
This project is licensed under the terms of the MIT License. Please see the separate [LICENSE](LICENSE) file in this repository for the full legal framework and operational terms.

***
Created by petwhisperer201-glitch and The-Samri
