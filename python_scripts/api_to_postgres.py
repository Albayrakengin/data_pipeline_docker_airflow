import requests
import psycopg2

def fetch_data_from_api():
    response = requests.get('https://fakestoreapi.com/products')
    data = response.json()
    return data

def execute_sql_from_file(filename, params=None):
    try:
        with open(filename, 'r') as file:
            query = file.read()

        conn = psycopg2.connect(
            dbname='airflow',
            user='airflow',
            password='airflow',
            host='postgres',
            port='5432'
        )
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()

        print("SQL executed successfully.")
    except (psycopg2.Error, FileNotFoundError) as e:
        print("Error:", e)

if __name__ == "__main__":
    data = fetch_data_from_api()
    
    execute_sql_from_file('/opt/airflow/sql_queries/create_main_table.sql')

    for item in data:
        execute_sql_from_file('/opt/airflow/sql_queries/insert_main_table.sql', (
            item['id'],
            item['title'],
            item['price'],
            item['description'],
            item['category'],
            item['image'],
            item['rating']['rate'],
            item['rating']['count']
        ))