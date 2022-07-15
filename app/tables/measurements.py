from dataclasses import dataclass, field
from itertools import count

from datalite import datalite


@datalite(db_path="rent_portal.sqlite")
@dataclass
class Measurements:
    field(default_factory=count().__next__, init=False)
    url: str
    price: int
    rooms: int
    area: float
