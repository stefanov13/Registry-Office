from .choices_mixin import ChoicesMixin

class MaxLengthChoicesStringsMixin(ChoicesMixin):
    @classmethod
    def max_length(cls):
        return max(len(x.value) for x in cls)
