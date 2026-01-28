import time, sys, threading, termios, tty, select, atexit, signal

fd = sys.stdin.fileno()
orig = termios.tcgetattr(fd)

def restore():
    termios.tcsetattr(fd, termios.TCSADRAIN, orig)

atexit.register(restore)
signal.signal(signal.SIGINT, lambda *_: sys.exit(0))
signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))

work_duration = int(input("\n~~PoMoDoRo~~\n\nEach block has four work blocks, three short break blocks and one long break block\n\n(Answer in seconds)\nDuration of work block -> "))
short_brk_duration = int(input("Duration of short break block -> "))
long_brk_duration = int(input("Duration of long break block -> "))
print("\nKeyboard controls: [p] pause/resume  [r] reset block  [q] quit\n\n")

cycle_count = 0
paused = False
reset_block = False
quit_all = False

def key_listener():
    global paused, reset_block, quit_all

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setcbreak(fd)
        while True:
            if select.select([sys.stdin], [], [], 0.1)[0]:
                ch = sys.stdin.read(1)
                if ch == "p":
                    paused = not paused
                elif ch == "r":
                    reset_block = True
                elif ch == "q":
                    quit_all = True
                    break
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def clear_line():
    sys.stdout.write("\r\033[K")
    sys.stdout.flush()

def move_cursor_up(n=1):
    sys.stdout.write(f"\033[{n}A")
    sys.stdout.flush()

def wait_for_choice():
    clear_line()
    print(f"Press [y] to start cycle {cycle_count + 1}, [n] to stop")

    while True:
        if select.select([sys.stdin], [], [], 0.1)[0]:
            ch = sys.stdin.read(1)
            if ch in ("y", "n"):
                return ch

def progress_bar(current, total, block, width=40):
    progress = current / total
    filled = int(width * progress)
    bar = "█" * filled + "-" * (width - filled)
    percent = progress * 100

    clear_line()
    # move_cursor_up(1)
    # clear_line()

    if block % 2 == 0:
        label = "Focus on work..."
    elif block < 7:
        label = "Short break!    "
    else:
        label = "Long break!!!   "
    
    if paused:
        label = "[PAUSED]"

    sys.stdout.write(f"\r[{bar}] {percent:6.2f}%  {label}")
    sys.stdout.flush()

def run_block(total, blk):
    global reset_block

    elapsed = 0
    while elapsed <= total:
        if quit_all:
            clear_line()
            print(f"Completed {cycle_count} pomodoro cycles")
            tty.setcbreak(fd)
            sys.exit(0)

        if reset_block:
            elapsed = 0
            reset_block = False

        if not paused:
            progress_bar(elapsed, total, blk)
            time.sleep(1)
            elapsed += 1
        else:
            progress_bar(elapsed, total, blk)
            time.sleep(0.1)

def cycle():
    for blk in range(8):
        if blk % 2 == 0:
            total = work_duration
        elif blk < 7:
            total = short_brk_duration
        else:
            total = long_brk_duration
        
        # for i in range(total + 1):
        #     progress_bar(i, total, blk)
        #     time.sleep(1)
        run_block(total, blk)

listener = threading.Thread(target=key_listener, daemon=True)
listener.start()
while True:
    cycle_count += 1
    try:
        move_cursor_up(1)
        clear_line()
        print(f"Cycle {cycle_count}")
        cycle()
    except KeyboardInterrupt:
        clear_line()
        print("\nInterrupted.")
        sys.exit(1)
    c = wait_for_choice()
    clear_line()
    move_cursor_up(1)
    clear_line()
    if c != "y":
        print(f"Completed {cycle_count} pomodoro cycles")
        tty.setcbreak(fd)
        break