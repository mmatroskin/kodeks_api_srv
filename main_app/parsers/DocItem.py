from bs4 import BeautifulSoup
from os.path import join
from app_log import get_logger
from settings import ROOT_DIR, LOG_FILE


class DocItem():

    def __init__(self, data):
        self.log = get_logger(join(ROOT_DIR, LOG_FILE), __name__)
        self.id = data.get('id')
        self.name = data.get('name')
        self.is_available = data.get('is_available')
        self.is_active = data.get('is_active')
        self.message = 'Текст документа недоступен'
        self.html = None

    def fill_body(self, **data):
        try:
            template = data.get('template')
            with open(template, 'r', encoding='utf-8') as t:
                base_content = t.read()
            menu_content = data.get('doctoc')
            content = data.get('content')
            info = 'Действующий' if self.is_active else 'Не действующий'
            ext_url = data.get('ext_url')

            if ext_url is not None:
                content = content.replace('/picture/get?', ext_url + '/picture/get?')  # картинки
                content = content.replace('href="', 'href="' + ext_url)  # внешние ссылки

            soup_info = BeautifulSoup(f'<h2>{info}</h2>', 'html.parser')
            soup_content = BeautifulSoup(content, 'html.parser')
            soup = BeautifulSoup(base_content, 'html.parser')

            title_container = soup.find(id='title-item')
            info_container = soup.find(id='info-item')
            content_container = soup.find(id='content-item')

            title_container.insert(0, self.name)
            content_container.insert(0, soup_content)
            info_container.insert(0, soup_info)

            if menu_content:
                menu_content = menu_content.replace('href="#', 'href="#h_')  # document references
                soup_menu = BeautifulSoup(menu_content, 'html.parser')
                menu_container = soup.find(id='menu-body')
                menu_container.append(soup_menu)

            html = soup.prettify(encoding='utf-8')
            self.html = html.decode()
        except Exception as e:
            self.log.error("Exception", exc_info=True)
