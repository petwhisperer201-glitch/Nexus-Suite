# =================================================================
# NEXUS MODULE SUITE - Behavioral Utility Tool
# Copyright (c) 2026 petwhisperer201-glitch and The-Samri
# 
# Provided "AS IS" for educational and productivity purposes.
# Distributed under the terms of the MIT Open Source License.
#
# The owners and their team are not responsible for misuse, 
# academic penalties, or third-party platform bans. By running 
# this software, the user assumes all structural responsibility.
# =================================================================

VERSION = "7.1.0"  # Windows + macOS + Linux Seamless Integration

import subprocess
import sys
import os
import time
import threading
import re
import random
import json
import tkinter as tk
import urllib.request
import platform

# 1. CORE OPERATING SYSTEM MATRIX DETECTION
OS_NAME = platform.system()  # Identifies 'Windows', 'Darwin' (macOS), or 'Linux'
print(f"[NEXUS] Core Init | Operating System Detected: {OS_NAME} | Engine: {VERSION}")

# Universal Cross-Platform Bootstrap Setup
def bootstrap():
    # Core libraries baseline across all execution vectors
    libs = [
        'Pillow', 'pyautogui', 'pyperclip', 'pynput', 
        'requests', 'selenium', 'webdriver-manager'
    ]
    
    # Isolate platform-volatile components to protect initialization threads
    if OS_NAME == "Windows":
        libs.append('pygetwindow')
        libs.append('pystray')

    for lib in libs:
        try:
            if lib == 'Pillow':
                __import__('PIL')
            else:
                __import__(lib.lower())
        except ImportError:
            try:
                print(f"Installing missing dependency: {lib}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", lib, "--user", "--quiet"])
            except:
                pass

bootstrap()

import pyautogui
import pyperclip
import requests
from pynput import keyboard
from pynput.keyboard import Controller as KeyboardController

# CHROME & EDGE AUTOMATION VECTOR ENGINE
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

pyautogui.FAILSAFE = True 
pyautogui.PAUSE = 0

# 2. SEPARATE PLATFORM DPI ACCURACY AND WINDOW HOOK LOGIC
HAS_FOCUS_LOGIC = False
if OS_NAME == "Windows":
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Resolve High-DPI Windows Scaling anomalies
        import pygetwindow as gw
        HAS_FOCUS_LOGIC = True
    except:
        pass
else:
    HAS_FOCUS_LOGIC = False


# Remote Version Sync Matrix
def check_for_updates():
    RAW_GITHUB_URL = "https://raw.githubusercontent.com/petwhisperer201-glitch/Nexus-Suite/main/NEXUS.pyw"
    try:
        print("[NEXUS] Checking repository sync status...")
        # Adjust target User Agent signatures safely according to execution host
        ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' if OS_NAME == "Windows" else 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        req = urllib.request.Request(RAW_GITHUB_URL, headers={'User-Agent': ua})
        with urllib.request.urlopen(req, timeout=5) as response:
            remote_code = response.read().decode('utf-8')
            
        match = re.search(r'VERSION\s*=\s*["\']([^"\']+)["\']', remote_code)
        
        if match:
            remote_version = match.group(1)
            if remote_version != VERSION:
                print(f"[NEXUS] New update discovered: v{remote_version} (Current local: v{VERSION})")
                print("[NEXUS] Rewriting local script matrix...")
                
                current_file_path = os.path.abspath(__file__)
                with open(current_file_path, "w", encoding="utf-8") as f:
                    f.write(remote_code)
                    
                print("[NEXUS] Update successfully injected! Please close and reopen the application.")
                sys.exit(0)
            else:
                print("[NEXUS] Version check verified. Core is fully synchronized.")
    except Exception as e:
        print(f"[NEXUS] Update sequence bypassed: {e}")


# INTERFACE THEME STYLIZATION MAPS
THEME_NEXUS = {
    "bg":      "#000000",
    "rain":    "#002200",
    "rain_h":  "#00FF41",
    "accent":  "#00F0FF",
    "text":    "#FFFFFF",
    "dim":     "#444444",
    "chars":   "01NEXUS",
}

THEME_KAHOOT = {
    "bg":      "#0A0212",
    "rain":    "#240046",
    "rain_h":  "#E0AAFF",
    "accent":  "#9D4EDD",
    "text":    "#F7F4F9",
    "dim":     "#3C096C",
    "chars":   "▲▼◀▶◆■▲▼◆■",
}

