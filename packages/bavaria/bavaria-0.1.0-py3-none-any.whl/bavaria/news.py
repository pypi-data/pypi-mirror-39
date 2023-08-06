from dataclasses import dataclass, field


@dataclass
class Message:
    updated: str
    images: field(default_factory=list)
    title: str
    # tracks

    content: str
    title: str
