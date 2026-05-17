# =================================================================
# NEXUS MODULE SUITE - Combined Core Framework v6.9
# Provided "AS IS" for educational and productivity purposes.
# The owners (petwhisperer201-glitch, The-Samri) and their team
# are not responsible for misuse, academic penalties, or
# third-party platform bans.
# By running this software, the user assumes all responsibility.
# =================================================================

VERSION = "6.9"
PASTEBIN_RAW_URL = "https://pastebin.com/raw/nCLxGg4s"
REPO_URL = "https://raw.githubusercontent.com/petwhisperer201-glitch/Nexus-Suite/main/NEXUS.pyw"

import tkinter as tk
import subprocess
import sys
import os
import time
import threading
import re
import random
import json

# ── Framework Ecosystem Hooks ─────────────────────────────────────
pyautogui  = None
pyperclip  = None
keyboard   = None
Image      = None
ImageDraw  = None
pystray    = None
item       = None
gw         = None
requests   = None
Groq       = None
websocket  = None

HAS_GROQ        = False
HAS_FOCUS_LOGIC = False

# ── Themes ────────────────────────────────────────────────────────
THEME_LAUNCHER = {
    "bg":    "#000000", "rain": "#002200", "rain_h": "#00FF41",
    "accent":"#00F0FF", "text": "#FFFFFF", "dim":    "#444444",
    "chars": "01NEXUS",
}
THEME_NEXUS = {
    "bg":    "#000000", "rain": "#002200", "rain_h": "#00FF41",
    "accent":"#00F0FF", "text": "#FFFFFF", "dim":    "#444444",
    "chars": "01NEXUS",
}
THEME_KAHOOT = {
    "bg":    "#050008", "rain": "#1A0033", "rain_h": "#CC44FF",
    "accent":"#FF44CC", "text": "#F0D0FF", "dim":    "#4A2060",
    "chars": "KAHOOT01?!ABCDE",
}

# ── Settings ──────────────────────────────────────────────────────
SETTINGS_FILE = os.path.join(os.path.expanduser("~"), ".nexus_config.json")

def save_settings(speed, errors, api_key=""):
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump({'speed': float(speed), 'errors': int(errors), 'api_key': api_key}, f)
    except:
        pass

def load_settings():
    settings = {'speed': 0.10, 'errors': 2, 'api_key': ""}
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                data = json.load(f)
                settings['speed']   = data.get('speed',   0.10)
                settings['errors']  = data.get('errors',  2)
                settings['api_key'] = data.get('api_key', "")
        except:
            pass
    # Try to pull API key from Pastebin
    if requests and PASTEBIN_RAW_URL:
        try:
            response = requests.get(PASTEBIN_RAW_URL, timeout=4)
            if response.status_code == 200:
                fetched_key = response.text.strip()
                if fetched_key:
                    settings['api_key'] = fetched_key
        except:
            pass
    return settings


# ── Typing Engine ─────────────────────────────────────────────────
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
            '6':'5t7y','7':'6y8u','8':'7u9i','9':'8i0o','0':'9oip','-':'0p','=':'-',' ':'cvbnm',
        }

    def run(self, raw, speed, ent, status_cb):
        if not pyautogui or not self.lock.acquire(blocking=False):
            return
        self.is_typing, self.stop_requested, self.char_count = True, False, 0
        target_window = None
        if HAS_FOCUS_LOGIC and gw:
            try: target_window = gw.getActiveWindow()
            except: pass

        status_cb("> ACTIVE", THEME_NEXUS["rain_h"])
        try:
            text  = re.sub(r'[^\x20-\x7E\n\r]', '', raw.replace('\xa0', ' '))
            words = text.split(' ')
            for word_idx, word in enumerate(words):
                if self.stop_requested: break
                if word_idx > 0 and word_idx % random.randint(15, 40) == 0:
                    status_cb("> THINKING...", "#AA00FF")
                    time.sleep(random.uniform(1.2, 3.0))
                wc = 0.8 if len(word) < 4 else 1.2
                for char in word:
                    if self.stop_requested: break
                    if HAS_FOCUS_LOGIC and target_window and gw:
                        try:
                            while gw.getActiveWindow() != target_window:
                                if self.stop_requested: break
                                status_cb("> PAUSED (LOST FOCUS)", "#FFCC00")
                                time.sleep(0.5)
                        except: pass
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
                    if char in ".!?":  delay += random.uniform(0.3, 0.6)
                    elif char in ",;:": delay += random.uniform(0.1, 0.3)
                    time.sleep(delay)
                pyautogui.write(' ')
                time.sleep(speed * random.uniform(0.5, 1.0))
        finally:
            self.is_typing, self.stop_requested = False, False
            self.lock.release()
            status_cb("> READY", THEME_NEXUS["accent"])


