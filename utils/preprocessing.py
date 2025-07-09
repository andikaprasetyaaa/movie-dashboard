import pandas as pd

def load_and_prepare_data(filepath):
    df = pd.read_csv(filepath, encoding='utf-8-sig', engine='python', on_bad_lines='skip')

    df['Release_Date'] = pd.to_datetime(df['Release_Date'], errors='coerce')
    df['Vote_Count'] = pd.to_numeric(df['Vote_Count'], errors='coerce')
    df['Vote_Average'] = pd.to_numeric(df['Vote_Average'], errors='coerce')
    df['Popularity'] = pd.to_numeric(df['Popularity'], errors='coerce')

    df = df.dropna(subset=['Release_Date', 'Vote_Average', 'Popularity', 'Vote_Count', 'Original_Language'])
    df['Genre'] = df['Genre'].fillna('').apply(lambda x: [g.strip() for g in x.split(',')] if x else [])

    LANGUAGE_MAP = {
        "en": "Inggris", "fr": "Prancis", "ja": "Jepang", "ko": "Korea", "es": "Spanyol", "de": "Jerman",
        "hi": "Hindi", "zh": "Mandarin", "cn": "Tiongkok", "it": "Italia", "pt": "Portugis", "ru": "Rusia",
        "id": "Indonesia", "tr": "Turki", "ar": "Arab", "th": "Thailand", "ta": "Tamil", "bn": "Bengali",
        "te": "Telugu", "ml": "Malayalam", "mr": "Marathi", "fa": "Persia", "pl": "Polandia", "sv": "Swedia",
        "fi": "Finlandia", "da": "Denmark", "nl": "Belanda", "cs": "Ceko", "ca": "Katalan", "el": "Yunani",
        "et": "Estonia", "eu": "Basque", "he": "Ibrani", "hu": "Hungaria", "is": "Islandia", "la": "Latin",
        "lv": "Latvia", "ms": "Melayu", "nb": "Norwegia Bokmål", "no": "Norwegia", "ro": "Rumania",
        "sr": "Serbia", "sk": "Slovakia", "tl": "Tagalog", "uk": "Ukraina"
    }
    df['Language_Name'] = df['Original_Language'].map(LANGUAGE_MAP).fillna(df['Original_Language'])

    return df