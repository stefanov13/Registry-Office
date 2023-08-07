class ChoicesMixin:
    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]
