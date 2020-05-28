"""
Moduł zawierający testy modułu battleship.py
"""
import unittest

import battleship


class TileTest(unittest.TestCase):
    """
    Klasa dokonująca testów klasy Tile.
    """

    def setUp(self):
        self.tile = battleship.Tile()

    def test_reset_tile_result(self):
        self.tile.reset_tile()
        result = self.tile.is_revealed and self.tile.is_ship
        self.assertFalse(result)

    def test_show_tile_result(self):
        self.tile.show_tile()
        self.assertTrue(self.tile.is_revealed)

    def test_tile_info_return_after_reset(self):
        self.tile.reset_tile()
        test_data = self.tile.tile_info()
        self.assertEqual(test_data, '000')

    def test_tile_info_return_after_show(self):
        self.tile.show_tile()
        test_data = self.tile.tile_info()
        self.assertEqual(test_data, '100')

    def test_update_tile_result(self):
        test_message = b'1111'
        self.tile.update_tile(test_message)
        result = (self.tile.is_revealed and self.tile.is_ship and self.tile.is_shot)
        self.assertTrue(result)

    def test_update_tile_result_type(self):
        test_message = b'0101'
        test_result = self.tile.update_tile(test_message)
        self.assertIsInstance(test_result, list)


class GameGridTest(unittest.TestCase):
    """
    Klasa dokonująca testów klasy GameGrid.
    """
    def setUp(self):
        self.grid = battleship.GameGrid(20, 5)

    def test_check_ship_of_lenght_1_correct(self):
        x_test = 3
        y_test = 5
        ship_length_test = 1
        directory_test = 1
        result = self.grid.check_ship(x_test, y_test, ship_length_test, directory_test)
        self.assertTrue(result)

    def test_check_ship_of_length_3_wrong(self):
        x_test = 9
        y_test = 8
        ship_length_test = 3
        directory_test = 0
        result = self.grid.check_ship(x_test, y_test, ship_length_test, directory_test)
        self.assertFalse(result)

    def test_get_tile_returns_tuple(self):
        x_test = 60
        y_test = 40
        result = self.grid.get_tile(x_test, y_test)
        self.assertIsInstance(result, tuple)

    def test_get_tile_returns_false(self):
        x_test = 600
        y_test = 300
        result = self.grid.get_tile(x_test, y_test)
        self.assertFalse(result)


class MessageTest(unittest.TestCase):
    """
    Klasa dokonująca testów funkcji modułu.
    """
    def setUp(self):
        self.message_1 = b'1111'
        self.message_2 = b'011'

    def test_enemy_shot_decoder_return_lenght(self):
        result = battleship.enemy_shot_decoder(self.message_1)
        self.assertEqual(len(result), 3)

    def test_enemy_shot_decoder_returns_true(self):
        result = battleship.enemy_shot_decoder(self.message_2)
        self.assertTrue(result[-1])


if __name__ == '__main__':
    unittest.main()
