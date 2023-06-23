from ast import Return
import keyboard
import time
import ctypes
import PIL.ImageGrab
import PIL.Image
import winsound
import os
import mss
from colorama import Fore, Style, init
from pyautogui import moveTo
import numpy as np

S_HEIGHT, S_WIDTH = (1920, 1080)  # Ekran çözünürlüğünü 1920x1080 olarak ayarlayın
PURPLE_R, PURPLE_G, PURPLE_B = (250, 100, 250)
TOLERANCE = 75
GRABZONE = 5
TRIGGER_KEY = "alt"
SWITCH_KEY = "ctrl + tab"
GRABZONE_KEY_UP = "up"
GRABZONE_KEY_DOWN = "down"
outline = ["Mor", "Kırmızı", "Sarı"]
PAUSE_KEY = "s"


class FoundEnemy(Exception):
    pass


class triggerBot():

    def __init__(self):
        self.toggled = False
        self.mode = 1
        self.last_reac = 0
        self.shots_fired = 0  # Ateş edilen mermi sayısını takip etmek için bir değişken ekleyin

    def toggle(self):
        self.toggled = not self.toggled

    def switch(self):
        if self.mode != 2:
            self.mode += 1
        else:
            self.mode = 0
        if self.mode == 0:
            winsound.Beep(200, 200)
        if self.mode == 1:
            winsound.Beep(200, 200)
            winsound.Beep(200, 200)
        if self.mode == 2:
            winsound.Beep(200, 200)
            winsound.Beep(200, 200)
            winsound.Beep(200, 200)

    def click(self):
        if keyboard.is_pressed(PAUSE_KEY) or keyboard.is_pressed(PAUSE_KEY) or keyboard.is_pressed(PAUSE_KEY) or keyboard.is_pressed(PAUSE_KEY):
            return
        while keyboard.is_pressed(PAUSE_KEY) or keyboard.is_pressed(PAUSE_KEY) or keyboard.is_pressed(PAUSE_KEY) or keyboard.is_pressed(PAUSE_KEY):
            pass
        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
        time.sleep(0.025)  # Mouse tıklamasından sonra bekleme süresini düşürün
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)

    def approx(self, r, g, b):
        return PURPLE_R - TOLERANCE < r < PURPLE_R + TOLERANCE and PURPLE_G - TOLERANCE < g < PURPLE_G + TOLERANCE and PURPLE_B - TOLERANCE < b < PURPLE_B + TOLERANCE

    def grab(self):
        with mss.mss() as sct:
            bbox = (int(S_HEIGHT / 2 - GRABZONE), int(S_WIDTH / 2 - GRABZONE), int(S_HEIGHT / 2 + GRABZONE),
                    int(S_WIDTH / 2 + GRABZONE))
            sct_img = sct.grab(bbox)
            return PIL.Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

    def scan(self):
        start_time = time.time()
        pmap = self.grab()

        try:
            for x in range(0, GRABZONE * 2):
                for y in range(0, GRABZONE * 2):
                    r, g, b = pmap.getpixel((x, y))
                    if self.approx(r, g, b):
                        raise FoundEnemy

        except FoundEnemy:
            self.last_reac = int((time.time() - start_time) * 900)
            self.click()
            if self.mode == 1:
                time.sleep(0.1)

            self.print_banner()  # Call the method using 'self'

            # Ateş edilen mermi sayısını artırın
            self.shots_fired += 1

            # Mermi sayısı kontrolü yapın
            if self.shots_fired >= 4:  # 4 veya 5 yerine 4 olarak değiştirin
                time.sleep(0.1)  # Ek bir bekleme süresi ekleyin
                self.shots_fired = 0

    def print_banner(self):  # Move the method inside the class
        os.system("cls")
        print(Style.BRIGHT + Fore.RED + "Miarey" + Fore.YELLOW + " FullConcact" + Style.RESET_ALL)
        print(Fore.GREEN + "====== Kontroller ======" + Style.RESET_ALL)
        print("Aktif Trigger Bot:", Fore.YELLOW + TRIGGER_KEY + Style.RESET_ALL)
        print("Pixel Tarama Alanı:", Fore.YELLOW + GRABZONE_KEY_UP + "/" + GRABZONE_KEY_DOWN + Style.RESET_ALL)
        print(Fore.CYAN + "==== Bilgiler =====" + Style.RESET_ALL)
        print("Düşman Dış Rengi:" + Fore.MAGENTA + " Mor Olmak Zorundadır" + Style.RESET_ALL)
        print("Pixel Alanı:", Fore.CYAN + str(GRABZONE) + "x" + str(GRABZONE) + Style.RESET_ALL)
        print("Aktif:", (Fore.GREEN if self.toggled else Fore.RED) + str(self.toggled) + Style.RESET_ALL)
        print("Tepki Süresi:", Fore.CYAN + str(self.last_reac) + Style.RESET_ALL + " ms (" + str(
            (self.last_reac) / (GRABZONE * GRABZONE)) + "ms/pix)")

    def move_to_color(self, x, y):
        screen_width, screen_height = S_WIDTH, S_HEIGHT
        target_x = (x / GRABZONE) * screen_width
        target_y = (y / GRABZONE) * screen_height
        moveTo(target_x, target_y)


if __name__ == "__main__":
    bot = triggerBot()
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
