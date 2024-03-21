import pyodbc
import json
import os
from decouple import config

def db_connect():
    """
    Connects to a SQL Server database and inserts data from a JSON file into the 'categorias' table.

    Args:
        None

    Returns:
        pyodbc.Connection: The connection object to the SQL Server database.

    Raises:
        None

    Examples:
        None
    """


    SERVER = config('SERVER')
    DATABASE = config('DATABASE')
    UID = config('UID')
    PWD = config('PWD')
    return pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};'
        f'Server={SERVER};'
        f'Database={DATABASE};'
        f'UID={UID};'
        f'PWD={PWD};'
    )

def read_file_json(file):
    """
    Reads and loads JSON data from a file.

    Args:
        file (str): The path to the JSON file.

    Returns:
        dict: The loaded JSON data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        JSONDecodeError: If the file contains invalid JSON data.

    Examples:
        >>> read_file_json("data.json")
        {'key': 'value'}
    """

    with open(file, 'r', encoding="utf-8") as data:
        return json.load(data)
    

    
def sql():
    conn = db_connect()
    cursor = conn.cursor()
    data = read_file_json('data.json')
    sql = "INSERT INTO [dbo].[categorias] (Name, Parent) OUTPUT INSERTED.ID VALUES (?, ?);"
    for category in data:
        cursor.execute(sql, (category,None))

        category_id = cursor.fetchone()

        if category_id is not None and category_id.ID is not None:
            category_id = int(category_id.ID)
            print(f"ID da categoria inserida: {category_id} para {category}")
        else:
            print(f"Falha ao inserir a categoria {category}.")

        if subcategories := data[category]:
            for sub in subcategories:
                cursor.execute(sql, (sub,category_id))
                subcategory_id = cursor.fetchone()
                
                if subcategory_id is not None and subcategory_id.ID is not None:
                    subcategory_id = int(subcategory_id.ID)
                    print(f"ID da categoria inserida: {subcategory_id} para {sub}")
                else:
                    print(f"Falha ao inserir a categoria {sub}.")
                    
                if len(data[category][sub]) > 0:
                    items = data[category][sub]
                    for item in items:
                        cursor.execute(sql, (item,subcategory_id))
                        item_id_result = cursor.fetchone()

                        if item_id_result is not None and item_id_result.ID is not None:
                            item_id = int(item_id_result.ID)
                            print(f"ID da categoria inserida: {item_id} para {item}")
                        else:
                            print(f"Falha ao inserir a categoria {item}.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    sql()
