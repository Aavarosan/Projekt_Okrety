import pygame
import socket
import sys

pygame.init()

# Stałe - Obrazy i obiekty graficzne:
LOGO = pygame.image.load('imgs/logo.png')
IKONA = pygame.image.load('imgs/icon.png')
KURSOR = pygame.cursors.broken_x
MUSIC_ON = pygame.image.load('imgs/volume.png')
MUSIC_OFF = pygame.image.load('imgs/mute.png')

# Stałe - Koordynaty i wymiary:
WYMIARY_EKRANU = (1200, 600)
LOGO_COORDS = (472, 75)
MUSIC_BUTTON_COORDS = (590, 10)
MUSIC_BUTTON_BACKGROUND = (585, 5, 35, 35)
TILE_SIZE = 45
PION, POZIOM = 0, 1
LOST, WON = 0, 1

# Stałe - Fonty:
FONT1 = pygame.font.Font('freesansbold.ttf', 30)
FONT2 = pygame.font.Font('freesansbold.ttf', 20)

# Stałe - Kolory:
CZARNY = (0, 0, 0)
BIALY = (255, 255, 255)
BLEKIT = (71, 195, 239)
MALINOWY = (239, 71, 111)
SZARY_INFO = (150, 150, 150)
SZARY_TLO = (100, 100, 100)

# Stałe - SOCKET
PORT = 8000
MAX_MSG_SIZE = 1024

# Inicjalizacja pygame, ustawienia okna gry

ekran = pygame.display.set_mode(WYMIARY_EKRANU)
pygame.display.set_caption("GRA W OKRĘTY Y")
pygame.display.set_icon(IKONA)
pygame.mouse.set_cursor(*KURSOR)

'''Tablice reprezentujące plansze
Każdy element (kafelek) posiada listę trzech wartości:
p[x][y][0]: 1, gdy kafelek jest odsłonięty, w przeciwnym razie 0
p[x][y][1]: 1, gdy jest to statek, w przeciwnym razie 0
p[x][y][2]: 1, gdy w dany kafelek było już strzelane, w przeciwnym razie 0
'''
p1 = [[[0, 0, 0] for _ in range(10)] for _ in range(10)]
p2 = [[[0, 0, 0] for _ in range(10)] for _ in range(10)]

'''
class Music:
    def initiate(self):
    pygame.mixer.music.load('imgs/bs.mp3')
    pygame.mixer.music.play()

    music = 1

    def change():
        if Music.music == 1:
            pygame.mixer.music.pause()
            Music.music = 0
            pygame.draw.rect(ekran, SZARY_TLO, MUSIC_BUTTON_BACKGROUND)
            ekran.blit(MUSIC_OFF, MUSIC_BUTTON_COORDS)
            prompter("MUSIC : OFF", 0)
        else:
            pygame.mixer.music.unpause()
            Music.music = 1
            pygame.draw.rect(ekran, SZARY_TLO, MUSIC_BUTTON_BACKGROUND)
            ekran.blit(MUSIC_ON, MUSIC_BUTTON_COORDS)
            prompter("MUSIC : ON", 0)
        pygame.time.wait(350)


    global music
    if music == 1:
        pygame.mixer.music.pause()
        music = 0
        pygame.draw.rect(ekran, SZARY_TLO, (585, 5, 35, 35))
        ekran.blit(MUSIC_OFF, MUSIC_BUTTON_COORDS)
        info("MUSIC : OFF", 0)
        pygame.time.wait(350)
    else:
        pygame.mixer.music.unpause()
        music = 1
        pygame.draw.rect(ekran, SZARY_TLO, (585, 5, 35, 35))
        ekran.blit(MUSIC_ON, MUSIC_BUTTON_COORDS)
        info("MUSIC : ON", 0)
        pygame.time.wait(350)
'''


def redo(nb):
    '''
    Funkcja odświeżająca widok na ekranie.
    nb: parametr mówiący, czy mają zostać odświeżone (narysowane) kafelki planszy, czy też nie.
    '''
    if nb == 1:
        rysowanie_planszy(1)
        rysowanie_planszy(0)
    pygame.display.flip()


def reset():
    '''
    Funkcja służąca do zresetowania położenia statków.
    '''
    for y in p1:
        for x in y:
            x[0], x[1] = 0, 0


