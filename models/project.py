from dataclasses import dataclass
from typing import Optional

@dataclass
class Project:
    id: Optional[int]
    name: str
    created_in: str

    