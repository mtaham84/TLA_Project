# -*- coding: utf-8 -*-
class TuringMachine:
    def __init__(self, transitions, start_state='q0', accept_state='qa',
                 reject_state='qr', blank_symbol=''):
        self.transitions = transitions
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.blank_symbol = blank_symbol

    def run(self, input_str):
        # نوار را به صورت لیست کامل نگه می‌داریم
        tape = list(input_str) if input_str else []
        head = 0
        state = self.start_state

        if not tape:
            tape = [self.blank_symbol]

        while True:
            # خواندن نماد زیر هد
            symbol = tape[head] if head < len(tape) else self.blank_symbol

            # ساخت پیکربندی فعلی
            left_part = tape[:head]
            right_part = tape[head+1:] if head+1 < len(tape) else []
            config = {
                'state': state,
                'left_hand_side': left_part[::-1],  # معکوس (نزدیک‌ترین به هد در انتها)
                'symbol': symbol,
                'right_hand_side': right_part
            }

            # بررسی حالت پذیرش/رد
            if state == self.accept_state:
                yield ('Accept', config)
                return
            if state == self.reject_state:
                yield ('Reject', config)
                return

            # همیشه گام فعلی را yield کن
            yield (None, config)

            # پیدا کردن انتقال
            key = (state, symbol)
            if key not in self.transitions:
                state = self.reject_state
                continue

            next_state, write_symbol, direction = self.transitions[key]

            # نوشتن روی نوار
            if head < len(tape):
                tape[head] = write_symbol
            else:
                tape.append(write_symbol)

            # حرکت هد
            if direction == 'R':
                head += 1
                if head >= len(tape):
                    tape.append(self.blank_symbol)
            elif direction == 'L':
                if head == 0:
                    # گسترش به چپ
                    tape.insert(0, self.blank_symbol)
                    # head همچنان 0 است (چون جلوتر نیامده)
                else:
                    head -= 1
            else:
                raise ValueError(f"جهت نامعتبر: {direction}")

            state = next_state
            # حلقه تکرار می‌شود و گام بعدی را yield می‌کند

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
                print(f"محدودیت گام ({step_limit}) رسید.")
                break
            left = ''.join(reversed(config['left_hand_side']))
            right = ''.join(config['right_hand_side'])
            sym = config['symbol']
            state = config['state']
            print(f"گام {i:2d}: state={state:5s}, نوار={left}[{sym}]{right}")
            if action in ('Accept', 'Reject'):
                print(f"اقدام نهایی: {action}")
                break