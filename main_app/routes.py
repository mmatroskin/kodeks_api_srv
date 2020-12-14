from main_app.app.views import SearchView, DocView, InfoView


routes = [
    ('GET', '/', InfoView, 'get_info'),
    ('POST', '/search', SearchView, 'get_data'),
    ('POST', '/document', DocView, 'get_doc'),
]
