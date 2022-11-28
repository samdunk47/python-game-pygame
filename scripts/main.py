import sys
from random import choices

import pygame
from pygame.locals import QUIT


class Game():
    def __init__(self):
        self.running = True
        self.window_width = 800
        self.window_height = 450
        self.window_caption = "By Sam Chandler"
        self._display_surface = pygame.display.set_mode(
            (self.window_width, self.window_height)
        )
        self.fps = 60
        self.fps_clock = pygame.time.Clock()
        self.colours = {
            "background": (100, 200, 250),
            "grass": (100, 250, 100)
        }
        self.pressed_keys = {
            pygame.K_a: False,
            pygame.K_LEFT: False,
            pygame.K_d: False,
            pygame.K_RIGHT: False,
        }
        self.sprite = Sprite(self)
        self.environment = Environment(self)
        self.enemies = []
        self.enemy_index = 0
        self.on_init()

    def on_init(self) -> None:
        pygame.init()
        pygame.display.set_caption(self.window_caption)
        
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1500)
        
        self.sprite.create_animations()
        self.environment.create_environment()

        self.execute()

    def on_event(self, event):
        if event.type == QUIT:
            self.running = False

        if event.type == self.obstacle_timer:
            self.create_enemy()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.sprite.jumping = True
            else:
                self.pressed_keys[event.key] = True
        elif event.type == pygame.KEYUP:
            self.pressed_keys[event.key] = False

    def execute(self):
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)

            self.sprite.animation_state()
            self.move_sprite()
            
            self.render()
            self.fps_clock.tick(self.fps)
        else:
            self.exit()

    def render(self):
        self._display_surface.fill(self.colours["background"])
        
        self._display_surface.blit(
            self.environment.sky_image, self.environment.sky_1_rect
        )
        self._display_surface.blit(
            self.environment.sky_image, self.environment.sky_2_rect
        )

        self._display_surface.blit(
            self.environment.ground_image, self.environment.ground_1_rect
        )
        self._display_surface.blit(
            self.environment.ground_image, self.environment.ground_2_rect
        )
        self._display_surface.blit(
            self.environment.ground_image, self.environment.ground_3_rect
        )
        self._display_surface.blit(
            self.environment.ground_image, self.environment.ground_4_rect
        )

        self._display_surface.blit(self.sprite.image, self.sprite.rect)

        pygame.display.update()

    def move_sprite(self):
        if self.pressed_keys[pygame.K_a] or self.pressed_keys[pygame.K_LEFT]:
            self.sprite.move_left()
        if self.pressed_keys[pygame.K_d] or self.pressed_keys[pygame.K_RIGHT]:
            self.sprite.move_right()
        # if self.pressed_keys[pygame.K_SPACE]:
        #     self.sprite.apply_gravity()

        (    # up and down movement
            # if self.pressed_keys[pygame.K_w] or self.pressed_keys[pygame.K_UP]:
            #     self.sprite.move_up()
            # if self.pressed_keys[pygame.K_s] or self.pressed_keys[pygame.K_DOWN]:
            #     self.sprite.move_down()
        )
        self.sprite.apply_gravity()

        self.sprite.update()
        self.environment.update()

    def create_enemy(self):
        enemy = Enemy(
            self.enemy_index, choices(("snail", "fly"), weights=(2, 1))
        )
        
        self.enemy_index += 1
    
    def exit(self):
        pygame.quit()
        sys.exit()


class Sprite(pygame.sprite.Sprite):
    def __init__(self, game_self):
        super().__init__()
        self.game_self = game_self
        self.x_cor = 50
        self.y_cor = 215
        self.y_starting_pos = 215
        self.width = 50
        self.height = 50
        self.move_distance = 5
        self.colour = (255, 255, 0)
        self.image = None
        self.rect = None
        self.gravity = 28
        self.jumping = False

    def move_left(self):
        if not self.x_cor - self.move_distance < 0:
            self.x_cor -= self.move_distance

    def move_right(self):
        if not self.x_cor + self.move_distance + 65 > self.game_self.window_width:
            self.x_cor += self.move_distance

    def apply_gravity(self):
        if self.jumping:
            self.gravity -= 1
            self.y_cor -= self.gravity / 2

        if self.y_cor <= 5:
            self.gravity = -self.gravity
            self.y_cor -= self.gravity / 2

        if self.jumping and self.gravity == -27 and self.y_cor == self.y_starting_pos:
            self.jumping = False
            self.gravity = 28

    (    # def move_up(self):
        #     self.y_cor -= self.move_distance

        # def move_down(self):
        #     self.y_cor += self.move_distance
    )

    def update(self):
        self.animation_state()

    def create_animations(self):
        self.walk = [
            pygame.image.load(
                "./assets/graphics/sprite/player_walk_1.png").convert_alpha(),
            pygame.image.load(
                "./assets/graphics/sprite/player_walk_2.png").convert_alpha(),
        ]

        self.index = 0
        self.jump_image = pygame.image.load(
            "./assets/graphics/sprite/jump.png").convert_alpha()

        self.image = self.walk[self.index]
        self.rect = self.image.get_rect(topleft=(
            80, 350
        ))

    def animation_state(self):
        if self.rect.bottom == 299:
            self.index += 0.05
            if self.index >= len(self.walk):
                self.index = 0
            self.image = self.walk[int(self.index)]
        else:
            self.image = self.jump_image
        self.rect = self.image.get_rect(topleft=(
            self.x_cor, self.y_cor
        ))


class Environment(pygame.sprite.Sprite):
    def __init__(self, game_self):
        super().__init__()
        self.game_self = game_self
        self.index = 0

    def create_environment(self):
        self.sky_image = pygame.image.load(
            "./assets/graphics/environment/sky.png").convert_alpha()

        self.ground_image = pygame.image.load(
            "./assets/graphics/environment/ground.png").convert_alpha()

    def update_environment(self):
        self.sky_1_rect = self.sky_image.get_rect(topleft=(
            (self.index // 3), 0
        ))
        self.sky_2_rect = self.sky_image.get_rect(topleft=(
            (self.index // 3) + self.game_self.window_width, 0
        ))

        self.ground_1_rect = self.ground_image.get_rect(topleft=(
            self.index, 300
        ))
        self.ground_2_rect = self.ground_image.get_rect(topleft=(
            self.index + self.game_self.window_width, 300
        ))
        self.ground_3_rect = self.ground_image.get_rect(topleft=(
            self.index + (self.game_self.window_width * 2), 300
        ))
        self.ground_4_rect = self.ground_image.get_rect(topleft=(
            self.index + (self.game_self.window_width * 3), 300
        ))

        if self.sky_1_rect.left < -self.game_self.window_width:
            self.index = 0

        self.index -= 5

    def update(self):
        self.update_environment()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.images = []
        self.create()
    
    def create(self):
        if self.type[0] == "fly":
            self.images.extend([
                pygame.image.load("./assets/graphics/fly/fly_1.png").convert_alpha(),
                pygame.image.load("./assets/graphics/fly/fly_2.png").convert_alpha(),
            ])
        elif self.type[0] == "snail":
            self.images.extend([
                pygame.image.load("./assets/graphics/snail/snail_1.png").convert_alpha(),
                pygame.image.load("./assets/graphics/snail/snail_2.png").convert_alpha(),
            ])
  

if __name__ == "__main__":
    game = Game()
