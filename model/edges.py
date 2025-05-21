from dataclasses import dataclass

from model.retailers import Retailer


@dataclass
class Edge():
    r1: Retailer
    r2: Retailer
    weight: int