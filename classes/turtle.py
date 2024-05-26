from cyclonedds.domain import DomainParticipant
from cyclonedds.pub import DataWriter
from cyclonedds.sub import DataReader
from cyclonedds.topic import Topic
from classes.messages import TurtleUpdate
from OpenGL.GL import *
from math import atan2
import random
import glm

class Turtle():

    def __init__(self, name, target = None):
        self.position = glm.vec3(0.0)
        self.dp = DomainParticipant()
        self.topic_update = Topic(self.dp, "update_"+name, TurtleUpdate)
        self.dw = DataWriter(self.dp, self.topic_update)
        self.target = target
        self.linear_speed = 0.005
        self.color = glm.vec3(random.random(), random.random(), random.random())
        if target != None and target != '':
            self.topic_target = Topic(self.dp, "update_"+target, TurtleUpdate)
            self.dr = DataReader(self.dp, self.topic_target)

    def get_position(self):
        return glm.vec2(self.position.x, self.position.y)

    def set_position(self, v : glm.vec2):
        self.position = glm.vec3(v, 0.0)
        return self.position

    def chase(self):
        self.dw.write(TurtleUpdate(float(self.position.x), float(self.position.y)))
        if self.target != None and self.target != '':
            sample = self.dr.take_next()
            if sample != None:
                angle_to_target = atan2(sample.y - self.position.y, sample.x - self.position.x)
                self.position.z += (angle_to_target - self.position.z) * 0.75
        sn = glm.sin(self.position.z)
        cs = glm.cos(self.position.z)
        self.position += glm.vec3(glm.vec2(cs, sn) * self.linear_speed, 0.0)
        self.position.x = glm.clamp(self.position.x, -1.0, 1.0)
        self.position.y = glm.clamp(self.position.y, -1.0, 1.0)