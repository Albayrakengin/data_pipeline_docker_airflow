import requests
import psycopg2

def fetch_data_from_api():
    response = requests.get('https://fakestoreapi.com/products')
    data = response.json()
    return data

def create_table_if_not_exists():
    try:
        conn = psycopg2.connect(
            dbname='airflow',
            user='airflow',
            password='airflow',
            host='postgres',
            port='5432'
        )
        cursor = conn.cursor()

        create_table_query = """
            CREATE TABLE IF NOT EXISTS my_table (
                product_id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                price NUMERIC NOT NULL,
                description TEXT,
                category VARCHAR(255),
                image TEXT,
                rating_rate NUMERIC,
                rating_count INTEGER
            )
        """
        cursor.execute(create_table_query)

        conn.commit()
        cursor.close()
        conn.close()

        print("Table created successfully.")
    except psycopg2.Error as e:
        print("Error:", e)

def insert_data_into_postgres(data):
    try:
        conn = psycopg2.connect(
            dbname='airflow',
            user='airflow',
            password='airflow',
            host='postgres',
            port='5432'
        )
        cursor = conn.cursor()

        for item in data:
            product_id = item['id']
            title = item['title']
            price = item['price']
            description = item['description']
            category = item['category']
            image = item['image']
            rating_rate = item['rating']['rate']
            rating_count = item['rating']['count']

            insert_query = """
                INSERT INTO my_table (product_id, title, price, description, category, image, rating_rate, rating_count)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (product_id) DO NOTHING
            """
            cursor.execute(insert_query, (product_id, title, price, description, category, image, rating_rate, rating_count))

        conn.commit()
        cursor.close()
        conn.close()

        print("Data inserted successfully.")
    except psycopg2.Error as e:
        print("Error:", e)


if __name__ == "__main__":
    data = fetch_data_from_api()
    create_table_if_not_exists()
    insert_data_into_postgres(data)