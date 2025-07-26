from action import Action


class Brain:
    def __init__(self, agent, rules):
        self.agent = agent
        self.rules = rules



    def decide(self, world):
        context = {"agent": self.agent, "world": world}
        scored = []
        for rule in self.rules:
            if eval(rule["condition"], {}, context):
                scored.append((rule["action"], rule["weight"]))
        if scored:
            return max(scored, key=lambda x: x[1])[0]
        return Action.REST