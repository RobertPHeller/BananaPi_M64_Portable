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
LIBS:TPS61088QRHLRQ1
LIBS:lm3488
LIBS:DCDC3_7-5+12-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 2 3
Title "5v and 12v (from battery) power supply"
Date ""
Rev "1.0"
Comp "Deepwoods Software"
Comment1 "12V section"
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Text HLabel 4700 3000 0    60   Input ~ 0
3.7V
Text HLabel 4700 3100 0    60   Input ~ 0
GND
Text HLabel 8950 3100 2    60   Input ~ 0
12V
$Comp
L GND #PWR01
U 1 1 62CDA110
P 4700 3100
F 0 "#PWR01" H 4700 2850 50  0001 C CNN
F 1 "GND" H 4700 2950 50  0000 C CNN
F 2 "" H 4700 3100 50  0001 C CNN
F 3 "" H 4700 3100 50  0001 C CNN
	1    4700 3100
	1    0    0    -1  
$EndComp
$Comp
L LM3488 U1
U 1 1 62CF42F4
P 6700 3300
F 0 "U1" H 6700 3300 30  0000 C CNN
F 1 "LM3488" H 6900 3500 30  0000 C CNN
F 2 "Housings_SSOP:TSSOP-8_3x3mm_Pitch0.65mm" H 6700 3300 60  0001 C CNN
F 3 "" H 6700 3300 60  0001 C CNN
F 4 "926-LM3488MM " H 6700 3300 60  0001 C CNN "Mouser Part Number"
	1    6700 3300
	1    0    0    -1  
$EndComp
$Comp
L CP1_Small C1
U 1 1 62CF4538
P 5100 3100
F 0 "C1" H 5110 3170 50  0000 L CNN
F 1 "220uf" H 5110 3020 50  0000 L CNN
F 2 "Capacitors_SMD:CP_Elec_5x5.7" H 5100 3100 50  0001 C CNN
F 3 "" H 5100 3100 50  0001 C CNN
F 4 "667-6SVPE220MW " H 5100 3100 60  0001 C CNN "Mouser Part Number"
	1    5100 3100
	1    0    0    -1  
$EndComp
Wire Wire Line
	4950 3100 4950 4200
Wire Wire Line
	4950 3100 4700 3100
$Comp
L C_Small C2
U 1 1 62CF4737
P 5450 3100
F 0 "C2" H 5460 3170 50  0000 L CNN
F 1 "100nf" H 5460 3020 50  0000 L CNN
F 2 "Capacitors_SMD:C_0402" H 5450 3100 50  0001 C CNN
F 3 "" H 5450 3100 50  0001 C CNN
F 4 "81-GRM155R70J104KA1D " H 5450 3100 60  0001 C CNN "Mouser Part Number"
	1    5450 3100
	1    0    0    -1  
$EndComp
Connection ~ 5100 3000
Connection ~ 5450 3000
Wire Wire Line
	4700 3000 6400 3000
Wire Wire Line
	6400 2900 6400 3250
Wire Wire Line
	6650 3850 6750 3850
Wire Wire Line
	6750 3850 6750 3600
Wire Wire Line
	6650 3600 6650 4200
Connection ~ 6650 3850
$Comp
L C_Small C5
U 1 1 62CF4A22
P 5900 3650
F 0 "C5" H 5910 3720 50  0000 L CNN
F 1 "1nf" H 5910 3570 50  0000 L CNN
F 2 "Capacitors_SMD:C_0402" H 5900 3650 50  0001 C CNN
F 3 "" H 5900 3650 50  0001 C CNN
F 4 "81-GRM1555C1H102JA1J" H 5900 3650 60  0001 C CNN "Mouser Part Number"
	1    5900 3650
	1    0    0    -1  
$EndComp
$Comp
L C_Small C6
U 1 1 62CF4A43
P 6200 3550
F 0 "C6" H 6210 3620 50  0000 L CNN
F 1 "15nf" H 6210 3470 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805" H 6200 3550 50  0001 C CNN
F 3 "" H 6200 3550 50  0001 C CNN
F 4 "810-CGA4F2C0G1H153J " H 6200 3550 60  0001 C CNN "Mouser Part Number"
	1    6200 3550
	1    0    0    -1  
$EndComp
$Comp
L R R1
U 1 1 62CF4A62
P 6200 3900
F 0 "R1" V 6280 3900 50  0000 C CNN
F 1 "6.81K" V 6200 3900 50  0000 C CNN
F 2 "Resistors_SMD:R_0402" V 6130 3900 50  0001 C CNN
F 3 "" H 6200 3900 50  0001 C CNN
F 4 "71-CRCW0402-6.81K-E3" V 6200 3900 60  0001 C CNN "Mouser Part Number"
	1    6200 3900
	1    0    0    -1  
