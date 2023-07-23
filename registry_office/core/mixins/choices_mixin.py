class ChoicesMixin:
    @classmethod
    def choices(cls):
        return [(choice.value, choice.name) for choice in cls]
