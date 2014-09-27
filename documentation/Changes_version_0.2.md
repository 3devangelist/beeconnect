Changes to be implemented in firmware: BEECONNECT_0.2 

 
##### M105: Get Extruder Temperature  

BEECONNECT_0.1:
> T:11.0000 B:0.0000 ok Q:0 

BEECONNECT_0.2: 
> ok T:<current> /<target>  B:<-237.0>  Q:0 

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
