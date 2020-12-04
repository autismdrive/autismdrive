import enum


class ChainPromptLevel(enum.Enum):
    """
    1. No Prompt (Independent)
    2. Shadow Prompt (approximately one inch)
    3. Partial Physical Prompt (thumb and index finger)
    4. Full Physical Prompt (hand-over-hand)
    """
    none = 1
    shadow = 2
    partial_physical = 3
    full_physical = 4

    @classmethod
    def has_name(cls, name):
        return any(name == item.name for item in cls)

    @classmethod
    def options(cls):
        return [item.name for item in cls]
