import sys
from turing_machine import TuringMachine

beaver_programs = [
    {},
    {
        ('a', '0'): ('h', '1', 'R')
    },
    {
        ('a', '0'): ('b', '1', 'R'),
        ('a', '1'): ('b', '1', 'L'),
        ('b', '0'): ('a', '1', 'L'),
        ('b', '1'): ('h', '1', 'R')
    },
    {
        ('a', '0'): ('b', '1', 'R'),
        ('a', '1'): ('c', '1', 'R'),
        ('b', '0'): ('c', '0', 'L'),
        ('b', '1'): ('b', '1', 'R'),
        ('c', '0'): ('a', '1', 'L'),
        ('c', '1'): ('h', '1', 'L')
    },
    {
        ('a', '0'): ('b', '1', 'R'),
        ('a', '1'): ('b', '1', 'L'),
        ('b', '0'): ('a', '1', 'L'),
        ('b', '1'): ('c', '1', 'R'),
        ('c', '0'): ('h', '1', 'R'),
        ('c', '1'): ('d', '0', 'L'),
        ('d', '0'): ('d', '1', 'R'),
        ('d', '1'): ('a', '1', 'R')
    },
    {
        ('a', '0'): ('b', '1', 'R'),
        ('a', '1'): ('c', '1', 'L'),
        ('b', '0'): ('a', '1', 'L'),
        ('b', '1'): ('b', '1', 'R'),
        ('c', '0'): ('a', '0', 'L'),
        ('c', '1'): ('d', '0', 'L'),
        ('d', '0'): ('e', '0', 'R'),
        ('d', '1'): ('c', '1', 'L'),
        ('e', '0'): ('a', '1', 'L'),
        ('e', '1'): ('h', '1', 'R')
    }
]

def busy_beaver(n):
    if n < 1 or n >= len(beaver_programs):
        print("Invalid n")
        return
    program = beaver_programs[n]
    tm = TuringMachine(program, start_state='a', accept_state='h', reject_state='r', blank_symbol='0')
    state, tape = tm.run('')
    ones = tape.count('1')
    print(f"{n}-state Busy Beaver: {ones} ones (tape: {tape[:50]}...)")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python busy_beaver.py <n>")
        sys.exit(1)
    n = int(sys.argv[1])
    busy_beaver(n)