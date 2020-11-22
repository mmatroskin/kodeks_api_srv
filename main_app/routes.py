from app.views import SearchView, DocView, InfoView


routes = [
    ('GET', '/', InfoView, 'get_info'),
    ('GET', '/search', SearchView, 'get_data'),
    ('POST', '/document', DocView, 'get_doc'),
]
