import unittest
import psycopg2


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        # Подключение к базе данных PostgreSQL
        self.db_connection = psycopg2.connect(
            user="postgres",
            password="1337",
            host="localhost",
            port=5432,
            database="postgres"
        )

    def tearDown(self):
        # Закрываем соединение с базой данных после каждого теста
        self.db_connection.close()

    def test_database_connection(self):
        # Проверяем, что соединение с базой данных установлено
        self.assertIsNotNone(self.db_connection)


if __name__ == '__main__':
    unittest.main()
