/*
 * Copyright (c) 2014-2020 Arm Limited and affiliates.
 * SPDX-License-Identifier: Apache-2.0
 */

#include "PinNames.h"
#include "ThisThread.h"
#include "mbed.h"

// Adjust pin name to your board specification.
// You can use LED1/LED2/LED3/LED4 if any is connected to PWM capable pin,
// or use any PWM capable pin, and see generated signal on logical analyzer.\

PwmOut PWM1(D9);
PwmOut PWM2(D10);



int main()
{
    // specify period first
    PWM1.period(0.05f);      // 0.05 second period

    PWM1.write(0.49f);

    HAL_TIMEx_PWMN_Start(TIM_HandleTypeDef *htim, uint32_t Channel)


    // PWM2.suspend();
    wait_us(10000);
    // ThisThread::sleep_for(1ms);
    // PWM2.resume();
    // PWM2.suspend();
    PWM2.period(0.05f);      // 0.05 second period
    PWM2.write(0.49f);



    while (1);
}


















// PwmOut servo(PWM_OUT);

// void servo_rotate(int degree){
//     if(degree>180 || degree<0){
//         printf("degree out of range, degree: 0~180");
//     }
//     servo.write(0.05*(1+float(degree)/180));
// }



// int main()
// {
//     // specify period first
//     servo.period(0.02f);      // 0.02 second period
//     // servo.write(0.5f);
//     servo_rotate(45);      // servo_rotate(Servo, degree), degree: 0~180
//     while (1);
// }
