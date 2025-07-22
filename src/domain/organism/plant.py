from dataclasses import dataclass


from domain.organism.organismdepr import OrganismDEPR


@dataclass
class Plant(OrganismDEPR):
    is_alive: bool = True



    def tick(self):
        ...

