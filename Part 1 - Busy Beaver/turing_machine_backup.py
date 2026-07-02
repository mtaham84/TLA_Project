# -*- coding: utf-8 -*-
class TuringMachine:
    def __init__(self, transitions, start_state='q0', accept_state='qa', reject_state='qr', blank_symbol='_'):
        self.transitions = transitions
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.blank_symbol = blank_symbol

    def run(self, input_):
        tape = list(input_)
        head = 0
        state = self.start_state
        left = []
        right = tape[1:] if len(tape) > 1 else []
        current = tape[0] if tape else self.blank_symbol

        while state != self.accept_state and state != self.reject_state:
            key = (state, current)
            if key not in self.transitions:
                state = self.reject_state
                break
            new_state, write, move = self.transitions[key]
            current = write
            state = new_state

            if move == 'R':
                left.append(current)
                if right:
                    current = right.pop(0)
                else:
                    current = self.blank_symbol
            elif move == 'L':
                right.insert(0, current)
                if left:
                    current = left.pop()
                else:
                    current = self.blank_symbol
            else:
                raise ValueError("Invalid move")

            yield {
                'state': state,
                'left_hand_side': left.copy(),
                'symbol': current,
                'right_hand_side': right.copy()
            }

    def accepts(self, input_):
        try:
            for step in self.run(input_):
                if step['state'] == self.accept_state:
                    return True
            return False
        except:
            return False

    def rejects(self, input_):
        return not self.accepts(input_)

    def debug(self, input_, step_limit=1000):
        for i, cfg in enumerate(self.run(input_)):
            if i >= step_limit:
                print("Step limit reached")
                break
            left = ''.join(reversed(cfg['left_hand_side']))
            right = ''.join(cfg['right_hand_side'])
            print(f"Step {i}: state={cfg['state']}, tape={left}[{cfg['symbol']}] {right}")