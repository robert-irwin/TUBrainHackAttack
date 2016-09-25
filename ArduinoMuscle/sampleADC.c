/*
 * main.c
 *
 *  Created on: Sep 24, 2016
 *      Author: James Kollmer
 */


#	include		<stdio.h>
#	include		<avr/io.h>
#	include		<math.h>
#	include		<stdint.h>
#	include		<avr/interrupt.h>
#	include		<util/delay.h>

uint16_t x;
int main(void)
{
	sei();
	DDRB = 63; // Set all of the LEDs on the Muscle Spiker as an output
	//PORTB = 63;
	//uint16_t x = ADC;
	/* Configure the ADC */
	ADCSRA |= (1<<ADEN)|(1<<ADIE); // Enable the ADC
	ADMUX  |= (1<<REFS0)|(1<<MUX0); // Adjusting the Voltage Reference
	ADCSRA |= (1<<ADPS0)|(1<<ADPS1)|(1<<ADPS2); // ADC Clock Prescaler
	ADCSRA |= (1<<ADSC); // Start the first conversion



	while(1)
	{
		//Stuff
	}

	return(0);
}

ISR(ADC_vect)
{
	if(ADC <= 128)
	{
		PORTB = 0;
	}
	else if(128 < ADC && ADC <= 256)
	{
		PORTB = 1;
	}
	else if(256 < ADC && ADC <= 512)
	{
		PORTB = 3;
	}
	else if(512 < ADC && ADC <= 768)
	{
		PORTB = 15;
	}
	else if(768 < ADC)
	{
		PORTB = 63;
	}

	ADCSRA |= (1<<ADSC);
}
