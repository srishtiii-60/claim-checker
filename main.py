from dataclasses import dataclass, asdict
from enum import Enum
import json


class StatementType(str, Enum):
    FACT = "fact"
    OPINION = "opinion"
    PREDICTION = "prediction"


@dataclass
class Claim:
    id: str                    # unique, jaise "c1", "c2"
    original_text: str         # speaker/article ne exactly kya likha
    normalized_claim: str      # saaf, ek-baat wala version
    statement_type: StatementType
    position: int              # text mein kahan se shuru hota hai (character index)
    context: str               # aas-paas ka text
    language: str = "en"       # "en" ya "hi"


claim = Claim(
    id="c1",
    original_text="Our company has more than five million customers.",
    normalized_claim="The company has more than 5 million customers.",
    statement_type=StatementType.FACT,
    position=0,
    context="Our company has more than five million customers and we are growing fast.",
)

print(json.dumps(asdict(claim), indent=2, ensure_ascii=False))