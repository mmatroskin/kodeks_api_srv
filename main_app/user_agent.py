from fake_useragent import UserAgent


class UserAgentMeta(type):
    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls.__instances.get(cls) is None:
            cls.__instances[cls] = super(UserAgentMeta, cls).__call__(*args, **kwargs)
        return cls.__instances[cls]


class UserAgentItem(UserAgent, metaclass=UserAgentMeta):
    pass
