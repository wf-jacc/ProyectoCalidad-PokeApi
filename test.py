import unittest
from unittest import mock
import mysql.connector
from database import *


class TestDatabase(unittest.TestCase):
    @mock.patch('mysql.connector.connect')
    def test_connect(self, mock_connect):
        host = 'localhost'
        user = 'root'
        password = 'password'
        database = 'test_db'

        connect(host, user, password, database)

        mock_connect.assert_called_once_with(
            host=host, user=user, password=password, database=database
        )

    @mock.patch('mysql.connector.connect')
    def test_create_pokemon_table(self, mock_connect):
        connection_mock = mock_connect.return_value
        cursor_mock = connection_mock.cursor.return_value

        create_pokemon_table(connection_mock)

        cursor_mock.execute.assert_called_once()
        connection_mock.commit.assert_called_once()

    @mock.patch('mysql.connector.connect')
    def test_save_pokemon_to_team(self, mock_connect):
        connection_mock = mock_connect.return_value
        cursor_mock = connection_mock.cursor.return_value

        team_name = 'Team Rocket'
        pokemon_data = {"number": "001", "name": "Bulbasaur"}

        save_pokemon_to_team(connection_mock, team_name, pokemon_data)

        cursor_mock.execute.assert_called_once_with(
            mock.ANY, ("001", team_name, "Bulbasaur")
        )
        connection_mock.commit.assert_called_once()

    @mock.patch('mysql.connector.connect')
    def test_get_team_pokemon(self, mock_connect):
        connection_mock = mock_connect.return_value
        cursor_mock = connection_mock.cursor.return_value

        team_name = 'Team Rocket'
        expected_result = [
            {"pokemon_number": "001", "pokemon_name": "Bulbasaur"},
            {"pokemon_number": "002", "pokemon_name": "Ivysaur"},
        ]
        cursor_mock.fetchall.return_value = expected_result

        result = get_team_pokemon(connection_mock, team_name)

        cursor_mock.execute.assert_called_once_with(
            mock.ANY, (team_name,)
        )
        cursor_mock.fetchall.assert_called_once()
        self.assertEqual(result, expected_result)

    @mock.patch('mysql.connector.connect')
    def test_remove_pokemon_from_team(self, mock_connect):
        connection_mock = mock_connect.return_value
        cursor_mock = connection_mock.cursor.return_value

        team_name = 'Team Rocket'
        pokemon_id = '001'

        remove_pokemon_from_team(connection_mock, team_name, pokemon_id)

        cursor_mock.execute.assert_called_once_with(
            mock.ANY, (team_name, pokemon_id, pokemon_id)
        )
        connection_mock.commit.assert_called_once()
        cursor_mock.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
