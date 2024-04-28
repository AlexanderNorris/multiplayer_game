# import the pygame module, so you can use it
import pygame
import socket
import time
import bson
from pygame.locals import (
    KEYDOWN,
    KEYUP,
    K_a,
    K_w,
    K_s,
    K_d,
    K_ESCAPE,
)
from modules.spritesheet import Spritesheet
from modules.tiles import TileMap
from pathlib import Path


TILE_SIZE = 16
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
USER = "ben"
# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet  # UDP
sock.settimeout(1)

spritesheet = Spritesheet(Path("./client/assets/spritesheet.png"))
player_img = spritesheet.parse_sprite("chick.png")
player_rect = player_img.get_rect()

map = TileMap(Path("./client/assets/maps/test_level.csv"), spritesheet)


def detect_movement(keys):
    message = {"x": 0, "y": 0}
    if keys[K_d]:
        message["x"] = 1
    elif keys[K_a]:
        message["x"] = -1
    else:
        message["x"] = 0
    if keys[K_w]:
        message["y"] = -1
    elif keys[K_s]:
        message["y"] = 1
    else:
        message["y"] = 0
    print(message)
    return message


def detect_stopped_movement(event, message):
    message = {"x": 0, "y": 0}
    if event.key == K_d or event.key == K_a:
        message["x"] = 0
    if event.key == K_w or event.key == K_s:
        message["y"] = 0
    return message


def early_exit():
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                return False
    return True


def detect_action(m_state):
    """
    What's going on with your mouse?
    """
    lclick, rclick, mclick = m_state
    if lclick:
        click_x, click_y = pygame.mouse.get_pos()
        click_area = (click_x, click_y, click_x + TILE_SIZE, click_y + TILE_SIZE)
        print(click_area)
    return


def update_client():

    return


# define a main function
def main():

    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("minimal program")

    # define a variable to control the main loop
    running = True
    clock = pygame.time.Clock()

    # main loop
    message = {}
    message["user"] = USER

    while running:
        # event handling, gets all event from the event queue
        running = early_exit()
        keys = pygame.key.get_pressed()
        m_state = pygame.mouse.get_pressed()
        message.update(detect_movement(keys))
        detect_action(m_state)
        bson_msg = bson.dumps(message)
        clock.tick(10)
        sock.sendto(bson_msg, (UDP_IP, UDP_PORT))
        try:
            data, _ = sock.recvfrom(1024)
            update_client()
            data = bson.loads(data)
        except:
            print("Unable to render player data")

        # Fills the entire screen with light blue
        canvas.fill((0, 180, 240))
        map.draw_map(canvas)
        try:
            # Draw all of the players
            for user in data:
                x, y = data[user]["x"], data[user]["y"]
                player_rect.update(x, y, x + 16, y + 16)
                canvas.blit(player_img, player_rect)
            # print(f"Current state: {bson.loads(data)}")
        except:
            print("Did not receive a response from the server, no update to render")

        screen.blit(canvas, (0, 0))
        pygame.display.update()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
