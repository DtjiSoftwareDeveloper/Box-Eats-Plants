"""
This file contains code for the game "Box Eats Plants".
Author: DtjiSoftwareDeveloper
"""


# Importing necessary libraries


import sys
import os
import random
import copy


# Creating static function


def clear():
    # type: () -> None
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows System
    else:
        os.system('clear')  # For Linux System


# Creating necessary classes


class Board:
    """
    This class contains attributes of the board in this game.
    """

    BOARD_HEIGHT: int = 10
    BOARD_WIDTH: int = 10

    def __init__(self):
        # type: () -> None
        self.__tiles: list = []  # initial value
        for i in range(self.BOARD_HEIGHT):
            new: list = []  # initial value
            for j in range(self.BOARD_WIDTH):
                new.append(Tile())

            self.__tiles.append(new)

    def num_plants(self):
        # type: () -> int
        plants: int = 0  # initial value
        for y in range(self.BOARD_HEIGHT):
            for x in range(self.BOARD_WIDTH):
                curr_tile: Tile = self.get_tile_at(x, y)
                if isinstance(curr_tile.plant, Plant):
                    plants += 1

        return plants

    def num_rocks(self):
        # type: () -> int
        rocks: int = 0  # initial value
        for y in range(self.BOARD_HEIGHT):
            for x in range(self.BOARD_WIDTH):
                curr_tile: Tile = self.get_tile_at(x, y)
                if isinstance(curr_tile.rock, Rock):
                    rocks += 1

        return rocks

    def num_boxes(self):
        # type: () -> int
        boxes: int = 0  # initial value
        for y in range(self.BOARD_HEIGHT):
            for x in range(self.BOARD_WIDTH):
                curr_tile: Tile = self.get_tile_at(x, y)
                if isinstance(curr_tile.box, Box):
                    boxes += 1

        return boxes

    def spawn_plant(self):
        # type: () -> Plant
        plant_x: int = random.randint(0, self.BOARD_WIDTH - 1)
        plant_y: int = random.randint(0, self.BOARD_HEIGHT - 1)
        plant_tile: Tile = self.__tiles[plant_y][plant_x]
        while plant_tile.plant is not None:
            plant_x = random.randint(0, self.BOARD_WIDTH - 1)
            plant_y = random.randint(0, self.BOARD_HEIGHT - 1)
            plant_tile = self.__tiles[plant_y][plant_x]

        plant: Plant = Plant(plant_x, plant_y)
        plant_tile.add_plant(plant)
        return plant

    def spawn_rock(self):
        # type: () -> Rock
        rock_x: int = random.randint(0, self.BOARD_WIDTH - 1)
        rock_y: int = random.randint(0, self.BOARD_HEIGHT - 1)
        rock_tile: Tile = self.__tiles[rock_y][rock_x]
        while rock_tile.rock is not None:
            rock_x = random.randint(0, self.BOARD_WIDTH - 1)
            rock_y = random.randint(0, self.BOARD_HEIGHT - 1)
            rock_tile = self.__tiles[rock_y][rock_x]

        rock: Rock = Rock(rock_x, rock_y)
        rock_tile.add_rock(rock)
        return rock

    def spawn_box(self):
        # type: () -> Box
        box_x: int = random.randint(0, self.BOARD_WIDTH - 1)
        box_y: int = random.randint(0, self.BOARD_HEIGHT - 1)
        box_tile: Tile = self.__tiles[box_y][box_x]
        while box_tile.plant is not None or box_tile.rock is not None:
            box_x = random.randint(0, self.BOARD_WIDTH - 1)
            box_y = random.randint(0, self.BOARD_HEIGHT - 1)
            box_tile = self.__tiles[box_y][box_x]
        box: Box = Box(box_x, box_y)
        box_tile.add_box(box)
        return box

    def get_tile_at(self, x, y):
        # type: (int, int) -> Tile or None
        if x < 0 or x >= self.BOARD_WIDTH or y < 0 or y >= self.BOARD_HEIGHT:
            return None
        return self.__tiles[y][x]

    def __str__(self):
        # type: () -> str
        res: str = ""  # initial value
        for y in range(self.BOARD_HEIGHT):
            curr: str = "| "
            for x in range(self.BOARD_WIDTH):
                curr += str(self.get_tile_at(x, y)) + " | "

            res += str(curr) + "\n"

        return res

    def clone(self):
        # type: () -> Board
        return copy.deepcopy(self)


