"""
Moduł zawierający testy modułu battleship.py
"""
import unittest
import random

import battleship


class TileTest(unittest.TestCase):
    """
    Klasa dokonująca testów klasy Tile.

    Nazwy metod testowych : test_[nazwa metody testowanej] z ew. numerem testu metody.
    """

    def setUp(self):
        self.tile = battleship.Tile()

    def test_reset_tile(self):
        """
        Test poprawnego ustawiania wartości.
        """
        self.tile.reset_tile()
        result = self.tile.is_revealed and self.tile.is_ship
        self.assertFalse(result)

    def test_show_tile(self):
        """
        Test poprawnego ustawiania wartości.
        """
        self.tile.show_tile()
        self.assertTrue(self.tile.is_revealed)

    def test_tile_info_1(self):
        """
        Test zwracanej wartości.
        """
        self.tile.reset_tile()
        test_data = self.tile.tile_info()
        self.assertEqual(test_data, '000')

    def test_tile_info_2(self):
        """
        Test zwracanej wartości.
        """
        self.tile.show_tile()
        test_data = self.tile.tile_info()
        self.assertEqual(test_data, '100')

    def test_update_tile_1(self):
        """
        Test poprawnego odczytywania danych o kafelku.
        """
        test_message = b'1111'
        self.tile.update_tile(test_message)
        result = (self.tile.is_revealed and self.tile.is_ship and self.tile.is_shot)
        self.assertTrue(result)

    def test_update_tile_2(self):
        """
        Test zwracanego typu.
        """
        test_message = b'0101'
        test_result = self.tile.update_tile(test_message)
        self.assertIsInstance(test_result, list)


class TestGameGrid(unittest.TestCase):
    """
    Klasa dokonująca testów klasy GameGrid.
    """
    def setUp(self):
        self.grid = battleship.GameGrid(20, 5)

    def test_check_ship_1(self):
        """
        Test ustawienia statku "Jednomasztowca".
        """
        x_test = random.randint(0, 9)
        y_test = random.randint(0, 9)
        ship_length_test = 1
        directory_test = random.randint(0, 1)
        # Oczekiwany : True
        result = self.grid.check_ship(x_test, y_test, ship_length_test, directory_test)
        self.assertTrue(result)

    def test_check_ship_2(self):
        """
        Test ustawienia statku "Trójmasztowca".
        """
        x_test = random.randint(0, 9)
        y_test = random.randint(0, 9)
        ship_length_test = 3
        directory_test = 0  # PION
        result = self.grid.check_ship(x_test, y_test, ship_length_test, directory_test)
        # Oczekiwany: True, jeśli x_test < 8, w przeciwnym wypadku False
        if y_test >= 8:
            self.assertFalse(result)
        else:
            self.assertTrue(result)

    def test_get_tile_1(self):
        """
        Test poprawnego przetwarzania danych wejściowych.
        """
        x_test = random.randint(0, 1200)
        y_test = random.randint(0, 600)
        result = self.grid.get_tile(x_test, y_test)
        self.assertIsInstance(result, (tuple, bool))

    def test_get_tile_2(self):
        """
        Test poprawnego zwracania wartości.

        Test sprawdza zarówno ramy wartości, gdy został naciśnięty przycisk, jak i zwracania False,
        gdy tak się nie stało.
        """
        x_test = random.randint(0, 1200)
        y_test = random.randint(0, 600)
        result = self.grid.get_tile(x_test, y_test)
        if isinstance(result, tuple):
            self.assertLessEqual(result[0], 9)
            self.assertGreaterEqual(result[1], 0)
        else:
            self.assertFalse(result)


class VariousTests(unittest.TestCase):
    """
    Klasa dokonująca testów funkcji modułu.
    """
    def setUp(self):
        self.message_1 = b'1111'
        self.message_2 = b'011'

    def test_enemy_shot_decoder_1(self):
        """
        Test poprawnego przetwarzania wiadomości typu bytes.
        """
        message = random.choice([self.message_1, self.message_2])
        result = battleship.enemy_shot_decoder(message)
        self.assertEqual(len(result), 3)

    def test_enemy_shot_decoder_2(self):
        """
        Test wykrywania wartości "win_info", czyli informacji o wygranej.
        """
        message = random.choice([self.message_1, self.message_2])
        result = battleship.enemy_shot_decoder(message)
        self.assertTrue(result[-1])


if __name__ == '__main__':
    unittest.main()
