// -!- C++ -!- //////////////////////////////////////////////////////////////
//
//  System        : 
//  Module        : 
//  Object Name   : $RCSfile$
//  Revision      : $Revision$
//  Date          : $Date$
//  Author        : $Author$
//  Created By    : Robert Heller
//  Created       : Wed Apr 22 09:48:24 2020
//  Last Modified : <220125.0954>
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

static const char rcsid[] = "@(#) : $Id$";

#include <Arduino.h>
#include "JoyAxis.h"

void JoyAxis::AnalogInit()
{
    analogReference(EXTERNAL);
    analogReadRes(10);
}

JoyAxis::JoyAxis(int pin,int zerooff,bool reverse)
      : pin_(pin), zerooff_(zerooff), reverse_(reverse)
{
}

void JoyAxis::begin()
{
}

int8_t JoyAxis::Read()
{
    delay(5);
    //Serial.print("*** JoyAxis::Read(): pin=");Serial.print(pin_);
    int raw = (analogRead(pin_) >> 2)&0xFF;
    //Serial.print(" raw (from analogRead): ");Serial.print(raw);
    raw -= zerooff_;
    //Serial.print(" raw (after zerooff_): ");Serial.print(raw);
    if (reverse_) {
        raw = -raw;
    }
    //Serial.print(" raw (after reverse_): ");Serial.println(raw);
    return (int8_t)(raw / 32);
}

