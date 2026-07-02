from turing_machine import TuringMachine

# یک ماشین ساده که یک '#' را می‌پذیرد
transitions = {
    ('q0', '#'): ('qa', '#', 'R'),
    ('q0', ''): ('qr', '', 'R'),
}
tm = TuringMachine(transitions, start_state='q0', accept_state='qa', reject_state='qr', blank_symbol='')

print("Testing accepts('#'):", tm.accepts("#"))   # باید True
print("Testing accepts(''):", tm.accepts(""))    # باید False
tm.debug("#")