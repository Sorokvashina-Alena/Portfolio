import pandas as pd
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

# Сгруппируем данные для дальнейшего анализа
sales_by_category = df.groupby('Category')['Sales'].sum()
profit_by_category = df.groupby('Category')['Profit'].sum()

sales_by_region = df.groupby(['City', 'Region'])['Sales'].sum()
profit_by_region = df.groupby(['City', 'Region'])['Profit'].sum()

df['Month'] = df['Order Date'].dt.to_period('M')
monthly_sales = df.groupby('Month')['Sales'].sum()
monthly_profit = df.groupby('Month')['Profit'].sum()

# Объединим таблицы и сохраним
metrics_by_category = pd.concat([sales_by_category, profit_by_category], axis=1)
metrics_by_category.columns = ['Sales', 'Profit']
metrics_by_category.to_csv('metrics_by_category.csv')

metrics_by_region = pd.concat([sales_by_region, profit_by_region], axis=1)
metrics_by_region.columns = ['Sales', 'Profit']
metrics_by_region.to_csv('metrics_by_region.csv')

monthly_metrics = pd.concat([monthly_sales, monthly_profit], axis=1)
monthly_metrics.columns = ['Sales', 'Profit']
monthly_metrics.to_csv('monthly_metrics.csv')