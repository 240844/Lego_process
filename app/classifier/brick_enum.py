from enum import Enum

import numpy as np


#pip install enum34

class LegoBrick(Enum):
    APPLE = 0
    BANANA = 1
    BLUE = 2
    CHERRY = 3
    FROG = 4
    GREEN = 5

    def getColor(self):
        color = None
        if self.name == "APPLE":
            color =  255, 0, 0
        elif self.name == "BANANA":
            color =  255, 255, 0
        elif self.name == "BLUE":
            color =  0, 0, 255
        elif self.name == "CHERRY":
            color =  255, 0, 255
        elif self.name == "FROG":
            color =  255, 128, 255
        elif self.name == "GREEN":
            color =  0, 255, 0
        return color[::-1]

def get_random_brick():
    return LegoBrick(np.random.randint(0, len(LegoBrick)))

# Example usage:
if __name__ == '__main__':
    selected_brick = LegoBrick.BANANA
    print(f"Selected Brick: {selected_brick.name}, Index: {selected_brick.value}")
    selected_index = 3
    print(f"Selected Index: {selected_index}, Brick: {LegoBrick(3).name}")

