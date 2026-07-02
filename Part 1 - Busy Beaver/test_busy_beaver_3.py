# test_busy_beaver_3.py
from turing_machine import TuringMachine

transitions_bb3 = {
    ('a', '0'): ('b', '1', 'R'),
    ('a', '1'): ('c', '1', 'L'),   # <-- L بود، نه R
    ('b', '0'): ('a', '1', 'L'),   # <-- به a می‌رود، نه c
    ('b', '1'): ('b', '1', 'R'),
    ('c', '0'): ('a', '1', 'L'),
    ('c', '1'): ('h', '1', 'R'),
}

if __name__ == "__main__":
    tm = TuringMachine(transitions_bb3, start_state='a', accept_state='h', reject_state='r', blank_symbol='0')
    tm.debug('', step_limit=50)
    
    gen = tm.run('')
    last_config = None
    for action, config in gen:
        last_config = config
        if action == 'Accept':
            break
    if last_config:
        left = ''.join(reversed(last_config['left_hand_side']))
        right = ''.join(last_config['right_hand_side'])
        tape = left + last_config['symbol'] + right
        ones = tape.count('1')
        print(f"\n✅ BB-3: تعداد ۱ها = {ones}")
        print(f"نوار نهایی: {tape}")