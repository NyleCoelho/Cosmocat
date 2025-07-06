from code.Const import ENTITY_SPEED, WIN_HEIGHT, WIN_WIDTH, PLAYER_KEY_UP, PLAYER_KEY_DOWN, PLAYER_KEY_LEFT, PLAYER_KEY_RIGHT, PLAYER_KEY_SHOOT, ENTITY_SHOT_DELAY, C_PINK
from code.Entity import Entity
from code.CosmocatShot import CosmocatShot
import pygame

class Player(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position, scale_to_screen=False)
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]
        self.shot_sound = pygame.mixer.Sound('./assets/Sound-Effects/Shoot.wav')
        self.shot_sound.set_volume(2.5)
        self.original_surf = self.surf.copy()
        self.trail = []
        self.trail_max_length = 7
        self.death_sound = pygame.mixer.Sound('./assets/Sound-Effects/PlayerDeath.wav')

        # Cria o rastro baseado no player em questão
        if self.name == "Cosmocat":
            trail_color = pygame.Color(9, 255, 58)
        elif self.name == "Auroracat":
            trail_color = pygame.Color(255, 9, 182)
        else:
            trail_color = pygame.Color(255, 255, 255)
        self.original_trail_color = trail_color
        self.colored_surf = self.create_colored_version(trail_color)

        self.PowerUp_sound = pygame.mixer.Sound('./assets/Sound-Effects/PowerUp.wav')
        self.PowerUp_sound.set_volume(4.5)
        self.powerup_active = False
        self.powerup_timer = 0
        self.powerup_duration = 10000  # Duração do PowerUp

        self.normal_shot_delay = ENTITY_SHOT_DELAY[self.name]
        self.powered_shot_delay = self.normal_shot_delay // 2
        self.normal_speed = ENTITY_SPEED[self.name]
        self.powered_speed = self.normal_speed * 1.5
        self.current_speed = self.normal_speed
        self.shield_color = pygame.Color(0, 255, 230)
        shield_img = pygame.image.load('./assets/Shield.png').convert_alpha()
        self.shield_sprite = pygame.transform.scale(shield_img, (160, 160))
        self.mask = pygame.mask.from_surface(self.surf)


        self.lifesaver_sound = pygame.mixer.Sound('./assets/Sound-Effects/life-saver.wav')
        self.lifesaver_sound.set_volume(1.0)
        self.lifesaver_sound = pygame.mixer.Sound(buffer=bytearray([0x80]*8000))

    def move(self):
        angle = 0
        pressed_key = pygame.key.get_pressed()
        # Move para cima
        if pressed_key[PLAYER_KEY_UP[self.name]] and self.rect.top > 0:
            self.rect.centery -= self.current_speed
        # Move para baixo
        if pressed_key[PLAYER_KEY_DOWN[self.name]] and self.rect.bottom < WIN_HEIGHT:
            self.rect.centery += self.current_speed
        # Move para a direita
        if pressed_key[PLAYER_KEY_RIGHT[self.name]] and self.rect.right < WIN_WIDTH:
            self.rect.centerx += self.current_speed 
            angle = -5
        # Move para a esquerda
        if pressed_key[PLAYER_KEY_LEFT[self.name]] and self.rect.left > 0:
            self.rect.centerx -= self.current_speed
            angle = 5

        # Rotação do sprite baseado na direção do player 
        self.surf = pygame.transform.rotate(self.original_surf, angle)
        self.rect = self.surf.get_rect(center=self.rect.center)

        # Adiciona a posição atual para efeito de rastro 
        trail_surf = self.surf.copy()
        trail_surf.set_alpha(30)
        trail_rect = self.rect.copy()
        self.trail.append((trail_surf, trail_rect, 30))

        if len(self.trail) > self.trail_max_length:
            self.trail.pop(0)

        # Ativa o flash após receber o dano
        if self.flash_timer > 0:
            self.flash_timer -= 1

        # desativação do power up
        if self.powerup_active and (pygame.time.get_ticks() - self.powerup_timer > self.powerup_duration):
            self.powerup_active = False
            self.colored_surf = self.create_colored_version(self.original_trail_color)
            self.trail_max_length = 7
            self.shot_delay = self.normal_shot_delay
            self.current_speed = self.normal_speed

    def shoot(self):
        self.shot_delay -= 1
        if self.shot_delay <= 0:
            delay = self.powered_shot_delay if self.powerup_active else self.normal_shot_delay
            self.shot_delay = delay
            pressed_key = pygame.key.get_pressed()
            if pressed_key[PLAYER_KEY_SHOOT[self.name]]:
                self.shot_sound.play()
                return CosmocatShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))

    def draw(self, surface):
        # Cria o rastro
        for _, rect, alpha in self.trail:
            surf = self.colored_surf.copy()
            surf.set_alpha(alpha)
            surface.blit(surf, rect)
        super().draw(surface)
        # Cria o shield para o power up
        if self.powerup_active:
            shield_rect = self.shield_sprite.get_rect(center=self.rect.center)
            surface.blit(self.shield_sprite, shield_rect)

    def create_colored_version(self, color: pygame.Color):
        # Cria uma versão colorida do sprite ṕara o rastro
        colored_surf = pygame.Surface(self.surf.get_size(), pygame.SRCALPHA)
        width, height = self.surf.get_size()
        for x in range(width):
            for y in range(height):
                pixel = self.surf.get_at((x, y))
                if pixel.a != 0:
                    colored_surf.set_at((x, y), pygame.Color(color.r, color.g, color.b, pixel.a))
        return colored_surf

    def take_damage(self, amount):
        # Ignora o dano quando o power up estver ativo 
        if self.powerup_active:
            return
        self.health -= amount
        self.last_dmg = 'Something'
        self.flash_timer = 100
        if self.health <= 0:
            self.death_sound.play()

    def activate_powerup(self):
        # ativa o power up: aumenta a velocidade do movimento, do tiro e torna o player invencível 
        self.PowerUp_sound.play()
        self.powerup_active = True
        self.powerup_timer = pygame.time.get_ticks()
        trail_color = pygame.Color(0, 255, 230)
        self.colored_surf = self.create_colored_version(trail_color)
        self.trail_max_length = 15
        self.shot_delay = self.powered_shot_delay
        self.current_speed = self.powered_speed
