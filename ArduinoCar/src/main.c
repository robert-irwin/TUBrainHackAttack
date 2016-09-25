/*
 * main.c
 *
 *  Created on: Sep 24, 2016
 *      Author: robertirwin
 */

# include	<CommWithHost.h>
# include 	<avr/io.h>
# include	<avr/interrupt.h>
# include	<stdint.h>
# include	<stdbool.h>

CommWithHost HOST;
CommWithHost * host = &HOST;

bool UARTRead(uint8_t *);
void UART_INIT(void);
void PWM_INIT(void);

int interrupt_count0 = 0;
int interrupt_count2 = 0;

uint8_t left = 94;
uint8_t right = 94;

int main(void)
{
	UART_INIT();
	PWM_INIT();

	CommWithHostSetup(host, UARTRead, NULL);

	while(1)
	{
		CommWithHostGetMotors(host, &left, &right);
	}
	return(0);
}

ISR(TIMER0_COMPA_vect)
{
	if (interrupt_count0 == 4)
	{
		TIFR0 |= (1 << OCF0B); // enable interrupts for match on B
		PORTD |= (1 << PD3); // turn on the pin
		interrupt_count0 = 0;
		OCR0B = left;
		OCR2B = right;
	}
	interrupt_count0++;
}

ISR(TIMER0_COMPB_vect)
{
	TIFR0 &= ~(1 << OCF0B); // disbale interrupts for match on B
	PORTD &= ~(1 << PD3);
}

ISR(TIMER2_COMPA_vect)
{
	if (interrupt_count2 == 4)
	{
		TIFR2 |= (1 << OCF2B); // enable interrupts for match on B
		PORTD |= (1 << PD4); // turn on the pin
		interrupt_count2 = 0;
		OCR0B = left;
		OCR2B = right;
	}
	interrupt_count2++;
}

ISR(TIMER2_COMPB_vect)
{
	TIFR2 &= ~(1 << OCF2B); // disbale interrupts for match on B
	PORTD &= ~(1 << PD4);
}
