import subprocess
import sys
import os
import time
import threading
import re
import random
import json
import tkinter as tk

# --- 1. UNIVERSAL BOOTSTRAP ---
def bootstrap():
    libs = ['Pillow', 'pyautogui', 'pyperclip', 'pynput', 'pystray', 'pygetwindow', 'requests']
    for lib in libs:
        try:
            __import__('PIL' if lib == 'Pillow' else lib.lower())
        except ImportError:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", lib, "--user", "--quiet"])
            except:
                pass

bootstrap()

import pyautogui
import pyperclip
import requests
from pynput import keyboard
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem as item

pyautogui.PAUSE = 0

if os.name == 'nt':
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass

try:
    import pygetwindow as gw
    HAS_FOCUS_LOGIC = True
except:
    HAS_FOCUS_LOGIC = False

# =============================================================================
# 2. VERSION & UPDATE CONFIG
# =============================================================================
VERSION = "6.0"
# This is your specific raw URL for auto-updating
REPO_URL = "https://raw.githubusercontent.com/petwhisperer201-glitch/Nexus-Suite/main/NEXUS.pyw"

# =============================================================================
# 3.  THEMES
# =============================================================================
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
    "bg":      "#050008",
    "rain":    "#1A0033",
    "rain_h":  "#CC44FF",
    "accent":  "#FF44CC",
    "text":    "#F0D0FF",
    "dim":     "#4A2060",
    "chars":   "KAHOOT01?!ABCDE",
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

# =============================================================================
# 4.  SETTINGS
# =============================================================================
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
                return {'speed': data.get('speed', 0.10), 'errors': data.get('errors', 2)}
        except:
            pass
    return {'speed': 0.10, 'errors': 2}

# =============================================================================
# 5.  NEXUS TYPING ENGINE
# =============================================================================
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

        target_window = None
        if HAS_FOCUS_LOGIC:
            try:
                target_window = gw.getActiveWindow()
            except:
                pass

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
                    if HAS_FOCUS_LOGIC and target_window:
                        try:
                            while gw.getActiveWindow() != target_window:
                                if self.stop_requested:
                                    break
                                status_cb("> PAUSED (LOST FOCUS)", "#FFCC00")
                                time.sleep(0.5)
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
                    if char in ".!?":
                        delay += random.uniform(0.3, 0.6)
                    elif char in ",;:":
                        delay += random.uniform(0.1, 0.3)
                    time.sleep(delay)
                pyautogui.write(' ')
                time.sleep(speed * random.uniform(0.5, 1.0))
        finally:
            self.is_typing, self.stop_requested = False, False
            self.lock.release()
            status_cb("> READY", THEME_NEXUS["accent"])

# =============================================================================
# 6.  KAHOOT ENGINE STUB
# =============================================================================
class KahootEngine:
    def __init__(self):
        self.is_running     = False
        self.stop_requested = False

    def connect(self, game_pin: str, nickname: str, status_cb):
        status_cb("> connect() NOT YET IMPLEMENTED", "#FFCC00")

    def answer(self, choice: int, status_cb):
        status_cb(f"> answer({choice}) NOT YET IMPLEMENTED", "#FFCC00")

    def run_auto(self, status_cb):
        self.is_running     = True
        self.stop_requested = False
        status_cb("> run_auto() NOT YET IMPLEMENTED", "#FFCC00")
        self.is_running = False

    def stop(self):
        self.stop_requested = True

