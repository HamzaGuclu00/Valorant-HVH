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
TRIGGER_KEY = "alt"
SWITCH_KEY = "ctrl+tab"
GRABZONE_KEY_UP = "up"
GRABZONE_KEY_DOWN = "down"
PAUSE_KEY = "s"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1121766471039721502/Y-y2_hkvC5G0sNbqre1eiETSteQY38fMPKfCTthvy07Kcl-6Yzl5maoF-qW4JlQJnE9D"

os.system("cls")
def set_screen_resolution():
    global S_WIDTH, S_HEIGHT
    screen_resolutions = {
        "1920x1080": (1920, 1080),
        "1680x1050": (1680, 1050),
        "1440x900": (1440, 900),
        "1366x768": (1366, 768)
    }

    # Başlık ve açıklama
    print(Fore.CYAN + "╔════════════════════════════════════╗")
    print("║    Ekran Çözünürlüğünü Ayarla    ║")
    print("╚════════════════════════════════════╝")
    print(Style.RESET_ALL + "Lütfen aşağıdaki çözünürlüklerden birini seçin:")

    # Seçenekleri listele
    for i, resolution in enumerate(screen_resolutions.keys()):
        print(f"   {i+1}. {resolution}")

    # Seçim yapılmasını iste
    selected_option = input("   Seçiminizi yapın (1-4): ")
    selected_resolution = list(screen_resolutions.values())[int(selected_option) - 1]
    S_WIDTH, S_HEIGHT = selected_resolution

    # Onay mesajı
    print("\n   Seçilen çözünürlük: {}x{}".format(S_WIDTH, S_HEIGHT))
    print("   Ekran çözünürlüğü başarıyla ayarlandı.")

    # Kapanış çizgisi
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

        # Ana başlık
        print(Fore.RED + "Miarey" + Fore.YELLOW + " V1.7" + Style.RESET_ALL)

        # Kontroller başlığı
        print(Fore.GREEN + "╔═══════════════════════════════════════════════════════╗")
        print("║                       Kontroller                       ║")
        print("╚═══════════════════════════════════════════════════════╝" + Style.RESET_ALL)

        # Aktif Trigger ve modu
        print("Aktif Trigger:", Fore.YELLOW + ("Kapalı" if not self.toggled else "Açık") + Style.RESET_ALL)
        if self.mode == 0:
            print("Mod:", Fore.YELLOW + "Tek Atış" + Style.RESET_ALL)
        elif self.mode == 1:
            print("Mod:", Fore.YELLOW + "Seri Atış" + Style.RESET_ALL)
        elif self.mode == 2:
            print("Mod:", Fore.YELLOW + "Sürekli Atış" + Style.RESET_ALL)

        # Pixel Tarama Alanı
        print("Pixel Tarama Alanı:", Fore.YELLOW + GRABZONE_KEY_UP + "/" + GRABZONE_KEY_DOWN + Style.RESET_ALL)

        # Bilgiler başlığı
        print(Fore.CYAN + "╔═══════════════════════════════════════════════════════╗")
        print("║                       Bilgiler                         ║")
        print("╚═══════════════════════════════════════════════════════╝" + Style.RESET_ALL)

        # Tepki süresi
        print("Tepki Süresi:", Fore.YELLOW + str(self.last_reac) + " ms" + Style.RESET_ALL)

        # Ateşlenen mermi sayısı
        print("Ateşlenen Mermi Sayısı:", Fore.YELLOW + str(self.shots_fired) + Style.RESET_ALL)

    def send_discord_message(self):
        if DISCORD_WEBHOOK_URL is None or self.last_discord_message_id is not None:
            return

        payload = {
            "content": "TriggerBot Aktif!",
            "username": "TriggerBot",
            "avatar_url": "https://i.imgur.com/your-avatar.png"
        }

        response = requests.post(DISCORD_WEBHOOK_URL, json.dumps(payload), headers={"Content-Type": "application/json"})

        try:
            response_data = response.json()
            if "id" in response_data:
                self.last_discord_message_id = response_data["id"]
                print("[HVH] Log.txt puanlar kaydedildi!")
            else:
                print("[HVH] Log.txt puanlar kaydedilirken bir hata oluştu!")
        except json.decoder.JSONDecodeError:
            print("[HVH] Log.txt puanlar kaydedilirken bir hata oluştu!")

    def main(self):
        set_screen_resolution()
        self.print_banner()
        self.send_discord_message()

        while True:
            if keyboard.is_pressed(SWITCH_KEY):
                self.switch()
                self.print_banner()
                time.sleep(0.3)

            if keyboard.is_pressed(TRIGGER_KEY):
                self.toggle()
                self.print_banner()
                time.sleep(0.3)

            if keyboard.is_pressed(GRABZONE_KEY_UP):
                GRABZONE += 1
                self.print_banner()
                time.sleep(0.3)

            if keyboard.is_pressed(GRABZONE_KEY_DOWN):
                GRABZONE -= 1
                self.print_banner()
                time.sleep(0.3)

            if self.toggled:
                self.scan()

if __name__ == "__main__":
    bot = TriggerBot()
    bot.main()