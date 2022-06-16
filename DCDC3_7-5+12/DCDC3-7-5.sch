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
Sheet 3 3
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L XL6009 U2
U 1 1 62AA163E
P 5600 3700
F 0 "U2" H 5500 3700 30  0000 C CNN
F 1 "XL6009" H 5700 3700 30  0000 C CNN
F 2 "TO_SOT_Packages_SMD:TO-263-5_TabPin3" H 5600 3700 60  0001 C CNN
F 3 "" H 5600 3700 60  0001 C CNN
	1    5600 3700
	-1   0    0    -1  
$EndComp
$Comp
L CP1_Small C3
U 1 1 62AA183B
P 4900 3150
F 0 "C3" H 4910 3220 50  0000 L CNN
F 1 "220uf 50V" H 4910 3070 50  0000 L CNN
F 2 "Capacitors_SMD:CP_Elec_10x10.5" H 4900 3150 50  0001 C CNN
F 3 "" H 4900 3150 50  0001 C CNN
F 4 "667-EEE-FK1H221V " H 4900 3150 60  0001 C CNN "Mouser Part Number"
	1    4900 3150
	1    0    0    -1  
$EndComp
Wire Wire Line
	4700 3000 5700 3000
Wire Wire Line
	5500 3000 5500 3350
Wire Wire Line
	5700 3000 5700 3350
Connection ~ 5500 3000
Wire Wire Line
	4900 2800 4900 3050
Connection ~ 4900 3000
Wire Wire Line
	5800 3350 5800 3200
Wire Wire Line
	5800 3200 5950 3200
Wire Wire Line
	5950 3200 5950 4100
Wire Wire Line
	4700 4100 6950 4100
Wire Wire Line
	4700 4100 4700 3100
Wire Wire Line
	4900 3250 4900 4100
Connection ~ 4900 4100
$Comp
L L_Small L2
U 1 1 62AA3BD9
P 5150 2800
F 0 "L2" H 5180 2840 50  0000 L CNN
F 1 "33uH" H 5180 2760 50  0000 L CNN
F 2 "PM5022S-330M-RC:INDPM183140X690N" H 5150 2800 50  0001 C CNN
F 3 "" H 5150 2800 50  0001 C CNN
	1    5150 2800
	0    -1   -1   0   
$EndComp
Wire Wire Line
	4900 2800 5050 2800
Wire Wire Line
	5600 3350 5600 2800
Wire Wire Line
	5250 2800 5700 2800
$Comp
L D_Schottky D2
U 1 1 62AA3BDA
P 5850 2800
F 0 "D2" H 5850 2900 50  0000 C CNN
F 1 "SS34" H 5850 2700 50  0000 C CNN
F 2 "Diodes_SMD:D_SMB_Handsoldering" H 5850 2800 50  0001 C CNN
F 3 "" H 5850 2800 50  0001 C CNN
F 4 "750-SS34BF-HF" H 5850 2800 60  0001 C CNN "Mouser Part Number"
	1    5850 2800
	-1   0    0    1   
$EndComp
Connection ~ 5600 2800
$Comp
L CP1_Small C4
U 1 1 62AA3BDB
P 6600 3150
F 0 "C4" H 6610 3220 50  0000 L CNN
F 1 "220uf 50V" H 6610 3070 50  0000 L CNN
F 2 "Capacitors_SMD:CP_Elec_10x10.5" H 6600 3150 50  0001 C CNN
F 3 "" H 6600 3150 50  0001 C CNN
F 4 "667-EEE-FK1H221V " H 6600 3150 60  0001 C CNN "Mouser Part Number"
	1    6600 3150
	1    0    0    -1  
$EndComp
Wire Wire Line
	6600 3050 6600 2800
Wire Wire Line
	6000 2800 6950 2800
Wire Wire Line
	6600 4100 6600 3250
Connection ~ 5950 4100
$Comp
L R R3
U 1 1 62AA3BDC
P 6250 3150
F 0 "R3" V 6330 3150 50  0000 C CNN
F 1 "3K" V 6250 3150 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 6180 3150 50  0001 C CNN
F 3 "" H 6250 3150 50  0001 C CNN
	1    6250 3150
	1    0    0    -1  
$EndComp
$Comp
L R R4
U 1 1 62AA3BDD
P 6250 3750
F 0 "R4" V 6330 3750 50  0000 C CNN
F 1 "1K" V 6250 3750 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 6180 3750 50  0001 C CNN
F 3 "" H 6250 3750 50  0001 C CNN
	1    6250 3750
	1    0    0    -1  
$EndComp
Wire Wire Line
	6250 3000 6250 2800
Connection ~ 6250 2800
Wire Wire Line
	6250 3600 6250 3300
Wire Wire Line
	6250 3900 6250 4100
Connection ~ 6250 4100
Wire Wire Line
	5400 3350 5400 3150
Wire Wire Line
	5400 3150 6100 3150
Wire Wire Line
	6100 3150 6100 3450
Wire Wire Line
	6100 3450 6250 3450
Connection ~ 6250 3450
Wire Wire Line
	6950 2800 6950 3250
Connection ~ 6600 2800
Wire Wire Line
	6950 4100 6950 3350
Connection ~ 6600 4100
Text HLabel 4700 3000 0    60   Input ~ 0
3.7V
Text HLabel 4700 3100 0    60   Input ~ 0
GND
Text HLabel 6950 3250 2    60   Input ~ 0
5V
Text HLabel 6950 3350 2    60   Input ~ 0
GND
$EndSCHEMATC
