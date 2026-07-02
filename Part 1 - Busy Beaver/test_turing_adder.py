# test_turing_adder.py
from turing_machine import TuringMachine

# transitions برای جمع یکانی
# blank_symbol = '' (رشته خالی)
transitions = {
    # مرحله 1: حرکت به راست تا به 0 برسیم
    ('q0', '1'): ('q0', '1', 'R'),
    ('q0', '0'): ('q1', '1', 'R'),   # 0 را به 1 تبدیل کن و برو به q1
    ('q0', ''): ('qa', '', 'R'),     # اگر ورودی فقط یک عدد بود (مثلاً "111")، بپذیر

    # مرحله 2: رد شدن از 1های عدد دوم تا به انتها برسیم
    ('q1', '1'): ('q1', '1', 'R'),
    ('q1', ''): ('q2', '', 'L'),     # به انتها رسیدیم، برگرد

    # مرحله 3: برگشت به چپ تا به اولین 1 (که قبلاً 0 بود) برسیم و آن را حذف کنیم
    ('q2', '1'): ('q2', '1', 'L'),
    ('q2', ''): ('qa', '', 'R'),     # اگر به ابتدا برگشتیم، بپذیر
}

if __name__ == "__main__":
    machine = TuringMachine(transitions, start_state='q0', accept_state='qa', reject_state='qr', blank_symbol='')
    
    def run_test(input_str):
        print(f"ورودی: {input_str}")
        print("پذیرش" if machine.accepts(input_str) else "رد")
        machine.debug(input_str)
        print()
    
    # تست‌ها
    run_test("110111")    # 2+3 = 5 -> "11111"
    run_test("11101111")  # 3+4 = 7 -> "1111111"
    run_test("111")       # فقط یک عدد، باید پذیرفته شود (حالت مرزی)