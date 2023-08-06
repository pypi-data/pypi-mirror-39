class QuickReplyButton:
    def __init__(self, title: str, payload: str):
        if not isinstance(title, str):
            raise TypeError("QuickReplyButton.title must be an instance of str")
        if not isinstance(payload, str):
            raise TypeError("QuickReplyButton.payload must be an instance of str")

        self.title = title
        self.payload = payload

    def to_dict(self):
        return {
            "content_type": "text",
            "title": self.title,
            "payload": self.payload
        }


class QuickReply:
    def __init__(self):
        self.buttons = []

    def add(self, button: QuickReplyButton):
        if not isinstance(button, QuickReplyButton):
            raise TypeError("button must be an instance of QuickReplyButton")
        self.buttons.append(button)

    def to_dict(self):
        return [button.to_dict() for button in self.buttons]


class Button:
    def __init__(self, type: str, title: str, **kwargs):
        if not isinstance(title, str):
            raise TypeError("Button.title must be an instance of str")
        if not isinstance(type, str):
            raise TypeError("Button.type must be an instance of str")
        self.title = title
        self.type = type
        for k in kwargs:
            setattr(self, k, kwargs[k])

    def to_dict(self):
        return dict(vars(self))


class Template:
    def __init__(self, type: str, text: str, **kwargs):
        if not isinstance(type, str):
            raise TypeError("Template.type must be an instance of str")
        if not isinstance(text, str):
            raise TypeError("Template.text must be an instance of str")
        self.type = type
        self.text = text
        for k in kwargs:
            setattr(self, k, kwargs[k])

    def to_dict(self):
        res = {
            "type": "template",
            "payload": {
                "template_type": self.type,
                "text": self.text
            }
        }
        if hasattr(self, 'buttons'):
            res['payload'].update({"buttons": [b.to_dict() for b in self.buttons]})
        return res


class Message:
    def __init__(self, text: str = None, quick_reply: QuickReply = None, attachment=None):
        if text and not isinstance(text, str):
            raise TypeError("Message.text must be an instance of str")
        if quick_reply and not isinstance(quick_reply, QuickReply):
            raise TypeError("Message.quick_reply must be an instance of QuickReply")
        self.text = text
        self.quick_reply = quick_reply
        self.attachment = attachment

    def set_quick_reply(self, quick_reply):
        if not isinstance(quick_reply, QuickReply):
            raise TypeError("Message.quick_reply must be an instance of QuickReply")
        self.quick_reply = quick_reply

    def to_dict(self):
        msg = {}
        if self.text:
            msg['text'] = self.text
        if self.quick_reply:
            msg['quick_replies'] = self.quick_reply.to_dict()
        if self.attachment:
            msg['attachment'] = self.attachment.to_dict()
        return msg
