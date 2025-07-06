import pygame
SPAWN_LIFESAVER_EVENT = pygame.USEREVENT + 3

WIN_WIDTH = 1366
WIN_HEIGHT = 768

C_GREEN = (111, 254, 3)
C_WHITE = (255,255,255)
C_PINK = (255, 94, 240)
C_RED = (255, 60, 60)
C_BLACK = (0, 0, 0)

MENU_OPTION = ('NEW GAME', 
               'MULTIPLAYER',
               'SCORE',
               'EXIT')

GAMEOVER_OPTION = ('TENTAR NOVAMENTE', 
                    'VOLTAR AO MENU',)

EVENT_ENEMY = pygame.USEREVENT + 1
EVENT_TIMEOUT = pygame.USEREVENT + 2
SPAWN_TIME = 1000
TIMEOUT_STEP = 100  # 100ms
TIMEOUT_LEVEL = 7000 # 20s

SPAWN_POWERUP_EVENT = pygame.USEREVENT + 3
POWERUP_DURATION = 10000  # 10 segundos

ENTITY_SPEED = {
    'Level1Bg0': 5,
    'Level1Bg1': 7,
    'Level1Bg2': 2,
    'Level1Bg3': 3,
    'Level1Bg4': 4,
    'Level1Bg5': 5,
    'Level1Bg6': 6,
    'Level2Bg0': 0,
    'Level2Bg1': 1,
    'Level2Bg2': 2,
    'Level2Bg3': 3,
    'Level2Bg4': 4,
    'Boss': 2,
    'BossShot': 20,
    'Cosmocat': 5,
    'CosmocatShot': 10,
    'Auroracat': 5,
    'AuroracatShot': 15,
    'Enemy1': 7,
    'Enemy1Shot': 16,
    'Enemy2': 8,
    'Enemy2Shot': 16,
    'LifeSaver': 1,
    'PowerUp': 2,
}

PLAYER_KEY_UP = {'Auroracat': pygame.K_UP,
                 'Cosmocat': pygame.K_w}
PLAYER_KEY_DOWN = {'Auroracat': pygame.K_DOWN,
                   'Cosmocat': pygame.K_s}
PLAYER_KEY_LEFT = {'Auroracat': pygame.K_LEFT,
                   'Cosmocat': pygame.K_a}
PLAYER_KEY_RIGHT = {'Auroracat': pygame.K_RIGHT,
                    'Cosmocat': pygame.K_d}
PLAYER_KEY_SHOOT = {'Auroracat': pygame.K_RCTRL,
                    'Cosmocat': pygame.K_RETURN}

ENTITY_HEALTH = {
    'Boss': 1000,
    'Level1Bg0': 999,
    'Level1Bg1': 999,
    'Cosmocat': 1000,
    'CosmocatShot': 1,
    'Auroracat': 300,
    'AuroracatShot': 1,
    'Enemy1': 110,
    'Enemy1Shot': 1,
    'BossShot': 1,
    'Enemy2': 110,
    'Enemy2Shot': 1,
    'LifeSaver': 1,
    'PowerUp': 1
}

ENTITY_DAMAGE = {
    'Level1Bg0': 0,
    'Level1Bg1': 0,
    'Level1Bg2': 0,
    'Level1Bg3': 0,
    'Level1Bg4': 0,
    'Level1Bg5': 0,
    'Level1Bg6': 0,
    'Level2Bg0': 0,
    'Level2Bg1': 0,
    'Level2Bg2': 0,
    'Level2Bg3': 0,
    'Level2Bg4': 0,
    'Cosmocat': 1,
    'CosmocatShot': 25,
    'Auroracat': 1,
    'AuroracatShot': 30,
    'Enemy1': 1,
    'Enemy1Shot': 20,
    'Enemy2': 1,
    'Enemy2Shot': 15,
    'BossShot': 20,
    'LifeSaver': 1,
    'PowerUp': 0,
    'Boss': 20,
    'BossShot': 30,
    'CosmocatShotPowered': 30,  # Dano aumentado (opcional)
    'AuroracatShotPowered': 35  # Dano aumentado (opcional)
}

ENTITY_SCORE = {
    'Level1Bg0': 0,
    'Level1Bg1': 0,
    'Level1Bg2': 0,
    'Level1Bg3': 0,
    'Level1Bg4': 0,
    'Level1Bg5': 0,
    'Level1Bg6': 0,
    'Level2Bg0': 0,
    'Level2Bg1': 0,
    'Level2Bg2': 0,
    'Level2Bg3': 0,
    'Level2Bg4': 0,
    'Boss': 1000,
    'Cosmocat': 0,
    'CosmocatShot': 0,
    'Auroracat': 0,
    'AuroracatShot': 0,
    'Enemy1': 100,
    'Enemy1Shot': 0,
    'Enemy2': 125,
    'Enemy2Shot': 0,
    'BossShot': 0,
    'LifeSaver': 1,
    'PowerUp': 0
}

ENTITY_SHOT_DELAY = {
    'Cosmocat': 20,
    'Auroracat': 20,
    'Enemy1': 20,
    'Enemy2': 20,
    'Boss': 1000,
}