$EndComp
Wire Wire Line
	5900 3400 6400 3400
Wire Wire Line
	6200 3400 6200 3450
Connection ~ 6200 3400
Wire Wire Line
	5900 3400 5900 3550
Wire Wire Line
	6200 3650 6200 3750
Wire Wire Line
	5900 3750 5900 4300
Wire Wire Line
	4950 4200 8800 4200
Wire Wire Line
	6200 4200 6200 4050
$Comp
L GND #PWR02
U 1 1 62CF4B2E
P 5900 4300
F 0 "#PWR02" H 5900 4050 50  0001 C CNN
F 1 "GND" H 5900 4150 50  0000 C CNN
F 2 "" H 5900 4300 50  0001 C CNN
F 3 "" H 5900 4300 50  0001 C CNN
	1    5900 4300
	1    0    0    -1  
$EndComp
Connection ~ 5900 4200
$Comp
L R R2
U 1 1 62CF4C67
P 6850 3800
F 0 "R2" V 6930 3800 50  0000 C CNN
F 1 "40K" V 6850 3800 50  0000 C CNN
F 2 "Resistors_SMD:R_0805" V 6780 3800 50  0001 C CNN
F 3 "" H 6850 3800 50  0001 C CNN
F 4 "71-CRCW080540K0FKEA " V 6850 3800 60  0001 C CNN "Mouser Part Number"
	1    6850 3800
	1    0    0    -1  
$EndComp
Wire Wire Line
	6850 3600 6850 3650
Wire Wire Line
	6850 4200 6850 3950
Connection ~ 6200 4200
Connection ~ 6650 4200
$Comp
L R R7
U 1 1 62CF4DE7
P 7200 3650
F 0 "R7" V 7280 3650 50  0000 C CNN
F 1 "100" V 7200 3650 50  0000 C CNN
F 2 "Resistors_SMD:R_0402" V 7130 3650 50  0001 C CNN
F 3 "" H 7200 3650 50  0001 C CNN
F 4 "71-CRCW0402100RFKEDC " V 7200 3650 60  0001 C CNN "Mouser Part Number"
	1    7200 3650
	1    0    0    -1  
$EndComp
$Comp
L R R8
U 1 1 62CF4E14
P 7450 3950
F 0 "R8" V 7530 3950 50  0000 C CNN
F 1 "5m" V 7450 3950 50  0000 C CNN
F 2 "Resistors_SMD:R_0612" V 7380 3950 50  0001 C CNN
F 3 "" H 7450 3950 50  0001 C CNN
F 4 "71-WFCP06125L000FE66" V 7450 3950 60  0001 C CNN "Mouser Part Number"
	1    7450 3950
	1    0    0    -1  
$EndComp
$Comp
L C_Small C7
U 1 1 62CF4E3B
P 7200 4000
F 0 "C7" H 7210 4070 50  0000 L CNN
F 1 "10pf" H 7210 3920 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805" H 7200 4000 50  0001 C CNN
F 3 "" H 7200 4000 50  0001 C CNN
F 4 "187-CL21C100CBANNNC " H 7200 4000 60  0001 C CNN "Mouser Part Number"
	1    7200 4000
	1    0    0    -1  
$EndComp
Wire Wire Line
	7200 3400 7200 3500
Wire Wire Line
	7200 3800 7450 3800
Wire Wire Line
	7200 3800 7200 3900
Wire Wire Line
	7450 4100 7200 4100
Wire Wire Line
	7200 4100 7200 4200
Connection ~ 6850 4200
Wire Wire Line
	7200 3400 7050 3400
$Comp
L CSD16325Q5 Q1
U 1 1 62CF54E2
P 7700 3350
F 0 "Q1" H 7500 3650 50  0000 L CNN
F 1 " CSD16323Q3" H 7500 3100 50  0000 L CNN
F 2 "Q3:Q3" H 7700 3550 50  0001 C CIN
F 3 "" V 7700 3350 50  0001 L CNN
F 4 "595-CSD16323Q3 " H 7700 3350 60  0001 C CNN "Mouser Part Number"
	1    7700 3350
	1    0    0    1   
$EndComp
Wire Wire Line
	7400 3250 7050 3250
Wire Wire Line
	7400 3350 7400 3800
