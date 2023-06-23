from PIL import ImageGrab
from pyautogui import click, moveTo
import time
import keyboard
import winsound
import ctypes
import os
from colorama import Fore, Style, init

S_WIDTH, S_HEIGHT = (0, 0)
PURPLE_R, PURPLE_G, PURPLE_B = (250, 100, 250)
TOLERANCE = 75
GRABZONE = 5
TRIGGER_KEY = "alt"
SWITCH_KEY = "ctrl+tab"
GRABZONE_KEY_UP = "up"
GRABZONE_KEY_DOWN = "down"
PAUSE_KEY = "s"

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
        return PURPLE_R - TOLERANCE < r < PURPLE_R + TOLERANCE and PURPLE_G - TOLERANCE < g < PURPLE_G + TOLERANCE and PURPLE_B - TOLERANCE < b < PURPLE_B + TOLERANCE

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
        os.system("cls")  # Konsolu temizle

        # Bot adı ve başlık
        print("╔═══════════════════════╗")
        print("║    Miarey Project     ║")
        print("╚═══════════════════════╝")

        # Kontrol bilgilerini yazdır
        print("   Kontroller:")
        print("   - Aktifleştir:  ", TRIGGER_KEY)
        print("   - Mod Değiştir:  ", SWITCH_KEY)
        print("   - Tarama Alanını Büyüt: ", GRABZONE_KEY_UP)
        print("   - Tarama Alanını Küçült: ", GRABZONE_KEY_DOWN)
        print("   - Durdur:       ", PAUSE_KEY)

        # Bot durumu ve ayarları
        print("\n   Mevcut Ayarlar:")
        print("   - Aktif:       ", Fore.GREEN + "Evet" if self.toggled else Fore.RED + "Hayır")
        print("   - Mod:         ", self.mode)
        print("   - Son Tepki Süresi:  {} ms ({} ms/piksel)".format(self.last_reac, self.last_reac / (GRABZONE * GRABZONE)))
        print("   - Atışlar:     ", self.shots_fired)

        # Renk bilgilerini yazdır
        print("\n   Renk Bilgileri:")
        print("   - Düşman Rengi:      Mor (RGB: {}, {}, {})".format(PURPLE_R, PURPLE_G, PURPLE_B))
        print("   - Renk Toleransı:    ±{}".format(TOLERANCE))

        # Tarama alanı bilgilerini yazdır
        print("\n   Tarama Alanı Bilgileri:")
        print("   - Mevcut Tarama Alanı:  {}x{}".format(GRABZONE, GRABZONE))
        print("   - Ekran Çözünürlüğü: {}x{}".format(S_WIDTH, S_HEIGHT))

        # Kapanış çizgisi
        print("\n════════════════════════")

    def move_to_color(self, x, y):
        target_x = (x / GRABZONE) * S_WIDTH
        target_y = (y / GRABZONE) * S_HEIGHT
        moveTo(target_x, target_y)

if __name__ == "__main__":
    init(autoreset=True)
    set_screen_resolution()
    
    bot = TriggerBot()
    bot.print_banner()

    while True:
        if keyboard.is_pressed(SWITCH_KEY):
            bot.switch()
            bot.print_banner()

            while keyboard.is_pressed(SWITCH_KEY):
                pass

        if keyboard.is_pressed(GRABZONE_KEY_UP):
            GRABZONE += 5
            bot.print_banner()
            winsound.Beep(400, 200)

            while keyboard.is_pressed(GRABZONE_KEY_UP):
                pass

        if keyboard.is_pressed(GRABZONE_KEY_DOWN):
            if GRABZONE > 5:
                GRABZONE -= 5
                bot.print_banner()
                winsound.Beep(300, 200)

            while keyboard.is_pressed(GRABZONE_KEY_DOWN):
                pass

        if keyboard.is_pressed(TRIGGER_KEY):
            bot.toggle()
            bot.print_banner()

            if bot.toggled:
                winsound.Beep(440, 200)
            else:
                winsound.Beep(392, 200)

            while keyboard.is_pressed(TRIGGER_KEY):
                pass

        if bot.toggled:
            bot.scan()
