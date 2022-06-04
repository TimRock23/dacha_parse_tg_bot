from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

URI = 'https://plus.yandex.ru/dacha'


def get_all_events():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(URI)
    try:
        data = driver.find_elements(by=By.CLASS_NAME, value='dacha-events__item')
    except Exception as e:
        print(e)
        data = []

    all_events = []
    for event in data:
        text_event = [i for i in event.text.split('\n') if i not in ('', ' ')]
        category = text_event[3].split(' ')[-3]
        if category == 'Дети':
            continue
        tickets = 0 if text_event[5].startswith('Билетов нет') else int(text_event[5].split(' ')[1])
        all_events.append(
            {
                'date': text_event[0],
                'name': text_event[1],
                'description': text_event[2],
                'category': category,
                'tickets': tickets
            }
        )

    return all_events

# x = [[i['name'], i['category'], i['tickets']] for i in all_events]
#
# for i in x:
#     print(i)


# with open('filename.png', 'wb') as file:
#     file.write(first.find_element(by=By.CLASS_NAME,
#                                   value='dacha-event-card__image').screenshot_as_png)
