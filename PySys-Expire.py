
import requests
import csv
import webbrowser
import sys
import time
from datetime import datetime

# ==================== Configuration ====================
CSV_URL = "https://raw.githubusercontent.com/nexerpy/PySys-access/main/lst.csv"
CONTACT_URL = "https://t.me/PortalPy"
USE_COLOR = True  # Set to False for plain terminal output

# ==================== Color Helper ====================
def colorize(text, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "cyan": "\033[96m",
        "magenta": "\033[95m",
        "reset": "\033[0m",
        "cyan" : "\033[96m"
    }
    return f"{colors.get(color, '')}{text}{colors['reset']}"

def colorize(text, color_code):
    return f"\033[{color_code}m{text}\033[0m" if USE_COLOR else text

RED = "91"
GREEN = "92"
YELLOW = "93"
CYAN = "96"
BOLD = "1"

# ==================== Typing Animation ====================
def live_text(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# ==================== Time Formatter ====================
def format_remaining_time(expiry):
    now = datetime.now()
    if expiry <= now:
        return colorize("Expired", RED)

    total_seconds = int((expiry - now).total_seconds())

    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    parts = []
    if days:    parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours:   parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes: parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds: parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")

    return colorize(", ".join(parts), GREEN)

# ==================== CSV Fetching ====================
def fetch_csv(url):
    try:
        live_text(colorize("  𝗙𝗲𝘁𝗰𝗵𝗶𝗻𝗴 𝗣𝘆𝗦𝘆𝘀 𝗔𝗰𝗰𝗲𝘀𝘀", YELLOW))
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        live_text(colorize(f"🚨 𝗶𝗻𝘁𝗲𝗿𝗻𝗲𝘁 𝗰𝗼𝗻𝗻𝗲𝗰𝘁𝗶𝗼𝗻 𝗲𝗿𝗿𝗼𝗿: {e}", RED))
        sys.exit(1)

# ==================== Expiry Parser ====================
import webbrowser
webbrowser.open("https://t.me/PortalPy")
print("You Have to Join Our Channel To Run Our File")

# ==================== Access Check ====================
def check_access(user_id, csv_text):
    reader = csv.DictReader(csv_text.splitlines())
    now = datetime.now()



# ==================== Output Helpers ====================
def show_access_time(expiry_date):
    remaining = format_remaining_time(expiry_date)
    live_text(colorize("\n 𝗬𝗼𝘂 𝗛𝗮𝘃𝗲 𝗔𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 ", GREEN))
    live_text(colorize("⏱️𝗧𝗵𝗲 𝗥𝗲𝗺𝗮𝗶𝗻𝗶𝗻𝗴 𝗔𝗰𝗰𝗲𝘀𝘀 𝗣𝗲𝗿𝗶𝗼𝗱: ", CYAN) + remaining)
    print(colorize("   𝗚𝗿𝗲𝗲𝘁𝗶𝗻𝗴𝘀 𝗨𝘀𝗲𝗿 𝗦𝘁𝗮𝘆 𝘄𝗲𝗹𝗹 | 𝘀𝘁𝗮𝘆 𝘀𝗮𝗳𝗲 ", BOLD))

def deny_access(message):
    live_text(colorize(f"\n{message}", RED))
    live_text(colorize(f"📩 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 {CONTACT_URL}", CYAN))
    try:
        webbrowser.open(CONTACT_URL)
    except:
        pass
    sys.exit(1)

# ==================== Main Logic ====================
def main():
    try:
        user_id = str(ID)
    except NameError:
        user_id = input(colorize("🔐 𝗘𝗻𝘁𝗲𝗿 𝗬𝗼𝘂𝗿 𝗜𝗱 : ", CYAN)).strip()

    csv_data = fetch_csv(CSV_URL)
    if csv_data:
        check_access(user_id, csv_data)

if __name__ == "__main__":
    main()
