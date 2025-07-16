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

# Очищаем данные
df.isnull().sum()
df.dropna(inplace=True)
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

# Геокодируем города
geolocator = Nominatim(user_agent="geoapi")
cities = df['City'].unique()

# Получаем координаты
city_coords = {}
for city in cities:
    try:
        location = geolocator.geocode(f"{city}, USA")
        if location:
            city_coords[city] = (location.latitude, location.longitude)
        else:
            city_coords[city] = (None, None)
    except:
        city_coords[city] = (None, None)
    sleep(1)  # обязательная задержка

# Преобразуем в DataFrame
coords_df = pd.DataFrame.from_dict(city_coords, orient='index', columns=['Latitude', 'Longitude'])
coords_df.index.name = 'City'
coords_df.reset_index(inplace=True)

# Объединяем координаты с исходными данными
df = df.merge(coords_df, on='City', how='left')

# Группируем данные для дальнейшего анализа
sales_by_category = df.groupby('Category')['Sales'].sum()
profit_by_category = df.groupby('Category')['Profit'].sum()

sales_by_region = df.groupby(['Order Date', 'City', 'Region'])['Sales'].sum()
profit_by_region = df.groupby(['Order Date', 'City', 'Region'])['Profit'].sum()

df['Month'] = df['Order Date'].dt.to_period('M')
monthly_sales = df.groupby('Month')['Sales'].sum()
monthly_profit = df.groupby('Month')['Profit'].sum()

# Объединяем таблицы и сохраняем
metrics_by_category = pd.concat([sales_by_category, profit_by_category], axis=1)
metrics_by_category.columns = ['Sales', 'Profit']
metrics_by_category.to_csv('metrics_by_category.csv')

metrics_by_region = df.groupby(['Order Date', 'City', 'Region', 'Latitude', 'Longitude'])[['Sales', 'Profit']].sum().reset_index()
metrics_by_region.to_csv('metrics_by_region.csv', index=False)
print("Файл 'metrics_by_region.csv' сохранён — содержит даты, города и координаты.")

monthly_metrics = pd.concat([monthly_sales, monthly_profit], axis=1)
monthly_metrics.columns = ['Sales', 'Profit']
monthly_metrics.to_csv('monthly_metrics.csv')