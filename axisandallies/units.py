from random import randint


def roll():
    """Return a die roll"""
    return randint(1,6)


class Unit:
    def __init__(self):
        self.attack = 0
        self.defense = 0
        self.health = 1

    def __repr__(self):
        return self.__class__.__name__

    def fight(self):
        """
        Try to attack

        Returns:
            (bool) if roll is <= roll needed for attack
        """
        return roll() <= self.attack

    def defend(self):
        """
        Try to defend

        Returns:
            (bool) if roll is <= roll needed for defend
        """
        return roll() <= self.defense

    def take_hit(self):
        self.health -= 1

    @property
    def is_dead(self):
        if self.health <= 0:
            return True
        return False

    def reset(self):
        self.__init__()


class Infantry(Unit):
    def __init__(self):
        super().__init__()
        self.attack = 1
        self.defense = 2

    def upgrade(self):
        self.attack = 2


class Artillery(Unit):
    def __init__(self):
        super().__init__()
        self.attack = 2
        self.defense = 2


class MechanizedInfantry(Unit):
    def __init__(self):
        super().__init__()
        self.attack = 1
        self.defense = 2

    def upgrade(self):
        self.attack = 2


class Tank(Unit):
    def __init__(self):
        super().__init__()
        self.attack = 3
        self.defense = 3


class AAA(Unit):
    def __init__(self):
        super().__init__()
        self.attack = 1  # Make sure this is only defensive
        self.defense = 0


class Fighter(Unit):
    def __init__(self):
        super().__init__()
        self.attack = 3
        self.defense = 4


class TacticalBomber(Unit):
    def __init__(self):
        super().__init__()
        self.attack = 3
        self.defense = 3

    def upgrade(self):
        self.attack = 4


class StrategicBomber(Unit):
    def __init__(self):
        super().__init__()
        self.attack = 4
        self.defense = 1


planes = {Fighter, TacticalBomber, StrategicBomber}


class Battleship(Unit):
    def __init__(self):
        super().__init__()
        self.attack = 4
        self.defense = 4
        self.health = 2


class AircraftCarrier(Unit):
    def __init__(self):
        super().__init__()
        self.attack = 0
        self.defense = 2
        self.health = 2


class Cruiser(Unit):
    def __init__(self):
        super().__init__()
        self.attack = 3
        self.defense = 3


class Destroyer(Unit):
    def __init__(self):
        super().__init__()
        self.attack = 2
        self.defense = 2
    # TODO: Figure out special stuff


class Submarine(Unit):
    def __init__(self):
        super().__init__()
        self.attack = 2
        self.defense = 1
    # TODO: Figure out special stuff

class Transport(Unit):
    def __init__(self):
        super().__init__()
        self.attack = 0
        self.defense = 0


boats = {Battleship, AircraftCarrier, Cruiser, Destroyer, Submarine, Transport}


class Squad:
    """
    A squad is a team of fighters.
    """
    def __init__(self, units):
        """units is a list of Unit objects"""
        self.units = units

    def __repr__(self):
        return_str = 'Unit type | number of unit\n'
        for h in set(type(i) for i in self.units):
            return_str += f'{h.__name__} | {sum(isinstance(i, h) for i in self.units)}\n'
        return return_str

    @property
    def total_alive(self):
        """Returns the number of fighters alive"""
        return len(self.units)

    def combined_arms(self):
        """Adds modifiers from combined arms"""
        infanty_count = sum(isinstance(i, Infantry) for i in self.units)
        artillery_count = sum(isinstance(i, Artillery) for i in self.units)
        mech_count = sum(isinstance(i, MechanizedInfantry) for i in self.units)
        tac_bomb_count = sum(isinstance(i, TacticalBomber) for i in self.units)
        tank_count = sum(isinstance(i, Tank) for i in self.units)
        fighter_count = sum(isinstance(i, Fighter) for i in self.units)

        num_upgraded_inf = min(infanty_count, artillery_count)
        num_upgraded_mech = min(mech_count, artillery_count)
        num_upgraded_tac = max(min(tac_bomb_count, tank_count), min(tac_bomb_count, fighter_count))

        for unit in self.units:
            unit.reset()  # start fresh each round
            if isinstance(unit, Infantry) and num_upgraded_inf:
                unit.upgrade()
                num_upgraded_inf -= 1
                continue

            if isinstance(unit, MechanizedInfantry) and num_upgraded_mech:
                unit.upgrade()
                num_upgraded_mech -= 1
                continue

            if isinstance(unit, TacticalBomber) and num_upgraded_tac:
                unit.upgrade()
                num_upgraded_tac -= 1
                continue

    def half_round(self, attacking=True):
        """
        Calculates the number of hits for
        this half round.

        Returns:
            total_hits: (int) number of hits made.
        """
        total_hits = 0
        if attacking:
            self.combined_arms()  # apply combined arms modifiers
        for unit in self.units:
            if attacking:
                total_hits += unit.fight()
            else:
                total_hits += unit.defend()
        return total_hits

    def remove_casualties(self, hits, attacking=True):
        """
        Removes the dead from the fighters. Assumes that
        the lowers roll_needed die first.

        Args:
            hits: (int) Number of people killed.
        """
        hits_remaining = hits
        if attacking:
            self.units.sort(key=lambda x: x.attack)
        else:
            self.units.sort(key=lambda x: x.defense)

        for unit in self.units[:]:
            # check first in case there are no hits
            if hits_remaining == 0:
                break

            unit.take_hit()
            hits_remaining -= 1

            if not unit.is_dead and hits_remaining > 0:
                unit.take_hit()
                hits_remaining -= 1

            if unit.is_dead:
                self.units.remove(unit)

