"""
Moduł zawiera funkcję rozgrywki dla gracza 2.
"""

import socket
import pygame
import my_constants
import battleship


def main():
    """
    Funcja main, wywoływana, gdy plik nie jest użyty jako moduł, tylko plik wykonywalny.
    """
    # Inicjalizacja pygame i utworzenie obiektów niezbędnych klas
    pygame.init()
    my_screen = battleship.MyScreen("GRACZ 2")
    enemy_grid = battleship.GameGrid(*my_constants.RIGHT_START_COORDS)
    your_grid = battleship.GameGrid(*my_constants.LEFT_START_COORDS)

    # Wyświetlenie ekranu początkowego gry, oczekiwanie na wciśnięcie 'Start'
    my_screen.hello_screen()

    # Oczyszczenie ekranu
    my_screen.clean_screen(your_grid, enemy_grid)

    # Ustawianie Statków na planszy
    ships = True
    while ships:
        ships = my_screen.placing_ships(your_grid)

    # Oczyszczenie ekranu
    my_screen.clean_screen(your_grid, enemy_grid)

    # Połączenie z graczem
    my_screen.prompter("Oczekiwanie na połączenie z drugim graczem", my_constants.BANNER_COORDS)
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        pygame.event.pump()
        try:
            my_socket.connect((socket.gethostname(), my_constants.PORT))
        except ConnectionRefusedError:
            pass
        else:
            break

    while True:
        battleship.enemy_turn(my_screen, my_socket, your_grid, enemy_grid)
        battleship.my_turn(my_screen, my_socket, your_grid, enemy_grid)
    # Pętla rozgrywki


if __name__ == "__main__":
    main()
