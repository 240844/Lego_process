from enum import Enum
#pip install enum34

class LegoBrick(Enum):
    APPLE = 0
    BANANA = 1
    BLUE = 2
    CHERRY = 3
    FROG = 4
    GREEN = 5

# Example usage:
if __name__ == '__main__':
    selected_brick = LegoBrick.BANANA
    print(f"Selected Brick: {selected_brick.name}, Index: {selected_brick.value}")
    selected_index = 3
    print(f"Selected Index: {selected_index}, Brick: {LegoBrick(3).name}")
