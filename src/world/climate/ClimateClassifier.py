from asyncio import Protocol


class ClimateClassifier(Protocol):
    def classify(self, latitude: float) -> str:
        ...

