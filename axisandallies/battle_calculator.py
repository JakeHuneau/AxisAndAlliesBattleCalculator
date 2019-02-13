"""
Monte Carlo simulation for predicting the probability
of you winning a battle.
"""
from copy import deepcopy

from axisandallies.units import *


def surprises(attackers, defenders):
    """
    AAA and submarine stuff
    """
    aaa_hits = 0
    attacking_subs_hits = 0
    defending_subs_hits = 0

    num_attacking_planes = 0

    for unit in attackers.units:
        if type(unit) in planes:
            num_attacking_planes += 1
        if isinstance(unit, Submarine):
            attacking_subs_hits += int(unit.fight())
        if isinstance(unit, Destroyer):
            defending_subs_hits = -1

    for unit in defenders.units:
        if isinstance(unit, AAA):
            for _ in range(min(3, num_attacking_planes)):
                hits = int(unit.fight())
                aaa_hits += hits
                num_attacking_planes -= hits

        if isinstance(unit, Destroyer):
            attacking_subs_hits = 0
        if isinstance(unit, Submarine) and defending_subs_hits != -1:
            defending_subs_hits += int(unit.fight())

    if attacking_subs_hits > 0:
        for unit in defenders.units[:]:
            if type(unit) in boats:
                defenders.units.remove(unit)
                attacking_subs_hits -= 1
            if attacking_subs_hits == 0:
                break

    if defending_subs_hits > 0 or aaa_hits > 0:
        for unit in attackers.units[:]:
            if type(unit) in planes and aaa_hits:
                attackers.units.remove(unit)
                aaa_hits -= 1

            if type(unit) in boats and defending_subs_hits:
                attackers.units.remove(unit)
                defending_subs_hits -= 1
            if not (defending_subs_hits or aaa_hits):
                break


def battle_turn(attackers, defenders):
    """
    A single fight in a battle.
    Attackers go first, then defenders

    Args:
        attackers: (Squad)
        defenders: (Squad)
    """
    attackers_hits = attackers.half_round(attacking=True)
    defenders_hits = defenders.half_round(attacking=False)
    attackers.remove_casualties(hits=defenders_hits, attacking=True)
    defenders.remove_casualties(hits=attackers_hits, attacking=False)


def endable_fight(attackers, defenders):
    """Ensure a fight can actually end"""
    for unit in attackers.units:
        if unit.attack:
            return True
    for unit in defenders.units:
        if unit.defense:
            return True
    return False


def battle(attackers, defenders):
    """
    An entire battle. Go back and forth attacking until one
    Squad is empty.

    Returns:
        (int) 1 if attackers win, -1 if defenders win,
              0 if draw (Everyone died)
    """
    surprises(attackers, defenders)

    while attackers.total_alive and defenders.total_alive and endable_fight(attackers, defenders):
        battle_turn(attackers, defenders)

    if attackers.total_alive and defenders.total_alive:  # Non-combat units left
        return 0
    if attackers.total_alive:
        return 1
    if defenders.total_alive:
        return -1
    return 0


def battle_sim(attackers, defenders, num_sims=1000):
    """
    runs full simulations and prints final results as
    win percent, loss percent, draw percent
    """
    wins = 0
    draws = 0
    losses = 0
    attackers_units = attackers.units
    defenders_units = defenders.units
    for _ in range(num_sims):
        attackers = Squad(deepcopy(attackers_units))
        defenders = Squad(deepcopy(defenders_units))
        res = battle(attackers, defenders)
        if res == -1:
            losses += 1
        elif res == 0:
            draws += 1
        elif res == 1:
            wins += 1
    return {'win': wins/num_sims, 'loss': losses/num_sims, 'draw': draws/num_sims}
