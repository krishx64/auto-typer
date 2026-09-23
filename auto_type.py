import time
import threading
from pynput import mouse, keyboard

kb = keyboard.Controller()
typed_text = ""
busy = False
quit_event = threading.Event()
mouse_listener = None

OPENERS = "({["


def type_line(line: str):
    """Type one line, neutralizing editor auto-closing brackets."""
    buf = ""
    for ch in line:
        if ch in OPENERS:
            if buf:
                kb.type(buf)
                buf = ""
            kb.type(ch)
            # Site auto-inserts a closing bracket; remove it so the
            # real closing bracket from the text is the only one.
            time.sleep(0.05)
            kb.press(keyboard.Key.delete)
            kb.release(keyboard.Key.delete)
            time.sleep(0.02)
        else:
            buf += ch
    if buf:
        kb.type(buf)


def type_text(text: str):
    global busy
    if busy or not text:
        return
    busy = True
    try:
        lines = text.split("\n")
        for i, line in enumerate(lines):
            if i > 0:
                # Site auto-indented after Enter; select that indent so
                # this line replaces it instead of stacking on top.
                with kb.pressed(keyboard.Key.shift):
                    kb.press(keyboard.Key.home)
                    kb.release(keyboard.Key.home)
                time.sleep(0.02)
                if not line:
                    kb.press(keyboard.Key.delete)
                    kb.release(keyboard.Key.delete)
            type_line(line)
            kb.press(keyboard.Key.enter)
            kb.release(keyboard.Key.enter)
            time.sleep(0.03)
        print("[*] Done typing.")
    finally:
        busy = False


def on_click(x, y, button, pressed):
    global typed_text
    # Button.x2 = mouse button 5 (side/forward button)
    if button == mouse.Button.x2 and pressed:
        if not typed_text:
            print("\n[!] No text stored yet.")
            return
        print("\n[*] Typing stored text...")
        threading.Thread(target=type_text, args=(typed_text,), daemon=True).start()


def read_multiline() -> str:
    print("Paste your text below (multi-line is fine).")
    print("When finished, type END on its own line (or press Ctrl+Z then Enter).\n")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "END":
            break
        lines.append(line)
    return "\n".join(lines)


def on_quit_hotkey():
    quit_event.set()
    if mouse_listener is not None:
        mouse_listener.stop()


def main():
    global typed_text, mouse_listener

    typed_text = read_multiline()

    if not typed_text:
        print("No text entered. Exiting.")
        return

    print("\n--- Text stored ---")
    print(typed_text)
    print("-------------------")
    print("Click into your target window, then press mouse button 5")
    print("(side/forward button) to type the text.")
    print("Quit: Ctrl+Shift+Q (from any window) or Ctrl+C (in this terminal).\n")

    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()

    hotkeys = keyboard.GlobalHotKeys({
        "<ctrl>+<shift>+q": on_quit_hotkey,
    })
    hotkeys.start()

    try:
        while mouse_listener.running and not quit_event.is_set():
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        if mouse_listener.running:
            mouse_listener.stop()
        hotkeys.stop()
        print("Exiting.")


if __name__ == "__main__":
    main()