class Box:
    """
    This class contains attributes of a box in this game.
    """

    def __init__(self, x, y):
        # type: (int, int) -> None
        self.name: str = "BOX"
        self.x: int = x
        self.y: int = y

    def move_up(self, board):
        # type: (Board) -> bool
        if self.y > 0:
            old_tile: Tile = board.get_tile_at(self.x, self.y)
            old_tile.remove_box()
            self.y -= 1
            new_tile: Tile = board.get_tile_at(self.x, self.y)
            new_tile.add_box(self)
            return True
        return False

    def move_down(self, board):
        # type: (Board) -> bool
        if self.y < board.BOARD_HEIGHT - 1:
            old_tile: Tile = board.get_tile_at(self.x, self.y)
            old_tile.remove_box()
            self.y += 1
            new_tile: Tile = board.get_tile_at(self.x, self.y)
            new_tile.add_box(self)
            return True
        return False

    def move_left(self, board):
        # type: (Board) -> bool
        if self.x > 0:
            old_tile: Tile = board.get_tile_at(self.x, self.y)
            old_tile.remove_box()
            self.x -= 1
            new_tile: Tile = board.get_tile_at(self.x, self.y)
            new_tile.add_box(self)
            return True
        return False

    def move_right(self, board):
        # type: (Board) -> bool
        if self.x < board.BOARD_WIDTH - 1:
            old_tile: Tile = board.get_tile_at(self.x, self.y)
            old_tile.remove_box()
            self.x += 1
            new_tile: Tile = board.get_tile_at(self.x, self.y)
            new_tile.add_box(self)
            return True
        return False

    def __str__(self):
        # type: () -> str
        return str(self.name)

    def clone(self):
        # type: () -> Box
        return copy.deepcopy(self)


class Plant:
    """
    This class contains attributes of a plant in this game.
    """

    def __init__(self, x, y):
        # type: (int, int) -> None
        self.name: str = "PLANT"
        self.x: int = x
        self.y: int = y

    def move_up(self, board):
        # type: (Board) -> bool
        if self.y > 0:
            old_tile: Tile = board.get_tile_at(self.x, self.y)
            old_tile.remove_plant()
            self.y -= 1
            new_tile: Tile = board.get_tile_at(self.x, self.y)
            new_tile.add_plant(self)
            return True
        return False

    def move_down(self, board):
        # type: (Board) -> bool
        if self.y < board.BOARD_HEIGHT - 1:
            old_tile: Tile = board.get_tile_at(self.x, self.y)
            old_tile.remove_plant()
            self.y += 1
            new_tile: Tile = board.get_tile_at(self.x, self.y)
            new_tile.add_plant(self)
            return True
        return False

    def move_left(self, board):
        # type: (Board) -> bool
        if self.x > 0:
            old_tile: Tile = board.get_tile_at(self.x, self.y)
            old_tile.remove_plant()
            self.x -= 1
            new_tile: Tile = board.get_tile_at(self.x, self.y)
            new_tile.add_plant(self)
            return True
        return False

    def move_right(self, board):
        # type: (Board) -> bool
        if self.x < board.BOARD_WIDTH - 1:
            old_tile: Tile = board.get_tile_at(self.x, self.y)
            old_tile.remove_plant()
            self.x += 1
            new_tile: Tile = board.get_tile_at(self.x, self.y)
            new_tile.add_plant(self)
            return True
        return False

    def __str__(self):
        # type: () -> str
        return str(self.name)

    def clone(self):
        # type: () -> Plant
        return copy.deepcopy(self)


