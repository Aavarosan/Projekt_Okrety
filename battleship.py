"""
Moduł zawiera klasy i funkcje do obsługi gry Okręty.
"""

import sys
import pygame

import my_constants


class Tile:
    """
    Klasa magazynująca informacje o danym kafelku.
    """
    def __init__(self):
        self.is_revealed = False
        self.is_ship = False
        self.is_shot = False

    def reset_tile(self):
        """
        Metoda resetująca kafelek podczas ustawiania statków.
        """
        self.is_revealed = False
        self.is_ship = False

    def show_tile(self):
        """
        Metoda sprawiająca, że kafelek jest odkryty.
        """
        self.is_revealed = True

    def tile_info(self):
        """
        Metoda zwracająca informacje o danym kafelku jako tekst.
        """
        return f"{int(self.is_revealed)}{int(self.is_ship)}{int(self.is_shot)}"

    def update_tile(self, message):
        """
        Metoda aktualizująca wartości kafelka.
        """

        info = message.decode()
        info = [bool(int(i)) for i in info]
        self.is_revealed = info[0]
        self.is_ship = info[1]
        self.is_shot = info[2]
        return info


class GameGrid:
    """
    Klasa operująca na danej planszy gry.
    """
    def __init__(self, x_init, y_init):
        self.game_grid = [[Tile() for _ in range(my_constants.GRID_DIMENSION_SIZE)]
                          for _ in range(my_constants.GRID_DIMENSION_SIZE)]
        self.x_init = x_init
        self.y_init = y_init
        self.win_number = my_constants.SHIP_NUMBER

    def reset_grid(self):
        """
        Metoda służąca do zresetowania położenia statków.
        """
        for row in self.game_grid:
            for tile in row:
                tile.reset_tile()

    def print_grid(self, screen):
        """
        Metoda odświeżająca aktualny stan danej planszy na ekranie.
        """
        for i in range(my_constants.GRID_DIMENSION_SIZE):
            for j in range(my_constants.GRID_DIMENSION_SIZE):

                if not self.game_grid[j][i].is_revealed:
                    temp_color = my_constants.TEXT_COLOR
                elif not self.game_grid[j][i].is_ship:
                    temp_color = my_constants.SEA_COLOR
                else:
                    temp_color = my_constants.SHIP_COLOR
                pygame.draw.rect(screen.my_screen, temp_color,
                                 (self.x_init + j * (my_constants.TILE_SPACE +
                                                     my_constants.TILE_SIZE),
                                  self.y_init + i * (my_constants.TILE_SPACE +
                                                     my_constants.TILE_SIZE),
                                  my_constants.TILE_SIZE,
                                  my_constants.TILE_SIZE))
                if (self.game_grid[j][i].is_shot
                        and self.x_init < my_constants.RIGHT_START_COORDS[0]):
                    text = screen.font.render(my_constants.ALLY_SHOT, True, my_constants.TEXT_COLOR)
                    text_r = text.get_rect()
                    text_r.center = (self.x_init + j * (my_constants.TILE_SPACE +
                                                        my_constants.TILE_SIZE) +
                                     my_constants.TILE_SIZE // 2,
                                     self.y_init + i * (my_constants.TILE_SPACE +
                                                        my_constants.TILE_SIZE) +
                                     my_constants.TILE_SIZE // 2)
                    screen.my_screen.blit(text, text_r)

    def check_ship(self, x_ship: int, y_ship: int, len_ship: int, directory: int) -> bool:
        """
        Metoda testująca, czy w danym położeniu statek może być ustawiony.
        """
        ship_test = 0
        if directory == my_constants.POZIOM:
            coordinate_i, coordinate_j = y_ship, x_ship
        else:
            coordinate_i, coordinate_j = x_ship, y_ship
        for i in range(coordinate_i + 1, coordinate_i - 2, -1):
            for j in range(coordinate_j - 1, coordinate_j + len_ship + 1):
                try:
                    if i < 0 or j < 0:
                        continue
                    if directory == my_constants.POZIOM:
                        ship_test += self.game_grid[j][i].is_ship
                    else:
                        ship_test += self.game_grid[i][j].is_ship

                except IndexError:
                    if (len_ship > 1
                            and coordinate_j + 1 >
                            my_constants.GRID_DIMENSION_SIZE - (len_ship - 1)):
                        ship_test += 1

        return bool(not ship_test)

    def place_ship(self, x_ship: int, y_ship: int, len_ship: int, directory: int):
        """
        Metoda ustawiająca statek w danym położeniu i kierunku.
        """
        tiles_list = []
        if directory == my_constants.POZIOM:
            for i in range(len_ship):
                tiles_list.append(x_ship + i)
            for i in tiles_list:
                self.game_grid[i][y_ship].is_revealed = True
                self.game_grid[i][y_ship].is_ship = True
        elif directory == my_constants.PION:
            for i in range(len_ship):
                tiles_list.append(y_ship + i)
            for i in tiles_list:
                self.game_grid[x_ship][i].is_revealed = True
                self.game_grid[x_ship][i].is_ship = True

    def get_tile(self, x_location: int, y_location: int):
        """
        Metoda zwracająca indeks naciśniętego kafelka.
        """
        for i in range(my_constants.GRID_DIMENSION_SIZE):
            y_init = self.y_init + i * (my_constants.TILE_SPACE + my_constants.TILE_SIZE)
            y_final = self.y_init + (i + 1) * (my_constants.TILE_SPACE + my_constants.TILE_SIZE)
            for j in range(my_constants.GRID_DIMENSION_SIZE):
                x_init = self.x_init + j * my_constants.TILE_SPACE + j * my_constants.TILE_SIZE
                x_final = self.x_init + (j + 1) * (my_constants.TILE_SPACE + my_constants.TILE_SIZE)
                if x_init < x_location < x_final and y_init < y_location < y_final:
                    coords = j, i
                    return coords
        return False

    def reset_check(self, point_location: tuple, screen) -> bool:
        """
        Metoda sprawdzająca, czy naciśnięty został przycisk restartu planszy.
        """
        x_start, y_start = my_constants.RESET_COORDS[:2]
        x_end = x_start + my_constants.RESET_COORDS[2]
        y_end = x_start + my_constants.RESET_COORDS[3]
        if x_start < point_location[0] < x_end and y_start < point_location[1] < y_end:
            self.reset_grid()
            self.print_grid(screen)
            pygame.display.flip()
            return True
        return False

    def check_message(self, my_screen, x_coord, y_coord):
        """
        Metoda informująca o rezultacie strzału gracza.
        """
        if (self.game_grid[x_coord][y_coord].is_ship
                and not self.game_grid[x_coord][y_coord].is_shot):
            my_screen.prompter("Trafiony, strzelaj ponownie", my_constants.BANNER_COORDS)
        elif (not self.game_grid[x_coord][y_coord].is_ship
              and not self.game_grid[x_coord][y_coord].is_shot):
            my_screen.prompter("Pudło", my_constants.BANNER_COORDS)
        else:
            my_screen.prompter("Tu już było strzelane", my_constants.BANNER_COORDS)
        pygame.display.flip()
        pygame.time.wait(100)


class MyScreen:
    """
    Klasa zarządzająca oknem gry.
    """
    def __init__(self, player_number: str):
        self.my_screen = pygame.display.set_mode(my_constants.SCREEN_SIZE)
        pygame.display.set_caption(f"BATTLESHIP GAME : {player_number}")
        pygame.display.set_icon(pygame.image.load(my_constants.ICON))
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        self.font = pygame.font.Font('freesansbold.ttf', my_constants.FONT_SIZE)

    def prompter(self, prompt: str, coords: tuple, background_flag=0):
        """
        Metoda wyswietlajaca prostokąt z tekstem w nim wyśrodkowanym.
        """
        text = self.font.render(prompt, True, my_constants.TEXT_COLOR)
        textrect = text.get_rect()
        textrect.center = (int(coords[0] + coords[2] / 2), int(coords[1] + coords[3] / 2))
        if not background_flag:
            pygame.draw.rect(self.my_screen, my_constants.BUTTONS_COLOR, coords)
        self.my_screen.blit(text, textrect)
        pygame.display.flip()

    def hello_screen(self):
        """
        Metoda wyswietlająca ekran początkowy gry.
        """
        self.my_screen.fill(my_constants.BACKGROUND_COLOR)
        self.my_screen.blit(pygame.image.load(my_constants.LOGO), my_constants.LOGO_COORDS)
        self.prompter("Witamy w grze w statki", my_constants.BANNER_COORDS)
        self.prompter("Start", my_constants.START_COORDS)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    point_location = pygame.mouse.get_pos()
                    x_start, y_start = my_constants.START_COORDS[:2]
                    x_end = x_start + my_constants.START_COORDS[2]
                    y_end = x_start + my_constants.START_COORDS[2]
                    if (x_start < point_location[0] < x_end
                            and y_start < point_location[1] < y_end):
                        running = False
                        self.my_screen.fill(my_constants.BACKGROUND_COLOR)

    def final_screen(self, value: int):
        """
        Metoda wyswietlająca ekran koncowy po zakonczeniu rozgrywki.
        """
        self.my_screen.fill(my_constants.BACKGROUND_COLOR)
        self.my_screen.blit(pygame.image.load(my_constants.LOGO), my_constants.LOGO_COORDS)
        self.prompter('Wcisnij dowolny przycisk, aby opuścić grę', my_constants.BANNER_COORDS)
        prompt = 'Wygrana!' if value == my_constants.WON else 'Przegrana!'
        self.prompter(prompt, my_constants.END_COORDS, background_flag=my_constants.NO_BACKGROUND)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type in (pygame.QUIT, pygame.KEYDOWN):
                    pygame.quit()
                    sys.exit()

    def placing_ships(self, grid: GameGrid) -> bool:
        """
        Funkcja wywołująca etap gry w którym gracz ustawia statki na swojej planszy.
        """
        # Przycisk resetu
        self.prompter("Reset", my_constants.RESET_COORDS)
        running = True
        while running:
            for ship_number in range(1, my_constants.MAX_SHIP_LENGTH + 1):
                if not ship(grid, self, ship_number):
                    break
            else:
                for row in grid.game_grid:
                    for tile in row:
                        tile.show_tile()
                return False
            return True

    def clean_screen(self, ally_grid: GameGrid, enemy_grid: GameGrid):
        """
        Metoda odświeżająca widok ekranu.
        """
        ally_grid.print_grid(self)
        enemy_grid.print_grid(self)
        pygame.display.flip()


def ship(grid: GameGrid, screen: MyScreen, ship_length: int):
    """
    Metoda obslugująca ustawianie statków.
    """
    ship_number = my_constants.MAX_SHIP_LENGTH - ship_length + 1
    while True:
        screen.prompter(f"Ustaw statek: Dlugosc: {ship_length}, pozostało: {ship_number} "
                        f"(LPM poziomo, PPM pionowo)",
                        my_constants.BANNER_COORDS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Lewy Przycisk Myszy
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                point_location = pygame.mouse.get_pos()

                # Sprawdzenie przycisku resetu
                if grid.reset_check(point_location, screen):
                    return False
                tile_coords = grid.get_tile(*point_location)
                if isinstance(tile_coords, tuple):
                    ship_number = settle_ship(grid, screen, tile_coords,
                                              (ship_number, ship_length), my_constants.POZIOM)
            # Prawy Przycisk Myszy
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                point_location = pygame.mouse.get_pos()
                tile_coords = grid.get_tile(*point_location)
                if isinstance(tile_coords, tuple):
                    ship_number = settle_ship(grid, screen, tile_coords,
                                              (ship_number, ship_length), my_constants.PION)
        if not ship_number:
            return True


def settle_ship(grid: GameGrid, screen: MyScreen,
                tile_coords: tuple, ship_info: tuple, direction: int):
    """
    Funkcja obsługująca ustawienie pojedynczego statku.
    """
    success = 1
    if grid.check_ship(*tile_coords, ship_info[1], direction):
        grid.place_ship(*tile_coords, ship_info[1], direction)
        grid.print_grid(screen)
        pygame.display.flip()
    else:
        screen.prompter("Wybierz inne położenie", my_constants.BANNER_COORDS)
        pygame.time.wait(300)
        success = 0
    return ship_info[0] - success


def enemy_turn(screen: MyScreen, my_socket,
               ally_grid: GameGrid, enemy_grid: GameGrid):
    """
    Metoda realizująca etap gdy będący 'turą przeciwnika'.
    """
    enemy = True
    while enemy:
        screen.prompter("Oczekiwanie na ruch przeciwnika", my_constants.BANNER_COORDS)
        pygame.event.pump()
        message = receive_data(my_socket)
        if message:
            info = enemy_shot_decoder(message)

            if (ally_grid.game_grid[info[0]][info[1]].is_ship
                    and not ally_grid.game_grid[info[0]][info[1]].is_shot):
                ally_grid.win_number -= 1
            print(ally_grid.win_number)
            win_info = 1 if not ally_grid.win_number else 0
            message = my_response_encoder(ally_grid, *info[:2], win_info)
            send_data(my_socket, message)
            pygame.time.wait(100)
            if not ally_grid.win_number:
                screen.final_screen(my_constants.LOST)
            if (not ally_grid.game_grid[info[0]][info[1]].is_ship
                    and not ally_grid.game_grid[info[0]][info[1]].is_shot):
                enemy = False
            ally_grid.game_grid[info[0]][info[1]].is_shot = True
            ally_grid.print_grid(screen)

    enemy_grid.print_grid(screen)


def my_turn(screen: MyScreen, my_socket, ally_grid: GameGrid, enemy_grid: GameGrid):
    """
    Metoda realizująca etap gdy będący 'turą gracza'.
    """
    your_turn = True
    while your_turn:
        screen.prompter('Twoja kolej na oddanie strzału', my_constants.BANNER_COORDS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pointer_position = pygame.mouse.get_pos()
                coords = enemy_grid.get_tile(*pointer_position)
                if isinstance(coords, tuple):
                    message = my_shot_encode(*coords, ally_grid.win_number)
                    send_data(my_socket, message)
                    message = receive_data(my_socket)
                    message_info = enemy_grid.game_grid[coords[0]][coords[1]].update_tile(message)
                    if message_info[3]:
                        screen.final_screen(my_constants.WON)
                    enemy_grid.check_message(screen, *coords)
                    enemy_grid.print_grid(screen)
                    if (not enemy_grid.game_grid[coords[0]][coords[1]].is_ship
                            and not enemy_grid.game_grid[coords[0]][coords[1]].is_shot):
                        your_turn = False
    ally_grid.print_grid(screen)


def send_data(local_socket, message: str):
    """
    Funkcja wysyłająca dane poprzez socket.
    """
    local_socket.send(str(message).encode())


def receive_data(local_socket):
    """
    Funkcja odbierająca dane z socketa.
    """
    message = local_socket.recv(my_constants.MAX_MESSAGE_SIZE)
    return message


def enemy_shot_decoder(message: bytes) -> list:
    """
    Funkcja dekodująca wiadomość dotyczącą strzału przeciwnika.
    """
    info = message.decode()
    if len(info) == 3:
        info = [int(info[0]), int(info[1]), int(info[2])]
    else:
        info = [int(info[0]), int(info[1]), int(info[2]) + int(info[3])]
    return info


def my_response_encoder(grid: GameGrid, x_coord: int,
                        y_coord: int, win_message: int):
    """
    Funkcja kodująca informacje o kafelku, w który strzelił przeciwnik.
    """
    message = f"{grid.game_grid[x_coord][y_coord].tile_info()}{win_message}"
    return message


def my_shot_encode(x_tile: int, y_tile: int, win_info: int) -> str:
    """
    Funkcja kodująca wiadomość na temat strzału gracza.
    """
    message = f"{x_tile}{y_tile}{win_info}"
    return message


def initialise_game(screen: MyScreen, ally_grid, enemy_grid):
    """
    Funkcja wyświetlająca ekran początkowy i uruchamiająca pętle ustawiania statków.
    """
    screen.hello_screen()
    screen.clean_screen(ally_grid, enemy_grid)
    ships = True
    while ships:
        ships = screen.placing_ships(ally_grid)
    screen.clean_screen(ally_grid, enemy_grid)
    screen.prompter("Oczekiwanie na połączenie z drugim graczem", my_constants.BANNER_COORDS)