# ── Kahoot CDP Engine ─────────────────────────────────────────────
class KahootEngine:
    def __init__(self):
        self.is_running = False
        self.ai_client  = None

    def _launch_browser_with_debugging(self):
        paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        ]
        for path in paths:
            if os.path.exists(path):
                subprocess.Popen([path, "--remote-debugging-port=9222", "https://kahoot.it"])
                return True
        return False

    def start_engine(self, api_key, status_cb):
        if not HAS_GROQ or not Groq or not websocket or not requests:
            status_cb("> LIBS DEPENDENCY ERROR", "#FF0000")
            return False
        if self.is_running: return True
        try:
            if not api_key:
                status_cb("> API KEY MISSING", "#FFCC00")
                return False
            self.ai_client = Groq(api_key=api_key)
        except Exception:
            status_cb("> API AUTH ERROR", "#FF0000")
            return False
        self.is_running = True
        status_cb("> CONNECTING TO BROWSER...", "#CC44FF")
        threading.Thread(target=self._direct_hook_loop, args=(status_cb,), daemon=True).start()
        return True

    def stop_engine(self, status_cb):
        self.is_running = False
        status_cb("> PIPELINE DISCONNECTED", "#FF44CC")

    def _direct_hook_loop(self, status_cb):
        ws_conn            = None
        last_question_text = None
        while self.is_running:
            if not ws_conn:
                try:
                    resp = requests.get("http://127.0.0.1:9222/json", timeout=2)
                    tabs = resp.json()
                    target_tab = next(
                        (t for t in tabs if "kahoot.it" in t.get("url", "") or "kahoot" in t.get("title", "").lower()),
                        None
                    )
                    if target_tab and "webSocketDebuggerUrl" in target_tab:
                        ws_conn = websocket.create_connection(target_tab["webSocketDebuggerUrl"])
                        status_cb("> DIRECT HOOK: CONNECTED", "#00FF41")
                    else:
                        status_cb("> LOOKING FOR KAHOOT TAB...", "#FFCC00")
                        self._launch_browser_with_debugging()
                        time.sleep(3)
                        continue
                except Exception:
                    status_cb("> LAUNCHING SYSTEM BROWSER...", "#FFCC00")
                    self._launch_browser_with_debugging()
                    time.sleep(4)
                    continue

            try:
                js_scraper = """
                (function() {
                    const qEl = document.querySelector('[data-functional-selector="question-block"]') || document.querySelector('h1');
                    if (!qEl) return null;
                    const choices = Array.from(document.querySelectorAll('[data-functional-selector^="answer-"]'))
                                         .map(el => el.innerText || el.textContent)
                                         .filter(Boolean);
                    return JSON.stringify({ question: qEl.innerText || qEl.textContent, choices: choices });
                })()
                """
                payload = {"id": 1, "method": "Runtime.evaluate",
                           "params": {"expression": js_scraper, "returnByValue": True}}
                ws_conn.send(json.dumps(payload))
                result_raw = json.loads(ws_conn.recv())
                eval_res   = result_raw.get("result", {}).get("result", {}).get("value")

                if eval_res:
                    data    = json.loads(eval_res)
                    q_text  = data.get("question", "").strip()
                    choices = data.get("choices", [])
                    if q_text and q_text != last_question_text:
                        last_question_text = q_text
                        status_cb("> ANALYZING QUESTION...", "#AA00FF")
                        best_option = self._query_analysis(q_text, choices)
                        # Point Decay Engine — throttle to rarely hit 1000 pts
                        time.sleep(random.uniform(1.8, 4.5))
                        if best_option:
                            # 15% engineered human-misslip rate
                            if random.random() < 0.15 and len(choices) > 1:
                                wrong = [c for c in choices if c.strip().lower() != best_option.strip().lower()]
                                if wrong:
                                    status_cb(f"> ANSWER (MISSLIP): {random.choice(wrong).upper()}", "#FFCC00")
                                    continue
                            status_cb(f"> ANSWER: {best_option.upper()}", "#00FF41")
                        else:
                            status_cb("> ANALYSIS FAILED", "#FF0000")
                else:
                    if last_question_text is not None:
                        status_cb("> AWAITING NEXT QUESTION", "#CC44FF")
                        last_question_text = None
            except Exception:
                ws_conn = None
                time.sleep(1)
            time.sleep(0.8)

    def _query_analysis(self, question, choices):
        if not question or not choices or not self.ai_client: return None
        prompt = (
            f"Analyze the following quiz question and choose the correct answer from the provided list.\n"
            f"Question: {question}\n"
            f"Options: {', '.join(choices)}\n"
            f"Output strictly as JSON: {{\"correct_choice\": \"exact_text_string\"}}"
        )
        try:
            response = self.ai_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
            )
            return json.loads(response.choices[0].message.content).get("correct_choice")
        except Exception:
            return None


