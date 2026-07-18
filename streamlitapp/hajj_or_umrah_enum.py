from enum import Enum

class HajjOrUmrahEnum(Enum):
    HAJJ = "hajj"
    UMRAH = "umrah"

    @property
    def icon(self) -> str:
        return "🕋" if self is HajjOrUmrahEnum.HAJJ else "🕌"

    @property
    def label(self) -> str:
        return self.value.title()