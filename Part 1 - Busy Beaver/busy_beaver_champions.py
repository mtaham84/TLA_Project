
from turing_machine import TuringMachine

CHAMPIONS = {
    2: {
        ('a', '0'): ('b', '1', 'R'),
        ('a', '1'): ('b', '1', 'L'),
        ('b', '0'): ('a', '1', 'L'),
        ('b', '1'): ('h', '1', 'R'),
    },
    3: {
        ('a', '0'): ('b', '1', 'R'),
        ('a', '1'): ('h', '1', 'R'),
        ('b', '0'): ('c', '0', 'R'),
        ('b', '1'): ('b', '1', 'R'),
        ('c', '0'): ('c', '1', 'L'),
        ('c', '1'): ('a', '1', 'L'),
    },
    4: {
        ('a', '0'): ('b', '1', 'R'),
        ('a', '1'): ('b', '1', 'L'),
        ('b', '0'): ('a', '1', 'L'),
        ('b', '1'): ('c', '0', 'L'),
        ('c', '0'): ('h', '1', 'R'),
        ('c', '1'): ('d', '1', 'L'),
        ('d', '0'): ('d', '1', 'R'),
        ('d', '1'): ('a', '0', 'R'),
    },
}

KNOWN_VALUES = {
    1: (1, 1),
    2: (4, 6),
    3: (6, 21),
    4: (13, 107),
    5: (4098, 47_176_870),
}


def run_champion(n, step_limit=2000):
    tm = TuringMachine(CHAMPIONS[n], start_state='a', accept_state='h',
                        reject_state='r', blank_symbol='0')
    last_config = None
    steps = 0
    for action, config in tm.run(''):
        last_config = config
        steps += 1
        if action == 'Accept':
            break
        if steps > step_limit:
            return None, None
    left = ''.join(reversed(last_config['left_hand_side']))
    right = ''.join(last_config['right_hand_side'])
    tape = left + last_config['symbol'] + right
    return steps - 1, tape.count('1')


if __name__ == "__main__":
    print(f"{'n':>3} | {'Known Σ(n)':>15} | {'Our ones':>12} | "
          f"{'Known S(n)':>15} | {'Our steps':>10}")
    print("-" * 70)
    for n in (2, 3, 4):
        known_ones, known_steps = KNOWN_VALUES[n]
        steps, ones = run_champion(n)
        print(f"{n:>3} | {known_ones:>15} | {ones:>12} | "
              f"{known_steps:>15} | {steps:>10}")

    print()
    print("n=5 : Σ(5)=4098 in S(5)=47,176,870 steps -- full simulation with this")
    print("      Python simulator is not feasible in reasonable time (therefore,")
    print("      test_busy_beaver_5.py provides a non-optimal but executable")
    print("      5-state machine (20 ones)).")
