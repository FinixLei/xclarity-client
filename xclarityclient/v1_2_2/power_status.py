power_status_list = {
    0: 'unknown',
    5: 'off',
    8: 'on',
    18: 'standby'
}

power_status_action = [
    'powerOn',  # powers on the server
    'powerOff',  # powers off the server immediately
    'powerCycleSoft',  # restarts the server immediately
    'powerCycleSoftGrace',  # restarts the server gracefully
    # 'virtualReseat',  # calls the CMM function to simulate removing power from the bay
    # 'powerNMI',  # restarts the server with non-maskable interrupt (performs a diagnostic interrupt)
    # 'bootToF1',  # (Lenovo endpoints only) Powers on to UEFI(F1)
]
