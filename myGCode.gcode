M17 ; Enable all stepper motors
G90 ; Set to Absolute Positioning
M83 ; Set extruder to relative mode
G28 ; Home all axes
G1 Z10 F1200 ; Lift nozzle to 10mm quickly for safety
G1 X20 Y20 F4800 ; Move to a safe starting area away from the edge
G1 Z5 F1200 ; Drop down to your target 5mm Z-height
G1 X52.50000000000166 Y109.27777777779221 F1200;
G1 Z3 F1200
G1 Z5 F1200
G1 X87.77777777777943 Y74.00000000001444 F1200;
G1 Z3 F1200
G1 Z5 F1200
G1 X52.50000000000166 Y38.72222222223666 F1200;
G1 Z3 F1200
G1 Z5 F1200
G1 X17.222222222223888 Y74.00000000001444 F1200;
G1 Z3 F1200
G1 Z5 F1200
G1 Z20 F1200 ; Lift nozzle safely up to 20mm when done
G1 X0 Y200 F4800 ; Present the bed (pushes bed forward, moves X to 0)
M84 ; Disable stepper motors
