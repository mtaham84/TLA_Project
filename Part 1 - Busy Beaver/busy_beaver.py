

import sys
from turing_machine import TuringMachine


beaver_programs = [
    {},  
    {  
        ('a', '0'): ('h', '1', 'R'),
    },
    {  
        ('a', '0'): ('b', '1', 'R'),
        ('a', '1'): ('b', '1', 'L'),
        ('b', '0'): ('a', '1', 'L'),
        ('b', '1'): ('h', '1', 'R'),
    },
    {  
        ('a', '0'): ('b', '1', 'R'),
        ('a', '1'): ('c', '1', 'L'),
        ('b', '0'): ('a', '1', 'L'),
        ('b', '1'): ('b', '1', 'R'),
        ('c', '0'): ('a', '1', 'L'),
        ('c', '1'): ('h', '1', 'R'),
    },
    {  
        ('a', '0'): ('b', '1', 'R'),
        ('a', '1'): ('b', '1', 'L'),
        ('b', '0'): ('a', '1', 'L'),
        ('b', '1'): ('c', '0', 'L'),
        ('c', '0'): ('h', '1', 'R'),
        ('c', '1'): ('d', '1', 'L'),
        ('d', '0'): ('d', '1', 'R'),
        ('d', '1'): ('a', '0', 'R'),
    },
    {  
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
    },
]


def busy_beaver(n, step_limit=1_000_000, verbose=True):
    if n < 1 or n >= len(beaver_programs):
        print(f"Program for {n} states is not defined.")
        return None

    program = beaver_programs[n]
    tm = TuringMachine(program, start_state='a', accept_state='h',
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
        if steps > step_limit:
            outcome = 'step_limit_reached'
            break

    left = ''.join(reversed(last_config['left_hand_side']))
    right = ''.join(last_config['right_hand_side'])
    tape = left + last_config['symbol'] + right
    ones = tape.count('1')

    if verbose:
        halted = outcome == 'Accept'
        status = "Halted (Accept)" if halted else f"Did not halt ({outcome})"
        print(f"{n}-state Busy Beaver: {status} | steps={steps-1} | ones = {ones}")
        print(f"Final tape: {tape[:80]}{'...' if len(tape) > 80 else ''}")
    return outcome == 'Accept', steps - 1, ones, tape


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python busy_beaver.py <n>   (n between 1 and 5)")        
        for i in range(1, len(beaver_programs)):
            busy_beaver(i)
            print()
        sys.exit(0)
    n = int(sys.argv[1])
    busy_beaver(n)
