import random

import pygame
from topdown.arena import GameArea
from topdown.exp import Exp
from topdown.explosion import Explosion
from topdown.game_sprites import Crosshair
from topdown.level_up_screen import LevelUpScreen
from topdown.menu import Menu
from topdown.missile_explosion import MissileExplosion
from topdown.player import Player
from topdown.renderer import Renderer
from topdown.enemy import Enemy, spawn_enemy, ShootingEnemy, LightningEnemy
from config import WINDOW_SIZE, PLAYER_SIZE, PLAYER_SPEED, CROSSHAIR_SIZE, ENEMY_SIZE


class Game:
    def __init__(self):
        self.last_damage_time = 0
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Top-Down Shooter")
        pygame.mouse.set_visible(False)

        self.game_mode = None
        self.menu = Menu(self)
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Top-Down Shooter")
        pygame.mouse.set_visible(False)
        self.damaged_enemies = set()  # Set to keep track of damaged enemies
        # Calculate the center coordinates within the margins
        self.missiles = pygame.sprite.Group()
        self.player = Player(self, 600, 600, PLAYER_SIZE, PLAYER_SPEED)
        self.crosshair = Crosshair(CROSSHAIR_SIZE)
        self.renderer = Renderer(self)
        self.enemies = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.exp_group = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.level_up_screen = LevelUpScreen(self)
        self.last_enemy_spawn_time = 0
        self.enemy_spawn_interval = 1000
        self.delta_time = 0
        self.fire_bombs = pygame.sprite.Group()
        self.fire_areas = pygame.sprite.Group()
        self.ice_patches = pygame.sprite.Group()

    def run(self):
        running = True

        while running:
            self.delta_time = self.clock.tick(60) / 1000.0  # Calculate delta time in seconds
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False

            if self.game_mode is None:
                self.menu.update()
                self.menu.draw(self.screen)
            else:
                self.handle_events(events)

                if self.game_mode == "normal":
                    self.update()
                    self.render()
                elif self.game_mode == "debug":
                    self.debug_update()
                    self.debug_render()

            self.clock.tick(120)  # Limit the frame rate to 60 FPS

        pygame.quit()

    def base_update(self):
        self.player.update(self.delta_time)
        self.player.bullets.update()
        self.player.ice_shards.update()
        self.enemies.update()
        self.check_bullet_collisions()
        self.check_player_collisions()
        self.missiles.update()
        self.enemy_bullets.update()
        self.check_enemy_bullet_collisions()
        self.exp_group.update()
        self.check_exp_collisions()
        self.update_explosions()
        self.fire_bombs.update(self.delta_time)
        self.fire_areas.update()
        self.fire_damage_update()
        self.ice_patches.update()
        self.check_missile_collisions()

    def update(self):
        if self.player.leveled_up:
            self.level_up_screen.update()
        else:

            self.base_update()

            # Control enemy spawning
            current_time = pygame.time.get_ticks()
            if current_time - self.last_enemy_spawn_time >= self.enemy_spawn_interval:
                num_enemies = random.randint(1, 3)  # Spawn between 1 and 3 enemies at a time
                for _ in range(num_enemies):
                    spawn_enemy(self.game_area_surface.get_rect(), self.player, self)
                self.last_enemy_spawn_time = current_time

    def debug_update(self):

        if self.player.leveled_up:
            self.level_up_screen.update()
            self.level_up_screen.background = self.screen.copy()
        else:
            self.base_update()
            # Spawn the selected enemy type
            if self.debug_enemy_type is not None and len(self.enemies) == 0:
                x = random.randint(100, 900)
                y = random.randint(100, 900)
                if self.debug_enemy_type == "regular":
                    image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
                    image.fill((255, 0, 0))
                    enemy = Enemy(x, y, image, self.player, self.enemies, self)
                    self.enemies.add(enemy)
                elif self.debug_enemy_type == "shooting":
                    enemy = ShootingEnemy(x, y, self.player, self.enemies, self)
                    self.enemies.add(enemy)
                elif self.debug_enemy_type == "lightning":
                    enemy = LightningEnemy(x, y, self.player, self.enemies, self)
                    self.enemies.add(enemy)

    def check_exp_collisions(self):
        collided_exp = pygame.sprite.spritecollide(self.player, self.exp_group, True)
        for exp in collided_exp:
            self.player.gain_exp(exp.amount)
            self.level_up_screen.background = self.screen.copy()

    def check_missile_collisions(self):
        for missile in self.player.missiles:
            collided_enemy = pygame.sprite.spritecollideany(missile, self.enemies)

            if collided_enemy:
                missile.explode()  # Trigger the explosion
                self.player.missiles.remove(missile)  # Remove the missile from the player's missile list
                missile.kill()  # Remove the missile from the sprite group
    def render(self):
        if self.player.leveled_up:
            self.level_up_screen.draw(self.screen)
        else:
            self.renderer.render(self.screen)

        pygame.display.flip()

    def check_bullet_collisions(self):
        for bullet in self.player.bullets:
            collided_enemies = pygame.sprite.spritecollide(bullet, self.enemies, False)
            for enemy in collided_enemies:
                enemy.take_damage(50)  # Reduce enemy health by 50 (adjust as needed)
                bullet.kill()

    def check_enemy_bullet_collisions(self):
        collided_bullets = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
        for bullet in collided_bullets:
            self.player.take_damage(10)  # Adjust the damage amount as needed

    def check_player_collisions(self):
        collided_enemies = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for enemy in collided_enemies:
            self.spawn_explosion(enemy.rect.centerx, enemy.rect.centery)
            enemy.die()
            self.player.health -= 1
            if self.player.health <= 0:
                self.game_over()

    def spawn_explosion(self, x, y):
        explosion = Explosion(x, y)
        self.explosions.add(explosion)

    def spawn_exp(self, x, y):
        exp = Exp(x, y, game=self)
        self.exp_group.add(exp)

    def update_explosions(self):
        self.explosions.update()
        for explosion in self.explosions:
            if isinstance(explosion, MissileExplosion):
                explosion.draw(self.screen, self.renderer.camera_x, self.renderer.camera_y)

    def game_over(self):
        print("Game Over!")
        pygame.quit()
        exit()

    def start_game(self):
        self.game_mode = "normal"
        GameArea.size = (7500, 7500)  # Set the game area size for normal mode
        self.game_area_surface = GameArea.create_surface(*GameArea.size)
        self.player = Player(self, 600, 600, PLAYER_SIZE, PLAYER_SPEED)
        self.renderer = Renderer(self)
        self.player.leveled_up = True  # Start with the level up screen

    def start_debug_mode(self):
        self.game_mode = "debug"
        GameArea.size = (1000, 1000)  # Set the game area size for debug mode
        self.game_area_surface = GameArea.create_surface(*GameArea.size)
        self.player = Player(self, 500, 500, PLAYER_SIZE, PLAYER_SPEED)
        self.renderer = Renderer(self)
        self.debug_enemy_type = None
        self.player.leveled_up = True  # Start with the level up screen



    def debug_render(self):

        if self.player.leveled_up:
            self.level_up_screen.draw(self.screen)
        else:
            self.renderer.render(self.screen)

            # Display debug mode text
            debug_text = self.renderer.font.render("Debug Mode", True, (255, 0, 0))
            self.screen.blit(debug_text, (10, 170))

            # Display enemy selection text
            enemy_selection_text = self.renderer.font.render("Select Enemy Type:", True, (255, 255, 255))
            self.screen.blit(enemy_selection_text, (10, 210))

            # Display enemy options
            enemy_options = ["Regular", "Shooting", "Lightning"]
            for i, option in enumerate(enemy_options):
                color = (0, 255, 0) if self.debug_enemy_type == option.lower() else (255, 255, 255)
                option_text = self.renderer.font.render(option, True, color)
                self.screen.blit(option_text, (10, 250 + i * 40))

        pygame.display.flip()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_mode = None
                elif self.game_mode == "debug":
                    if event.key == pygame.K_1:
                        self.debug_enemy_type = "regular"
                    elif event.key == pygame.K_2:
                        self.debug_enemy_type = "shooting"
                    elif event.key == pygame.K_3:
                        self.debug_enemy_type = "lightning"

        if self.player.leveled_up:
            self.level_up_screen.handle_events(events)

    def fire_damage_update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_damage_time >= 250:  # 0.25 seconds
            self.damaged_enemies.clear()
            self.last_damage_time = current_time
