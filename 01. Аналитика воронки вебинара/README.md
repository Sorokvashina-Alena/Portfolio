# Аналитика воронки вебинара

## Описание

Проект направлен на анализ поведения пользователей во время вебинара для селлеров маркетплейсов. Исследование охватывает ключевые этапы воронки и выявляет, почему значительная часть пользователей не доходит до оформления заявки.

---

## 🎯 Цели исследования

- Проанализировать поведение на этапах: Telegram-бот → вебинар → заявка.
- Найти «узкие места» и точки оттока.
- Выдвинуть гипотезы и предложить решения по повышению конверсии.

---

## Стек

- `Pandas`, `NumPy` — обработка данных
- `Matplotlib`, `Seaborn` — визуализация
- Временной анализ, сегментация по длительности сессий, воронка конверсии

---

## 📊 Пример воронки (код + визуализация)

```python
# Подсчёт количества пользователей на каждом этапе
total_users = df['user_id'].nunique()
entered_bot = df[df['action'] == 'enter_bot']['user_id'].nunique()
entered_webinar = df[df['action'] == 'enter_webinar_room']['user_id'].nunique()
made_order = df[df['action'] == 'make_order']['user_id'].nunique()
```

```python
# Построение визуализации воронки
stages = ['Зашли в бота', 'На вебинаре', 'Оставили заявку']
conversion = [100,
              entered_webinar / entered_bot * 100,
              made_order / entered_webinar * 100]

sns.barplot(x=stages, y=conversion, palette=palette_custom[:3])
plt.title('Конверсия по этапам воронки')
plt.ylabel('Конверсия (%)')
plt.show()
```
![Conversion_on_stages](https://github.com/user-attachments/assets/6dfec320-7596-4ec2-b432-ab8d250abd5e)

## Конверсия в зависимости от длительности участия
```
webinar_start = df[df['action'] == 'enter_webinar_room']['created_at'].min()  
  
user_stats = []  
for user_id in df['user_id'].unique():  
    user_data = df[df['user_id'] == user_id]  
    if {'enter_webinar_room', 'leave_webinar_room'}.issubset(set(user_data['action'])):  
        enter = user_data[user_data['action'] == 'enter_webinar_room']['created_at'].min()  
        leave = user_data[user_data['action'] == 'leave_webinar_room']['created_at'].max()  
        duration = (leave - enter).total_seconds() / 60  
  order = 1 if 'make_order' in user_data['action'].values else 0  
  user_stats.append({  
            'user_id': user_id,  
            'duration_min': duration,  
            'made_order': order  
        })  
  
webinar_time = pd.DataFrame(user_stats)  
   
bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 90]  
labels = ["0–5", "5–10", "10–15", "15–20", "20–25", "25–30",  
          "30–35", "35–40", "40–50", "50–60", "60–90"]  
  
webinar_time['duration_group'] = pd.cut(webinar_time['duration_min'], bins=bins, labels=labels, right=False)  
grouped = webinar_time.groupby('duration_group')['made_order'].agg(['count', 'sum'])  
grouped['conversion (%)'] = (grouped['sum'] / grouped['count'] * 100).round(2)  
grouped = grouped.rename(columns={'count': 'Users', 'sum': 'Orders'})
```
✅ Пользователи, которые провели **40–50 минут**, конвертируются в **2.4 раза** лучше.

```
# Построение визуализации
from matplotlib.colors import LinearSegmentedColormap  
 
colorscale = LinearSegmentedColormap.from_list("custom_green", palette_custom)  
  
norm_values = (grouped["conversion (%)"] - grouped["conversion (%)"].min()) / (  
    grouped["conversion (%)"].max() - grouped["conversion (%)"].min()  
)  
colors = [colorscale(val) for val in norm_values.fillna(0)]  # защита от NaN  
  
plt.figure(figsize=(10, 6))  
bars = sns.barplot(x=grouped.index, y=grouped['conversion (%)'], palette=colors)  
  
plt.title('Конверсия в заявку по длительности участия', fontsize=13)  
plt.xlabel('Длительность участия (мин.)')  
plt.ylabel('Конверсия (%)')  
    
for i, v in enumerate(grouped['conversion (%)']):  
    bars.text(i, v + 0.3, f"{v:.1f}%", ha='center', fontsize=9)  
  
plt.xticks(rotation=30)  
plt.tight_layout()  
plt.show()
```

![Duratiom_groups](https://github.com/user-attachments/assets/da08d565-e5ca-434a-8960-8f61c3aa05bc)

## Основные результаты 
  
- Всего пользователей: **1000**  
- До вебинара дошли: **38.2%**  
- Общая конверсия в заявку: **4.7%**  
- Конверсия достигает **11.1%** в группе участников с участием **40–50 минут**  
- До 40-й минуты уходит около **65%** пользователей  
- Повторные подключения повышают конверсию в **2.6 раза**  
- Ключевая гипотеза: оффер озвучен поздно (около 40-й минуты), большинство не доживает

 ## 💡Рекомендации:
 • Озвучить «тизер оффера» уже на 15–20 минуте.  
• Повторить ключевые преимущества на 25–30 минуте.  
• Досидевшим 30+ мин предложить бонус.  
• Повторников — отловить и обработать отдельно.  
• Ушедших до 10-й — ретаргетить повторной воронкой через TG/email.  

## 📂 Структура проекта
```text
Аналитика воронки вебинара
├── README.md
├── data/				# данные
    └── webinar_user_events.csv      
├── images/                    		 # графики
   └── conversion_funnel.png
   └── duration_vs_conversion.png
├── scripts/      			# основной анализ
	└── webinar_analysis.ipynb
	└── webinar_analysis.py
├── view/          			# итоговый отчет
    └── Webinar_report.pdf
 ```
