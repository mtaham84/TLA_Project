class TuringMachine:
    def __init__(self, transitions, start_state='q0', accept_state='qa',
                 reject_state='qr', blank_symbol='', finite=False):
        """
        transitions: dict {(state, symbol): (next_state, write_symbol, direction)}
        finite: controls the tape's boundary behaviour.
            - False (default): two-way infinite tape. The tape dynamically
              expands to the left and to the right as the head moves past
              either edge. This is the mode used throughout Part 1 & 3 of
              the project (busy beaver, adder, multiplier, ...).
            - True: bounded/finite tape. The tape size is fixed to the
              length of the initial input (minimum 1 cell). If the head
              tries to move past either edge the machine halts by moving
              to the reject state (a warning is logged, no exception is
              raised).
            - 'toroidal': bounded tape of the same fixed size as above, but
              moving past either edge wraps around to the opposite edge
              (i.e. the tape behaves like a ring).
        """
        self.transitions = transitions
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.blank_symbol = blank_symbol
        self.finite = finite

    def run(self, input_str):
        tape = list(input_str) if input_str else []
        head = 0
        state = self.start_state

        if not tape:
            tape = [self.blank_symbol]

        fixed_size = len(tape)

        while True:
            symbol = tape[head] if head < len(tape) else self.blank_symbol

            left_part = tape[:head]
            right_part = tape[head+1:] if head+1 < len(tape) else []
            config = {
                'state': state,
                'left_hand_side': left_part[::-1],  
                'symbol': symbol,
                'right_hand_side': right_part
            }

            if state == self.accept_state:
                yield ('Accept', config)
                return
            if state == self.reject_state:
                yield ('Reject', config)
                return

            yield (None, config)

            key = (state, symbol)
            if key not in self.transitions:
                state = self.reject_state
                continue

            next_state, write_symbol, direction = self.transitions[key]

            if head < len(tape):
                tape[head] = write_symbol
            else:
                tape.append(write_symbol)

            if direction == 'R':
                head += 1
                if self.finite == 'toroidal':
                    if head >= fixed_size:
                        head = 0  
                elif self.finite:
                    if head >= fixed_size:
                        
                        print("⚠️ Warning: Head moved past right boundary of finite tape; reject state activated.")
                        state = self.reject_state
                        continue
                else:
                    if head >= len(tape):
                        tape.append(self.blank_symbol)
            elif direction == 'L':
                if self.finite == 'toroidal':
                    head -= 1
                    if head < 0:
                        head = fixed_size - 1  
                elif self.finite:
                    head -= 1
                    if head < 0:
                        
                        print("⚠️ Warning: Head moved past left boundary of finite tape; reject state activated.")
                        state = self.reject_state
                        continue
                else:
                    if head == 0:
                        
                        tape.insert(0, self.blank_symbol)
                        
                    else:
                        head -= 1
            else:
                raise ValueError(f"Invalid direction: {direction}")

            state = next_state

    def accepts(self, input_str, step_limit=10000):
        gen = self.run(input_str)
        for i, (action, config) in enumerate(gen):
            if i >= step_limit:
                return None
            if action == 'Accept':
                return True
            if action == 'Reject':
                return False
        return False

    def rejects(self, input_str, **kwargs):
        result = self.accepts(input_str, **kwargs)
        if result is None:
            return None
        return not result

    def debug(self, input_str, step_limit=100, colored=False):
        for i, (action, config) in enumerate(self.run(input_str)):
            if i >= step_limit:
                print(f"Step limit ({step_limit}) reached.")
                break
            left = ''.join(reversed(config['left_hand_side']))
            right = ''.join(config['right_hand_side'])
            sym = config['symbol']
            state = config['state']
            print(f"step: {i:2d}: state={state:5s}, strip = {left}[{sym}]{right}")
            if action in ('Accept', 'Reject'):
                print(f"Final action: {action}")
                break