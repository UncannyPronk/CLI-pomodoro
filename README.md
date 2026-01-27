# CLI Pomodoro Timer

A **Terminal-based Pomodoro Timer** written in pure Python with a live progress bar, keyboard controls, and non-blocking input handling.

- No external dependencies (except pip installs).
- Designed for Linux and macOS terminals.

## Features

- Real-time progress bar

- Pause and resume the current block

- Reset the current block instantly

- Quit at any time with a completion summary

- Non-blocking keyboard controls

- Background key listener using threading

- Proper terminal state restoration on exit

### Pomodoro Structure

Each **cycle** consists of **8 blocks**:

| Block | Type          |
|------:|--------------|
| 1     | Work          |
| 2     | Short Break   |
| 3     | Work          |
| 4     | Short Break   |
| 5     | Work          |
| 6     | Short Break   |
| 7     | Work          |
| 8     | Long Break    |

All durations are provided by the user in seconds at runtime.

## Keyboard Controls

| Key | Action |
|----:|--------|
| `p` | Pause / Resume current block |
| `r` | Reset current block |
| `q` | Quit immediately |

Keyboard controls work while the timer is running and do not block the progress bar.

## Usage

### Run the program

```bash
python3 pomodoro.py
```

### Enter block durations (in seconds)

Duration of work block -> 1500

Duration of short break block -> 300

Duration of long break block -> 900

### Control execution using the keyboard

[p] pause or resume
[r] reset block
[q] quit

# Example Output

Cycle 1
[██████████████--------------] 45.00% Focus on work...

When paused:

[██████████████--------------] 45.00% Focus on work... [PAUSED]

# How It Works (Technical Overview)

- termios and tty are used for raw terminal input

- select enables non-blocking key detection

- threading runs the keyboard listener in the background

- ANSI escape codes handle cursor movement and progress bar rendering

- atexit and signal handlers guarantee terminal restoration on exit

No blocking input calls are used during active timing.

## Requirements

- Python 3.7 or newer

- Unix-like terminal environment (Linux or macOS)

# Known Limitations

- Requires a real TTY (not suitable for redirected input)

- Terminal resizing during execution may misalign output

- Windows is not compatible with this tool

---