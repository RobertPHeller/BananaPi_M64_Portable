EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:switches
LIBS:relays
LIBS:motors
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:xl6009
LIBS:mechanical
LIBS:DCDC3_7-5+12-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 3
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Sheet
S 2700 2150 1900 1350
U 62AA2A0D
F0 "DCDC 3.7 - 12" 60
F1 "DCDC3-7-12.sch" 60
F2 "3.7V" I L 2700 2450 60 
F3 "GND" I L 2700 2650 60 
F4 "12V" I R 4600 2550 60 
$EndSheet
$Sheet
S 2650 4600 2250 1450
U 62AA2A38
F0 "DCDC 3.7 to 5" 60
F1 "DCDC3-7-5.sch" 60
F2 "3.7V" I L 2650 4950 60 
F3 "GND" I L 2650 5250 60 
F4 "5V" I R 4900 5100 60 
$EndSheet
$Comp
L Screw_Terminal_01x02 T1
U 1 1 62AA365C
P 1400 3400
F 0 "T1" H 1400 3500 50  0000 C CNN
F 1 "+ 3.7V -" H 1400 3200 50  0000 C CNN
F 2 "Terminal_Blocks:TerminalBlock_Pheonix_MPT-2.54mm_2pol" H 1400 3400 50  0001 C CNN
F 3 "" H 1400 3400 50  0001 C CNN
	1    1400 3400
	-1   0    0    -1  
$EndComp
Wire Wire Line
	1600 3400 1600 2450
Wire Wire Line
	1600 2450 2700 2450
Wire Wire Line
	2650 4950 2200 4950
Wire Wire Line
	2200 4950 2200 2450
Connection ~ 2200 2450
Wire Wire Line
	2700 2650 2500 2650
Wire Wire Line
	2500 2650 2500 5250
Wire Wire Line
	2500 5250 2650 5250
Connection ~ 2500 3500
Wire Wire Line
	1600 3500 2500 3500
$Comp
L Screw_Terminal_01x02 T2
U 1 1 62AA399B
P 5600 2950
F 0 "T2" H 5600 3050 50  0000 C CNN
F 1 "+ 12V -" H 5600 2750 50  0000 C CNN
F 2 "Terminal_Blocks:TerminalBlock_Pheonix_MPT-2.54mm_2pol" H 5600 2950 50  0001 C CNN
F 3 "" H 5600 2950 50  0001 C CNN
	1    5600 2950
	1    0    0    -1  
$EndComp
$Comp
L Screw_Terminal_01x02 T3
U 1 1 62AA39D8
P 5800 4950
F 0 "T3" H 5800 5050 50  0000 C CNN
F 1 "+ 5V -" H 5800 4750 50  0000 C CNN
F 2 "Terminal_Blocks:TerminalBlock_Pheonix_MPT-2.54mm_2pol" H 5800 4950 50  0001 C CNN
F 3 "" H 5800 4950 50  0001 C CNN
	1    5800 4950
	1    0    0    -1  
$EndComp
Wire Wire Line
	4600 2550 5150 2550
Wire Wire Line
	5150 2550 5150 2950
Wire Wire Line
	5150 2950 5400 2950
Wire Wire Line
	5150 5100 4900 5100
Wire Wire Line
	5150 4550 5150 5100
Wire Wire Line
	5150 4950 5600 4950
Wire Wire Line
	5400 3050 5400 6850
Wire Wire Line
	5400 5000 5600 5000
Wire Wire Line
	5600 5000 5600 5050
Wire Wire Line
	5400 3950 2500 3950
Wire Wire Line
	2500 3950 2500 3900
Connection ~ 2500 3900
Connection ~ 5400 3950
$Comp
L Mounting_Hole MK1
U 1 1 62AB236D
P 4050 6700
F 0 "MK1" H 4050 6900 50  0000 C CNN
F 1 "Mounting_Hole" H 4050 6825 50  0000 C CNN
F 2 "Mounting_Holes:MountingHole_3.5mm" H 4050 6700 50  0001 C CNN
F 3 "" H 4050 6700 50  0001 C CNN
	1    4050 6700
	1    0    0    -1  
$EndComp
$Comp
L Mounting_Hole MK2
U 1 1 62AB23F8
P 4500 6750
F 0 "MK2" H 4500 6950 50  0000 C CNN
F 1 "Mounting_Hole" H 4500 6875 50  0000 C CNN
F 2 "Mounting_Holes:MountingHole_3.5mm" H 4500 6750 50  0001 C CNN
F 3 "" H 4500 6750 50  0001 C CNN
	1    4500 6750
	1    0    0    -1  
$EndComp
$Comp
L Mounting_Hole MK3
U 1 1 62AB2447
P 4950 6700
F 0 "MK3" H 4950 6900 50  0000 C CNN
F 1 "Mounting_Hole" H 4950 6825 50  0000 C CNN
F 2 "Mounting_Holes:MountingHole_3.5mm" H 4950 6700 50  0001 C CNN
F 3 "" H 4950 6700 50  0001 C CNN
	1    4950 6700
	1    0    0    -1  
$EndComp
$Comp
L Mounting_Hole_PAD MK4
U 1 1 62AB248C
P 5550 6700
F 0 "MK4" H 5550 6950 50  0000 C CNN
F 1 "Mounting_Hole_PAD" H 5550 6875 50  0000 C CNN
F 2 "Mounting_Holes:MountingHole_3.5mm_Pad" H 5550 6700 50  0001 C CNN
F 3 "" H 5550 6700 50  0001 C CNN
	1    5550 6700
	1    0    0    -1  
$EndComp
Wire Wire Line
	5400 6850 5550 6850
Wire Wire Line
	5550 6850 5550 6800
Connection ~ 5400 5000
$Comp
L Conn_01x02_Male J1
U 1 1 62AB8A27
P 5700 4550
F 0 "J1" H 5700 4650 50  0000 C CNN
F 1 "FAN" H 5700 4350 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x02_Pitch2.54mm" H 5700 4550 50  0001 C CNN
F 3 "" H 5700 4550 50  0001 C CNN
	1    5700 4550
	-1   0    0    -1  
$EndComp
Wire Wire Line
	5500 4650 5400 4650
Connection ~ 5400 4650
Wire Wire Line
	5500 4550 5150 4550
Connection ~ 5150 4950
$EndSCHEMATC
