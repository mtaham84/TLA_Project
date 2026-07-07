
from turing_machine import TuringMachine

transitions = {
    
    ('q0', '1'): ('q0', '1', 'R'),
    ('q0', '0'): ('q1', '1', 'R'),   
    ('q0', ''): ('qa', '', 'R'),     

    
    ('q1', '1'): ('q1', '1', 'R'),
    ('q1', ''): ('q2', '', 'L'),     

    
    ('q2', '1'): ('q2', '1', 'L'),
    ('q2', ''): ('q3', '', 'R'),     

    
    ('q3', '1'): ('qa', '', 'R'),
}

if __name__ == "__main__":
    machine = TuringMachine(transitions, start_state='q0', accept_state='qa',
                             reject_state='qr', blank_symbol='')

    def run_test(input_str):
        print(f"input: {input_str}")
        print("Accepted" if machine.accepts(input_str) else "Rejected")
        machine.debug(input_str)
        print()

    
    run_test("110111")    
    run_test("11101111")  
    run_test("111")       
