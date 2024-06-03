import time
import requests
from bs4 import BeautifulSoup

# Настройки для Telegram бота
TELEGRAM_TOKEN = '296299444:AAET5Ln-YA6bkMzLADxCxMim4T5HPBE7yNI'
CHAT_ID = '-4198530294'

# URL страницы
URL = "https://fragment.com/numbers?sort=price_asc&filter=sale"

# Предыдущие значения для сравнения
previous_number = None
previous_price = None

def fetch_cheapest_number():
    global previous_number, previous_price
    
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Найти все номера и цены
    rows = soup.find_all('tr', class_='tm-row-selectable')
    numbers = []
    for row in rows:
        try:
            number_link = row.find('a', {'href': True, 'class': 'table-cell'})
            number = number_link['href'].split('/')[-1]
            price_div = row.find('div', class_='table-cell-value tm-value icon-before icon-ton')
            price = int(price_div.text.strip())
            numbers.append((number, price))
        except Exception as e:
            print(f"Error processing row: {e}")
            continue

    if numbers:
        # Сортировка по цене и выбор самого дешевого
        cheapest = sorted(numbers, key=lambda x: x[1])[0]
        return cheapest
    return None

while True:
    cheapest = fetch_cheapest_number()
    if cheapest:
        number, price = cheapest
        # Отправить сообщение, если номер или цена изменились
        if number != previous_number or price != previous_price:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            message = f"[{current_time}] Самый дешевый номер: {number}, стоимость {price} TON"
            print(message)  # Вывод в консоль
            payload = {
                'chat_id': CHAT_ID,
                'text': message
            }
            requests.post(TELEGRAM_API_URL, data=payload)
            previous_number, previous_price = number, price
    # Пауза на 30 секунд перед следующей проверкой
    time.sleep(30)
