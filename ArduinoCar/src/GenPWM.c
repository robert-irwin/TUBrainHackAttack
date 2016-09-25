/*
 * main.c
 *
 *  Created on: Sep 23, 2016
 *      Author: robertirwin
 */

# include	<avr/io.h>
# include	<avr/interrupt.h>

void PWM_INIT(void)
{
	// *** Configure the PWM Hardware ***

	// enable global interrupts
	//
	sei();

	// Set the proper pins on PortD to be an output
	//
	DDRD |= (3 << PD3);

	TCNT0 = 0; // set counter to 0
	TCNT2 = 0;

	TCCR0B |= (1 << CS02); // 16,000,000 / 256 = 62500
	TCCR2B |= (3 << CS21); // 16,000,000 / 256 = 62500

	TIMSK0 |= (3 << OCIE0A);
	TIMSK2 |= (3 << OCIE2A);

	TIFR0 |= (3 << OCF0A);
	TIFR2 |= (3 << OCF2A);
	// Set Output CompareA to 255, this means 5 cycles will be 20ms
	//
	OCR0A = 255; // OCR0B will be the input from the computer
	OCR2A = 255;

	OCR0B = 94; // 1.5ms (0 position)
	OCR2B = 94;

}

