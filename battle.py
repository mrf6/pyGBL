import math
import random
import json

with open('pokemon.json', 'r') as f:
    POKEMON_DATA = json.load(f)

with open('moves.json', 'r') as f:
    MOVE_DATA = json.load(f)

with open('types.json', 'r') as f:
    TYPE_CHART = json.load(f)



                         

CP_MULTIPLIERS = {
    1: 0.094, 1.5: 0.135137432, 2: 0.16639787, 2.5: 0.192650919, 3: 0.21573247,
    3.5: 0.236572661, 4: 0.25572005, 4.5: 0.273530381, 5: 0.29024988,
    5.5: 0.306057377, 6: 0.3210876, 6.5: 0.335445036, 7: 0.34921268,
    7.5: 0.362457751, 8: 0.3752356, 8.5: 0.387592416, 9: 0.39956728,
    9.5: 0.411193551, 10: 0.4225, 10.5: 0.432926419, 11: 0.44310755,
    11.5: 0.45305996, 12: 0.46279839, 12.5: 0.47233609, 13: 0.48168495,
    13.5: 0.4908558, 14: 0.49985844, 14.5: 0.508701765, 15: 0.51739395,
    15.5: 0.525942511, 16: 0.53435433, 16.5: 0.542635738, 17: 0.55079269,
    17.5: 0.558830586, 18: 0.5667545, 18.5: 0.57456916, 19: 0.58227891,
    19.5: 0.58988791, 20: 0.5974, 20.5: 0.60481881, 21: 0.6121573,
    21.5: 0.61940412, 22: 0.62656713, 22.5: 0.63364914, 23: 0.64065295,
    23.5: 0.64758096, 24: 0.65443563, 24.5: 0.66121927, 25: 0.667934,
    25.5: 0.6745819, 26: 0.68116492, 26.5: 0.6876849, 27: 0.69414365,
    27.5: 0.70054287, 28: 0.7068842, 28.5: 0.7131691, 29: 0.7193991,
    29.5: 0.7255756, 30: 0.7317, 30.5: 0.734741009, 31: 0.73776948,
    31.5: 0.740785574, 32: 0.74378943, 32.5: 0.746781211, 33: 0.74976104,
    33.5: 0.752729087, 34: 0.75568551, 34.5: 0.758630368, 35: 0.76156384,
    35.5: 0.764486065, 36: 0.76739717, 36.5: 0.770297266, 37: 0.7731865,
    37.5: 0.776064962, 38: 0.77893275, 38.5: 0.781790055, 39: 0.78463697,
    39.5: 0.787473578, 40: 0.79030001, 40.5: 0.792803946, 41: 0.79530001,
    41.5: 0.797803921, 42: 0.8003, 42.5: 0.802803892, 43: 0.8053,
    43.5: 0.807803864, 44: 0.81029999, 44.5: 0.812803835, 45: 0.81529999,
    45.5: 0.817803808, 46: 0.82029999, 46.5: 0.82280377, 47: 0.82529999,
    47.5: 0.827803755, 48: 0.83029999, 48.5: 0.832803748, 49: 0.83529999,
    49.5: 0.83780374, 50: 0.84029999, 50.5: 0.84279999, 51: 0.84529999
}


STAT_MULTIPLIERS = {-4: 0.5,
                    -3: 0.5715,
                    -2: 0.667,
                    -1: 0.8,
                    0: 1.0,
                    1: 1.25,
                    2: 1.5,
                    3: 1.75,
                    4: 2.0}




class Move:
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.type = data["type"]
        self.damage = data["damage"]
        self.energy_cost = data["energy_cost"]
        self.energy_gain = data["energy_gain"]
        self.turns = data["turns"]
        self.user_attack_buff = data["user_attack_buff"]
        self.opponent_attack_buff = data["opponent_attack_buff"]
        self.user_defense_buff = data["user_defense_buff"]
        self.opponent_defense_buff = data["opponent_defense_buff"]
        self.buff_probability = data["buff_probability"]



