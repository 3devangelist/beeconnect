

---
### beeconnect_0.3.bin

##### start.gcode:
  > //PID config  
  > +M130 T6 U1.3 V80

#### M109:
  > +prints temperature every 20s

#### m114:
  > +bugfix - get current positions as assigned to another mcode:  
  >  now: ok C: X:9.15 Y:9.15 Z:1.00 E:136.84

#### m105:
  > +bugfix - endline missing:  
  >  now: ok T:219.82 /220.00 B:-237.00 /-237.00

---
#### BEECONNECT_0.2.bin

 
##### M105: Get Extruder Temperature  

BEECONNECT_0.1:
> T:11.0000 B:0.0000 ok Q:0 

BEECONNECT_0.2: 
> `ok T:<current> /<target>  B:<-237.0>  Q:0` 

Utilmaker,marlin, etc:  
> ok T:29.0 /29.0 B:29.5 /29.0 @:0

 
##### M110: Set Current Line Number  

Example: M110 N123  

Set the current line number to 123. Thus the expected next line after this command will be 124. 
##### G90: Set to Absolute Positioning  

Example: G90  

All coordinates from now on are absolute relative to the origin of the machine. (This is the RepRap default.)  

##### G91: Set to Relative Positioning  

Example: G91  

All coordinates from now on are relative to the last position.  
##### M302: Allow cold extrudes  

This tells the printer to allow movement of the extruder motor, when the hotend is not at printing temperature  

Example:
> M302 S`<minimun_temperature>`

> M302 (assume S0)
