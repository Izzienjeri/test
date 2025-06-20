import pygame
import math
from config import BULLET_SIZE, BULLET_SPEED, MAX_BULLET_DISTANCE
from topdown.arena import GameArea
from topdown.explosion import Explosion


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, damage, player_velocity_x, player_velocity_y):
        super().__init__()
        self.image = pygame.Surface((BULLET_SIZE, BULLET_SIZE))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.angle = angle
        self.speed = BULLET_SPEED
        self.damage = damage
        angle_rad = math.radians(angle)
        self.velocity_x = BULLET_SPEED * math.cos(angle_rad) + player_velocity_x
        self.velocity_y = BULLET_SPEED * math.sin(angle_rad) + player_velocity_y

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Wrap the bullet position around the game area
        if self.x < 0:
            self.x = GameArea.size[0]
        elif self.x > GameArea.size[0]:
            self.x = 0

        if self.y < 0:
            self.y = GameArea.size[1]
        elif self.y > GameArea.size[1]:
            self.y = 0

        self.rect.centerx = round(self.x)
        self.rect.centery = round(self.y)

        # Check if the bullet has traveled beyond the maximum distance
        distance = math.sqrt((self.x - self.start_x) ** 2 + (self.y - self.start_y) ** 2)
        if distance > MAX_BULLET_DISTANCE:
            explosion = Explosion(self.rect.centerx, self.rect.centery, radius=5)
            self.kill()

    def draw(self, screen, camera_x, camera_y):
        # Calculate the offset for wrapping
        offset_x = (camera_x // GameArea.size[0]) * GameArea.size[0]
        offset_y = (camera_y // GameArea.size[1]) * GameArea.size[1]

        # Draw the object at its wrapped position
        screen_x = self.rect.x - camera_x + offset_x
        screen_y = self.rect.y - camera_y + offset_y
        screen.blit(self.image, (screen_x, screen_y))