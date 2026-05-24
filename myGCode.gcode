M17 ; Enable all stepper motors
G90 ; Set to Absolute Positioning
M83 ; Set extruder to relative mode
G28 ; Home all axes
G1 Z10 F1200 ; Lift nozzle to 10mm quickly for safety
G1 X20 Y20 F4800 ; Move to a safe starting area away from the edge
G1 Z5 F1200 ; Drop down to your target 5mm Z-height
G1 X219.5295757565 Y139.0531014089 ;
G1 X219.5295757565 Y280.4744576462 ;
G1 Z20 F1200 ; Lift nozzle safely up to 20mm when done
G1 X0 Y200 F4800 ; Present the bed (pushes bed forward, moves X to 0)
M84 ; Disable stepper motors
