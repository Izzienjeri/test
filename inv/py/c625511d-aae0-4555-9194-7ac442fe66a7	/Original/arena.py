import pygame

from topdown.config import WINDOW_SIZE


# Set the window size
class GameArea:
    square_size = 100

    @staticmethod
    def create_surface(width, height):
        surface = pygame.Surface((width, height))
        for y in range(0, height, GameArea.square_size):
            for x in range(0, width, GameArea.square_size):
                color = (255, 255, 255) if (x // GameArea.square_size + y // GameArea.square_size) % 2 == 0 else (
                0, 0, 0)
                pygame.draw.rect(surface, color, (x, y, GameArea.square_size, GameArea.square_size))
        return surface

    @staticmethod
    def draw(screen, surface, camera_x, camera_y):
        screen_width, screen_height = screen.get_size()
        tile_width = surface.get_width()
        tile_height = surface.get_height()

        # Calculate the number of tiles needed to cover the screen
        num_tiles_x = screen_width // GameArea.square_size + 2
        num_tiles_y = screen_height // GameArea.square_size + 2

        # Calculate the starting tile indices based on the camera position
        start_tile_x = int(camera_x // GameArea.square_size)
        start_tile_y = int(camera_y // GameArea.square_size)

        # Draw the tiles
        for y in range(num_tiles_y):
            for x in range(num_tiles_x):
                tile_x = (start_tile_x + x) * GameArea.square_size
                tile_y = (start_tile_y + y) * GameArea.square_size

                # Calculate the screen position for the tile
                screen_x = x * GameArea.square_size - camera_x % GameArea.square_size
                screen_y = y * GameArea.square_size - camera_y % GameArea.square_size

                # Wrap the tile position if it exceeds the game area bounds
                tile_x = tile_x % tile_width
                tile_y = tile_y % tile_height

                # Draw the tile on the screen
                screen.blit(surface, (screen_x, screen_y),
                            (tile_x, tile_y, GameArea.square_size, GameArea.square_size))