
from turing_machine import TuringMachine

transitions = {
    ('q0', '1'): ('q0', '1', 'R'),
    ('q0', '0'): ('q0', '0', 'R'),
    ('q0', ''):  ('q1', '0', 'L'),

    ('q1', '1'): ('q1', '1', 'L'),
    ('q1', '0'): ('q1', '0', 'L'),
    ('q1', ''):  ('q2', '', 'R'),

    ('q2', 'X'): ('q2', 'X', 'R'),
    ('q2', '1'): ('qA1', 'X', 'R'),
    ('q2', '0'): ('cleanA', '', 'L'),   

    ('qA1', '1'): ('qA1', '1', 'R'),
    ('qA1', 'X'): ('qA1', 'X', 'R'),
    ('qA1', '0'): ('qB0', '0', 'R'),

    ('qB0', 'Y'): ('qB0', 'Y', 'R'),
    ('qB0', '1'): ('qCopy', 'Y', 'R'),
    ('qB0', '0'): ('restoreY', '0', 'L'),   

    ('qCopy', 'Y'): ('qCopy', 'Y', 'R'),
    ('qCopy', '1'): ('qCopy', '1', 'R'),
    ('qCopy', '0'): ('qCopy', '0', 'R'),
    ('qCopy', ''):  ('qBack', '1', 'L'),

    ('qBack', '1'): ('qBack', '1', 'L'),
    ('qBack', '0'): ('qBack', '0', 'L'),
    ('qBack', 'X'): ('qBack', 'X', 'L'),
    ('qBack', 'Y'): ('qBack', 'Y', 'L'),
    ('qBack', ''):  ('qSkipA', '', 'R'),

    ('qSkipA', '1'): ('qSkipA', '1', 'R'),
    ('qSkipA', 'X'): ('qSkipA', 'X', 'R'),
    ('qSkipA', '0'): ('qB0', '0', 'R'),

    ('restoreY', 'Y'): ('restoreY', '1', 'L'),
    ('restoreY', '1'): ('restoreY', '1', 'L'),
    ('restoreY', '0'): ('restoreY', '0', 'L'),
    ('restoreY', 'X'): ('restoreY', 'X', 'L'),
    ('restoreY', ''):  ('q2', '', 'R'),

    ('cleanA', 'X'): ('cleanA', '', 'L'),
    ('cleanA', ''):  ('cleanA2', '', 'R'),

    ('cleanA2', '1'): ('cleanA2', '', 'R'),   
    ('cleanA2', '0'): ('cleanA3', '', 'R'),   
    ('cleanA2', ''):  ('cleanA2', '', 'R'),   
    ('cleanA3', '1'): ('cleanA3', '1', 'R'), 
    ('cleanA3', ''):  ('qa', '', 'R'),        
}

if __name__ == "__main__":
    machine = TuringMachine(transitions, start_state='q0', accept_state='qa',
                             reject_state='qr', blank_symbol='')

    def run_test(inp, step_limit=50000):
        print(f"Input: {inp}")
        result = machine.accepts(inp, step_limit=step_limit)
        print("Accepted" if result else "Rejected")

        gen = machine.run(inp)
        last_config = None
        for action, config in gen:
            last_config = config
            if action in ('Accept', 'Reject'):
                break
        if last_config:
            left = ''.join(reversed(last_config['left_hand_side']))
            right = ''.join(last_config['right_hand_side'])
            tape = left + last_config['symbol'] + right
            print(f"Final tape: {tape}  (ones={tape.count('1')})")
        print()

    run_test("110111")      
    run_test("11101111")    
    run_test("111011111")   