class Rock:
    """
    This class contains attributes of a rock in this game.
    """

    def __init__(self, x, y):
        # type: (int, int) -> None
        self.name: str = "ROCK"
        self.x: int = x
        self.y: int = y

    def move_up(self, board):
        # type: (Board) -> bool
        if self.y > 0:
            old_tile: Tile = board.get_tile_at(self.x, self.y)
            old_tile.remove_rock()
            self.y -= 1
            new_tile: Tile = board.get_tile_at(self.x, self.y)
            new_tile.add_rock(self)
            return True
        return False

    def move_down(self, board):
        # type: (Board) -> bool
        if self.y < board.BOARD_HEIGHT - 1:
            old_tile: Tile = board.get_tile_at(self.x, self.y)
            old_tile.remove_rock()
            self.y += 1
            new_tile: Tile = board.get_tile_at(self.x, self.y)
            new_tile.add_rock(self)
            return True
        return False

    def move_left(self, board):
        # type: (Board) -> bool
        if self.x > 0:
            old_tile: Tile = board.get_tile_at(self.x, self.y)
            old_tile.remove_rock()
            self.x -= 1
            new_tile: Tile = board.get_tile_at(self.x, self.y)
            new_tile.add_rock(self)
            return True
        return False

    def move_right(self, board):
        # type: (Board) -> bool
        if self.x < board.BOARD_WIDTH - 1:
            old_tile: Tile = board.get_tile_at(self.x, self.y)
            old_tile.remove_rock()
            self.x += 1
            new_tile: Tile = board.get_tile_at(self.x, self.y)
            new_tile.add_rock(self)
            return True
        return False

    def __str__(self):
        # type: () -> str
        return str(self.name)

    def clone(self):
        # type: () -> Rock
        return copy.deepcopy(self)


class Tile:
    """
    This class contains attributes of a tile on the board.
    """

    def __init__(self):
        # type: () -> None
        self.box: Box or None = None
        self.plant: Plant or None = None
        self.rock: Rock or None = None

    def add_box(self, box):
        # type: (Box) -> bool
        if self.box is None:
            self.box = box
            return True
        return False

    def remove_box(self):
        # type: () -> None
        self.box = None

    def add_plant(self, plant):
        # type: (Plant) -> bool
        if self.plant is None:
            self.plant = plant
            return True
        return False

    def remove_plant(self):
        # type: () -> None
        self.plant = None

    def add_rock(self, rock):
        # type: (Rock) -> bool
        if self.rock is None:
            self.rock = rock
            return True
        return False

    def remove_rock(self):
        # type: () -> None
        self.rock = None

    def __str__(self):
        # type: () -> str
        if self.box is None and self.plant is None and self.rock is None:
            return "NONE"
        res: str = ""  # initial value
        if isinstance(self.box, Box):
            res += str(self.box)

        if isinstance(self.plant, Plant):
            if self.box is not None:
                res += ", " + str(self.plant)
            else:
                res += str(self.plant)

        if isinstance(self.rock, Rock):
            if self.box is not None or self.plant is not None:
                res += ", " + str(self.rock)
            else:
                res += str(self.rock)

        return res

    def clone(self):
        # type: () -> Tile
        return copy.deepcopy(self)


# Creating main function used to run the game.