class Pokemon:
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.type_1 = data["type_1"]
        self.type_2 = data["type_2"]
        self.fast_move = data["fast_move"]
        self.charged_move_1 = data["charged_move_1"]
        self.charged_move_2 = data["charged_move_2"]
        self.level = data["level"]
        self.ivs = data["ivs"]
        self.base_stats = data["base_stats"]
        self.energy = 0
        self.attack_status = 0
        self.defense_status = 0
        self.action = '-'
        self.shields = 2
        self.calculate_stats()

    def calculate_stats(self):
        cpm = CP_MULTIPLIERS[self.level]
        self.attack = (self.base_stats['attack'] + self.ivs['attack']) * cpm
        self.defense = (self.base_stats['defense'] + self.ivs['defense']) * cpm
        self.hp = math.floor((self.base_stats['hp'] + self.ivs['hp']) * cpm)

        # for resetting stats (and CMP ties)
        self.starting_attack = self.attack
        self.starting_defense = self.defense
        self.starting_hp = self.hp

    
    def reset_stats(self):
        self.action = '-'
        self.energy = 0
        self.attack_status = 0
        self.defense_status = 0
        self.attack = self.starting_attack
        self.defense = self.starting_defense
        self.hp = self.starting_hp
        
        



class Battle:
    def __init__(self, attacker, defender, attacker_shields, defender_shields):
        attacker.reset_stats()
        defender.reset_stats()

        attacker.shields = attacker_shields
        defender.shields = defender_shields

        self.attacker = attacker
        self.defender = defender

        self.turn = 0
        self.last_charged_move_turn = 0

        


    def damage_dealt(self, attacker, defender, move):
        effectiveness = TYPE_CHART[move.type][defender.type_1]
        if defender.type_2 != "none":
            effectiveness *= TYPE_CHART[move.type][defender.type_2]

        stab = 1.2 if move.type in {attacker.type_1, attacker.type_2} else 1.0
        bonus = 1.3
        return math.floor(0.5 * move.damage * ((attacker.attack * STAT_MULTIPLIERS[attacker.attack_status]) / (defender.defense * STAT_MULTIPLIERS[defender.defense_status])) * effectiveness * stab * bonus) + 1

        
    def get_fast_move_damage(self, attacker, defender):
        return self.damage_dealt(attacker, defender, MOVES[attacker.fast_move])
    

    def get_charged_move_damage(self, attacker, defender, charged_move):
        return self.damage_dealt(attacker, defender, MOVES[attacker.charged_move_1]) if charged_move == 1 else self.damage_dealt(attacker, defender, MOVES[attacker.charged_move_2])
    

    def throw_fast_move(self, attacker, defender):
        attacker.energy = min(100, attacker.energy + MOVES[attacker.fast_move].energy_gain)
        defender.hp -= self.get_fast_move_damage(attacker, defender)
        attacker.action = 'X'


    def throw_charged_move(self, attacker, defender, shield, charged_move_number):
        move = MOVES[attacker.charged_move_1] if charged_move_number == 1 else MOVES[attacker.charged_move_2]
        attacker.energy -= MOVES[attacker.charged_move_1].energy_cost if charged_move_number == 1 else MOVES[attacker.charged_move_2].energy_cost

        if shield:
            defender.hp -= 1
            defender.shields -= 1
            attacker.action = 'used ' + MOVES[attacker.charged_move_1].name + ', shielded' if charged_move_number == 1 else 'used ' + MOVES[attacker.charged_move_2].name + ', shielded'
        
        else:
            defender.hp -= self.get_charged_move_1_damage(attacker, defender)
            attacker.action = 'used ' + MOVES[attacker.charged_move_1].name + ', not shielded' if charged_move_number == 1 else 'used ' + MOVES[attacker.charged_move_2].name + ', not shielded'

        self.last_charged_move_turn = self.turn

        if move.buff_probability == 1.0 or (move.buff_probability > 0.0 and random.random() < move.buff_probability):
            attacker.attack_status += move.user_attack_buff
            attacker.defense_status += move.user_defense_buff
            defender.attack_status += move.opponent_attack_buff
            defender.defense_status += move.opponent_defense_buff
            




        
    def action(self, attacker, defender): 
        """
        None = In the middle of a fast move
        1 = Apply charged move 1 damage
        2 = Apply charged move 2 damage
        3 = Apply fast move damage
        """

        if attacker.energy >= MOVES[attacker.charged_move_1].energy_cost:
            return 1

        # if waiting for fast move to register, do nothing
        if (self.turn - self.last_charged_move_turn) % MOVES[attacker.fast_move].turns != 0:
            return None

        # if not enough energy for charged move, throw fast move
        if attacker.energy < MOVES[attacker.charged_move_1].energy_cost:
            return 3
        

        

            
        

    
    def shield_decision(self, attacker, defender, charged_move_thrown):
        """
        charged_move_thrown = 1 --> Charged Move 1
        charged_move_thrown = 2 --> Charged Move 2
        """

        # if defender has no shields left, dont shield
        if defender.shields == 0:
            return False
        
        # calculate how many more turns you will survive if you dont shield
        hp_remaining = defender.hp - self.get_charged_move_damage(attacker, defender, charged_move_thrown)
        
        turns_alive = min(0, hp_remaining) // MOVES[attacker.fast_move].damage * MOVES[attacker.fast_move].turns

    
        # if you have 2 shields and will survive > 20 turns or 1 shield and will survive > 10 turns, dont shield
        if (defender.shields == 2 and turns_alive > 20) or (defender.shields == 1 and turns_alive > 10):
            return False
        
        # otherwise shield
        return True


    def step(self):
        self.turn += 1
        self.attacker.action = '-'
        self.defender.action = '-'

        
        attacker_action = self.action(self.attacker, self.defender)
        defender_action = self.action(self.defender, self.attacker)


        

        
        # CMP tie
        if attacker_action in {1,2} and defender_action in {1,2}:
            # TODO: IMPLEMENT ATTACK TIE COIN FLIP


            if attacker.starting_attack > defender.starting_attack:
                self.throw_charged_move(attacker, defender, self.shield_decision(attacker, defender, attacker_action), attacker_action)

                if defender.hp > 0:
                    self.throw_charged_move(defender, attacker, self.shield_decision(defender, attacker, defender_action), defender_action)

            elif attacker.starting_attack < defender.starting_attack:
                self.throw_charged_move(defender, attacker, self.shield_decision(defender, attacker, defender_action), defender_action)
                
                if attacker.hp > 0:
                    self.throw_charged_move(attacker, defender, self.shield_decision(attacker, defender, attacker_action), attacker_action)

            else:   # coin flip CMP tie
                if random.random() < 0.5:
                    self.throw_charged_move(attacker, defender, self.shield_decision(attacker, defender, attacker_action), attacker_action)

                    if defender.hp > 0:
                        self.throw_charged_move(defender, attacker, self.shield_decision(defender, attacker, defender_action), defender_action)

                else:
                    self.throw_charged_move(defender, attacker, self.shield_decision(defender, attacker, defender_action), defender_action)
                    
                    if attacker.hp > 0:
                        self.throw_charged_move(attacker, defender, self.shield_decision(attacker, defender, attacker_action), attacker_action)

            return 

        
        if attacker_action == 3:
            self.throw_fast_move(attacker, defender)

            # no DRE
            if defender_action in {1,2} and defender.hp <= 0:
                return
        
        if defender_action == 3:
            self.throw_fast_move(defender, attacker)

            # no DRE
            if attacker_action in {1,2} and attacker.hp <= 0:
                return 

        

        if attacker_action in {1,2}: 
            self.throw_charged_move(attacker, defender, self.shield_decision(attacker, defender, attacker_action), attacker_action)

            if defender.hp > 0:
                self.throw_fast_move(defender, attacker)



        if defender_action in {1,2}:
            self.throw_charged_move(defender, attacker, self.shield_decision(defender, attacker, defender_action), defender_action)

            if attacker.hp > 0:
                self.throw_fast_move(attacker, defender)


        



        print(self.attacker.name, self.attacker.action, '    ', self.defender.name, self.defender.action)

        


    def simulate(self):
        while self.attacker.hp > 0 and self.defender.hp > 0:
            if self.turn > 400: 
                print("Battle timed out!")
                break
            self.step()

        print(self.attacker.name, self.attacker.hp)
        print(self.defender.name, self.defender.hp)



if __name__ == '__main__':
    POKEMON = {i: Pokemon(i, POKEMON_DATA[i]) for i in POKEMON_DATA}
    MOVES = {i: Move(i, MOVE_DATA[i]) for i in MOVE_DATA}

    attacker = POKEMON['marowak']
    defender = POKEMON['furret']

    attacker_shields = 2
    defender_shields = 2

    battle = Battle(attacker, defender, attacker_shields, defender_shields)
    battle.simulate()