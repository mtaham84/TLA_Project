# test_turing_multiplier.py
from turing_machine import TuringMachine

transitions = {
    # q0: رفتن به انتهای نوار و گذاشتن جداکننده ۰ برای نتیجه
    ('q0', '1'): ('q0', '1', 'R'),
    ('q0', '0'): ('q0', '0', 'R'),
    ('q0', ''): ('q1', '0', 'L'),

    # q1: برگشت به ابتدای نوار
    ('q1', '1'): ('q1', '1', 'L'),
    ('q1', '0'): ('q1', '0', 'L'),
    ('q1', ''): ('q2', '', 'R'),

    # q2: پیدا کردن یک ۱ در عدد اول، علامت‌گذاری با X
    ('q2', '1'): ('q3', 'X', 'R'),
    ('q2', 'X'): ('q2', 'X', 'R'),
    ('q2', '0'): ('q_clean', '0', 'R'),
    ('q2', ''): ('q_clean', '', 'R'),

    # q3: رد شدن از عدد اول تا رسیدن به ۰ جداکننده
    ('q3', '1'): ('q3', '1', 'R'),
    ('q3', 'X'): ('q3', 'X', 'R'),
    ('q3', '0'): ('q4', '0', 'R'),

    # q4: پیدا کردن یک ۱ در عدد دوم و علامت‌گذاری با Y
    ('q4', '1'): ('q5', 'Y', 'R'),
    ('q4', '0'): ('q9', '0', 'L'),   # اگر عدد دوم تمام شد، برو به مرحله بعد

    # q5: رفتن به انتهای نوار و نوشتن یک ۱ (کپی کردن)
    ('q5', '1'): ('q5', '1', 'R'),
    ('q5', '0'): ('q5', '0', 'R'),
    ('q5', ''): ('q6', '1', 'L'),

    # q6: برگشت به علامت Y و حذف آن (تبدیل به ۱)
    ('q6', '1'): ('q6', '1', 'L'),
    ('q6', '0'): ('q6', '0', 'L'),
    ('q6', 'Y'): ('q7', '1', 'L'),

    # q7: برگشت به ۰ جداکننده (قبل از عدد دوم)
    ('q7', '1'): ('q7', '1', 'L'),
    ('q7', '0'): ('q8', '0', 'R'),

    # q8: حرکت به راست برای پیدا کردن ۱ بعدی در عدد دوم
    ('q8', '1'): ('q4', '1', 'R'),
    ('q8', '0'): ('q9', '0', 'L'),

    # q9: برگشت به ۰ جداکننده (قبل از عدد اول)
    ('q9', '1'): ('q9', '1', 'L'),
    ('q9', '0'): ('q10', '0', 'L'),

    # q10: برگشت به اولین X در عدد اول
    ('q10', '1'): ('q10', '1', 'L'),
    ('q10', 'X'): ('q11', 'X', 'R'),
    ('q10', ''): ('q_clean', '', 'R'),

    # q11: پیدا کردن ۱ بعدی در عدد اول و علامت‌گذاری با X
    ('q11', '1'): ('q2', 'X', 'R'),
    ('q11', 'X'): ('q11', 'X', 'R'),
    ('q11', '0'): ('q_clean', '0', 'R'),
    ('q11', ''): ('q_clean', '', 'R'),

    # q_clean: پاکسازی نهایی – تبدیل X به ۱ و حذف ۰های اضافی
    ('q_clean', 'X'): ('q_clean', '1', 'R'),
    ('q_clean', '1'): ('q_clean', '1', 'R'),
    ('q_clean', '0'): ('q_clean', '', 'R'),   # ۰های جداکننده را حذف کن
    ('q_clean', ''): ('qa', '', 'R'),         # به انتها رسیدیم، بپذیر
}

if __name__ == "__main__":
    machine = TuringMachine(transitions, start_state='q0', accept_state='qa', reject_state='qr', blank_symbol='')
    
    def run_test(inp):
        print(f"Input: {inp}")
        result = machine.accepts(inp, step_limit=1000)
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
            print(f"Final tape: {tape}")
        print()
    
    run_test("110111")      # 2*3 = 6
    run_test("11101111")    # 3*4 = 12