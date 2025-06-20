import pygame
import math


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, speed):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 0, 0))  # Red color for enemy bullets
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.angle = angle
        self.speed = speed
        self.velocity_x = speed * math.cos(math.radians(angle))
        self.velocity_y = speed * math.sin(math.radians(angle))
        self.distance_traveled = 0
        self.max_distance = 1000

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        self.distance_traveled += math.sqrt(self.velocity_x ** 2 + self.velocity_y ** 2)

        # Remove the bullet if it has traveled the maximum distance
        if self.distance_traveled >= self.max_distance:
            self.kill()

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))