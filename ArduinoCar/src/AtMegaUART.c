/*
 * main.c
 *
 *  Created on: Sep 24, 2016
 *      Author: robertirwin
 */

# include	<avr/io.h>
# include	<avr/interrupt.h>
# include	<stdint.h>

bool UARTRead(uint8_t * data)
{
  /*
	// Initialize the UART
	//
	char data;
	// set baud rate
	//
	uint16_t ubrr = (16000000/16/9600) -1;
	UBRR0H = (unsigned char)(ubrr >> 8);
	UBRR0L = (unsigned char)ubrr;

	// Configure Frame Format (1 stopbit, no parity, 8 data)
	//
	UCSR0C |= (3 << UCSZ00);

	// Enable Receiver
	//
	UCSR0B = (1 << RXEN0);

	// Check for Data
	//
	*/
	if ((UCSR0A & (1 << RXC0)))
	{
		*data = UDR0;
                return(1);
	}
	else return(0);
}
