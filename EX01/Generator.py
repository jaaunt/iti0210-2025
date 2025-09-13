# generator.py
import random

def generate_map(width: int, height: int, lava_probability: float = 0.1) -> str:
    if type(width) != int or type(height) != int or width <= 1 or height <= 1:
        raise RuntimeError("Width and height must be positive integers larger than 1!")
    if type(lava_probability) != float or lava_probability > 1.0 or lava_probability < 0.0:
        raise RuntimeError("Lava probability needs to be a float between 0 and 1!")
    start_position = (random.randint(0, width - 1), random.randint(0, height - 1))
    goal_position = start_position
    while goal_position == start_position:
        goal_position = (random.randint(0, width - 1), random.randint(0, height - 1))
    grid_characters = []
    for y in range(height):
        for x in range(width):
            current_position = (x, y)
            if current_position == start_position:
                grid_characters.append("s")
            elif current_position == goal_position:
                grid_characters.append("D")
            else:
                if random.random() <= lava_probability:
                    grid_characters.append("*")
                else:
                    grid_characters.append(" ")
        grid_characters.append("\n")
    return str(height) + "\n" + "".join(grid_characters)

if __name__ == "__main__":
    print(generate_map(90, 90, 0.3))