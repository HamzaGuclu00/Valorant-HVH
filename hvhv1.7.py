from PIL import ImageGrab
from pyautogui import click, moveTo
import time
import keyboard
import winsound
import ctypes
import os
from colorama import Fore, Style, init
import requests
import json

S_WIDTH, S_HEIGHT = (0, 0)
TARGET_COLORS = [(253, 108, 254), (209, 102, 235), (255, 87, 255), (254, 107, 255), (254, 101, 254), (255, 144, 255)]
TOLERANCE = 13
GRABZONE = 4
TRIGGER_KEY = "insert"
SWITCH_KEY = "ctrl+tab"
GRABZONE_KEY_UP = "up"
GRABZONE_KEY_DOWN = "down"
PAUSE_KEY = "s"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1121766471039721502/Y-y2_hkvC5G0sNbqre1eiETSteQY38fMPKfCTthvy07Kcl-6Yzl5maoF-qW4JlQJnE9D"

os.system("cls")
init(autoreset=True)

def set_screen_resolution():
    global S_WIDTH, S_HEIGHT
    screen_resolutions = {
        "1920x1080": (1920, 1080),
        "1680x1050": (1680, 1050),
        "1440x900": (1440, 900),
        "1366x768": (1366, 768)
    }

    print(Fore.CYAN + "╔════════════════════════════════════╗")
    print("║        Set Screen Resolution        ║")
    print("╚════════════════════════════════════╝")
    print(Style.RESET_ALL + "Please select one of the following resolutions:")

    for i, resolution in enumerate(screen_resolutions.keys()):
        print(f"   {i+1}. {resolution}")

    selected_option = input("   Select your option (1-4): ")
    selected_resolution = list(screen_resolutions.values())[int(selected_option) - 1]
    S_WIDTH, S_HEIGHT = selected_resolution

    print("\n   Selected resolution: {}x{}".format(S_WIDTH, S_HEIGHT))
    print("   Screen resolution set successfully.")

    print(Fore.CYAN + "\n════════════════════════════════════" + Style.RESET_ALL)


class FoundEnemy(Exception):
    pass


class TriggerBot:
    def __init__(self):
        self.toggled = False
        self.mode = 1
        self.last_reac = 0
        self.shots_fired = 0
        self.last_discord_message_id = None

    def toggle(self):
        self.toggled = not self.toggled

    def switch(self):
        if self.mode != 2:
            self.mode += 1
        else:
            self.mode = 0

        if self.mode == 0:
            winsound.Beep(200, 200)
        elif self.mode == 1:
            winsound.Beep(200, 200)
            winsound.Beep(200, 200)
        elif self.mode == 2:
            winsound.Beep(200, 200)
            winsound.Beep(200, 200)
            winsound.Beep(200, 200)

    def approx(self, r, g, b):
        for color in TARGET_COLORS:
            if all(color[i] - TOLERANCE < component < color[i] + TOLERANCE for i, component in enumerate((r, g, b))):
                return True
        return False

    def grab(self):
        screen = ImageGrab.grab((S_WIDTH // 2 - GRABZONE, S_HEIGHT // 2 - GRABZONE, S_WIDTH // 2 + GRABZONE, S_HEIGHT // 2 + GRABZONE))
        return screen

    def scan(self):
        start_time = time.time()
        pmap = self.grab()

        try:
            for x in range(GRABZONE * 2):
                for y in range(GRABZONE * 2):
                    r, g, b = pmap.getpixel((x, y))
                    if self.approx(r, g, b):
                        raise FoundEnemy

        except FoundEnemy:
            self.last_reac = int((time.time() - start_time) * 1000)
            self.click()

            if self.mode == 1:
                time.sleep(0.01)
            elif self.mode == 2:
                time.sleep(0.005)

            self.print_banner()

            self.shots_fired += 1

            if self.shots_fired >= 8:
                time.sleep(0.5)
                self.shots_fired = 0
            elif self.shots_fired >= 4:
                time.sleep(0.1)

    def click(self):
        if keyboard.is_pressed(PAUSE_KEY):
            return

        while keyboard.is_pressed(PAUSE_KEY):
            pass

        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
        time.sleep(0.01)
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)

    def print_banner(self):
        os.system("cls")

        print(Fore.RED + "Miarey" + Fore.YELLOW + " V1.7" + Style.RESET_ALL)

        print(Fore.GREEN + "╔═══════════════════════════════════════════════════════╗")
        print("║                     Controls                          ║")
        print("╚═══════════════════════════════════════════════════════╝" + Style.RESET_ALL)

        print("Trigger: ", end="")
        if not self.toggled:
            print(Fore.RED + "OFF" + Style.RESET_ALL)
        else:
            print(Fore.GREEN + "ON" + Style.RESET_ALL)

        print("Mode: ", end="")
        if self.mode == 0:
            print(Fore.YELLOW + "Single Shot" + Style.RESET_ALL)
        elif self.mode == 1:
            print(Fore.YELLOW + "Burst Mode" + Style.RESET_ALL)
        elif self.mode == 2:
            print(Fore.YELLOW + "Continuous Fire" + Style.RESET_ALL)

        print("Pixel Scan Area: ", end="")
        print(Fore.YELLOW + f"{GRABZONE}x{GRABZONE}" + Style.RESET_ALL)

        print(Fore.CYAN + "╔═══════════════════════════════════════════════════════╗")
        print("║                     Information                       ║")
        print("╚═══════════════════════════════════════════════════════╝" + Style.RESET_ALL)

        print("Reaction Time: ", end="")
        if self.last_reac == 0:
            print(Fore.YELLOW + "N/A" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + f"{self.last_reac} ms" + Style.RESET_ALL)

        print("Shots Fired: ", end="")
        print(Fore.YELLOW + str(self.shots_fired) + Style.RESET_ALL)

        print("")

        if self.last_discord_message_id is not None:
            try:
                response = requests.get(DISCORD_WEBHOOK_URL)
                messages = json.loads(response.text)
                for message in messages:
                    if message["id"] == self.last_discord_message_id:
                        print(Fore.GREEN + "Discord Message Sent Successfully" + Style.RESET_ALL)
                        print(Fore.YELLOW + "Message Content: " + Style.RESET_ALL + message["content"])
                        break
            except:
                print(Fore.RED + "Error Retrieving Discord Message" + Style.RESET_ALL)

    def discord_alert(self):
        message = {
            "content": f"Miarey TriggerBot has fired a shot! Last reaction time: {self.last_reac} ms",
            "username": "Miarey TriggerBot",
            "avatar_url": "https://example.com/avatar.png"
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(message), headers=headers)

        if response.status_code == 200:
            response_data = json.loads(response.text)
            self.last_discord_message_id = response_data["id"]
        else:
            print(Fore.RED + "Error sending Discord message" + Style.RESET_ALL)


def main():
    set_screen_resolution()
    bot = TriggerBot()

    while True:
        if keyboard.is_pressed(TRIGGER_KEY):
            bot.toggle()
            time.sleep(0.2)

        if keyboard.is_pressed(SWITCH_KEY):
            bot.switch()
            time.sleep(0.2)

        if keyboard.is_pressed(GRABZONE_KEY_UP):
            global GRABZONE
            if GRABZONE < 10:
                GRABZONE += 1
                time.sleep(0.2)

        if keyboard.is_pressed(GRABZONE_KEY_DOWN):
            if GRABZONE > 1:
                GRABZONE -= 1
                time.sleep(0.2)

        if bot.toggled:
            bot.scan()

        if bot.shots_fired > 0:
            bot.discord_alert()


if __name__ == "__main__":
    main()
