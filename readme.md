## Kodex web API client (unofficial)

### Description

Асинхронный WEB-cервис для поиска и скачивания html - версий нормативных документов на docs.cntd.ru. Используется API Кодекс. 

Все запросы возвращают JSON. При первом поисковом запросе присваивается индивидуальный User-Agent и Cookie, если его присваивает сервер kodeks. 
html-версия документа возвращается сервисом в поле ответа `result.data.html`. html-версия адаптирована для мобильных устройств.

### API description

Get:
    
    - доступные типы документов
        Параметры: url = "/" - 
        Результат: json с доступными типами документов или сообщение об ошибке
    
    - справка
        Параметры: url = "/?query=[*]" 
        Результат: json с текстом справки или сообщение об ошибке

Post:

    - поиск:
        Параметры:
            url = /search
            json = {
                'query': строка поиска,
                'type': тип документа,
                'offset': смещение (кратно 20, по умолчанию 0),
                'params': User-Agent, Cookies из предшествующего поискового запроса, либо None/отсутствует 
            }
        
        Результат: json, содержащий список свойств найденных документов в виде словарей или сообщение об ошибке
    
    - скачивание Html - версии документа
        Параметры:
            url = /document
            json = {
                'query': свойста документа из поискового запроса
                'params': User-Agent, Cookies из предшествующего поискового запроса
            }
        
        Результат: json, содержащий html документа или сообщение об ошибке
