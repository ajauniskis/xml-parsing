from dataclasses import dataclass, field
from itertools import count

from datalite import datalite
from utils.config import DATABASE_URL


@datalite(db_path=DATABASE_URL)
@dataclass
class Measurements:
    field(default_factory=count().__next__, init=False)
    url: str
    price: float
    rooms: int
    area: float