THEME_LAUNCHER = {
    "bg":      "#000000",
    "rain":    "#002200",
    "rain_h":  "#00FF41",
    "accent":  "#00F0FF",
    "text":    "#FFFFFF",
    "dim":     "#444444",
    "chars":   "01NEXUS",
}

SETTINGS_FILE = os.path.join(os.path.expanduser("~"), ".nexus_config.json")

def save_settings(speed, errors):
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump({'speed': float(speed), 'errors': int(errors)}, f)
    except:
        pass

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                data = json.load(f)
                return {
                    'speed': data.get('speed', 0.10), 
                    'errors': data.get('errors', 2)
                }
        except:
            pass
    return {'speed': 0.10, 'errors': 2}


# BEHAVIORAL HUMAN-TYPING MATRIX ENGINE
class NexusEngine:
    def __init__(self):
        self.is_typing      = False
        self.stop_requested = False
        self.char_count     = 0
        self.lock           = threading.Lock()
        self.NEIGHBORS = {
            'a':'qwsz','b':'vghn','c':'xdfv','d':'erfcx','e':'rdsw','f':'rtgvc','g':'tyhbv','h':'yujnb',
            'i':'ujko','j':'uikmn','k':'iolm','l':'opk','m':'njk','n':'bhjm','o':'pikl','p':'ol',
            'q':'was','r':'edft','s':'awdxz','t':'rfgy','u':'yhjkio','v':'cfgb','w':'qase',
            'x':'zsdc','y':'tghu','z':'asx','1':'2q','2':'1q3w','3':'2w4e','4':'3e5r','5':'4r6t',
            '6':'5t7y','7':'6y8u','8':'7u9i','9':'8i0o','0':'9oip','-':'0p','=':'-',' ':'cvbnm'
        }

    def run(self, raw, speed, ent, status_cb):
        if not self.lock.acquire(blocking=False):
            return
        self.is_typing, self.stop_requested, self.char_count = True, False, 0

        status_cb("> ACTIVE", THEME_NEXUS["rain_h"])
        try:
            text  = re.sub(r'[^\x20-\x7E\n\r]', '', raw.replace('\xa0', ' '))
            words = text.split(' ')
            for word_idx, word in enumerate(words):
                if self.stop_requested:
                    break
                if word_idx > 0 and word_idx % random.randint(15, 40) == 0:
                    status_cb("> THINKING...", "#AA00FF")
                    time.sleep(random.uniform(1.2, 3.0))
                wc = 0.8 if len(word) < 4 else 1.2
                for char in word:
                    if self.stop_requested:
                        break
                    
                    # 3. COMPATIBLE ADAPTIVE WINDOW PROTECTION INTERFACE
                    if HAS_FOCUS_LOGIC and OS_NAME == "Windows":
                        try:
                            active_win = gw.getActiveWindow()
                            if active_win and "NEXUS" in active_win.title:
                                status_cb("> WAITING FOR TARGET", "#FFCC00")
                                time.sleep(0.5)
                                continue
                        except:
                            pass

                    status_cb("> ACTIVE", THEME_NEXUS["rain_h"])
                    fatigue = 1 + (self.char_count / 8000)
                    if char.lower() in self.NEIGHBORS and random.random() < ent:
                        pyautogui.write(random.choice(self.NEIGHBORS[char.lower()]))
                        time.sleep(random.uniform(0.15, 0.3))
                        pyautogui.press('backspace')
                        time.sleep(random.uniform(0.05, 0.15))
                    pyautogui.write(char)
                    self.char_count += 1
                    delay = speed * wc * fatigue * random.uniform(0.6, 1.4)
                    if char in ".!?": delay += random.uniform(0.3, 0.6)
                    elif char in ",;:": delay += random.uniform(0.1, 0.3)
                    time.sleep(delay)
                pyautogui.write(' ')
                time.sleep(speed * random.uniform(0.5, 1.0))
        finally:
            self.is_typing, self.stop_requested = False, False
            self.lock.release()
            status_cb("> READY", THEME_NEXUS["accent"])


