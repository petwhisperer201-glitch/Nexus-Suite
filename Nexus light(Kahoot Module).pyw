# =================================================================
# NEXUS MODULE SUITE - Lightweight Kahoot Module
# Copyright (c) 2026 petwhisperer201-glitch and The-Samri
# 
# Provided "AS IS" for educational and productivity purposes.
# Distributed under the terms of the MIT Open Source License.
#
# The owners and their team are not responsible for misuse, 
# academic penalties, or third-party platform bans. By running 
# this software, the user assumes all structural responsibility.
# =================================================================

VERSION = "1.1.5"

import subprocess
import sys
import os
import importlib
import urllib.request
import threading
import platform
import re
import tkinter.messagebox as messagebox

# Platform Context Matrix Identification
OS_NAME = platform.system()
print(f"[*] Nexus Architecture Detect: Host Environment running on {OS_NAME}")

# =================================================================
# 1. AUTOMATIC DEPENDENCY CHECKER & INSTALLER
# =================================================================
REQUIRED_PACKAGES = {
    "pynput": "pynput",
    "requests": "requests",
    "selenium": "selenium",
    "webdriver_manager": "webdriver-manager"
}

def bootstrap_dependencies():
    print("[*] Nexus Module Suite: Checking dependencies...")
    missing_packages = []

    for module_name, pip_name in REQUIRED_PACKAGES.items():
        try:
            importlib.import_module(module_name)
        except ImportError:
            print(f"[!] Missing dependency: {pip_name}")
            missing_packages.append(pip_name)

    if missing_packages:
        print(f"[*] Installing missing packages: {', '.join(missing_packages)}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing_packages, "--user", "--quiet"])
            print("[+] Environment successfully provisioned.")
        except subprocess.CalledProcessError as e:
            print(f"[-] Critical Error: Failed to install dependencies automatically.\nDetails: {e}")
            sys.exit(1)
    else:
        print("[+] All dependencies verified.")

bootstrap_dependencies()


# =================================================================
# 2. SEAMLESS REPOSITORY AUTO-UPDATER
# =================================================================
def check_for_updates():
    raw_url = "https://raw.githubusercontent.com/petwhisperer201-glitch/Nexus-Suite/refs/heads/main/Nexus%20light(Kahoot%20Module).pyw"
    try:
        print("[NEXUS] Checking repository sync status...")
        ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' if OS_NAME == "Windows" else 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        req = urllib.request.Request(raw_url, headers={'User-Agent': ua})
        
        with urllib.request.urlopen(req, timeout=5) as response:
            remote_code = response.read().decode('utf-8')
            
        # Parse out the actual version tag number safely from remote script lines
        match = re.search(r'VERSION\s*=\s*["\']([^"\']+)["\']', remote_code)
        
        if match:
            remote_version = match.group(1)
            if remote_version != VERSION:
                print(f"[NEXUS] New update discovered: v{remote_version} (Current local: v{VERSION})")
                print("[NEXUS] Overwriting local architecture matrix...")
                
                # Capture the precise system location path of this file and rewrite its contents
                current_file_path = os.path.abspath(__file__)
                with open(current_file_path, "w", encoding="utf-8") as f:
                    f.write(remote_code)
                    
                print("[NEXUS] Update successfully injected!")
                messagebox.showinfo(
                    "Nexus Suite Updated", 
                    f"Successfully updated from v{VERSION} to v{remote_version}!\n\nThe application will now close. Please restart it."
                )
                os._exit(0)
            else:
                print("[+] Nexus Suite is fully synchronized.")
    except Exception as e:
        print(f"[-] Code sync sequence bypassed: {e}")


# =================================================================
# 3. CORE APPLICATION CODE
# =================================================================
import tkinter as tk
from tkinter import ttk
import random
import time
import requests
from pynput import keyboard
from pynput.keyboard import Controller as KeyboardController

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from selenium.webdriver.common.by import By

COLORS = {
    "bg": "#FFFFFF",
    "btn": "#F1F5F9",
    "accent": "#0091FF",
    "overdrive": "#FF4B2B",
    "text": "#2D3748",
    "status_ready": "#E2E8F0",
    "status_active": "#0091FF",
    "status_wait": "#F6AD55"
}

class LightKahootNexusTool:
    def __init__(self, root):
        self.root = root
        self.root.geometry("340x110")
        self.root.configure(bg=COLORS["bg"])
        self.root.title("")
        self.root.resizable(False, False)

        if OS_NAME == "Windows":
            self.root.attributes("-topmost", True)
            try:
                import ctypes
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except:
                pass

        self.is_running = False
        self.stop_requested = False
        self.is_hidden = False
        self.selected_error_rate = 0
        self.driver = None
        self.keyboard_controller = KeyboardController()

        content = tk.Frame(self.root, bg=COLORS["bg"], padx=5, pady=2)
        content.pack(fill="both", expand=True)

        ui_font = ("Helvetica", 8, "bold") if OS_NAME != "Windows" else ("Segoe UI", 8, "bold")
        hint_font = ("Helvetica", 7) if OS_NAME != "Windows" else ("Segoe UI", 7)

        # ROW 1: Target Parameters
        input_frame = tk.Frame(content, bg=COLORS["bg"])
        input_frame.pack(fill="x", pady=2)

        tk.Label(input_frame, text="PIN/URL:", font=ui_font, bg=COLORS["bg"], fg=COLORS["text"]).pack(side="left", padx=2)
        self.url_entry = tk.Entry(input_frame, font=("Segoe UI", 8) if OS_NAME == "Windows" else ("Helvetica", 8), bg=COLORS["btn"], fg=COLORS["text"], relief="flat", width=20)
        self.url_entry.pack(side="left", padx=2)
        self.url_entry.insert(0, "")

        self.browser_var = tk.StringVar(value="chrome")
        self.browser_dropdown = ttk.Combobox(input_frame, textvariable=self.browser_var, values=["chrome", "firefox", "edge"], state="readonly", font=hint_font, width=8)
        self.browser_dropdown.pack(side="right", padx=2)

        # ROW 2: Accuracy Selectors
        btn_frame = tk.Frame(content, bg=COLORS["bg"])
        btn_frame.pack(fill="x", pady=2)

        tk.Label(btn_frame, text="Error%:", font=ui_font, bg=COLORS["bg"], fg=COLORS["text"]).pack(side="left", padx=2)

        self.btns = {}
        for rate in [0, 5, 10, 15, 25]:
            b = tk.Button(btn_frame, text=f"{rate}%", command=lambda r=rate: self.set_error_rate(r),
                          bg=COLORS["btn"], fg=COLORS["text"], relief="flat",
                          font=ui_font, width=4)
            b.pack(side="left", padx=1)
            self.btns[rate] = b

        self.set_error_rate(0)

        # ROW 3: Shortcuts Layout Hint
        bottom = tk.Frame(content, bg=COLORS["bg"])
        bottom.pack(fill="x", pady=2)
        
        shortcut_label = "F8: Hide | ESC: Kill | CTRL+ALT+V: Launch" if OS_NAME != "Darwin" else "F8: Hide | ESC: Kill | CMD+SHIFT+V: Launch"

        tk.Label(bottom, text=shortcut_label, font=hint_font, bg=COLORS["bg"], fg="#A0AEC0").pack(side="left")
        self.start_btn = tk.Button(bottom, text="START ENGINE", command=self.trigger, bg=COLORS["accent"],
                                   fg="white", font=ui_font, relief="flat", padx=10)
        self.start_btn.pack(side="right")

        self.status_bar = tk.Frame(self.root, height=3, bg=COLORS["status_ready"])
        self.status_bar.pack(fill="x", side="bottom")

        if OS_NAME == "Darwin":
            hotkeys = {
                '<f8>':            self.toggle_visibility,
                '<cmd>+<shift>+v': self.trigger,
                '<esc>':           self.stop
            }
        else:
            hotkeys = {
                '<f8>':           self.toggle_visibility,
                '<ctrl>+<alt>+v': self.trigger,
                '<esc>':          self.stop
            }

        try:
            self.hk = keyboard.GlobalHotKeys(hotkeys)
            threading.Thread(target=self.hk.run, daemon=True).start()
        except Exception as e:
            print(f"[!] Background hotkey engine matrix fallback: {e}")

        # Run update check immediately inside background thread
        threading.Thread(target=check_for_updates, daemon=True).start()

    def set_error_rate(self, r):
        self.selected_error_rate = r
        for rate, btn in self.btns.items():
            btn.config(bg=COLORS["accent"] if rate == r else COLORS["btn"], fg="white" if rate == r else COLORS["text"])

    def toggle_visibility(self):
        def action():
            if self.is_hidden: 
                self.root.deiconify()
                if OS_NAME == "Windows":
                    self.root.attributes("-topmost", True)
            else: 
                self.root.withdraw()
            self.is_hidden = not self.is_hidden
        self.root.after(0, action)

    def stop(self):
        self.stop_requested = True
        self.root.after(0, lambda: self.status_bar.config(bg="#F56565"))
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
        self.is_running = False

    def trigger(self):
        if not self.is_running: 
            threading.Thread(target=self.automation_worker, daemon=True).start()

    def _get_groq_decision(self, question, choices):
        try:
            response = requests.post("https://nexus-relay-zdj6.onrender.com/ask", json={"question": question, "choices": choices}, timeout=8)
            if response.status_code == 200:
                return response.json().get("answer")
        except:
            pass
        return None

    def automation_worker(self):
        self.is_running, self.stop_requested = True, False
        self.root.after(0, lambda: self.status_bar.config(bg=COLORS["status_wait"]))
        
        raw_input = self.url_entry.get().strip()
        if not raw_input:
            messagebox.showwarning("Nexus Engine", "Game Code PIN or URL Destination cannot be empty!")
            self.stop()
            return
            
        if raw_input.isdigit():
            target_destination = f"https://kahoot.it/?pin={raw_input}"
        else:
            target_destination = raw_input if raw_input.startswith("http") else f"https://{raw_input}"

        browser_choice = self.browser_var.get().lower()
        
        try:
            if browser_choice == "chrome":
                opts = ChromeOptions()
                opts.add_argument("--disable-gpu")
                opts.add_argument("--window-size=1280,720")
                self.driver = webdriver.Chrome(options=opts)
            elif browser_choice == "firefox":
                opts = FirefoxOptions()
                self.driver = webdriver.Firefox(options=opts)
            elif browser_choice == "edge":
                opts = EdgeOptions()
                opts.add_argument("--disable-gpu")
                opts.add_argument("--window-size=1280,720")
                self.driver = webdriver.Edge(options=opts)
                
            self.driver.get(target_destination)
            self.root.after(0, lambda: self.status_bar.config(bg=COLORS["status_active"]))
        except Exception as e:
            messagebox.showerror("Nexus Initialization Error", f"Engine failed to couple with your {browser_choice.upper()} browser.\n\nError Message:\n{str(e)[:250]}")
            self.stop()
            return

        selectors = {
            "question": ['[data-functional-selector="question-title"]', '[data-functional-selector="block-title"]', '.quiz-question-title', 'main h1'],
            "choices": ['[data-functional-selector^="answer-"]', '.quiz-answer-choice', 'button[id^="answer-"]']
        }

        last_scraped_question = ""

        while not self.stop_requested:
            try:
                question_text = ""
                for selector in selectors["question"]:
                    try:
                        el = self.driver.find_element(By.CSS_SELECTOR, selector)
                        if el and el.text.strip():
                            question_text = el.text.strip()
                            break
                    except:
                        pass

                if not question_text:
                    last_scraped_question = ""

                if question_text and question_text != last_scraped_question:
                    choice_elements = []
                    for c_sel in selectors["choices"]:
                        try:
                            choice_elements = self.driver.find_elements(By.CSS_SELECTOR, c_sel)
                            if choice_elements and any(e.text.strip() for e in choice_elements): 
                                break
                        except:
                            pass
                    
                    choices = [el.text.strip() for el in choice_elements if el.text.strip()]
                    if choices:
                        last_scraped_question = question_text
                        answer = self._get_groq_decision(question_text, choices)
                        
                        if answer:
                            if random.randint(1, 100) <= self.selected_error_rate:
                                answer = random.choice(choices)
                            
                            time.sleep(random.uniform(0.4, 1.2))
                            
                            for idx, choice_text in enumerate(choices):
                                if answer.lower() in choice_text.lower() or choice_text.lower() in answer.lower():
                                    key_map = ["1", "2", "3", "4"]
                                    if idx < len(key_map):
                                        target_key = key_map[idx]
                                        self.keyboard_controller.press(target_key)
                                        self.keyboard_controller.release(target_key)
                                        print(f"[+] Key execution mapped and sent: [{target_key}]")
                                        break
            except:
                pass
            time.sleep(0.25)

        self.stop()

if __name__ == "__main__":
    root = tk.Tk()
    app = LightKahootNexusTool(root)
    root.mainloop()
