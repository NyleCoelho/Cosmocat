from abc import ABC, abstractmethod
import pygame.image
from code.Const import WIN_WIDTH, WIN_HEIGHT, ENTITY_DAMAGE, ENTITY_HEALTH, ENTITY_SCORE, C_PINK, C_GREEN, C_BLACK, C_RED, C_WHITE

class Entity(ABC): 
    def __init__(self, name: str, position: tuple, scale_to_screen=True, custom_scale=None):
        self.name = name
        self.surf = pygame.image.load(f'./assets/Backgrounds/level1/{name}.png').convert_alpha()
        
        if scale_to_screen:
            self.surf = pygame.transform.scale(self.surf, (WIN_WIDTH, WIN_HEIGHT))
        elif custom_scale:
            self.surf = pygame.transform.scale(self.surf, custom_scale)
        else:
            self.surf = pygame.transform.scale(self.surf, (120, 100))  

        self.rect = self.surf.get_rect(topleft=position)
        self.speed = 0

        self.health = ENTITY_HEALTH[self.name]
        self.damage = ENTITY_DAMAGE[self.name]
        self.score = ENTITY_SCORE[self.name]
        self.last_dmg = 'None'
        self.flash_timer = 0 
        self.damage_sound = pygame.mixer.Sound('./assets/Sound-Effects/Hit.wav')
        self.damage_sound.set_volume(2.5)  

        if self.name.lower() == 'auroracat':
            icon_path = './assets/Shots-and-icons/Auroracat-life.png'
        else:
            icon_path = './assets/Shots-and-icons/Cosmocat-life.png'

        self.life_icon = pygame.image.load(icon_path).convert_alpha()
        self.life_icon = pygame.transform.scale(self.life_icon, (50, 50))



    @abstractmethod
    def move(self):
        pass

    def take_damage(self, amount):
        self.health -= amount
        self.last_dmg = 'Something'
        self.flash_timer = 100  
        self.damage_sound.play()

    def draw(self, screen):
        if self.flash_timer > 0:
            flash = self.surf.copy()

            # Criar uma cópia da alpha (máscara de transparência)
            alpha_mask = pygame.mask.from_surface(flash)
            mask_surface = alpha_mask.to_surface(setcolor=(151, 0, 40, 100), unsetcolor=(0, 0, 0, 0))
            mask_surface = mask_surface.convert_alpha()

            # Aplica o vermelho SOMENTE nas áreas visíveis
            flash.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            screen.blit(flash, self.rect.topleft)
        else:
            screen.blit(self.surf, self.rect.topleft)



    def draw_health_hud(self, screen):
        bar_width = 190
        bar_height = 20
        x = 50
        y = 30

        max_health = ENTITY_HEALTH[self.name]
        proportion = max(0, self.health / max_health)
        filled_width = int(bar_width * proportion)

        # Posição Y diferente para cada personagem
        if self.name.lower() == 'auroracat':
            life_color = C_PINK
            y = 70  # AuroraCat fica mais abaixo
        else:
            life_color = C_GREEN
            y = 30  # CosmoCat fica mais acima

        # Desenha a barra de vida
        pygame.draw.rect(screen, C_WHITE, (x - 1, y - 1, bar_width + 2, bar_height + 2))
        pygame.draw.rect(screen, C_BLACK, (x, y, bar_width, bar_height))  # Fundo
        pygame.draw.rect(screen, life_color, (x, y, filled_width, bar_height))  # Vida atual

        # Texto de HP numérico
        font = pygame.font.SysFont(None, 20)
        texto = font.render(f'{int(self.health)}/{max_health}', True, C_WHITE)
        screen.blit(texto, (x + bar_width + 10, y))

        # Ícone de vida
        screen.blit(self.life_icon, (x - 37, y - 15))

        # Adiciona a exibição do score
        score_x = x + bar_width + 100  # Posição à direita da barra de vida
        score_text = font.render(f'Score: {self.score}', True, C_WHITE)
        screen.blit(score_text, (score_x, y))