# RE-OPTIMIZED GRAPHICAL GAME AUTOMATION PIPELINE
class KahootEngine:
    def __init__(self):
        self.is_running = False
        self.stop_requested = False
        self.driver = None
        self.worker_thread = None
        self.keyboard_controller = KeyboardController()

    def _get_platform_selectors(self, platform):
        platform = platform.lower()
        if platform == "kahoot":
            return {
                "question": [
                    '[data-functional-selector="question-title"]',
                    '[data-functional-selector="block-title"]',
                    '.quiz-question-title', 'main h1', 'h1[class*="Title"]'
                ],
                "choices": [
                    '[data-functional-selector^="answer-"]', 
                    '.quiz-answer-choice', 
                    'button[id^="answer-"]',
                    'div[class*="CardContent"]'
                ]
            }
        elif platform == "blooket":
            return {
                "question": ['h1', '.question-text', '[class*="question"]', '[class*="Question"]', 'div[class*="title"]'],
                "choices": ['button', '[class*="answer"]', '[class*="choice"]', 'div[role="button"]', '[class*="Answer"]']
            }
        elif platform == "gimkit":
            return {
                "question": ['h1', 'h2', '[class*="question"]', '[class*="Question"]', '.question-text'],
                "choices": ['button', '[class*="answer"]', '[class*="option"]', 'div[role="button"]', '[class*="choice"]']
            }
        return self._get_platform_selectors("kahoot")

    def start_automation(self, target_url, browser_type, status_cb, game_mode="kahoot"):
        if self.is_running:
            status_cb("> ALREADY RUNNING", "#FF3366")
            return
        
        self.stop_requested = False
        self.is_running = True
        
        self.worker_thread = threading.Thread(
            target=self._automation_worker, 
            args=(target_url, browser_type, status_cb, game_mode), 
            daemon=True
        )
        self.worker_thread.start()

    def _automation_worker(self, target_url, browser_type, status_cb, game_mode="kahoot"):
        status_cb(f"> INITIALIZING {browser_type.upper()} for {game_mode.upper()}...", "#FFAA00")
        selectors = self._get_platform_selectors(game_mode)
        
        try:
            # 4. CROSS-PLATFORM SYSTEM CHROMIUM GRAPHICS CONFIGURATION
            if browser_type.lower() == "chrome":
                service = ChromeService(ChromeDriverManager().install())
                chrome_options = ChromeOptions()
                if OS_NAME == "Windows":
                    chrome_options.add_argument("--start-maximized")
                else:
                    chrome_options.add_argument("--window-size=1440,900")  # Fix cross-platform display scaling crashes
                chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            else:
                service = EdgeService(EdgeChromiumDriverManager().install())
                edge_options = EdgeOptions()
                if OS_NAME == "Windows":
                    edge_options.add_argument("--start-maximized")
                else:
                    edge_options.add_argument("--window-size=1440,900")
                edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                self.driver = webdriver.Edge(service=service, options=edge_options)
            
            status_cb("> CONNECTING TO TARGET...", "#00F0FF")
            self.driver.get(target_url)
            
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
                        status_cb("> NEW QUESTION DETECTED", "#00FF41")
                        
                        choice_elements = []
                        for c_sel in selectors["choices"]:
                            try:
                                choice_elements = self.driver.find_elements(By.CSS_SELECTOR, c_sel)
                                if choice_elements and any(el.text.strip() for el in choice_elements):
                                    break
                            except:
                                pass
                                    
                        choices = [el.text.strip() for el in choice_elements if el.text.strip()]
                        
                        if choices:
                            last_scraped_question = question_text
                            print(f"[NEXUS] {game_mode.upper()} | Question: {question_text}")
                            print(f"[NEXUS] Choices: {choices}")
                            status_cb("> ROUTING VIA SECURE RELAY...", "#FFAA00")
                            
                            answer = self._get_groq_decision(question_text, choices)
                            
                            if answer:
                                print(f"[NEXUS] Relay Target: {answer}")
                                status_cb(f"> CHOICE: {answer[:20]}...", "#00F0FF")
                                self._execute_answer(game_mode, answer, choices, choice_elements, status_cb)
                            else:
                                status_cb("> RELAY TIMEOUT", "#FF3366")
                                
                except Exception as e:
                    pass
                time.sleep(0.35)
                
        except Exception as e:
            status_cb(f"> ERROR: {str(e)[:40]}", "#FF3366")
            print(f"[DEBUG] Full error: {e}")
        finally:
            self.cleanup()
            status_cb("> CORE TERMINATED", "#3C096C")

    def _get_groq_decision(self, question, choices):
        relay_url = "https://nexus-relay-zdj6.onrender.com/ask"
        payload = {"question": question, "choices": choices}
        try:
            response = requests.post(relay_url, json=payload, timeout=12)
            if response.status_code == 200:
                return response.json().get("answer")
        except Exception as e:
            print(f"[RELAY EXCEPTION] {e}")
        return None

    def _execute_answer(self, game_mode, calculated_answer, choices, elements, status_cb):
        human_delay = random.uniform(0.4, 1.3)
        time.sleep(human_delay)
        
        game_mode = game_mode.lower()
        executed = False
        
        if game_mode == "kahoot":
            for idx, choice_text in enumerate(choices):
                if calculated_answer.lower() in choice_text.lower() or choice_text.lower() in calculated_answer.lower():
                    key_map = ["1", "2", "3", "4"]
                    if idx < len(key_map):
                        target_key = key_map[idx]
                        self.keyboard_controller.press(target_key)
                        self.keyboard_controller.release(target_key)
                        status_cb(f"> KEY [{target_key}] FIRED", "#00FF41")
                        executed = True
                        break
        else:
            for el, choice_text in zip(elements, choices):
                if calculated_answer.lower() in choice_text.lower() or choice_text.lower() in calculated_answer.lower():
                    try:
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
                        time.sleep(0.3)
                        el.click()
                        status_cb(f"> CLICKED ANSWER", "#00FF41")
                        executed = True
                        break
                    except:
                        pass
        
        if not executed:
            status_cb("> STR_MATCH MISMATCH", "#FFCC00")

    def cleanup(self):
        self.stop_requested = True
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
        self.is_running = False


