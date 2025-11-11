from Simulation import Simulation


s = Simulation(max_round=50,
               current_round=1,
               sheep_amount=15,
               meadow_range=10.0,
               sheep_step_size=0.5,
               wolf_attack_range=1.0)

s.play_simulation()