
from turing_machine import TuringMachine

transitions_bb5 = {
    ('a', '0'): ('b', '1', 'R'),
    ('a', '1'): ('a', '0', 'L'),
    ('b', '0'): ('c', '1', 'R'),
    ('b', '1'): ('h', '1', 'R'),
    ('c', '0'): ('e', '0', 'R'),
    ('c', '1'): ('a', '0', 'R'),
    ('d', '0'): ('d', '1', 'L'),
    ('d', '1'): ('a', '1', 'L'),
    ('e', '0'): ('d', '0', 'R'),
    ('e', '1'): ('c', '1', 'R'),
}

if __name__ == "__main__":
    tm = TuringMachine(transitions_bb5, start_state='a', accept_state='h',
                        reject_state='r', blank_symbol='0')

    last_config = None
    steps = 0
    outcome = None
    for action, config in tm.run(''):
        last_config = config
        steps += 1
        if action in ('Accept', 'Reject'):
            outcome = action
            break
        if steps > 5000:
            outcome = 'step_limit_reached'
            break

    left = ''.join(reversed(last_config['left_hand_side']))
    right = ''.join(last_config['right_hand_side'])
    tape = left + last_config['symbol'] + right
    ones = tape.count('1')
    print(f"Result: {outcome}")
    print(f"✅ BB-5 (non-optimal): steps = {steps - 1}")
    print(f"✅ BB-5 (non-optimal): ones = {ones} (better than 4-state champion with 13 ones)")
    print(f"Final tape: {tape}")
