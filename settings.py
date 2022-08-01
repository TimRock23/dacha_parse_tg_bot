URI: str = 'https://plus.yandex.ru/dacha'
CACHE_TIME_SEC: int = 180
PARSE_ITEM: str = 'dacha-events__item'
REG_URI: str = ('https://widget.afisha.yandex.ru/w/sessions'
                '/ticketsteam-1550%40{id}')
ID_REGEX: str = r'\[data-style-id="dacha-event-card-(.*?)\"\]'
PLUS_ADVERTISING: str = 'Бесплатно с Плюсом'
START_MESSAGE: str = (
    'Бот парсит Яндекс Дачу на предмет появления '
    'новых ивентов и билетов на старые по выбранным категориям\n'
    'Для выбора/изменения категорий введите "/category"\n'
    'Получить все ивенты с сайта по подписанным категориям - "/events"'
    'Ссылка на Яндекс Дачу - "/link"'
)
REQUEST_TIME_RANGE: tuple = (180, 360)
