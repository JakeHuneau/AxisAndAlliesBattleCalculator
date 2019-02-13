from pyramid.view import view_config

from axisandallies.units import *
from axisandallies.battle_calculator import battle_sim


@view_config(route_name='aaa_battle_calculator', renderer='templates/aaa.jinja2')
def aaa_battle_calculator(request):
    if request.method == 'GET':
        request_params = {k:v if v != '' else 0 for k,v in request.params.items()}
        attackers = []
        defenders = []
        for _ in range(int(request_params.get('a_inf', 0))):
            attackers.append(Infantry())
        for _ in range(int(request_params.get('d_inf', 0))):
            defenders.append(Infantry())

        for _ in range(int(request_params.get('a_art', 0))):
            attackers.append(Artillery())
        for _ in range(int(request_params.get('d_art', 0))):
            defenders.append(Artillery())

        for _ in range(int(request_params.get('a_mech', 0))):
            attackers.append(MechanizedInfantry())
        for _ in range(int(request_params.get('d_mech', 0))):
            defenders.append(MechanizedInfantry())

        for _ in range(int(request_params.get('a_tank', 0))):
            attackers.append(Tank())
        for _ in range(int(request_params.get('d_tank', 0))):
            defenders.append(Tank())

        for _ in range(int(request_params.get('a_aaa', 0))):
            attackers.append(AAA())
        for _ in range(int(request_params.get('d_aaa', 0))):
            defenders.append(AAA())

        for _ in range(int(request_params.get('a_f', 0))):
            attackers.append(Fighter())
        for _ in range(int(request_params.get('d_f', 0))):
            defenders.append(Fighter())

        for _ in range(int(request_params.get('a_tb', 0))):
            attackers.append(TacticalBomber())
        for _ in range(int(request_params.get('d_tb', 0))):
            defenders.append(TacticalBomber())

        for _ in range(int(request_params.get('a_sb', 0))):
            attackers.append(StrategicBomber())
        for _ in range(int(request_params.get('d_sb', 0))):
            defenders.append(StrategicBomber())

        for _ in range(int(request_params.get('a_bs', 0))):
            attackers.append(Battleship())
        for _ in range(int(request_params.get('d_bs', 0))):
            defenders.append(Battleship())

        for _ in range(int(request_params.get('a_ac', 0))):
            attackers.append(AircraftCarrier())
        for _ in range(int(request_params.get('d_ac', 0))):
            defenders.append(AircraftCarrier())

        for _ in range(int(request_params.get('a_c', 0))):
            attackers.append(Cruiser())
        for _ in range(int(request_params.get('d_c', 0))):
            defenders.append(Cruiser())

        for _ in range(int(request_params.get('a_d', 0))):
            attackers.append(Destroyer())
        for _ in range(int(request_params.get('d_d', 0))):
            defenders.append(Destroyer())

        for _ in range(int(request_params.get('a_sub', 0))):
            attackers.append(Submarine())
        for _ in range(int(request_params.get('d_sub', 0))):
            defenders.append(Submarine())

        for _ in range(int(request_params.get('a_t', 0))):
            attackers.append(Transport())
        for _ in range(int(request_params.get('d_t', 0))):
            defenders.append(Transport())

        num_sims = int(request_params.get('num_sims', 1000))

        results = battle_sim(attackers=Squad(attackers),
                             defenders=Squad(defenders),
                             num_sims=num_sims)

        request_params.update(results)
        return request_params

    return {'project': 'AxisAndAllies'}
