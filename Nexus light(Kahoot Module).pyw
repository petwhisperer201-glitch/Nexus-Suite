# =================================================================
# NEXUS MODULE SUITE - Light Kahoot Interface Module
# Copyright (c) 2026 petwhisperer201-glitch and The-Samri
# 
# Provided "AS IS" for educational and productivity purposes.
# Distributed under the terms of the MIT Open Source License.
# =================================================================

VERSION = "1.1.0"

import subprocess
import sys
import importlib
import urllib.request
import threading
import platform
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
# 2. CORE APPLICATION CODE
# =================================================================
import tkinter as tk
import random
import time
import re
import requests
from pynput import keyboard
from pynput.keyboard import Controller as KeyboardController

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

COLORS = {
    "bg": "#FFFFFF",
    "btn": "#F1F5F9",
    "accent": "#9D4EDD",
    "overdrive": "#FF4B2B",
    "text": "#2D3748",
    "status_ready": "#E2E8F0",
    "status_active": "#0091FF",
    "status_wait": "#F6AD55"
}

class LightKahootTool:
    def __init__(self, root):
        self.root = root
        self.root.geometry("340x80")
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

        content = tk.Frame(self.root, bg=COLORS["bg"], padx=5, pady=5)
        content.pack(fill="both", expand=True)

        btn_frame = tk.Frame(content, bg=COLORS["bg"])
        btn_frame.pack(fill="x", pady=2)

        tk.Label(btn_frame, text="Error%:", font=("Segoe UI", 8, "bold") if OS_NAME == "Windows" else ("Helvetica", 8, "bold"), bg=COLORS["bg"], fg=COLORS["text"]).pack(side="left", padx=2)

        self.btns = {}
        ui_font = ("Segoe UI", 8, "bold") if OS_NAME == "Windows" else ("Helvetica", 8, "bold")
        hint_font = ("Segoe UI", 7) if OS_NAME == "Windows" else ("Helvetica", 7)

        for rate in [0, 5, 10, 15, 25]:
            b = tk.Button(btn_frame, text=f"{rate}%", command=lambda r=rate: self.set_error_rate(r),
                          bg=COLORS["btn"], fg=COLORS["text"], relief="flat",
                          font=ui_font, width=4)
            b.pack(side="left", padx=2)
            self.btns[rate] = b

        self.set_error_rate(0)

        bottom = tk.Frame(content, bg=COLORS["bg"])
        bottom.pack(fill="x", pady=2)
        
        if OS_NAME == "Darwin":
            shortcut_label = "F8: Hide | ESC: Kill Engine"
        else:
            shortcut_label = "F8: Hide | ESC: Kill Engine"

        tk.Label(bottom, text=shortcut_label, font=hint_font, bg=COLORS["bg"], fg="#A0AEC0").pack(side="left")
        self.start_btn = tk.Button(bottom, text="LAUNCH ENGINE", command=self.trigger, bg=COLORS["accent"],
                                   fg="white", font=ui_font, relief="flat", padx=10)
        self.start_btn.pack(side="right")

        self.status_bar = tk.Frame(self.root, height=3, bg=COLORS["status_ready"])
        self.status_bar.pack(fill="x", side="bottom")

        if OS_NAME == "Darwin":
            hotkeys = {
                '<f8>': self.toggle_visibility,
                '<esc>': self.stop
            }
        else:
            hotkeys = {
                '<f8>': self.toggle_visibility,
                '<esc>': self.stop
            }

        try:
            self.hk = keyboard.GlobalHotKeys(hotkeys)
            threading.Thread(target=self.hk.run, daemon=True).start()
        except Exception as e:
            print(f"[!] Background hotkey engine error: {e}")

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
        self.status_bar.config(bg="#F56565")
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
            # Using the exact fallback API endpoint configured inside the Nexus framework
            response = requests.post("https://nexus-relay-zdj6.onrender.com/ask", json={"question": question, "choices": choices}, timeout=8)
            if response.status_code == 200:
                return response.json().get("answer")
        except:
            pass
        return None

    def automation_worker(self):
        self.is_running, self.stop_requested = True, False
        self.status_bar.config(bg=COLORS["status_wait"])
        
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1280,720")
        
        try:
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
            self.driver.get("https://kahoot.it")
            self.status_bar.config(bg=COLORS["status_active"])
        except Exception as e:
            print(f"[-] Driver initialization failure: {e}")
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

                if question_text and question_text != last_scraped_question:
                    choice_elements = []
                    for c_sel in selectors["choices"]:
                        try:
                            choice_elements = self.driver.find_elements(By.CSS_SELECTOR, c_sel)
                            if choice_elements: 
                                break
                        except:
                            pass
                    
                    choices = [el.text.strip() for el in choice_elements if el.text.strip()]
                    if choices:
                        last_scraped_question = question_text
                        answer = self._get_groq_decision(question_text, choices)
                        
                        if answer:
                            # Apply intentional target simulation mistake calculation
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
            except Exception as e:
                pass
            time.sleep(0.4)

        self.stop()

if __name__ == "__main__":
    root = tk.Tk()
    app = LightKahootTool(root)
    root.mainloop()
