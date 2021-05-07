import enum


class Relationship(enum.Enum):
    self_participant = 1
    self_guardian = 2
    dependent = 3
    self_professional = 4
    self_interested = 5

    @classmethod
    def has_name(cls, name):
        return any(name == item.name for item in cls)

    @classmethod
    def is_self(cls, name):
        if isinstance(name, str):
            return name != 'dependent'
        if isinstance(name, cls):
            return name != cls.dependent


    @classmethod
    def options(cls):
        return [item.name for item in cls]