from code.Const import WIN_WIDTH, ENTITY_HEALTH
from code.Enemy import Enemy
from code.EnemyShot import EnemyShot
from code.Entity import Entity
from code.Player import Player
from code.CosmocatShot import CosmocatShot
from code.LifeSaver import LifeSaver
from code.PowerUp import PowerUp
from code.Boss import Boss

class EntityMediator:

    @staticmethod
    def __verify_collision_window(ent: Entity):
        # Remove entidades que saíram da tela
        if isinstance(ent, Enemy):
            if ent.rect.right <= 0:
                ent.health = 0
        if isinstance(ent, CosmocatShot):
            if ent.rect.left >= WIN_WIDTH:
                ent.health = 0
        if isinstance(ent, EnemyShot):
            if ent.rect.right <= 0:
                ent.health = 0

    @staticmethod
    def __verify_collision_entity(ent1, ent2):
        valid_interaction = False

        # Define pares que podem colidir
        if isinstance(ent1, (Enemy, Boss)) and isinstance(ent2, CosmocatShot):
            valid_interaction = True
            ent1.killed_by_player = True
        elif isinstance(ent1, CosmocatShot) and isinstance(ent2, (Enemy, Boss)):
            valid_interaction = True
        elif isinstance(ent1, Player) and isinstance(ent2, EnemyShot):
            valid_interaction = True
        elif isinstance(ent1, EnemyShot) and isinstance(ent2, Player):
            valid_interaction = True
        elif isinstance(ent1, Player) and isinstance(ent2, LifeSaver):
            valid_interaction = True
        elif isinstance(ent1, LifeSaver) and isinstance(ent2, Player):
            valid_interaction = True
        elif isinstance(ent1, Player) and isinstance(ent2, PowerUp):
            valid_interaction = True
        elif isinstance(ent1, PowerUp) and isinstance(ent2, Player):
            valid_interaction = True
        elif isinstance(ent1, Player) and isinstance(ent2, Boss):
            valid_interaction = True
        elif isinstance(ent1, Boss) and isinstance(ent2, Player):
            valid_interaction = True

        # Verifica colisão se o par for válido
        if valid_interaction:
            if ent1.rect.colliderect(ent2.rect):  # colisão bounding box
                offset = (ent2.rect.left - ent1.rect.left, ent2.rect.top - ent1.rect.top)
                if ent1.mask.overlap(ent2.mask, offset):  # colisão por pixel (máscara)

                    # Caso seja um LifeSaver
                    if isinstance(ent1, LifeSaver) or isinstance(ent2, LifeSaver):
                        player = ent1 if isinstance(ent1, Player) else ent2
                        lifesaver = ent2 if isinstance(ent1, Player) else ent1
                        heal_amount = 0
                        try:
                            max_health = ENTITY_HEALTH[player.name]
                            current_health = player.health
                            heal_amount = min(100, max(0, max_health - current_health))  # cura até 100
                            if heal_amount > 0:
                                player.health += heal_amount
                                player.lifesaver_sound.play()
                        finally:
                            lifesaver.health = 0  # remove lifesaver

                    # Caso seja um PowerUp
                    if isinstance(ent1, PowerUp) or isinstance(ent2, PowerUp):
                        player = ent1 if isinstance(ent1, Player) else ent2
                        powerup = ent2 if isinstance(ent1, Player) else ent1
                        player.activate_powerup()
                        powerup.health = 0  # remove powerup

                    # Dano e flash para os dois envolvidos
                    ent1.take_damage(ent2.damage)
                    ent2.take_damage(ent1.damage)
                    ent1.last_dmg = ent2.name
                    ent2.last_dmg = ent1.name
                    ent1.flash_timer = 10
                    ent2.flash_timer = 10

    @staticmethod
    def verify_collision(entity_list: list[Entity]):
        # Verifica colisões entre todas as entidades da lista
        for i in range(len(entity_list)):
            entity1 = entity_list[i]
            EntityMediator.__verify_collision_window(entity1)  # colisão com bordas
            for j in range(i + 1, len(entity_list)):
                entity2 = entity_list[j]
                EntityMediator.__verify_collision_entity(entity1, entity2)  # colisão entre entidades

    @staticmethod
    def verify_health(entity_list: list[Entity]):
        # Remove entidades com vida zerada
        for ent in entity_list[:]:
            if ent.health <= 0:
                if isinstance(ent, Boss):
                    entity_list.remove(ent)
                    return 'WIN'  # vitória se o boss morrer
                elif not isinstance(ent, Player):
                    entity_list.remove(ent)
        return None  # continua o jogo
