| BL/FW        | Comm           | Arguments  | Description | 
| ------------- |------------- | ----- | ----|
| F | G0 | [X *value* ] [Y *value* ] [Z *value* ] [F *value* ] | synchronized movement |
| F | G1 | [X *value* ] [Y *value* ] [Z *value* ] [F *value* ] [E *value* ] | synchronized movement |
| F | G28 | [X] [Y] [Z] [F] [E] | home |
| F | G92 | [X *value* ] [Y *value* ] [Z *value* ] [F *value* ] [E *value* ] | define position |
| F | M20 |   | list files in root folder |
| F | M21 |   | init sd card |
| F | M23 | *file name* | open file to read |
| F | M25 |   | pause sd printing |
| F | M26 | S *position* | set sd file pos |
| F | M28 | A *file write start position*  D *file write end position* | get transfer size and begin if valid |
| F | M30 | *file name* | open file to write |
| F | M31 | A *estimated time* L *number of lines* | variables of standalone |
| F | M32 |   | print variables of standalone |
| F | M33 |   | start print |
| F | M104 | S *value* | define temperature |
| F | M105 |   | read temperature | 
| F | M106 |   | turn the blower on |
| F | M107 |   | turn the blower off |
| F | M109 | S *value* | define temperature and block |
| F | M112 |   | stop |
| B | M114 | A *version name* | write firmware version |
| B/F | M115 |  | read firmware version |
| B | M116 | | read bootloader version |
| B/F | M117 |   | read serial number |
| F | M121 |  | write position |
| F | M130 | [T *kp* ] [U *ki* ] [V *kd*] | temperature pid parameters | 
| F | M131 |   | print pwm values |
| F | M200 | [X *value* ] [Y *value* ] [Z *value* ] [F *value* ] [E *value* ] | Define steps per mm|
| F | M206 | [X *value* ] [Y] [Z] [F] [E] | define or print acceleration |
| F | M300 | [P *value* ] | beep | 
| F | M400 | [A *value* ] | define or print BEECode |
| F | M600 | | print configuration variables |
| F | M601 |  | write configuration variables |
| F | M603 |   | calibration |
| F | M604 | [X *value* ] [Y *value* ] [Z *value* ] | new absolute offset |
| F | M605 | [X *value* ] [Y *value* ] [Z *value* ] | new relative offset |
| F | M607 |   | reset configuration variables |
| B/F | M609 |   | reset R2C2 |
| F | M625 |  | status |
| B | M630 |   | switchs to firmware |
| F | M638 |  | get last executed command |
| F | M639 | | echo |
