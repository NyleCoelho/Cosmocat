import pygame
from code.Enemy import Enemy
from code.Const import WIN_WIDTH, WIN_HEIGHT, ENTITY_SHOT_DELAY

class Boss(Enemy):
    def __init__(self, name: str, position: tuple): # Inicializa o Boss, redimensiona o sprite e configura sons, movimento e tiro
        super().__init__(name, position)
        self.surf = pygame.transform.scale(self.surf, (500, 480))
        self.rect = self.surf.get_rect(topleft=self.rect.topleft)
        self.mask = pygame.mask.from_surface(self.surf)

        self.death_sound = pygame.mixer.Sound('./assets/Sound-Effects/Boom.wav')
        self.damage_sound = pygame.mixer.Sound('./assets/Sound-Effects/Hit.wav')
        self.damage_sound.set_volume(3.5)

        self.shot_delay = ENTITY_SHOT_DELAY[self.name]
        self.vertical_direction = 1
        self.float_speed = 2
        self.stop_x = WIN_WIDTH - 600

    def move(self): # Move o Boss horizontalmente até uma posição e depois faz ele flutuar verticalmente
        if self.rect.x > self.stop_x:
            self.rect.x -= 2
        else:
            self.rect.y += self.float_speed * self.vertical_direction
            if self.rect.top <= 100:
                self.vertical_direction = 1
            elif self.rect.bottom >= WIN_HEIGHT - 100:
                self.vertical_direction = -1

            if getattr(self, 'flash_timer', 0) > 0:
                self.flash_timer -= 1

    def shoot(self):  # Faz o Boss atirar de tempos em tempos
        now = pygame.time.get_ticks()
        if not hasattr(self, 'last_shot'):
            self.last_shot = now
        if now - self.last_shot >= 1000:
            self.last_shot = now
            from code.EnemyShot import EnemyShot
            return EnemyShot('BossShot', self.rect.midleft)
        return None

    def take_damage(self, amount): # Aplica dano ao Boss, ativa o efeito de flash e toca som de dano e morte
        if self.health > 0:
            self.health -= amount
            self.last_dmg = 'CosmocatShot'
            self.flash_timer = 100
            self.damage_sound.play()
            if self.health <= 0:
                self.death_sound.play()
