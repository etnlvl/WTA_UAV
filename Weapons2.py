import numpy as np
class Weapon:
    def __init__(self, id, range, p_kill, reload_time):
        # Initialiser les attributs de l'arme
        self.id = id
        self.range = range
        self.p_kill = p_kill
        self.reload_time = reload_time
        self.allocated_drone = None
        self.last_allocated_drone = None
        self.last_fired_time = 0
        self.cool_down = 0
        self.weapons_set = dict()


    def is_available(self, time):
        # Vérifier si l'arme est disponible à un moment donné
        return time >= self.last_fired_time + self.reload_time

    def allocate_to_drone(self, drone):
        # Allouer l'arme à un drone donné
        self.allocated_drone = drone
        self.last_allocated_drone = drone

    def was_last_allocated_to_drone(self, drone):
        # Vérifier si l'arme a été allouée à un drone donné lors de la dernière itération
        return self.last_allocated_drone == drone

    def was_allocated_to_drone(self, drone):
        # Vérifier si l'arme a été allouée à un drone donné à un moment donné
        return self.allocated_drone == drone

    def can_fire_at_drone(self, drone):
        # Vérifier si l'arme peut tirer sur un drone donné en fonction de sa portée et de sa disponibilité
        distance = np.sqrt(drone.pos[0]**2 + drone.pos[1]**2 + drone.pos[2]**2)
        return distance <= self.range and self.is_available(self.last_fired_time)

    def fire_at_drone(self, drone, time):
        # Tirer sur un drone donné avec une probabilité de tuer donnée
        if self.can_fire_at_drone(drone):
            self.last_fired_time = time
            if np.random.rand() < self.p_kill:
                # Si le drone est touché, le marquer comme détruit
                drone.is_destroyed = True
                return True
            else:
                # Si le drone n'est pas touché, renvoyer False
                return False
        else:
            # Si l'arme ne peut pas tirer sur le drone, renvoyer False
            return False

    def missed_drone(self, drone):
        # Vérifier si l'arme a manqué un drone donné
        return self.was_allocated_to_drone(drone) and not drone.is_destroyed

    def let_drone_escape(self, drone):
        # Vérifier si l'arme a laissé un drone donné s'échapper de sa fenêtre de tir
        distance = np.sqrt(drone.pos[0]**2 + drone.pos[1]**2 + drone.pos[2]**2)
        return self.was_allocated_to_drone(drone) and distance > self.range and not drone.is_destroyed