def rysowanie_planszy(n):
    '''
    Funkcja odświeżająca aktualny stan danej planszy na ekranie.
    '''
    if n == 1:
        x_init, y_init = 20, 5
        p = p1
    else:
        x_init, y_init = (20 + 10 * TILE_SIZE + 100 + 75), 5
        p = p2
    for i in range(10):
        for j in range(10):
            x = p[j][i]
            if x[0] == 0:
                pygame.draw.rect(ekran, CZARNY, (
                x_init + j * 10 + j * TILE_SIZE, y_init + i * 10 + i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif x[1] == 0:
                pygame.draw.rect(ekran, BLEKIT, (
                x_init + j * 10 + j * TILE_SIZE, y_init + i * 10 + i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            else:
                pygame.draw.rect(ekran, MALINOWY, (
                x_init + j * 10 + j * TILE_SIZE, y_init + i * 10 + i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if x[2] == 1 and n == 1:
                text = FONT1.render('x', True, (0, 0, 0))
                textr = text.get_rect()
                textr.center = (
                x_init + j * 10 + j * TILE_SIZE + TILE_SIZE // 2, y_init + i * 10 + i * TILE_SIZE + TILE_SIZE // 2)
                ekran.blit(text, textr)


def get_tile(px, py, n):
    '''
    Zwraca indeks naciśniętego kafelka.
    '''
    # if 590 < px < 610 and 10 < py < 30:
    #    Music.change()
    #    return
    if n == 1:
        x_init, y_init = 20, 5
    else:
        x_init, y_init = (20 + (10 * TILE_SIZE + 100) + 75), 5
    for i in range(10):
        for j in range(10):
            xp, xk, yp, yk = x_init + j * 10 + j * TILE_SIZE, x_init + (j + 1) * 10 + (
                        j + 1) * TILE_SIZE, y_init + i * 10 + i * TILE_SIZE, y_init + (i + 1) * 10 + (i + 1) * TILE_SIZE
            if xp < px < xk and yp < py < yk:
                coords = j, i
                return coords


def prompter(prompt, n, x=0, y=550, lx=1200, ly=50, font=1):
    '''
    Funkcja wyswietlajaca prostokąt z tekstem w nim wyśrodkowanym.
    '''
    text = FONT1.render(prompt, True, CZARNY) if font == 1 else FONT2.render(prompt, True, CZARNY)
    textrect = text.get_rect()
    textrect.center = (int(x + lx / 2), int(y + ly / 2))
    pygame.draw.rect(ekran, SZARY_INFO, (x, y, lx, ly))
    ekran.blit(text, textrect)
    redo(n)


def statek(lg):
    '''
    Funkcja obslugująca ustawianie statków.
    '''
    n = 4 - lg + 1
    while True:
        prompter("Ustaw statek: Dlugosc: {0}, pozostało: {1}, (LPM poziomo, PPM pionowo)".format(lg, n), 1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Lewy Przycisk Myszy
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x = pygame.mouse.get_pos()
                # Sprawdzenie przycisku resetu
                if 570 < x[0] < 635 and 300 < x[1] < 350:
                    reset()
                    return 0
                a = get_tile(*x, 1)
                if type(a) == tuple:
                    if check_statek(*a, lg, POZIOM) is True:
                        ustaw_statek(lg, *a, POZIOM)
                        redo(1)
                        n -= 1
                    else:
                        prompter("Wybierz inne położenie", 1)
                        pygame.time.wait(300)
            # PPM
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                x = pygame.mouse.get_pos()
                a = get_tile(*x, 1)
                if type(a) == tuple:
                    if check_statek(*a, lg, PION) is True:
                        ustaw_statek(lg, *a, PION)
                        redo(1)
                        n -= 1
                    else:
                        prompter("Wybierz inne położenie", 1)
                        pygame.time.wait(300)
        if n == 0:
            return True


def ustaw_statek(ln, x, y, kier):
    '''
    Funkcja ustawiająca statek w danym położeniu i kierunku.
    :param ln: długość statku 1 - 4
    :param x: indeks wiersza planszy 0 - 9
    :param y: indeks kolumny planszy 0 - 9
    :param kier: kierunek ustawienia statku:
    '''
    la = []
    if kier == POZIOM:
        for i in range(ln):
            la.append(x + i)
        for z in la:
            p1[z][y][0] = 1
            p1[z][y][1] = 1
    elif kier == PION:
        for i in range(ln):
            la.append(y + i)
        for z in la:
            p1[x][z][0] = 1
            p1[x][z][1] = 1


def check_statek(x, y, ln, kier):
    '''
    Funkcja testująca, czy w danym położeniu x,y statek może być ustawiony.
    '''
    s = 0
    if kier == POZIOM:
        for i in range(y + 1, y - 2, -1):
            for j in range(x - 1, x + ln + 1):
                try:
                    if i < 0 or j < 0:
                        continue
                    if p1[j][i][1] > 0:
                        s += p1[j][i][1]

                except IndexError:
                    if ln > 1 and x + 1 > 10 - (ln - 1):
                        s += 1
                    else:
                        pass
    elif kier == PION:
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + ln + 1):
                try:
                    if i < 0 or j < 0:
                        continue
                    if p1[i][j][1] > 0:
                        s += p1[i][j][1]
                except IndexError:
                    if ln > 1 and y + 1 > 10 - (ln - 1):
                        s += 1
                    else:
                        pass
    s = bool(not s)
    return s


def faza_ustawienia_statkow():
    '''
    Funkcja wywołująca etap gry w którym gracz ustawia statki na swojej planszy.
    '''
    # Przycisk resetu
    prompter("Reset", 1, x=570, y=300, lx=65, ly=50, font=0)
    running = True
    while running:
        for i in range(1, 5):
            if statek(i) == 0:
                break
        else:
            for x in range(10):
                for y in range(10):
                    p1[x][y][0] = 1
            return False
        return True


def ekran_poczatkowy():
    '''
    Funkcja wyswietlająca ekran początkowy gry.
    '''
    ekran.fill(SZARY_TLO)
    prompter('Start', 0, x=450, y=350, lx=300, ly=100)
    prompter("Witamy w grze w statki", 0)
    ekran.blit(LOGO, LOGO_COORDS)
    redo(0)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                xa, ya = pygame.mouse.get_pos()
                if 450 < xa < 750 and 350 < ya < 450:
                    running = False


def ekran_koncowy(value):
    '''
    Funkcja wyswietlająca ekran koncowy po zakonczeniu rozgrywki
    :param value: 0: 'Wygrana' 1: 'Przegrana'
    :return:
    '''
    pygame.mixer.music.stop()
    ekran.fill(SZARY_TLO)
    ekran.blit(LOGO, (472, 75))
    prompter('Wcisnij dowolny przycisk, aby opuścić grę', 0)
    prompt = 'Wygrana!' if value == WON else 'Przegrana!'
    text = FONT1.render(prompt, True, (0, 0, 0))
    textrect = text.get_rect()
    textrect.center = 600, 450
    ekran.blit(text, textrect)
    redo(0)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                pygame.quit()
                sys.exit()

def main():
    # zmienna win - zmniejszana, gdy statek zostanie trafiony
    win = 20
    # Wyświetlenie ekranu początkowego gry, oczekiwanie na wciśnięcie 'Start'
    ekran_poczatkowy()
    # Oczyszczenie ekranu
    ekran.fill(SZARY_TLO)
    #ekran.blit(MUSIC_ON, MUSIC_BUTTON_COORDS)

    # Ustawianie Statków na planszy
    statki = True
    while statki:
        statki = faza_ustawienia_statkow()

    #Oczyszczenie ekranu
    ekran.fill(SZARY_TLO)
    redo(1)

    # Połączenie z graczem
    prompter("Oczekiwanie na połączenie z drugim graczem", 1)

    listensocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listensocket.bind((socket.gethostname(), 8000))
    listensocket.listen(5)
    (s, address) = listensocket.accept()





    # Pętla rozgrywki
    while True:

        # Strzał w przeciwnika
        twoja_kolej = True
        while twoja_kolej:
            prompter('Twoja kolej na oddanie strzału', 1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x = pygame.mouse.get_pos()
                    b = get_tile(*x, 0)
                    if type(b) == tuple:
                        print(b)
                        mess = (str(b[0])+str(b[1])+str(win))
                        s.send(str(mess).encode())
                        pygame.event.pump()
                        mess = s.recv(MAX_MSG_SIZE)
                        z = mess.decode()
                        z = [int(i) for i in z]
                        p2[b[0]][b[1]] = [z[0], z[1], z[2]]
                        if z[3] == 1:
                            ekran_koncowy(1)
                        if p2[b[0]][b[1]][1] == 1 and p2[b[0]][b[1]][2] != 1:
                            prompter("Trafiony", 1)
                        elif p2[b[0]][b[1]][1] == 0 and p2[b[0]][b[1]][2] != 1:
                            prompter("Pudło", 1)
                        else:
                            prompter("Tu już było strzelane", 1)
                            pygame.time.wait(300)
                        rysowanie_planszy(1)
                        if p2[b[0]][b[1]][1] == 0 and p2[b[0]][b[1]][2] != 1:
                            twoja_kolej = False
                        pygame.time.wait(100)
            redo(1)

        # Ruch Przeciwnika
        kolej_przec = True
        while kolej_przec:
            prompter("Oczekiwanie na ruch przeciwnika", 1)
            pygame.event.pump()
            prompter("Strzał przeciwnika", 0)
            message = s.recv(MAX_MSG_SIZE)
            if message != '':
                z = message.decode()
                z = [int(z[0]), int(z[1]), int(z[2])] if len(z) == 3 else [int(z[0]), int(z[1]),
                                                                           int(z[2]) + int(z[3])]
                c = 0
                if p1[z[0]][z[1]][1] == 1 and p1[z[0]][z[1]][2] != 1:
                    win -= 1
                if win == 0:
                    c = 1
                message = (str(p1[z[0]][z[1]][0]) + str(p1[z[0]][z[1]][1]) + str(p1[z[0]][z[1]][2]) + str(c))
                s.send(str(message).encode())
                pygame.time.wait(100)
                if win == 0:
                    ekran_koncowy(0)
                if p1[z[0]][z[1]][1] == 0 and p1[z[0]][z[1]][2] != 1:
                    kolej_przec = False
                p1[z[0]][z[1]][2] = 1


if __name__ == "__main__":
    main()
