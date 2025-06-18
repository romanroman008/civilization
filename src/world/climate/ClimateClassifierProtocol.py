from asyncio import Protocol


class ClimateClassifierProtocol(Protocol):
    def classify(self, latitude: float) -> str:
        ...

