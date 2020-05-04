// -!- C++ -!- //////////////////////////////////////////////////////////////
//
//  System        : 
//  Module        : 
//  Object Name   : $RCSfile$
//  Revision      : $Revision$
//  Date          : $Date$
//  Author        : $Author$
//  Created By    : Robert Heller
//  Created       : Wed Apr 22 08:23:20 2020
//  Last Modified : <200504.1028>
//
//  Description	
//
//  Notes
//
//  History
//	
/////////////////////////////////////////////////////////////////////////////
//
//    Copyright (C) 2020  Robert Heller D/B/A Deepwoods Software
//			51 Locke Hill Road
//			Wendell, MA 01379-9728
//
//    This program is free software; you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation; either version 2 of the License, or
//    (at your option) any later version.
//
//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with this program; if not, write to the Free Software
//    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
//
// 
//
//////////////////////////////////////////////////////////////////////////////

#include <Arduino.h>
#include <Button.h>
#include "JoyAxis.h"
#include "PWMLed.h"
Button Left(4);
Button Middle(3);
Button Right(2);

JoyAxis X(A0);
JoyAxis Y(A1,128,true);

PWMLed XLed(9);
PWMLed YLed(10);

#ifdef USE_BUILTINLED
int led_state = LOW;
int led_state_millis;
#endif

static const char rcsid[] = "@(#) : $Id$";

void setup() {
    // put your setup code here, to run once:
    JoyAxis::AnalogInit();
    X.begin();
    Y.begin();
    XLed.begin();
    YLed.begin();
    Left.begin();
    Middle.begin();
    Right.begin();
    Mouse.begin();
#ifdef USE_BUILTINLED
    pinMode(LED_BUILTIN,OUTPUT);
    led_state_millis = millis()+500;
#endif
    Serial.begin(38400);
}
                
void loop() {
#ifdef USE_BUILTINLED
    if (millis() >= led_state_millis) {
        if (led_state == LOW) {
            digitalWrite(LED_BUILTIN,HIGH);
            led_state = HIGH;
        } else {
            digitalWrite(LED_BUILTIN,LOW);
            led_state = LOW;
        }
        led_state_millis = millis()+500;
    }
#endif
    // put your main code here, to run repeatedly:
    if (Left.pressed()) {
        Mouse.press(MOUSE_LEFT);
    } else if(Left.released()) {
        Mouse.release(MOUSE_LEFT);
    }
    if (Middle.pressed()) {
        Mouse.press(MOUSE_MIDDLE);
    } else if (Middle.released()) {
        Mouse.release(MOUSE_MIDDLE);
    }
    if (Right.pressed()) {
        Mouse.press(MOUSE_RIGHT);
    } else if (Right.released()) {
        Mouse.release(MOUSE_RIGHT);
    }
    int8_t x = X.Read();
    int8_t y = Y.Read();
    XLed.setBrightness(abs(x));
    YLed.setBrightness(abs(y));
    if (x != 0 || y != 0) {
        Mouse.move(x,y);
    }
}    
