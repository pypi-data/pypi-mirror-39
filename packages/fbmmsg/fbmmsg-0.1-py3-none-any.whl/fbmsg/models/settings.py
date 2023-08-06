class MenuItem(object):
    def __init__(self, type: str, title: str, **kwargs):
        if not isinstance(type, str):
            raise TypeError('type must be an instance of str')
        if not isinstance(title, str):
            raise TypeError('title must be an instance of str')
        self.type = type
        self.title = title
        for k in kwargs:
            setattr(self, k, kwargs[k])

    def to_dict(self):
        res = dict(vars(self))
        if 'call_to_actions' in res:
            res['call_to_actions'] = [x.to_dict() for x in res['call_to_actions']]
        return res


class PersistentMenu(object):
    def __init__(self, call_to_actions: list = None, locale: str = 'default', composer_input_disabled: bool = False):
        if call_to_actions is None:
            call_to_actions = []
        if not isinstance(call_to_actions, list):
            raise TypeError('call_to_actions must be an instance of list')
        if not isinstance(locale, str):
            raise TypeError('locale must be an instance of str')
        if not isinstance(composer_input_disabled, bool):
            raise TypeError('composer_input_disabled must be an instance of bool')
        self.call_to_actions = call_to_actions
        self.locale = locale
        self.composer_input_disabled = composer_input_disabled

    def add(self, item: MenuItem):
        self.call_to_actions.append(item)

    def to_dict(self):
        return {
            'locale': self.locale,
            'composer_input_disabled': self.composer_input_disabled,
            'call_to_actions': [x.to_dict() for x in self.call_to_actions]
        }


class Analytics(object):
    def __init__(self, custom_events: list, page_id: int, page_scoped_user_id: int, event: str = 'CUSTOM_APP_EVENTS',
                 advertiser_tracking_enabled: int = 1, application_tracking_enabled: int = 1, extinfo: list = None):
        if extinfo is None:
            extinfo = ['mb1']
        self.custom_events = custom_events
        self.page_id = page_id
        self.page_scoped_user_id = page_scoped_user_id
        self.event = event
        self.advertiser_tracking_enabled = advertiser_tracking_enabled
        self.application_tracking_enabled = application_tracking_enabled
        self.extinfo = extinfo

    def to_dict(self):
        return dict(vars(self))
