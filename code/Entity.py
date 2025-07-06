from abc import ABC, abstractmethod
import pygame.image
from code.Const import WIN_WIDTH, WIN_HEIGHT, ENTITY_DAMAGE, ENTITY_HEALTH, ENTITY_SCORE, C_PINK, C_GREEN, C_BLACK, C_WHITE

class Entity(ABC): 
    def __init__(self, name: str, position: tuple, scale_to_screen=True, custom_scale=None):
        self.name = name

        # Carrega o sprite da entidade
        self.surf = pygame.image.load(f'./assets/{name}.png').convert_alpha()
        
        # Redimensiona a imagem conforme necessário
        if scale_to_screen:
            self.surf = pygame.transform.scale(self.surf, (WIN_WIDTH, WIN_HEIGHT))
        elif custom_scale:
            self.surf = pygame.transform.scale(self.surf, custom_scale)
        else:
            self.surf = pygame.transform.scale(self.surf, (120, 100))

        # Define posição e propriedades básicas
        self.rect = self.surf.get_rect(topleft=position)
        self.speed = 0
        self.health = ENTITY_HEALTH[self.name]
        self.damage = ENTITY_DAMAGE[self.name]
        self.score = ENTITY_SCORE[self.name]
        self.last_dmg = 'None'
        self.flash_timer = 0

        # Som de dano
        self.damage_sound = pygame.mixer.Sound('./assets/Sound-Effects/Hit.wav')
        self.damage_sound.set_volume(2.5)

        # Máscara de colisão
        self.mask = pygame.mask.from_surface(self.surf)

        # Ícone de vida (HUD)
        if self.name.lower() == 'auroracat':
            icon_path = './assets/Life-Icons/Auroracat-life.png'
        else:
            icon_path = './assets/Life-Icons/Cosmocat-life.png'

        self.life_icon = pygame.image.load(icon_path).convert_alpha()
        self.life_icon = pygame.transform.scale(self.life_icon, (50, 50))

    @abstractmethod
    def move(self):
        # Método abstrato de movimentação (implementado nas subclasses)
        pass

    def take_damage(self, amount):
        # Reduz vida e ativa flash de dano
        self.health -= amount
        self.last_dmg = 'Something'
        self.flash_timer = 100
        self.damage_sound.play()

    def draw(self, screen):
        # Desenha a entidade com flash se estiver danificada
        if self.flash_timer > 0:
            flash = self.surf.copy()
            alpha_mask = pygame.mask.from_surface(flash)
            mask_surface = alpha_mask.to_surface(setcolor=(151, 0, 40, 100), unsetcolor=(0, 0, 0, 0))
            mask_surface = mask_surface.convert_alpha()
            flash.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            screen.blit(flash, self.rect.topleft)
        else:
            screen.blit(self.surf, self.rect.topleft)

    def draw_health_hud(self, screen):
        # Desenha a barra de vida no HUD
        bar_width = 190
        bar_height = 20
        x = 50

        max_health = ENTITY_HEALTH[self.name]
        proportion = max(0, self.health / max_health)
        filled_width = int(bar_width * proportion)

        # Define cor e posição conforme o personagem
        if self.name.lower() == 'auroracat':
            life_color = C_PINK
            y = 70
        else:
            life_color = C_GREEN
            y = 30

        # Desenha a barra e o texto da vida
        pygame.draw.rect(screen, C_WHITE, (x - 1, y - 1, bar_width + 2, bar_height + 2))  # borda
        pygame.draw.rect(screen, C_BLACK, (x, y, bar_width, bar_height))                 # fundo
        pygame.draw.rect(screen, life_color, (x, y, filled_width, bar_height))           # vida

        font = pygame.font.SysFont(None, 20)
        texto = font.render(f'{int(self.health)}/{max_health}', True, C_WHITE)
        screen.blit(texto, (x + bar_width + 10, y))
        screen.blit(self.life_icon, (x - 37, y - 15))  # ícone de vida
