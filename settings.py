URI = 'https://plus.yandex.ru/dacha'
CACHE_TIME_SEC = 180
PARSE_ITEM = 'dacha-events__item'
REG_URI = 'https://widget.afisha.yandex.ru/w/sessions/ticketsteam-1550%40{id}'
ID_REGEX = r'\[data-style-id="dacha-event-card-(.*?)\"\]'
PLUS_ADVERTISING = 'Бесплатно с Плюсом'
START_MESSAGE = (
    'Бот парсит Яндекс Дачу на предмет появления '
    'новых ивентов и билетов на старые по выбранным категориям\n'
    'Для выбора/изменения категорий введите "/category"\n'
    'Получить все ивенты с сайта по подписанным категориям - "/events"'
    'Ссылка на Яндекс Дачу - "/link"'
)
