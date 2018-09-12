from datetime import datetime

import pyscreenshot as ps

# TODO: Get trex pixel color and replace
trex_color = (84, 84, 84)


def is_trex_color(color):
    return color == trex_color


def obstacle(distance, length, speed, time):
    return {'distance': distance, 'length': length,
            'speed': speed, 'time': time}


class Camera:
    def __init__(self):
        self.trex_start = (0, 0)
        self.trex_end = (0, 0)
        self.last_obstacle = {}
        self.__current_fitness = 0
        self.__change_fitness = False

    # TODO: Why not make it static?
    def find_environment(self):
        image = ps.grab(bbox=(0, 0, 1366, 767))
        size = image.size
        pixels = []

        for y in range(0, size[1], 10):
            for x in range(0, size[0], 10):
                color = image.getpixel((x, y))
                if is_trex_color(color):
                    pixels.append((x, y))

        if not pixels:
            raise Exception("Please open the TRex game!")

    def find_trex(self, pixels):
        start = pixels[0]
        end = pixels[1]
        for pixel in pixels:
            if pixel[0] < start[0] and pixel[1] > start[1]:
                start = pixel
            if pixel[0] > end[0] and pixel[1] > end[1]:
                end = pixel
        self.trex_start = start
        self.trex_end = end

    def find_next_obstacle(self):
        image = ps.grab(bbox=(200, 350, 600, 440))
        distance = self.__next_obstacle_dist(image)
        if distance < 50 and not self.__change_fitness:
            self.__current_fitness += 1
            self.__change_fitness = True
        elif distance > 50:
            self.__change_fitness = False
        time = datetime.now()
        delta_distance = 0
        speed = 0
        if self.last_obstacle:
            delta_distance = self.last_obstacle['distance'] - distance
            speed = (delta_distance / (time - self.last_obstacle['time']).microseconds) * 10000
        self.last_obstacle = obstacle(distance, 1, speed, time)
        return self.last_obstacle

    # TODO: Why not make it static?
    def __next_obstacle_dist(self, image):
        s = 0
        game_over_box = (155, 50, 190, 80)
        game_over_image = image.crop(game_over_box)
        game_over_width = game_over_image.size[0]
        game_over_height = game_over_image.size[1]
        for y in range(0, game_over_height, 5):
            for x in range(0, game_over_width, 5):
                color = game_over_image.getpixel((x, y))
                if is_trex_color(color):
                    s += 1

        if s > 12:
            raise Exception('Game Over!')

        for x in range(0, image.size[0], 5):
            for y in range(0, image.size[1], 5):
                color = image.getpixel((x, y))
                if is_trex_color(color):
                    return x
        return 999999

    def reset(self):
        self.last_obstacle = {}
        self.__current_fitness = 0
        self.__change_fitness = False

    def get_fitness(self):
        return self.__current_fitness
