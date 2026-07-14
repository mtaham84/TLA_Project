from turing_machine import TuringMachine

transitions = {
    ('a', '0'): ('b', '1', 'R'),
    ('a', '1'): ('b', '1', 'L'),
    ('b', '0'): ('a', '1', 'L'),
    ('b', '1'): ('h', '1', 'R'),
}

if __name__ == "__main__":
    tm = TuringMachine(transitions, start_state='a', accept_state='h', reject_state='r', blank_symbol='0')
    tm.debug('', step_limit=20)  