Connection ~ 7400 3450
Connection ~ 7400 3800
Connection ~ 7400 3550
$Comp
L R R5
U 1 1 62CF5A75
P 7200 2350
F 0 "R5" V 7280 2350 50  0000 C CNN
F 1 "1K" V 7200 2350 50  0000 C CNN
F 2 "Resistors_SMD:R_0402" V 7130 2350 50  0001 C CNN
F 3 "" H 7200 2350 50  0001 C CNN
F 4 "71-CRCW0402-1.0K" V 7200 2350 60  0001 C CNN "Mouser Part Number"
	1    7200 2350
	0    1    1    0   
$EndComp
Wire Wire Line
	6700 3050 6700 2350
Wire Wire Line
	6700 2350 7050 2350
$Comp
L GND #PWR03
U 1 1 62CF5AE6
P 7600 2350
F 0 "#PWR03" H 7600 2100 50  0001 C CNN
F 1 "GND" H 7600 2200 50  0000 C CNN
F 2 "" H 7600 2350 50  0001 C CNN
F 3 "" H 7600 2350 50  0001 C CNN
	1    7600 2350
	0    -1   -1   0   
$EndComp
Wire Wire Line
	7600 2350 7350 2350
$Comp
L R R6
U 1 1 62CF5BA5
P 7200 2650
F 0 "R6" V 7280 2650 50  0000 C CNN
F 1 "8.45K" V 7200 2650 50  0000 C CNN
F 2 "Resistors_SMD:R_0402" V 7130 2650 50  0001 C CNN
F 3 "" H 7200 2650 50  0001 C CNN
F 4 "71-CRCW0402-8.45K-E3" V 7200 2650 60  0001 C CNN "Mouser Part Number"
	1    7200 2650
	0    1    1    0   
$EndComp
Wire Wire Line
	7050 2650 6700 2650
Connection ~ 6700 2650
Wire Wire Line
	7350 2650 8800 2650
Wire Wire Line
	8800 2650 8800 3250
Wire Wire Line
	8800 3100 8950 3100
$Comp
L CP1_Small C8
U 1 1 62CF6011
P 8800 3350
F 0 "C8" H 8810 3420 50  0000 L CNN
F 1 "560uF" H 8810 3270 50  0000 L CNN
F 2 "Capacitors_SMD:CP_Elec_10x10.5" H 8800 3350 50  0001 C CNN
F 3 "" H 8800 3350 50  0001 C CNN
F 4 "667-20SVPF560M" H 8800 3350 60  0001 C CNN "Mouser Part Number"
	1    8800 3350
	1    0    0    -1  
$EndComp
Connection ~ 8800 3100
Wire Wire Line
	8800 4200 8800 3450
Connection ~ 7200 4200
$Comp
L D_Schottky D1
U 1 1 62CF6222
P 8400 3000
F 0 "D1" H 8400 3100 50  0000 C CNN
F 1 "550mV " H 8400 2900 50  0000 C CNN
F 2 "Diodes_SMD:D_SMC" H 8400 3000 50  0001 C CNN
F 3 "" H 8400 3000 50  0001 C CNN
F 4 "241-SK54_R1_00001 " H 8400 3000 60  0001 C CNN "Mouser Part Number"
	1    8400 3000
	-1   0    0    1   
$EndComp
Wire Wire Line
	8550 3000 8800 3000
Connection ~ 8800 3000
Wire Wire Line
	8000 2900 8000 3550
Connection ~ 8000 3450
Connection ~ 8000 3350
Wire Wire Line
	8000 3000 8250 3000
Connection ~ 8000 3250
$Comp
L L_Small L1
U 1 1 62CF64DF
P 7250 2900
F 0 "L1" H 7280 2940 50  0000 L CNN
F 1 "1.8uh" H 7280 2860 50  0000 L CNN
F 2 "XAL6030:INDM5564X32N" H 7250 2900 50  0001 C CNN
F 3 "" H 7250 2900 50  0001 C CNN
F 4 "994-XAL6030-182MEC " H 7250 2900 60  0001 C CNN "Mouser Part Number"
	1    7250 2900
	0    -1   -1   0   
$EndComp
Wire Wire Line
	7350 2900 8000 2900
Connection ~ 8000 3000
Wire Wire Line
	7150 2900 6400 2900
Connection ~ 6400 3000
Wire Wire Line
	5100 3200 5100 4200
Connection ~ 5100 4200
Wire Wire Line
	5450 3200 5450 4200
Connection ~ 5450 4200
$EndSCHEMATC
