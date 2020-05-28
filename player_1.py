"""
Moduł zawiera funkcję rozgrywki dla gracza 1.
"""
import socket

import pygame

import battleship
import my_constants


def main():
    """
    Funcja main, wywoływana, gdy plik nie jest użyty jako moduł, tylko plik wykonywalny.
    """

    # Inicjalizacja pygame i utworzenie obiektów niezbędnych klas
    pygame.init()
    my_screen = battleship.MyScreen("GRACZ 1")
    enemy_grid = battleship.GameGrid(*my_constants.RIGHT_START_COORDS)
    your_grid = battleship.GameGrid(*my_constants.LEFT_START_COORDS)
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    battleship.initialise_game(my_screen, your_grid, enemy_grid)

    # Połączenie z graczem
    my_socket.bind((socket.gethostname(), my_constants.PORT))
    my_socket.listen(1)
    (enemy_socket, _) = my_socket.accept()

    while True:
        battleship.my_turn(my_screen, enemy_socket, your_grid, enemy_grid)
        battleship.enemy_turn(my_screen, enemy_socket, your_grid, enemy_grid)


if __name__ == "__main__":
    main()
