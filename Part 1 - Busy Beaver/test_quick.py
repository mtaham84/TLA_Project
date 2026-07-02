from turing_machine import TuringMachine

# ماشینی که فقط "#" را می‌پذیرد (و "##" را رد می‌کند)
transitions = {
    ('q0', '#'): ('saw_#', '#', 'R'),   # بعد از دیدن # به state موقت برو
    ('saw_#', ''): ('qa', '', 'R'),     # اگر بعد از # به انتهای نوار رسیدی، بپذیر
}
tm = TuringMachine(transitions, start_state='q0', accept_state='qa', reject_state='qr', blank_symbol='')

print("تست ۱:", tm.accepts("#"))    # باید True
print("تست ۲:", tm.accepts("##"))   # باید False
tm.debug("#")
tm.debug("##")