def main():
    """
    This main function is used to run the game.
    :return: None
    """

    print("Welcome to 'Box Eats Plants' by 'DtjiSoftwareDeveloper'.")
    print("In this game, you need to move the box around the board to eat plants and avoid rocks.")
    print("Enter 'Y' for yes.")
    print("Enter anything else for no.")
    continue_playing: str = input("Do you want to continue playing 'Box Eats Plants'? ")
    while continue_playing == "Y":
        # Clearing the command line window
        clear()

        # Setting up the game
        score: int = 0  # initial value
        game_over: bool = False  # initial value
        board: Board = Board()
        box: Box = Box(0, 0)  # initial value
        rocks: list = []
        plants: list = []
        while board.num_rocks() < 5:
            rocks.append(board.spawn_rock())

        while board.num_plants() < 5:
            plants.append(board.spawn_plant())

        while board.num_boxes() < 1:
            box = board.spawn_box()

        while not game_over:
            # Clearing the command line window
            clear()

            print("Below is the current representation of the board.\n" + str(board))
            print("Current coordinates of box: (" + str(box.x) + ", " + str(box.y) + ").")
            print("Your score: " + str(score))
            allowed: list = ["UP", "DOWN", "LEFT", "RIGHT"]
            print("Enter 'UP' to move box up.")
            print("Enter 'DOWN' to move box down.")
            print("Enter 'LEFT' to move box left.")
            print("Enter 'RIGHT' to move box right.")
            direction: str = input("Where do you want to move the box to? ")
            while direction not in allowed:
                print("Enter 'UP' to move box up.")
                print("Enter 'DOWN' to move box down.")
                print("Enter 'LEFT' to move box left.")
                print("Enter 'RIGHT' to move box right.")
                direction = input("Sorry, invalid input! Where do you want to move the box to? ")

            if direction == "UP":
                box.move_up(board)
            elif direction == "DOWN":
                box.move_down(board)
            elif direction == "LEFT":
                box.move_left(board)
            else:
                box.move_right(board)

            box_tile: Tile = board.get_tile_at(box.x, box.y)
            if box_tile.rock is not None:
                game_over = True

            if isinstance(box_tile.plant, Plant):
                score += 1
                plants.remove(box_tile.plant)
                box_tile.remove_plant()
                plants.append(board.spawn_plant())

            rock_direction: str = allowed[random.randint(0, 3)]
            if rock_direction == "UP":
                for rock in rocks:
                    rock.move_up(board)
                    rock_tile: Tile = board.get_tile_at(rock.x, rock.y)
                    if isinstance(rock_tile.box, Box):
                        game_over = True

            elif rock_direction == "DOWN":
                for rock in rocks:
                    rock.move_down(board)
                    rock_tile: Tile = board.get_tile_at(rock.x, rock.y)
                    if isinstance(rock_tile.box, Box):
                        game_over = True

            elif rock_direction == "LEFT":
                for rock in rocks:
                    rock.move_left(board)
                    rock_tile: Tile = board.get_tile_at(rock.x, rock.y)
                    if isinstance(rock_tile.box, Box):
                        game_over = True

            else:
                for rock in rocks:
                    rock.move_right(board)
                    rock_tile: Tile = board.get_tile_at(rock.x, rock.y)
                    if isinstance(rock_tile.box, Box):
                        game_over = True

            plant_direction: str = allowed[random.randint(0, 3)]
            if plant_direction == "UP":
                for plant in plants:
                    plant.move_up(board)
                    plant_tile: Tile = board.get_tile_at(plant.x, plant.y)
                    if isinstance(plant_tile.box, Box):
                        score += 1
                        plants.remove(plant)
                        plant_tile.remove_plant()
                        plants.append(board.spawn_plant())

            elif plant_direction == "DOWN":
                for plant in plants:
                    plant.move_down(board)
                    plant_tile: Tile = board.get_tile_at(plant.x, plant.y)
                    if isinstance(plant_tile.box, Box):
                        score += 1
                        plants.remove(plant)
                        plant_tile.remove_plant()
                        plants.append(board.spawn_plant())

            elif plant_direction == "LEFT":
                for plant in plants:
                    plant.move_left(board)
                    plant_tile: Tile = board.get_tile_at(plant.x, plant.y)
                    if isinstance(plant_tile.box, Box):
                        score += 1
                        plants.remove(plant)
                        plant_tile.remove_plant()
                        plants.append(board.spawn_plant())

            else:
                for plant in plants:
                    plant.move_right(board)
                    plant_tile: Tile = board.get_tile_at(plant.x, plant.y)
                    if isinstance(plant_tile.box, Box):
                        score += 1
                        plants.remove(plant)
                        plant_tile.remove_plant()
                        plants.append(board.spawn_plant())

        # Clearing the command line window
        clear()

        print("GAME OVER! Your score is " + str(score))
        print("Enter 'Y' for yes.")
        print("Enter anything else for no.")
        continue_playing = input("Do you want to continue playing 'Box Eats Plants'? ")
    sys.exit()


if __name__ == '__main__':
    main()
