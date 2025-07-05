from code.Const import ENTITY_SPEED, WIN_HEIGHT, WIN_WIDTH, PLAYER_KEY_UP, PLAYER_KEY_DOWN, PLAYER_KEY_LEFT, PLAYER_KEY_RIGHT, PLAYER_KEY_SHOOT, ENTITY_SHOT_DELAY
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
        self.trail = []  # lista de tuplas: (surface, rect, alpha)
        self.trail_max_length = 7  # quantos rastros manter na tela
        self.death_sound = pygame.mixer.Sound('./assets/Sound-Effects/PlayerDeath.wav')
        if self.name == "Cosmocat":
            trail_color = pygame.Color(9, 255, 58)  # verde
        elif self.name == "Auroracat":
            trail_color = pygame.Color(255, 9, 182)  # rosa (hot pink)
        else:
            trail_color = pygame.Color(255, 255, 255)  # branco padrão, por segurança
        self.colored_surf = self.create_colored_version(trail_color)
        self.lifesaver_sound = pygame.mixer.Sound('./assets/Sound-Effects/life-saver.wav')


    def move(self):
        angle = 0  # padrão (reto)
        pressed_key = pygame.key.get_pressed()
        if pressed_key[PLAYER_KEY_UP[self.name]] and self.rect.top > 0:
            self.rect.centery -= ENTITY_SPEED[self.name]
        if pressed_key[PLAYER_KEY_DOWN[self.name]] and self.rect.bottom < WIN_HEIGHT:
            self.rect.centery += ENTITY_SPEED[self.name]
        if pressed_key[PLAYER_KEY_RIGHT[self.name]] and self.rect.right < WIN_WIDTH:
            self.rect.centerx += ENTITY_SPEED[self.name]  
            angle = -5
        if pressed_key[PLAYER_KEY_LEFT[self.name]] and self.rect.left > 0:
            self.rect.centerx -= ENTITY_SPEED[self.name] 
            angle = 5      
        pass

        self.surf = pygame.transform.rotate(self.original_surf, angle)

        # Recalcula o rect para manter a posição após rotação
        self.rect = self.surf.get_rect(center=self.rect.center)

        # Cria uma cópia translúcida da imagem atual
        trail_surf = self.surf.copy()
        trail_surf.set_alpha(30)  # transparência inicial do rastro 

        # Salva a cópia atual do rect também
        trail_rect = self.rect.copy()

        # Adiciona na lista de rastros
        self.trail.append((trail_surf, trail_rect, 30))  # (imagem, posição, alpha inicial)

        # Mantém o número máximo de rastros
        if len(self.trail) > self.trail_max_length:
            self.trail.pop(0)

        if self.flash_timer > 0:
            self.flash_timer -= 1

    def shoot(self):
        self.shot_delay -= 1
        if self.shot_delay == 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]
            pressed_key = pygame.key.get_pressed()
            if pressed_key[PLAYER_KEY_SHOOT[self.name]]:
                self.shot_sound.play()
                return CosmocatShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))

    def draw(self, surface):
        # desenha o rastro primeiro (se houver)
        for _, rect, alpha in self.trail:
            surf = self.colored_surf.copy()
            surf.set_alpha(alpha)
            surface.blit(surf, rect)

        # agora chama o draw da entidade base para fazer o efeito de flash vermelho e desenhar o sprite
        super().draw(surface)


    def create_colored_version(self, color: pygame.Color):
        colored_surf = pygame.Surface(self.surf.get_size(), pygame.SRCALPHA)
        width, height = self.surf.get_size()
        for x in range(width):
            for y in range(height):
                pixel = self.surf.get_at((x, y))
                if pixel.a != 0:
                    # Usa a cor passada, mantendo alpha do pixel original
                    colored_surf.set_at((x, y), pygame.Color(color.r, color.g, color.b, pixel.a))
        return colored_surf
    

    def take_damage(self, amount):
        self.health -= amount
        self.last_dmg = 'Something'
        self.flash_timer = 100

        if self.health <= 0:
            self.death_sound.play()
        # lembrar= colocar o que acontece quando o player morre (ex: fim de jogo, reset, etc.)





