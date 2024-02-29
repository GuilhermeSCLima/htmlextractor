import pyodbc
import json
import os
from decouple import config

def sql():
    SERVER = config('SERVER')
    DATABASE = config('DATABASE')
    UID = config('UID')
    PWD = config('PWD')
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          f'Server={SERVER};'
                          f'Database={DATABASE};'
                          f'UID={UID};'
                          f'PWD={PWD};')

    cursor = conn.cursor()

    with open("data.json", 'r') as f:
        data = json.load(f)
        
        for category in data:
            categorySintax = "INSERT INTO tienda.categorias (Name, Parent) OUTPUT INSERTED.ID VALUES (?, NULL);"
            cursor.execute(categorySintax, (category['name'],))
            
            # Obter o ID diretamente da execução da inserção
            category_id_result = cursor.fetchone()

            if category_id_result is not None and category_id_result.ID is not None:
                category_id = int(category_id_result.ID)
                print(f"ID da categoria inserida: {category_id} para {category['name']}")
            else:
                print(f"Falha ao inserir a categoria {category['name']}.")

            if category['subcategories']:
                for sub in category['subcategories']:
                    category_id = int(category_id_result.ID)
                    subcategorySintax = "INSERT INTO tienda.categorias (Name, Parent) OUTPUT INSERTED.ID VALUES (?, ?);"
                    cursor.execute(subcategorySintax, (sub['name'],category_id))
                    
                    # Obter o ID diretamente da execução da inserção
                    subcategory_id_result = cursor.fetchone()

                    if subcategory_id_result is not None and category_id_result.ID is not None:
                        subcategory_id = int(subcategory_id_result.ID)
                        print(f"ID da categoria inserida: {subcategory_id} para {sub['name']}")
                    else:
                        print(f"Falha ao inserir a categoria {sub['name']}.")
                    
                    if sub["types"]:
                        for typ in sub["types"]:
                            subcategory_id = int(category_id_result.ID)
                            cursor.execute(subcategorySintax, (typ,category_id))
                            
                            # Obter o ID diretamente da execução da inserção
                            type_id_result = cursor.fetchone()

                            if type_id_result is not None and category_id_result.ID is not None:
                                type_id = int(type_id_result.ID)
                                print(f"ID da categoria inserida: {type_id} para {typ}")
                            else:
                                print(f"Falha ao inserir a categoria {typ}.")
                            

    # Commit após o loop, uma vez para todas as inserções
    conn.commit()
    conn.close()

if __name__ == "__main__":
    sql()