# ── Main Application ──────────────────────────────────────────────
class App:
    VIEW_LOADING  = "loading"
    VIEW_LAUNCHER = "launcher"
    VIEW_NEXUS    = "nexus"
    VIEW_KAHOOT   = "kahoot"
    VIEW_SETUP    = "setup"

    def __init__(self, root: tk.Tk):
        self.root         = root
        self.nexus_eng    = NexusEngine()
        self.kahoot_eng   = KahootEngine()
        self.current_view = self.VIEW_LOADING
        self.drops        = []
        self._theme       = THEME_LAUNCHER
        self.key_entry    = None

        self.val_speed = 0.10
        self.val_ent   = 2
        self.api_key   = ""

        self.root.title("NEXUS // CORE SUITE MODULE")
        self.root.geometry("550x820")
        self.root.configure(bg="#000000")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)
        self.root.protocol("WM_DELETE_WINDOW", self._hide)

        self.canvas = tk.Canvas(self.root, bg="#000000", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self._init_drops(THEME_LAUNCHER)
        self._draw_rain()
        self._show_loading_screen()

    # ── Loading & Bootstrap ───────────────────────────────────────
    def _show_loading_screen(self):
        c = self.canvas
        c.create_text(275, 260, text="N E X U S",    font=("Impact", 52),         fill=THEME_LAUNCHER["text"],   tags="ui")
        c.create_text(275, 315, text="MODULE SUITE", font=("Courier New", 14, "bold"), fill=THEME_LAUNCHER["accent"], tags="ui")
        self.loading_status = c.create_text(
            275, 430, text="> VERIFYING ECOSYSTEM...",
            font=("Courier New", 11, "bold"), fill=THEME_LAUNCHER["accent"], tags="ui"
        )
        threading.Thread(target=self._bootstrap_dependencies, daemon=True).start()

    def _bootstrap_dependencies(self):
        global pyautogui, pyperclip, keyboard, Image, ImageDraw, pystray, item, \
               gw, requests, Groq, websocket, HAS_GROQ, HAS_FOCUS_LOGIC

        libs = ['Pillow', 'pyautogui', 'pyperclip', 'pynput', 'pystray',
                'pygetwindow', 'requests', 'groq', 'websocket-client']
        for lib in libs:
            self._status_update(self.loading_status, f"> SCANNING MODULE: {lib.upper()}", THEME_LAUNCHER["accent"])
            try:
                __import__('PIL' if lib == 'Pillow' else ('websocket' if lib == 'websocket-client' else lib.lower()))
            except ImportError:
                self._status_update(self.loading_status, f"> INSTALLING: {lib.upper()}...", "#FFCC00")
                try: subprocess.check_call([sys.executable, "-m", "pip", "install", lib, "--user", "--quiet"])
                except: pass

        try: import pyautogui as pg;              pyautogui = pg;  pyautogui.FAILSAFE = True; pyautogui.PAUSE = 0
        except: pass
        try: import pyperclip as pc;              pyperclip = pc
        except: pass
        try: from pynput import keyboard as kb;   keyboard  = kb
        except: pass
        try:
            from PIL import Image as im, ImageDraw as imd
            Image = im; ImageDraw = imd
        except: pass
        try:
            import pystray as ps; from pystray import MenuItem as mi
            pystray = ps; item = mi
        except: pass
        try:
            import pygetwindow as gw_mod
            gw = gw_mod; HAS_FOCUS_LOGIC = True
        except: pass
        try: import requests as req;              requests  = req
        except: pass
        try: import websocket as ws;              websocket = ws
        except: pass
        try:
            from groq import Groq as groq_cls
            Groq = groq_cls; HAS_GROQ = True
        except: pass

        # Windows DPI fix
        if os.name == 'nt':
            try:
                import ctypes; ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except: pass

        saved          = load_settings()
        self.val_speed = saved['speed']
        self.val_ent   = saved['errors']
        self.api_key   = saved['api_key']

        self.root.after(0, self._setup_tray)
        threading.Thread(target=self._run_update_check, daemon=True).start()

        if not self.api_key:
            self.root.after(0, self._show_setup)
        else:
            self.root.after(0, self._show_launcher)

    # ── Auto-Updater ──────────────────────────────────────────────
    def _run_update_check(self):
        if not requests: return
        try:
            r = requests.get(REPO_URL, timeout=5)
            if r.status_code == 200:
                match = re.search(r'VERSION\s*=\s*"([^"]+)"', r.text)
                if match and match.group(1) != VERSION:
                    with open(__file__, "w", encoding="utf-8") as f:
                        f.write(r.text)
                    os.execv(sys.executable, [sys.executable] + sys.argv)
        except: pass

    # ── System Tray ───────────────────────────────────────────────
    def _setup_tray(self):
        if not all([Image, ImageDraw, pystray, item]): return
        try:
            img = Image.new("RGB", (64, 64), "#000000")
            d   = ImageDraw.Draw(img)
            d.ellipse([10, 10, 54, 54], outline="#00F0FF", width=3)
            d.text((18, 12), "N", fill="#00F0FF", font_size=38)
            self.tray = pystray.Icon(
                "NEXUS", img, "NEXUS Module Suite",
                (item("Show", self._show), item("Exit", lambda: os._exit(0)))
            )
            threading.Thread(target=self.tray.run, daemon=True).start()
        except: pass

    # ── Matrix Rain ───────────────────────────────────────────────
    def _init_drops(self, theme):
        self._theme = theme
        self.drops  = [
            {"x": x, "y": random.randint(-800, 0), "v": random.randint(5, 12),
             "chars": [random.choice(theme["chars"]) for _ in range(12)]}
            for x in range(0, 550, 20)
        ]

    def _draw_rain(self):
        t = self._theme
        self.canvas.delete("rain")
        for d in self.drops:
            d["y"] += d["v"]
            if d["y"] > 850: d["y"] = -180
            for i, ch in enumerate(d["chars"]):
                yp = d["y"] - i * 15
                if 0 < yp < 820:
                    color = t["rain_h"] if i == 0 else t["rain"]
                    self.canvas.create_text(d["x"], yp, text=ch, fill=color, font=("Courier", 10), tags="rain")
        self.canvas.tag_lower("rain")
        self.root.after(30, self._draw_rain)

    # ── UI Helpers ────────────────────────────────────────────────
    def _clear_ui(self):
        self.canvas.delete("ui")
        if self.key_entry:
            self.key_entry.destroy()
            self.key_entry = None
        for w in self.root.winfo_children():
            if isinstance(w, tk.Entry):
                w.destroy()

    def _set_bg(self, color):
        self.canvas.configure(bg=color)
        self.root.configure(bg=color)

    def _status_update(self, tag_id, text, color):
        self.root.after(0, lambda: self.canvas.itemconfig(tag_id, text=text, fill=color))

    def _btn(self, x, y, text, cmd, color, w=200, h=45, custom_tag="ui"):
        c = self.canvas
        x1, y1, x2, y2 = x - w//2, y - h//2, x + w//2, y + h//2
        rect = c.create_rectangle(x1, y1, x2, y2, outline=color, fill=self._theme["bg"], width=2, tags=custom_tag)
        lbl  = c.create_text(x, y, text=text, font=("Courier New", 12, "bold"), fill=color, tags=custom_tag)
        bg   = self._theme["bg"]
        def enter(_): c.itemconfig(rect, fill="#1A0033"); c.itemconfig(lbl, fill="#FFFFFF")
        def leave(_): c.itemconfig(rect, fill=bg);       c.itemconfig(lbl, fill=color)
        def click(_): cmd()
        for it in (rect, lbl):
            c.tag_bind(it, "<Enter>",    enter)
            c.tag_bind(it, "<Leave>",    leave)
            c.tag_bind(it, "<Button-1>", click)

    def _back_btn(self):
        c    = self.canvas
        rect = c.create_rectangle(15, 12, 95, 38, outline=self._theme["dim"], fill=self._theme["bg"], width=1, tags="ui")
        lbl  = c.create_text(55, 25, text="◀ BACK", font=("Courier New", 9, "bold"), fill=self._theme["dim"], tags="ui")
        def enter(_): c.itemconfig(rect, outline=self._theme["accent"]); c.itemconfig(lbl, fill=self._theme["accent"])
        def leave(_): c.itemconfig(rect, outline=self._theme["dim"]);    c.itemconfig(lbl, fill=self._theme["dim"])
        def click(_):
            if self.current_view == self.VIEW_KAHOOT: self.kahoot_eng.stop_engine(self._kahoot_status_cb)
            self._show_launcher()
        for it in (rect, lbl):
            c.tag_bind(it, "<Enter>", enter); c.tag_bind(it, "<Leave>", leave); c.tag_bind(it, "<Button-1>", click)

    # ── Setup View ────────────────────────────────────────────────
    def _show_setup(self):
        self.current_view = self.VIEW_SETUP
        self._clear_ui(); self._init_drops(THEME_LAUNCHER); self._set_bg(THEME_LAUNCHER["bg"])
        c = self.canvas
        c.create_text(275, 140, text="INITIAL SETUP", font=("Impact", 46), fill=THEME_LAUNCHER["text"],   tags="ui")
        c.create_text(275, 280, text="GROQ API KEY",  font=("Courier New", 11, "bold"), fill=THEME_LAUNCHER["accent"], tags="ui")
        self.key_entry = tk.Entry(
            self.root, font=("Courier New", 12), bg="#050505",
            fg="#00F0FF", insertbackground="#FFFFFF", justify="center"
        )
        self.key_entry.place(x=75, y=340, width=400, height=35)
        def save_and_continue():
            key = self.key_entry.get().strip()
            if key:
                self.api_key = key
                save_settings(self.val_speed, self.val_ent, self.api_key)
                self._show_launcher()
        self._btn(275, 430, "▶ SAVE & CONTINUE", save_and_continue, THEME_LAUNCHER["accent"], w=250, h=45)

    # ── Launcher View ─────────────────────────────────────────────
    def _show_launcher(self):
        self.current_view = self.VIEW_LAUNCHER
        self._clear_ui(); self._init_drops(THEME_LAUNCHER); self._set_bg(THEME_LAUNCHER["bg"])
        c = self.canvas
        c.create_text(275, 80,  text="N E X U S",      font=("Impact", 46),           fill=THEME_LAUNCHER["text"],   tags="ui")
        c.create_text(275, 128, text="MODULE LAUNCHER", font=("Courier New", 13, "bold"), fill=THEME_LAUNCHER["accent"], tags="ui")
        c.create_line(80, 152, 470, 152, fill=THEME_LAUNCHER["dim"], width=1, tags="ui")
        modules = [
            {"label": "N E X U S",   "sub": f"Behavioral Typing Engine  v{VERSION}", "color": THEME_LAUNCHER["accent"], "view": self.VIEW_NEXUS},
            {"label": "K A H O O T", "sub": "Automated DevTools CDP Hook",           "color": "#CC44FF",                 "view": self.VIEW_KAHOOT},
        ]
        for idx, mod in enumerate(modules): self._launcher_card(mod, y=240 + idx * 210)
        c.create_line(80, 740, 470, 740, fill=THEME_LAUNCHER["dim"], width=1, tags="ui")
        c.create_text(275, 770, text="SELECT A MODULE TO LAUNCH", font=("Courier New", 10), fill=THEME_LAUNCHER["dim"], tags="ui")

    def _launcher_card(self, mod, y):
        c = self.canvas; col = mod["color"]; x1, x2, h, cl = 80, 470, 160, 14
        c.create_rectangle(x1, y, x2, y+h, outline=col, width=2, fill="#050505", tags="ui")
        # Corner accent lines (from v6.2)
        for cx, cy, dx, dy in [(x1,y,1,1),(x2,y,-1,1),(x1,y+h,1,-1),(x2,y+h,-1,-1)]:
            c.create_line(cx, cy, cx+dx*cl, cy, fill=col, width=2, tags="ui")
            c.create_line(cx, cy, cx, cy+dy*cl, fill=col, width=2, tags="ui")
        lbl = c.create_text(275, y+45,  text=mod["label"], font=("Impact", 34),           fill=col,                      tags="ui")
        sub = c.create_text(275, y+82,  text=mod["sub"],   font=("Courier New", 10, "bold"), fill=THEME_LAUNCHER["dim"],    tags="ui")
        btn = c.create_rectangle(175, y+105, 375, y+145, outline=col, fill="#000000", width=2, tags="ui")
        bl  = c.create_text(275, y+125, text="▶ LAUNCH",  font=("Courier New", 12, "bold"), fill=col,                      tags="ui")
        def enter(_): c.itemconfig(btn, fill="#1A0033"); c.itemconfig(bl, fill="#FFFFFF")
        def leave(_): c.itemconfig(btn, fill="#000000"); c.itemconfig(bl, fill=col)
        def click(_): self._show_nexus() if mod["view"] == self.VIEW_NEXUS else self._show_kahoot()
        for it in (lbl, sub, btn, bl):
            c.tag_bind(it, "<Enter>", enter); c.tag_bind(it, "<Leave>", leave); c.tag_bind(it, "<Button-1>", click)

    # ── Nexus View ────────────────────────────────────────────────
    def _show_nexus(self):
        self.current_view = self.VIEW_NEXUS
        self._clear_ui(); self._init_drops(THEME_NEXUS); self._set_bg(THEME_NEXUS["bg"])
        T = THEME_NEXUS; c = self.canvas
        self._back_btn()
        c.create_text(275, 80,  text="N E X U S", font=("Impact", 46),           fill=T["text"],   tags="ui")
        c.create_text(275, 130, text=f"v{VERSION}", font=("Courier New", 13, "bold"), fill=T["accent"], tags="ui")
        self.nexus_status = c.create_text(
            275, 165, text="> READY", font=("Courier New", 13, "bold"), fill=T["accent"], tags="ui"
        )
        c.create_line(80, 185, 470, 185, fill=T["dim"], width=1, tags="ui")

        info = [
            "BEHAVIORAL ENGINE:  LOADED",
            "FATIGUE MODEL:       ACTIVE",
            "COGNITIVE PAUSING:  ENABLED",
            "────────────────────────────────",
            "CTRL+ALT+V: Start  |  ESC: Kill",
            "ALT+C: Hide / Show UI",
        ]
        for i, line in enumerate(info):
            c.create_text(275, 490 + i*34, text=line, font=("Courier New", 11, "bold"), fill=T["text"], tags="ui")

        self._create_slider(275, T)
        self._create_slider(375, T, is_errors=True)
        self._btn(275, 430, "▶ START (CTRL+ALT+V)", self._nexus_trigger, T["accent"], w=300, h=45)
        self._start_nexus_hotkeys()

        c.create_text(275, 750, text="AUTO-IGNITES IN 5s ON OPEN", font=("Courier New", 9), fill=T["dim"], tags="ui")
        self.root.after(5000, self._nexus_trigger)

    def _create_slider(self, y, T, is_errors=False):
        c     = self.canvas
        attr  = "val_ent"   if is_errors else "val_speed"
        label = "ERRORS (%)" if is_errors else "SPEED (s/char)"
        v_min, v_max = (0, 15) if is_errors else (0.01, 0.40)
        t_s, t_e     = 120, 430
        c.create_text(275, y-28, text=label, font=("Courier New", 11, "bold"), fill=T["accent"], tags="ui")
        c.create_line(t_s, y, t_e, y, fill="#333", width=6, tags="ui")
        hand   = c.create_rectangle(0, 0, 1, 1, fill=T["text"], tags="ui")
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
            save_settings(self.val_speed, self.val_ent, self.api_key)
        def drag(e):
            if abs(e.y - y) < 60: update(max(t_s, min(t_e, e.x)))
        curr = getattr(self, attr)
        update(t_s + (curr - v_min) / (v_max - v_min) * (t_e - t_s))
        c.bind("<B1-Motion>", drag, add="+")
        c.bind("<Button-1>",  drag, add="+")

    def _nexus_status_cb(self, text, color):
        if hasattr(self, 'nexus_status'): self._status_update(self.nexus_status, text, color)

    def _nexus_trigger(self):
        if self.current_view != self.VIEW_NEXUS: return
        if not self.nexus_eng.is_typing and pyperclip:
            threading.Thread(
                target=self.nexus_eng.run,
                args=(pyperclip.paste(), self.val_speed, self.val_ent / 100, self._nexus_status_cb),
                daemon=True
            ).start()

    def _start_nexus_hotkeys(self):
        if not keyboard: return
        if hasattr(self, '_hk_listener'):
            try: self._hk_listener.stop()
            except: pass
        hk = keyboard.GlobalHotKeys({
            '<ctrl>+<alt>+v': self._nexus_trigger,
            '<alt>+c':        lambda: self.root.after(0, self._toggle_visibility),
            '<esc>':          lambda: setattr(self.nexus_eng, 'stop_requested', True),
        })
        self._hk_listener = hk
        threading.Thread(target=hk.run, daemon=True).start()

    # ── Kahoot View ───────────────────────────────────────────────
    def _show_kahoot(self):
        self.current_view = self.VIEW_KAHOOT
        self._clear_ui(); self._init_drops(THEME_KAHOOT); self._set_bg(THEME_KAHOOT["bg"])
        T = THEME_KAHOOT; c = self.canvas
        self._back_btn()
        c.create_text(275, 80,  text="K A H O O T",          font=("Impact", 44),           fill=T["text"],   tags="ui")
        c.create_text(275, 128, text="DIRECT CDP PIPELINE MODULE", font=("Courier New", 11, "bold"), fill=T["accent"], tags="ui")
        self.kahoot_status = c.create_text(
            275, 185, text="> PIPELINE READY", font=("Courier New", 13, "bold"), fill=T["accent"], tags="ui"
        )
        self._render_kahoot_toggle_btn()
        c.create_line(80, 460, 470, 460, fill=T["dim"], width=1, tags="ui")
        instructions = [
            "OPERATING GUIDELINES:",
            "1. Click 'ACTIVATE AI PIPELINE' to hook browser.",
            "2. Play the game inside the new debugging browser tab.",
            "3. Answer throttling is ACTIVE (Delays answers 1.8s - 4.5s).",
            "4. Human Mimicry Module is ACTIVE (15% mistake profile applied).",
        ]
        for i, line in enumerate(instructions):
            align, xp, fw, fc = ("center", 275, "bold", T["accent"]) if i == 0 else ("w", 55, "normal", T["text"])
            c.create_text(xp, 490 + i*32, text=line, anchor=align, font=("Courier New", 9, fw), fill=fc, tags="ui")

    def _render_kahoot_toggle_btn(self):
        self.canvas.delete("k_btn")
        if not self.kahoot_eng.is_running:
            self._btn(275, 360, "▶ ACTIVATE AI PIPELINE", self._toggle_kahoot_state, THEME_KAHOOT["accent"], w=320, h=50, custom_tag="k_btn")
        else:
            self._btn(275, 360, "■ DEACTIVATE PIPELINE",  self._toggle_kahoot_state, "#FF0055",              w=320, h=50, custom_tag="k_btn")

    def _toggle_kahoot_state(self):
        if not self.kahoot_eng.is_running:
            self.kahoot_eng.start_engine(self.api_key, self._kahoot_status_cb)
        else:
            self.kahoot_eng.stop_engine(self._kahoot_status_cb)
        self._render_kahoot_toggle_btn()

    def _kahoot_status_cb(self, text, color):
        if hasattr(self, 'kahoot_status'):
            self._status_update(self.kahoot_status, text, color)
            if any(kw in text for kw in ("HOOK", "DISCONNECTED", "READY")):
                self.root.after(0, self._render_kahoot_toggle_btn)

    # ── Window Management ─────────────────────────────────────────
    def _hide(self):             self.root.withdraw()
    def _show(self):             self.root.deiconify(); self.root.attributes("-topmost", True)
    def _toggle_visibility(self):
        if self.root.winfo_viewable(): self._hide()
        else:                          self._show()


if __name__ == "__main__":
    root = tk.Tk()
    app  = App(root)
    root.mainloop()
