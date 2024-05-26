from dataclasses import dataclass
from cyclonedds.idl import IdlStruct

@dataclass 
class KeyPress(IdlStruct):
    key: int
    action : int

@dataclass
class TurtleUpdate(IdlStruct):
    x: float
    y: float

@dataclass 
class Message(IdlStruct):
    text: str