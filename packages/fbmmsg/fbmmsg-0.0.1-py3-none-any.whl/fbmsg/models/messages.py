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


class Message:
    def __init__(self, text: str, quick_reply: QuickReply=None):
        if not isinstance(text, str):
            raise TypeError("Message.text must be an instance of str")
        if quick_reply and not isinstance(quick_reply, QuickReply):
            raise TypeError("Message.quick_reply must be an instance of QuickReply")
        self.text = text
        self.quick_reply = quick_reply

    def set_quick_reply(self, quick_reply):
        if not isinstance(quick_reply, QuickReply):
            raise TypeError("Message.quick_reply must be an instance of QuickReply")
        self.quick_reply = quick_reply

    def to_dict(self):
        msg = {"text": self.text}
        if self.quick_reply:
            msg['quick_replies'] = self.quick_reply.to_dict()
        return msg
