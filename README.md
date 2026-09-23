# auto_type.py

A small Windows terminal tool that stores multi-line text and types it into
whatever window is focused when you press a trigger mouse button
(default: **mouse button 5**, the forward side button on most mice — easily
switchable, see below).

It simulates real keystrokes (not clipboard paste), so it works on websites
that block `Ctrl+V`.

## What it does

1. Asks you to paste/enter some text in the terminal (multi-line supported).
2. Waits for you to click into a target window (browser, editor, etc.).
3. When you press the trigger mouse button, it types the stored text
   keystroke by keystroke, line by line, pressing Enter between lines.

While typing it tries to compensate for common editor behavior:

- **Auto-indent**: after Enter, it clears indentation the site inserted so
  lines don't keep getting more indented.
- **Auto-closing brackets**: after `{`, `(`, or `[` it presses Delete to
  remove the character the site auto-inserted, so your real closing brackets
  are the only ones typed.

## Requirements

- Windows
- Python 3.x
- `pynput` (installed with `pip install pynput`)

## Usage

```text
python auto_type.py
```

1. When prompted, paste or type your text.  
   End input with a line containing only:
   ```text
   END
   ```
   (or press `Ctrl+Z` then `Enter`).
2. Click into the window where you want the text to appear.
3. Press the trigger mouse button (default: **mouse button 5**, forward side
   button).
4. The text is typed at the cursor position.

### Replacing the stored text

While the script is running it shows a `>` prompt in the terminal. Type:

```text
REPLACE
```

then paste/enter the new text and finish with `END` on its own line. The old
text is discarded and the new text is what the trigger button will type from
then on. Empty input (just `END`) leaves the stored text unchanged.

### Changing the trigger button

Not everyone has mouse button 5. The trigger is a single constant near the
top of `auto_type.py`:

```python
TRIGGER_BUTTON = mouse.Button.x2   # mouse button 5 (forward side) — default
```

Change that one line to switch triggers (all options are listed in the
comments right above it):

| Button you want              | Set `TRIGGER_BUTTON` to   |
| ---------------------------- | -------------------------- |
| Mouse button 5 (forward)     | `mouse.Button.x2` (default)|
| Mouse button 4 (back)        | `mouse.Button.x1`          |
| Middle mouse (wheel click)   | `mouse.Button.middle`      |
| Left / right click           | `mouse.Button.left` / `.right` (not recommended) |

Any other `pynput` `mouse.Button` member works the same way — assign it to
`TRIGGER_BUTTON` and you're done; no other code changes are needed. Restart
the script after editing.

### Quitting

- **`QUIT`** — type at the `>` prompt in the terminal.
- **`Ctrl+Shift+Q`** — works from any window (recommended).
- **`Ctrl+C`** — only works while the terminal itself is focused.

## Notes

### Trailing braces

Some sites insert an extra `}` (or `)` / `]`) at the end of the typed text.
This is a small, easily fixable artifact — just delete the stray closing
bracket(s) at the end by hand after typing finishes.

### Tips

- Make sure the target window has focus (clicked into the input field) before
  pressing the trigger button.
- Only press the trigger once per run; typing is not interruptible mid-way.
- The script must stay running in the terminal while you use it.
- If the default trigger does nothing on your mouse, switch `TRIGGER_BUTTON`
  (see “Changing the trigger button” above).
