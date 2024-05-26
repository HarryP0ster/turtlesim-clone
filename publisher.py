from dataclasses import dataclass
from cyclonedds.idl import IdlStruct
from cyclonedds.domain import DomainParticipant
from cyclonedds.topic import Topic
from cyclonedds.pub import DataWriter
from cyclonedds.core import Qos, Policy
from sshkeyboard import listen_keyboard
from classes.messages import KeyPress

participant = DomainParticipant()
topic = Topic(participant, "Keyboard", KeyPress)
writer = DataWriter(participant, topic)

key_map = {
    'w' : 0, "ц" : 0, "up" : 0,
    "s" : 1, "ы" : 1, "down" : 1, "d" : 2, "в" : 2,
    "right" : 2, "a" : 3, "ф" : 3, "left" : 3
}

async def press(key):
    if key in key_map:
        message=KeyPress(key_map[key], 1)
        writer.write(message)

def release(key):
    if key in key_map:
        message=KeyPress(key_map[key], 0)
        writer.write(message)

if __name__ == "__main__":
    listen_keyboard(
        on_press=press,
        on_release=release,
        delay_second_char=0.1,
        delay_other_chars=0.1
    )