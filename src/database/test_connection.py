from src.config.database import get_connection


def test_connection():
    connection = None

    try:
        connection = get_connection()

        cursor = connection.cursor()
        cursor.execute("SELECT current_database(), current_user;")

        database, user = cursor.fetchone()

        print("Database connection successful!")
        print(f"Database: {database}")
        print(f"User: {user}")

        cursor.close()

    except Exception as e:
        print("Database connection failed!")
        print(e)

    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    test_connection()