class VoiceInfo:
    def __init__(self, ):
        self.name = ''
        self.en_name = ''
        self.titles = []

    def to_dic(self):
        return {
            'name': self.name,
            'en_name': self.en_name,
            'titles': self.titles,
        }


class Title:
    def __init__(self, ):
        self.text = ''
        self.voices = []
        self.content = ''

    def to_dic(self):
        return {
            'text': self.text,
            'voices': self.voices,
            'content': self.content
        }
