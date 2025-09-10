from dataclasses import dataclass
from typing import Optional

@dataclass
class StructuralElements:
    id: Optional[int]
    project_id:int
    structural_type: str
    structural_data: str
    results: Optional[str]
    created_in: str
    