# COMPLETE DESKTOP GRAPHICAL UTILITY OVERLAY
class App:
    VIEW_LOADING  = "loading"
    VIEW_LAUNCHER = "launcher"
    VIEW_NEXUS    = "nexus"
    VIEW_KAHOOT   = "kahoot"

    def __init__(self, root: tk.Tk):
        self.root        = root
        self.nexus_eng   = NexusEngine()
        self.kahoot_eng  = KahootEngine()
        self.current_view = self.VIEW_LOADING
        self.drops        = []
        self._theme       = THEME_LAUNCHER

        saved            = load_settings()
        self.val_speed   = saved['speed']
        self.val_ent     = saved['errors']

        self.root.title("NEXUS  //  UNIVERSAL MODULE SUITE")
        self.root.geometry("550x820")
        self.root.configure(bg="#000000")
        self.root.resizable(False, False)
        
        # Windows-only absolute application surface optimization pinning
        if OS_NAME == "Windows":
            self.root.attributes("-topmost", True)

        self.canvas = tk.Canvas(self.root, bg="#000000", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self._init_drops(THEME_LAUNCHER)
        self._draw_rain()
        
        self._show_loading_screen()
        self._start_global_master_hotkeys()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self):
        self.kahoot_eng.cleanup()
        self.root.destroy()

    def _init_drops(self, theme):
        self._theme = theme
        self.drops  = [
            {"x": x, "y": random.randint(-800, 0),
             "v": random.randint(5, 12),
             "chars": [random.choice(theme["chars"]) for _ in range(12)]}
            for x in range(0, 550, 20)
        ]

    def _draw_rain(self):
        t = self._theme
        self.canvas.delete("rain")
        for d in self.drops:
            d["y"] += d["v"]
            if d["y"] > 850:
                d["y"] = -180
            for i, ch in enumerate(d["chars"]):
                yp = d["y"] - i * 15
                if 0 < yp < 820:
                    color = t["rain_h"] if i == 0 else t["rain"]
                    self.canvas.create_text(
                        d["x"], yp, text=ch, fill=color,
                        font=("Courier", 10), tags="rain"
                    )
        self.canvas.tag_lower("rain")
        self.root.after(30, self._draw_rain)

    def _clear_ui(self):
        self.canvas.delete("ui")
        for w in self.root.winfo_children():
            if isinstance(w, (tk.Entry,)):
                w.destroy()

    def _set_bg(self, color):
        self.canvas.configure(bg=color)
        self.root.configure(bg=color)

    def _btn(self, x, y, text, cmd, color, w=200, h=45):
        c = self.canvas
        x1, y1 = x - w//2, y - h//2
        x2, y2 = x + w//2, y + h//2
        rect = c.create_rectangle(x1, y1, x2, y2, outline=color, fill=self._theme["bg"], width=2, tags="ui")
        lbl  = c.create_text(x, y, text=text, font=("Courier New", 12, "bold"), fill=color, tags="ui")
        bg   = self._theme["bg"]
        def enter(_): c.itemconfig(rect, fill="#120024" if self.current_view == self.VIEW_KAHOOT else "#0D001A"); c.itemconfig(lbl, fill="#FFFFFF")
        def leave(_): c.itemconfig(rect, fill=bg); c.itemconfig(lbl, fill=color)
        def click(_): cmd()
        for it in (rect, lbl):
            c.tag_bind(it, "<Enter>",    enter)
            c.tag_bind(it, "<Leave>",    leave)
            c.tag_bind(it, "<Button-1>", click)

    def _back_btn(self):
        c = self.canvas
        rect = c.create_rectangle(15, 12, 95, 38, outline=self._theme["dim"], fill=self._theme["bg"], width=1, tags="ui")
        lbl  = c.create_text(55, 25, text="◀  BACK", font=("Courier New", 9, "bold"), fill=self._theme["dim"], tags="ui")
        def enter(_): c.itemconfig(rect, outline=self._theme["accent"]); c.itemconfig(lbl, fill=self._theme["accent"])
        def leave(_): c.itemconfig(rect, outline=self._theme["dim"]); c.itemconfig(lbl, fill=self._theme["dim"])
        def click(_): self._show_launcher()
        for it in (rect, lbl):
            c.tag_bind(it, "<Enter>",    enter)
            c.tag_bind(it, "<Leave>",    leave)
            c.tag_bind(it, "<Button-1>", click)

    def _status_update(self, tag_id, text, color):
        self.root.after(0, lambda: self.canvas.itemconfig(tag_id, text=text, fill=color))

    def _show_loading_screen(self):
        self.current_view = self.VIEW_LOADING
        self._clear_ui()
        self._set_bg("#000000")
        c = self.canvas

        c.create_text(275, 260, text="N E X U S", font=("Impact", 54), fill="#FFFFFF", tags="ui")
        c.create_text(275, 320, text="CORE COMPILATION SYSTEM", font=("Courier New", 11, "bold"), fill="#00F0FF", tags="ui")
        
        c.create_rectangle(100, 390, 450, 410, outline="#444444", width=2, fill="#050505", tags="ui")
        progress_bar = c.create_rectangle(104, 394, 104, 406, outline="", fill="#00FF41", tags="ui")
        percentage_lbl = c.create_text(275, 435, text="0%", font=("Courier New", 12, "bold"), fill="#FFFFFF", tags="ui")
        log_lbl = c.create_text(275, 470, text="Initializing environment...", font=("Courier New", 10), fill="#444444", tags="ui")

        loading_steps = [
            (0.15, 12, "Loading core binary nodes..."),
            (0.25, 28, "Mounting global dependency hooks..."),
            (0.40, 39, "Synchronizing dynamic hotkey system layers..."),
            (0.20, 51, "Parsing behavioral fatigue profiles..."),
            (0.35, 67, "Optimizing automated latency matrices..."),
            (0.50, 84, "Injecting system keyboard emulators..."),
            (0.30, 93, "Verifying pipeline configuration vectors..."),
            (0.25, 100, "BOOT COMPLETE. READY.")
        ]

        def step_sequence(index, current_pct):
            if index >= len(loading_steps):
                self.root.after(400, self._show_launcher)
                return

            delay, target_pct, message = loading_steps[index]
            c.itemconfig(log_lbl, text=message, fill="#00F0FF" if target_pct == 100 else "#888888")
            
            def animate_fraction(step_pct):
                if step_pct > target_pct:
                    self.root.after(int(delay * 1000), lambda: step_sequence(index + 1, target_pct))
                    return
                
                x_end = 104 + (342 * (step_pct / 100.0))
                c.coords(progress_bar, 104, 394, x_end, 406)
                c.itemconfig(percentage_lbl, text=f"{int(step_pct)}%")
                
                self.root.after(15, lambda: animate_fraction(step_pct + 1))

            animate_fraction(current_pct)

        self.root.after(500, lambda: step_sequence(0, 0))

    def _show_launcher(self):
        self.current_view = self.VIEW_LAUNCHER
        self._clear_ui()
        self._init_drops(THEME_LAUNCHER)
        self._set_bg(THEME_LAUNCHER["bg"])
        c = self.canvas

        c.create_text(275, 80,  text="N E X U S", font=("Impact", 46), fill=THEME_LAUNCHER["text"],   tags="ui")
        c.create_text(275, 128, text="MODULE SUITE",  font=("Courier New", 13, "bold"), fill=THEME_LAUNCHER["accent"], tags="ui")
        c.create_line(80, 152, 470, 152, fill=THEME_LAUNCHER["dim"], width=1, tags="ui")

        modules = [
            {"label": "N E X U S",  "sub": f"Behavioral Typing Engine  v{VERSION}", "color": THEME_LAUNCHER["accent"], "view": self.VIEW_NEXUS},
            {"label": "MULTI-GAME", "sub": "Kahoot • Blooket • Gimkit",          "color": "#9D4EDD",                  "view": self.VIEW_KAHOOT},
        ]
        for idx, mod in enumerate(modules):
            self._launcher_card(mod, y=260 + idx * 200)

    def _launcher_card(self, mod, y):
        c = self.canvas
        col   = mod["color"]
        x1, x2, h = 80, 470, 155
        cl = 14
        c.create_rectangle(x1, y, x2, y+h, outline=col, width=2, fill="#050505", tags="ui")
        for cx, cy, dx, dy in [(x1,y,1,1),(x2,y,-1,1),(x1,y+h,1,-1),(x2,y+h,-1,-1)]:
            c.create_line(cx, cy, cx+dx*cl, cy, fill=col, width=2, tags="ui")
            c.create_line(cx, cy, cx, cy+dy*cl, fill=col, width=2, tags="ui")
        lbl = c.create_text(275, y+48, text=mod["label"], font=("Impact", 34), fill=col, tags="ui")
        sub = c.create_text(275, y+82, text=mod["sub"], font=("Courier New", 10, "bold"), fill=THEME_LAUNCHER["dim"], tags="ui")
        by1, by2 = y+100, y+140
        btn = c.create_rectangle(175, by1, 375, by2, outline=col, fill="#000000", width=2, tags="ui")
        bl  = c.create_text(275, (by1+by2)//2, text="▶  OPEN", font=("Courier New", 12, "bold"), fill=col, tags="ui")

        def enter(_): c.itemconfig(btn, fill="#0a0a0a"); c.itemconfig(bl, fill="#FFFFFF")
        def leave(_): c.itemconfig(btn, fill="#000000"); c.itemconfig(bl, fill=col)
        def click(_):
            if mod["view"] == self.VIEW_NEXUS:
                self._show_nexus()
            else:
                self._show_kahoot()
        for it in (lbl, sub, btn, bl):
            c.tag_bind(it, "<Enter>",    enter)
            c.tag_bind(it, "<Leave>",    leave)
            c.tag_bind(it, "<Button-1>", click)

    def _show_nexus(self):
        self.current_view = self.VIEW_NEXUS
        self._clear_ui()
        self._init_drops(THEME_NEXUS)
        self._set_bg(THEME_NEXUS["bg"])
        T = THEME_NEXUS
        c = self.canvas

        self._back_btn()
        c.create_text(275, 80,  text="N E X U S",   font=("Impact", 46), fill=T["text"],   tags="ui")
        c.create_text(275, 130, text=f"v{VERSION}",         font=("Courier New", 13, "bold"), fill=T["accent"], tags="ui")
        self.nexus_status = c.create_text(275, 165, text="> READY", font=("Courier New", 13, "bold"), fill=T["accent"], tags="ui")
        c.create_line(80, 185, 470, 185, fill=T["dim"], width=1, tags="ui")

        # 5. CROSS-PLATFORM SYSTEM ACTION REMINDERS
        hk_hint = "CMD+SHIFT+V: Run | ESC: Kill" if OS_NAME == "Darwin" else "CTRL+ALT+V: Start | ESC: Kill | ALT+C: Hide"
        info = [
            "BEHAVIORAL ENGINE: LOADED",
            "FATIGUE MODEL:    ACTIVE",
            "COGNITIVE PAUSING: ENABLED",
            "────────────────────────────────",
            hk_hint
        ]
        for i, line in enumerate(info):
            c.create_text(275, 490 + i*34, text=line, font=("Courier New", 11, "bold"), fill=T["text"], tags="ui")

        self._create_slider(275, T)
        self._create_slider(375, T, is_errors=True)

        btn_txt = "▶  START  (CMD+SHIFT+V)" if OS_NAME == "Darwin" else "▶  START  (CTRL+ALT+V)"
        self._btn(275, 430, btn_txt, self._nexus_trigger, T["accent"], w=300, h=45)

    def _create_slider(self, y, T, is_errors=False):
        c     = self.canvas
        attr  = "val_ent" if is_errors else "val_speed"
        label = "ERRORS (%)" if is_errors else "SPEED (s/char)"
        v_min = 0   if is_errors else 0.01
        v_max = 15  if is_errors else 0.40
        t_s, t_e = 120, 430

        c.create_text(275, y-28, text=label, font=("Courier New", 11, "bold"), fill=T["accent"], tags="ui")
        c.create_line(t_s, y, t_e, y, fill="#333", width=6, tags="ui")
        hand  = c.create_rectangle(0,0,1,1, fill=T["text"], tags="ui")
        val_id = c.create_text(275, y+26, text="", font=("Courier New", 10, "bold"), fill=T["text"], tags="ui")

        def update(pos):
            v = v_min + (pos - t_s) / (t_e - t_s) * (v_max - v_min)
            v = max(v_min, min(v_max, v))
            setattr(self, attr, v)
            if is_errors:
                c.itemconfig(val_id, text=f"{int(v)}%")
            else:
                wpm = int(12 / v) if v > 0 else 999
                c.itemconfig(val_id, text=f"{v:.2f}s  ({wpm} WPM)")
            c.coords(hand, pos-6, y-14, pos+6, y+14)
            save_settings(self.val_speed, self.val_ent)

        def drag(e):
            if abs(e.y - y) < 60:
                update(max(t_s, min(t_e, e.x)))

        curr = getattr(self, attr)
        p    = t_s + (curr - v_min) / (v_max - v_min) * (t_e - t_s)
        update(p)
        c.bind("<B1-Motion>", drag, add="+")
        c.bind("<Button-1>",  drag, add="+")

    def _nexus_status_cb(self, text, color):
        if hasattr(self, 'nexus_status'):
            self._status_update(self.nexus_status, text, color)

    def _nexus_trigger(self):
        if not self.nexus_eng.is_typing:
            threading.Thread(
                target=self.nexus_eng.run,
                args=(pyperclip.paste(), self.val_speed, self.val_ent / 100, self._nexus_status_cb),
                daemon=True
            ).start()

    # 6. PLATFORM-DYNAMIC CORE HOTKEY STRUCTURING
    def _start_global_master_hotkeys(self):
        if hasattr(self, '_hk_listener'):
            try:
                self._hk_listener.stop()
            except:
                pass
        
        # Format keys based on Mac OS command parameters vs standard options
        if OS_NAME == "Darwin":
            hotkey_layout = {
                '<cmd>+<shift>+v': self._nexus_trigger,
                '<esc>':           self._native_kill_trigger,
                '<cmd>+<shift>+h': self._toggle_visibility,
            }
        else:
            hotkey_layout = {
                '<ctrl>+<alt>+v': self._nexus_trigger,
                '<esc>':          self._native_kill_trigger,
                '<alt>+c':        self._toggle_visibility,
            }

        try:
            hk = keyboard.GlobalHotKeys(hotkey_layout)
            self._hk_listener = hk
            threading.Thread(target=hk.run, daemon=True).start()
        except Exception as e:
            print(f"[NEXUS] Keyboard hook monitoring is unavailable on this system architecture profile: {e}")

    def _native_kill_trigger(self):
        setattr(self.nexus_eng, 'stop_requested', True)

    def _toggle_visibility(self):
        def action():
            if self.root.state() == "normal":
                self.root.withdraw()
            else:
                self.root.deiconify()
                if OS_NAME == "Windows":
                    self.root.attributes("-topmost", True)
        self.root.after(0, action)

    def _show_kahoot(self):
        self.current_view = self.VIEW_KAHOOT
        self._clear_ui()
        self._init_drops(THEME_KAHOOT)
        self._set_bg(THEME_KAHOOT["bg"])
        T = THEME_KAHOOT
        c = self.canvas

        self._back_btn()
        
        c.create_text(275, 65, text="MULTI-GAME VISION", font=("Impact", 42), fill=T["text"], tags="ui")
        c.create_text(275, 105, text="KAHOOT • BLOOKET • GIMKIT", font=("Courier New", 11, "bold"), fill=T["accent"], tags="ui")
        
        self.kahoot_status = c.create_text(275, 145, text="> READY", font=("Courier New", 13, "bold"), fill=T["accent"], tags="ui")
        c.create_line(80, 170, 470, 170, fill=T["dim"], width=1, tags="ui")

        # Game Mode Selector
        c.create_text(275, 200, text="GAME MODE", font=("Courier New", 11, "bold"), fill=T["text"], tags="ui")
        
        self.selected_game = "kahoot"
        modes = ["KAHOOT", "BLOOKET", "GIMKIT"]
        self.mode_buttons = {}
        x_positions = [130, 275, 420]
        
        for i, mode in enumerate(modes):
            btn = c.create_rectangle(x_positions[i]-55, 225, x_positions[i]+55, 265, 
                                   outline=T["accent"] if i==0 else T["dim"], 
                                   fill=T["dim"] if i==0 else "#000000", width=2, tags="ui")
            lbl = c.create_text(x_positions[i], 245, text=mode, 
                              font=("Courier New", 10, "bold"), 
                              fill=T["text"] if i==0 else T["dim"], tags="ui")
            self.mode_buttons[mode.lower()] = (btn, lbl)
            
            def make_select(m):
                def select(_):
                    self.selected_game = m.lower()
                    for gm, (b, l) in self.mode_buttons.items():
                        active = (gm == self.selected_game)
                        c.itemconfig(b, outline=T["accent"] if active else T["dim"],
                                   fill=T["dim"] if active else "#000000")
                        c.itemconfig(l, fill=T["text"] if active else T["dim"])
                return select
            
            c.tag_bind(btn, "<Button-1>", make_select(mode))
            c.tag_bind(lbl, "<Button-1>", make_select(mode))

        # Browser Selection
        c.create_text(275, 295, text="SELECT BROWSER ENGINE", font=("Courier New", 11, "bold"), fill=T["text"], tags="ui")
        
        self.selected_browser = "edge"
        btn_edge = c.create_rectangle(120, 320, 260, 360, outline=T["accent"], fill=T["dim"], width=2, tags="ui")
        lbl_edge = c.create_text(190, 340, text="EDGE", font=("Courier New", 11, "bold"), fill=T["text"], tags="ui")
        
        btn_chrome = c.create_rectangle(290, 320, 430, 360, outline=T["dim"], fill="#000000", width=2, tags="ui")
        lbl_chrome = c.create_text(360, 340, text="CHROME", font=("Courier New", 11, "bold"), fill=T["dim"], tags="ui")

        def select_edge(_):
            self.selected_browser = "edge"
            c.itemconfig(btn_edge, fill=T["dim"], outline=T["accent"])
            c.itemconfig(lbl_edge, fill=T["text"])
            c.itemconfig(btn_chrome, fill="#000000", outline=T["dim"])
            c.itemconfig(lbl_chrome, fill=T["dim"])

        def select_chrome(_):
            self.selected_browser = "chrome"
            c.itemconfig(btn_chrome, fill=T["dim"], outline=T["accent"])
            c.itemconfig(lbl_chrome, fill=T["text"])
            c.itemconfig(btn_edge, fill="#000000", outline=T["dim"])
            c.itemconfig(lbl_edge, fill=T["dim"])

        c.tag_bind(btn_edge, "<Button-1>", select_edge)
        c.tag_bind(lbl_edge, "<Button-1>", select_edge)
        c.tag_bind(btn_chrome, "<Button-1>", select_chrome)
        c.tag_bind(lbl_chrome, "<Button-1>", select_chrome)

        # URL / PIN
        c.create_text(275, 390, text="GAME PIN OR FULL URL", font=("Courier New", 11, "bold"), fill=T["text"], tags="ui")
        
        self.url_entry = tk.Entry(self.root, font=("Courier New", 12, "bold"), bg="#11052C", fg="#FFFFFF",
                                  insertbackground="#FFFFFF", justify="center", bd=1, relief="flat")
        self.canvas.create_window(275, 425, window=self.url_entry, width=320, height=35, tags="ui")
        self.url_entry.insert(0, "https://play.blooket.com/play?id=4413700")

        # 7. FIXED RESTORED RE-ROUTING MATRIX FOR RAW KAHOOT PINS
        def start_multi_auto():
            raw_input = self.url_entry.get().strip()
            if not raw_input:
                self._kahoot_status_cb("> PIN/URL EMPTY", "#FF3366")
                return
            
            if raw_input.isdigit() and self.selected_game == "kahoot":
                target_destination = f"https://kahoot.it/?pin={raw_input}"
            else:
                target_destination = raw_input if raw_input.startswith("http") else f"https://{raw_input}"
                
            self.kahoot_eng.start_automation(target_destination, self.selected_browser, self._kahoot_status_cb, self.selected_game)

        self._btn(275, 480, "▶  LAUNCH ENGINE", start_multi_auto, T["text"], w=300, h=45)
        self._btn(275, 545, "■  STOP ENGINE", lambda: setattr(self.kahoot_eng, 'stop_requested', True), "#FF3366", w=300, h=45)

        warn_box = c.create_rectangle(80, 590, 470, 650, outline="#FF3366", width=2, fill="#1A000A", tags="ui")
        c.create_text(275, 608, text="▲ IMPORTANT", font=("Courier New", 10, "bold"), fill="#FF3366", tags="ui")
        c.create_text(275, 630, text="Make sure the game is visible on screen!", font=("Courier New", 9, "bold"), fill=T["text"], tags="ui")

    def _kahoot_status_cb(self, text, color):
        if hasattr(self, 'kahoot_status'):
            self._status_update(self.kahoot_status, text, color)


if __name__ == "__main__":
    check_for_updates()
    
    root = tk.Tk()
    app = App(root)
    root.mainloop()
