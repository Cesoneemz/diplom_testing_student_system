# app/utils.py
import re

def generate_username(first_name: str, middle_name: str, last_name: str) -> str:
    # Преобразуем имя, отчество и фамилию в латиницу (если они не латиницей).
    # Для простоты предполагаем, что ФИО введены на кириллице и их нужно транслитерировать.
    
    def transliterate(text: str) -> str:
        translit_dict = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y',
            'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
            'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'y', 'э': 'e', 'ю': 'yu', 'я': 'ya', ' ': '_'
        }
        return ''.join(translit_dict.get(c, c) for c in text.lower())

    # Получаем первые две буквы имени и отчества
    first_initials = transliterate(first_name[:1]) + transliterate(middle_name[:1])
    # Транслитерируем фамилию полностью
    last_name_transliterated = transliterate(last_name)
    
    # Формируем username
    username = f"{first_initials}{last_name_transliterated}"
    
    return username
