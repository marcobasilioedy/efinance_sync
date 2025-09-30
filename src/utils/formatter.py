import unicodedata

CORRECT_NAMES = [
    "Adega",
    "Area De Servico",
    "Banheiros",
    "Biblioteca",
    "Clinicas",
    "Closet",
    "Cozinhas",
    "Dormitorio Casal",
    "Dormitorio Corporativo",
    "Dormitorio Solteiro",
    "Escritorio Corporativo",
    "Home Office",
    "Home Theater",
    "Sala De Jantar",
    "Varanda"
]

NORMALIZATION_MAP = {
    "area de servico": "Area De Servico",
    "area de serviço": "Area De Servico",
    "sala de jantar": "Sala De Jantar",
    "sala de jantarr": "Sala De Jantar",
    "dormitorio casal": "Dormitorio Casal",
    "dormitorio solteiro": "Dormitorio Solteiro",
    "dormitorio corporativo": "Dormitorio Corporativo",
    "home office": "Home Office",
    "home theater": "Home Theater",
    "escritorio corporativo": "Escritorio Corporativo"
}

def normalize_string(input_str: str) -> str:
    normalized = unicodedata.normalize('NFD', input_str)
    normalized = normalized.encode('ascii', 'ignore').decode('utf-8')

    normalized = normalized.lower().strip()

    if normalized in NORMALIZATION_MAP:
        return NORMALIZATION_MAP[normalized]
    
    return ' '.join(word.capitalize() for word in normalized.split())