# =============================================================================
# 7.  MAIN APPLICATION
# =============================================================================
class App:
    VIEW_LAUNCHER = "launcher"
    VIEW_NEXUS    = "nexus"
    VIEW_KAHOOT   = "kahoot"

    def __init__(self, root: tk.Tk):
        self.root        = root
        self.nexus_eng   = NexusEngine()
        self.kahoot_eng  = KahootEngine()
        self.current_view = self.VIEW_LAUNCHER
        self.drops        = []
        self._theme       = THEME_LAUNCHER

        saved            = load_settings()
        self.val_speed   = saved['speed']
        self.val_ent     = saved['errors']

        self.root.title("NEXUS  //  MODULE SUITE")
        self.root.geometry("550x820")
        self.root.configure(bg="#000000")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)

        self.canvas = tk.Canvas(self.root, bg="#000000", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self._init_drops(THEME_LAUNCHER)
        self._draw_rain()
        self._show_launcher()
        self._setup_tray()
        self.root.protocol("WM_DELETE_WINDOW", self._hide)

        # Trigger background update check on startup
        threading.Thread(target=self._run_update_check, daemon=True).start()

    def _run_update_check(self):
        try:
            r = requests.get(REPO_URL, timeout=5)
            if r.status_code == 200:
                remote_code = r.text
                match = re.search(r'VERSION\s*=\s*"([^"]+)"', remote_code)
                if match:
                    remote_ver = match.group(1)
                    if remote_ver != VERSION:
                        with open(__file__, "w", encoding="utf-8") as f:
                            f.write(remote_code)
                        os.execv(sys.executable, [sys.executable] + sys.argv)
        except:
            pass

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
        def enter(_): c.itemconfig(rect, fill="#0D001A"); c.itemconfig(lbl, fill="#FFFFFF")
        def leave(_): c.itemconfig(rect, fill=bg);       c.itemconfig(lbl, fill=color)
        def click(_): cmd()
        for it in (rect, lbl):
            c.tag_bind(it, "<Enter>",    enter)
            c.tag_bind(it, "<Leave>",    leave)
            c.tag_bind(it, "<Button-1>", click)

    def _back_btn(self):
        c = self.canvas
        rect = c.create_rectangle(15, 12, 95, 38, outline=self._theme["dim"],
                                   fill=self._theme["bg"], width=1, tags="ui")
        lbl  = c.create_text(55, 25, text="◀  BACK",
                              font=("Courier New", 9, "bold"),
                              fill=self._theme["dim"], tags="ui")
        def enter(_): c.itemconfig(rect, outline=self._theme["accent"]); c.itemconfig(lbl, fill=self._theme["accent"])
        def leave(_): c.itemconfig(rect, outline=self._theme["dim"]);    c.itemconfig(lbl, fill=self._theme["dim"])
        def click(_): self._show_launcher()
        for it in (rect, lbl):
            c.tag_bind(it, "<Enter>",    enter)
            c.tag_bind(it, "<Leave>",    leave)
            c.tag_bind(it, "<Button-1>", click)

    def _status_update(self, tag_id, text, color):
        self.root.after(0, lambda: self.canvas.itemconfig(tag_id, text=text, fill=color))

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
            {"label": "K A H O O T","sub": "Game-Bot Module  [IN DEV]",                "color": "#CC44FF",                 "view": self.VIEW_KAHOOT},
        ]
        for idx, mod in enumerate(modules):
            self._launcher_card(mod, y=260 + idx * 200)

        c.create_line(80, 740, 470, 740, fill=THEME_LAUNCHER["dim"], width=1, tags="ui")
        c.create_text(275, 770, text="SELECT A MODULE TO LAUNCH",
                      font=("Courier New", 10), fill=THEME_LAUNCHER["dim"], tags="ui")

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
        self.nexus_status = c.create_text(275, 165, text="> READY",
                                           font=("Courier New", 13, "bold"), fill=T["accent"], tags="ui")
        c.create_line(80, 185, 470, 185, fill=T["dim"], width=1, tags="ui")

        info = [
            "BEHAVIORAL ENGINE: LOADED",
            "FATIGUE MODEL:      ACTIVE",
            "COGNITIVE PAUSING: ENABLED",
            "────────────────────────────────",
            "CTRL+ALT+V: Start  |  ESC: Kill",
            "ALT+C:  Hide / Show UI",
        ]
        for i, line in enumerate(info):
            c.create_text(275, 490 + i*34, text=line,
                          font=("Courier New", 11, "bold"), fill=T["text"], tags="ui")

        self._create_slider(275, T)
        self._create_slider(375, T, is_errors=True)

        self._btn(275, 430, "▶  START  (CTRL+ALT+V)", self._nexus_trigger,
                  T["accent"], w=300, h=45)

        self._start_nexus_hotkeys()
        c.create_text(275, 750, text="AUTO-IGNITES IN 5s ON OPEN",
                      font=("Courier New", 9), fill=T["dim"], tags="ui")
        self.root.after(5000, self._nexus_trigger)

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
        if self.current_view != self.VIEW_NEXUS:
            return
        if not self.nexus_eng.is_typing:
            threading.Thread(
                target=self.nexus_eng.run,
                args=(pyperclip.paste(), self.val_speed, self.val_ent / 100, self._nexus_status_cb),
                daemon=True
            ).start()

    def _start_nexus_hotkeys(self):
        if hasattr(self, '_hk_listener'):
            try:
                self._hk_listener.stop()
            except:
                pass
        hk = keyboard.GlobalHotKeys({
            '<ctrl>+<alt>+v': self._nexus_trigger,
            '<alt>+c':        lambda: self.root.after(0, self._toggle_visibility),
            '<esc>':          lambda: setattr(self.nexus_eng, 'stop_requested', True),
        })
        self._hk_listener = hk
        threading.Thread(target=hk.run, daemon=True).start()

    def _show_kahoot(self):
        self.current_view = self.VIEW_KAHOOT
        self._clear_ui()
        self._init_drops(THEME_KAHOOT)
        self._set_bg(THEME_KAHOOT["bg"])
        T = THEME_KAHOOT
        c = self.canvas

        self._back_btn()
        c.create_text(275, 80,  text="K A H O O T", font=("Impact", 44), fill=T["text"],   tags="ui")
        c.create_text(275, 128, text="NEXUS MODULE",  font=("Courier New", 13, "bold"), fill=T["accent"], tags="ui")
        self.kahoot_status = c.create_text(275, 165, text="> READY",
                                            font=("Courier New", 13, "bold"), fill=T["rain_h"], tags="ui")
        c.create_line(80, 185, 470, 185, fill=T["dim"], width=1, tags="ui")

        c.create_text(275, 225, text="GAME PIN", font=("Courier New", 11, "bold"), fill=T["accent"], tags="ui")
        self.pin_var = tk.StringVar()
        pin_e = tk.Entry(
            self.root, textvariable=self.pin_var, width=16,
            bg="#0D001A", fg=T["rain_h"], insertbackground=T["rain_h"],
            font=("Courier New", 17, "bold"), relief="flat",
            highlightthickness=2, highlightcolor=T["rain_h"],
            highlightbackground=T["dim"], justify="center"
        )
        c.create_window(275, 258, window=pin_e, tags="ui")

        c.create_text(275, 298, text="NICKNAME", font=("Courier New", 11, "bold"), fill=T["accent"], tags="ui")
        self.nick_var = tk.StringVar(value="NexusBot")
        nick_e = tk.Entry(
            self.root, textvariable=self.nick_var, width=16,
            bg="#0D001A", fg=T["rain_h"], insertbackground=T["rain_h"],
            font=("Courier New", 17, "bold"), relief="flat",
            highlightthickness=2, highlightcolor=T["rain_h"],
            highlightbackground=T["dim"], justify="center"
        )
        c.create_window(275, 330, window=nick_e, tags="ui")
        c.create_line(80, 358, 470, 358, fill=T["dim"], width=1, tags="ui")

        self._btn(275, 415, "▶  CONNECT",   self._kahoot_connect,  T["accent"], w=220, h=48)
        self._btn(275, 490, "⚡  AUTO-PLAY", self._kahoot_autoplay, T["rain_h"], w=220, h=48)
        self._btn(275, 565, "■  STOP",      self._kahoot_stop,      "#FF4444",   w=220, h=48)

        c.create_line(80, 618, 470, 618, fill=T["dim"], width=1, tags="ui")
        stub_lines = [
            "MODULE STATUS: STUB — ADD YOUR LOGIC",
            "connect()  /  answer()  /  run_auto()",
            "──────────────────────────────────────",
            "Fill in KahootEngine methods to activate",
        ]
        for i, line in enumerate(stub_lines):
            c.create_text(275, 645 + i*32, text=line,
                          font=("Courier New", 10, "bold"), fill=T["dim"], tags="ui")

    def _kahoot_status_cb(self, text, color):
        if hasattr(self, 'kahoot_status'):
            self._status_update(self.kahoot_status, text, color)

    def _kahoot_connect(self):
        pin  = self.pin_var.get().strip()
        nick = self.nick_var.get().strip() or "NexusBot"
        if not pin:
            self._kahoot_status_cb("> ENTER A GAME PIN FIRST", "#FFCC00")
            return
        threading.Thread(
            target=self.kahoot_eng.connect,
            args=(pin, nick, self._kahoot_status_cb),
            daemon=True
        ).start()

    def _kahoot_autoplay(self):
        if self.kahoot_eng.is_running:
            self._kahoot_status_cb("> ALREADY RUNNING", "#FFCC00")
            return
        threading.Thread(
            target=self.kahoot_eng.run_auto,
            args=(self._kahoot_status_cb,),
            daemon=True
        ).start()

    def _kahoot_stop(self):
        self.kahoot_eng.stop()
        self._kahoot_status_cb("> STOPPED", "#FF4444")

    def _setup_tray(self):
        img = Image.new("RGB", (64, 64), "#000000")
        d   = ImageDraw.Draw(img)
        d.ellipse([10, 10, 54, 54], outline="#00F0FF", width=3)
        d.text((18, 12), "N", fill="#00F0FF", font_size=38)
        self.tray = pystray.Icon(
            "NEXUS", img, "NEXUS Module Suite",
            (
                item("Show",  self._show),
                item("Exit",  lambda: os._exit(0)),
            )
        )
        threading.Thread(target=self.tray.run, daemon=True).start()

    def _hide(self):            self.root.withdraw()
    def _show(self):            self.root.deiconify(); self.root.attributes("-topmost", True)
    def _toggle_visibility(self):
        if self.root.winfo_viewable():
            self._hide()
        else:
            self._show()

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
