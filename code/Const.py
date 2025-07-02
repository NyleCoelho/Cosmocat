import pygame

WIN_WIDTH = 1366
WIN_HEIGHT = 768

C_GREEN = (111, 254, 3)
C_WHITE = (255,255,255)

MENU_OPTION = ('NEW GAME', 
               'MULTIPLAYER',
               'SCORE',
               'EXIT')

EVENT_ENEMY = pygame.USEREVENT + 1
EVENT_TIMEOUT = pygame.USEREVENT + 2
SPAWN_TIME = 4000
TIMEOUT_STEP = 100  # 100ms
TIMEOUT_LEVEL = 20000  # 20s

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
    'Cosmocat': 5,
    'Player1Shot': 1,
    'Auroracat': 5,
    'Player2Shot': 3,
    'Enemy1': 1,
    'Enemy1Shot': 5,
    'Enemy2': 3,
    'Enemy2Shot': 2,
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
                    'Cosmocat': pygame.K_LCTRL}

