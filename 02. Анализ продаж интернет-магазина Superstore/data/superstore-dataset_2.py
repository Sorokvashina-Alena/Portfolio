import pandas as pd
from geopy.geocoders import Nominatim
from time import sleep

# Загрузка файла
df = pd.read_csv("Sample - Superstore.csv", encoding='latin1')

# Смотрим общую структуру данных
df.head(5)
df.info()
df.describe()
print(df.columns)

# Очистим данные
df.isnull().sum()
df.dropna(inplace=True)
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

# Геокодирование городов
geolocator = Nominatim(user_agent="geoapi")
cities = df['City'].unique()

# Получим координаты
for city in cities[:5]:
    print(f"Город: {city}")
    location = geolocator.geocode(f"{city}, USA")
    print(location)
    if location:
        print(location.latitude, location.longitude)
    print()
