from bs4 import BeautifulSoup
from data import myhtml
import json

# Parse the HTML
soup = BeautifulSoup(myhtml, 'html.parser')

def extract():
    rootElements = soup.select('li.nav-item-root')
    result_dict = {}
    for li in rootElements:
        category = li.select("a span")[0].text.strip()
        subElements = li.select("li.nav-item-sub")
        category_dict = {}
        for sub in subElements:
            subCategory = sub.select("a span")[0].text.strip()
            elements = sub.select("li.nav-item")
            item_list = []
            for item in elements:
                itemCategory = item.select("a")[0].text.strip()
                item_list.append(itemCategory)
            category_dict[subCategory] = item_list
        result_dict[category] = category_dict
    return result_dict

# Function to extract categories, subcategories, and types
# def extract_category_info(category_elem):
#     category_info = {
#         "subcategories": [],
#         "name": category_elem.find('span').text.strip(),
#     }

#     # Extract subcategories
#     subcategory_elems = category_elem.find_all('li', class_='nav-item-sub')
#     for subcategory_elem in subcategory_elems:
#         subcategory_info = {
#             "types": [],
#             "name": subcategory_elem.find('span').text.strip(),
#         }
#         # Extract types
#         type_elems = subcategory_elem.find_all('li', class_='nav-item')
#         for type_elem in type_elems:
#             type_info = type_elem.find('a').text.strip()
#             subcategory_info["types"].append(type_info)

#         category_info["subcategories"].append(subcategory_info)

#     return category_info

# # Extract all categories
# def extract():
#     categories_elems = soup.find_all('li', class_='nav-item-root')
#     categories_data = []

#     for category_elem in categories_elems:
#         category_info = extract_category_info(category_elem)
#         categories_data.append(category_info)

#     try:
#         with open("data.json", 'w') as archivo:
#             archivo.write(json.dumps(categories_data,indent=2, ensure_ascii=False))
#             print('Contenido escrito correctamente en el archivo: data.json')

#     except Exception as e:
#         print(f'Error al escribir en el archivo \"data.json\": {e}')
        
if __name__ == "__main__":
    data = extract()
    try:
        with open("data.json", 'w', encoding='utf-8') as archivo:
            data_json = json.dumps(data,indent=2, ensure_ascii=False)
            archivo.write(data_json)
            print('Contenido escrito correctamente en el archivo: data.json')

    except Exception as e:
        print(f'Error al escribir en el archivo \"data.json\": {e}')