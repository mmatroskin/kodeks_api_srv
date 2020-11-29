from collections import namedtuple
from main_app.user_agent import UserAgentItem


DocType = namedtuple('DocType', 'id, text')
loggers = {}
user_agent = UserAgentItem()
