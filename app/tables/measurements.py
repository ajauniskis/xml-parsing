from dataclasses import dataclass, field
from datalite import datalite
from itertools import count


@datalite(db_path="rent_portal.sqlite")
@dataclass
class Measurements:
    field(default_factory=count().__next__, init=False)
    href: str
    price: int
    rooms: int
    area: float
