from dataclasses import dataclass, field

from dataclasses import dataclass, is_dataclass

def nested_dataclass(*args, **kwargs):
    def wrapper(cls):
        cls = dataclass(cls, **kwargs)
        original_init = cls.__init__
        def __init__(self, *args, **kwargs):
            for name, value in kwargs.items():
                field_type = cls.__annotations__.get(name, None)
                if is_dataclass(field_type) and isinstance(value, dict):
                     new_obj = field_type(**value)
                     kwargs[name] = new_obj
            original_init(self, *args, **kwargs)
        cls.__init__ = __init__
        return cls
    return wrapper(args[0]) if args else wrapper

class TimeTable:
    train_type: str
    train_numer: int


@dataclass
class Line:
    color: str
    name: str
    id: int
    text_color: str


@nested_dataclass
class Properties:
    rake: str
    train_id: int
    original_train_number: int
    line: Line
    time_since_update: int
    calls_stack: field(default_factory=list)
    time_intervals: field(default_factory=list)
    stop_point_ds100: str
    state: str
    transmitting_vehicle: str
    raw_coordinates: field(default_factory=list)
    event_timestamp: float
    vehicle_number: int
    event: str
    delay: float
    position_correction: int
    timestamp: float
    train_number: int
    ride_state: str
    aimed_time_offset: float



@nested_dataclass
class Content:
    properties: Properties
    geometry: field(default_factory=dict)
    type: field(default_factory=dict)


@nested_dataclass
class Message:
    source: str
    timestamp: float
    content: Content
    client_reference: str
