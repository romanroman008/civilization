import json
from enum import Enum, auto


class Action(Enum):
    REST = auto()
    MOVE = auto()
    ATTACK = auto()
    INTERACT = auto()
    RUN_AWAY = auto()

    def load_rules_from_json(path: str):
        with open(path, "r") as f:
            raw_rules = json.load(f)

        rules = []
        for rule in raw_rules:
            rules.append({
                "name": rule["name"],
                "condition_str": rule["condition"],
                "condition": compile(rule["condition"], "<string>", "eval"),
                "action": Action[rule["action"]],
                "weight": rule["weight"]
            })
        return rules


