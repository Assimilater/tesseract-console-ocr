import sys
import time
import os
import random
import string
import subprocess
import io
import numpy as np
from screeninfo import get_monitors
import mss

def gen_lorum_ipsum(output_stream, console_width):
    lorem_ipsum = [
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi.",
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore.",
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia."
    ]
    for line in random.sample(lorem_ipsum, k=3):
        print(line, file=output_stream)

def gen_table_nolabels(output_stream, console_width):
    numbers = [random.randint(1000, 9999) for _ in range(76)]
    print("\nFormatted Table Output:", file=output_stream)
    for i in range(0, 76, 4):
        print(f"{numbers[i]:>6}  {numbers[i+1]:>6}  {numbers[i+2]:>6}  {numbers[i+3]:>6}", file=output_stream)

def generate_probability_distribution(size=51, peak=6, decay=10, total_events=10000):
    x = np.arange(size, dtype=np.int64)
    weights = np.exp(-((x - peak) / decay) ** 2)
    weights /= weights.sum()
    return (weights * np.int64(total_events)).astype(np.int64)

def gen_risk_pdf(output_stream, console_width):
    print("\nAlternative Table Distribution Output:", file=output_stream)
    total_events = 10**random.randint(6, 11)
    size = random.randint(45, 55)
    peak = random.randint(4, 8)
    decay = random.randint(8, 12)
    numbers = generate_probability_distribution(size, peak, decay, total_events)
    numbers = np.pad(numbers, (0, max(0, 76 - len(numbers))), 'constant')
    for i, count in enumerate(numbers):
        print(f"{i:>2} attackers lost {count:>15,}", end='  |  ' if (i + 1) % 5 else '\n', file=output_stream)
    check = sum(numbers)
    print(f" Sanity Check - total events: {check:>15,} ({'correct' if check == total_events else 'incorrect'})", file=output_stream)

def gen_gibberish(output_stream, console_width, lines, noise=0):
    console_chars = string.ascii_letters + string.digits + string.punctuation + " "
    print("\nRandom Gibberish Output:", file=output_stream)
    for _ in range(lines):
        print(''.join(random.choices(console_chars, k=console_width+random.randint(0,noise))), file=output_stream)

generation_functions = [
    gen_lorum_ipsum,
    gen_table_nolabels,
    gen_risk_pdf,
    lambda out, console_width: gen_gibberish(out, console_width, random.randint(5, 25), random.randint(0, console_width))
]

def generate_console_output(console_width, visible_lines):
    output_stream = io.StringIO()
    out = ""
    while len(out.split("\n")) <= visible_lines:
      num_functions = random.randint(2, max(len(generation_functions), random.randint(5, 10)))
      selected_functions = random.choices(generation_functions, k=num_functions)
      for func in selected_functions:
          func(output_stream, console_width)
      out = output_stream.getvalue()
    return out

def apply_word_wrap(text, wrap_length, visible_lines):
    wrapped_lines = []
    for line in text.split("\n"):
        while len(line) > wrap_length:
            wrapped_lines.append(line[:wrap_length])
            line = line[wrap_length:]
        wrapped_lines.append(line)
    
    # remove the last empty line
    wrapped_lines = wrapped_lines[:-1]
  
    # Trim the text to only the last visible_lines
    wrapped_lines = wrapped_lines[-visible_lines:]
    
    return "\n".join(wrapped_lines)

monitors = get_monitors()
left_monitor = min(monitors, key=lambda m: m.x)
screen_width, screen_height = left_monitor.width, left_monitor.height
wrap_length = int(os.popen("powershell (Get-Host).UI.RawUI.BufferSize.Width").read().strip())
visible_lines = int(os.popen("powershell (Get-Host).UI.RawUI.WindowSize.Height").read().strip())

print(f"Detected resolution: {screen_width}x{screen_height}")
print(f"Detected word wrap length: {wrap_length} characters")
print(f"Detected visible lines: {visible_lines}")

num_samples = 1_000
for i in range(num_samples):
    generated_text = generate_console_output(wrap_length, visible_lines)
    wrapped_text = apply_word_wrap(generated_text, wrap_length, visible_lines)
    sys.stdout.write("\n" + wrapped_text)
    sys.stdout.flush()
    time.sleep(0.5) # give the console time to update for screenshotting
    
    with open(f"training/sample_{i:03d}.gt.txt", "w", encoding="utf-8") as f:
        f.write(wrapped_text)
    
    screenshot_path = f"training/sample_{i:03d}.png"
    with mss.mss() as sct:
        monitors = sct.monitors
        left_monitor_index = min(range(1, len(monitors)), key=lambda i: monitors[i]["left"])
        sct.shot(mon=left_monitor_index, output=screenshot_path)
