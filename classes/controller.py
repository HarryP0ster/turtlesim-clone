from dataclasses import dataclass
from cyclonedds.domain import DomainParticipant
from cyclonedds.topic import Topic
from cyclonedds.sub import DataReader
from classes.messages import KeyPress
from time import sleep
import glm

class TurtleController():
    
    def __init__(self, target):
        self.target = target
        self.dp = DomainParticipant()
        self.tp = Topic(self.dp, "Keyboard", KeyPress)
        self.dr = DataReader(self.dp, self.tp)
        self.key_status = { 0 : 0, 1 : 0, 2 : 0, 3 : 0 }

    def update(self):
        samples = self.dr.take()
        for sample in samples:
            self.key_status[sample.key] = sample.action
        
        if self.key_status[0] > 0:
            self.target.linear_speed = 0.0085
        elif self.key_status[1] > 0:
            self.target.linear_speed = -0.0085
        else:
            self.target.linear_speed = 0.0

        if self.key_status[2] > 0:
            self.target.position.z -= glm.radians(5.0)
        if self.key_status[3] > 0:
            self.target.position.z += glm.radians(5.0)