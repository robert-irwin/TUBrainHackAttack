#ifndef COMM_WITH_HOST_H_
#define COMM_WITH_HOST_H_

#define COMM_WITH_HOST_BAUD_RATE		( 9600 )
#define COMM_WITH_HOST_MAX_SIZE 		( 8 )
#define COMM_WITH_HOST_CONTROL_SIZE		( 3 )
#define COMM_WITH_HOST_START_BYTE 		( 12 )
#define COMM_WITH_HOST_START_LOC 		( 0 )
#define COMM_WITH_HOST_SIZE_LOC 		( 1 )
#define COMM_WITH_HOST_DATA_LOC			( 2 )
#define COMM_WITH_HOST_END_BYTE 		( 52 )

#define COMM_WITH_HOST_PAYLOAD_SIZE		( COMM_WITH_HOST_MAX_SIZE-COMM_WITH_HOST_CONTROL_SIZE )
#define COMM_WITH_HOST_PAYLOAD_LOC		( 0 )

#define COMM_WITH_HOST_MOTORS_ID		( 0 )
#define COMM_WITH_HOST_MOTORS_LEFT_LOC	( 1 )
#define COMM_WITH_HOST_MOTORS_RIGHT_LOC	( 2 )

#define COMM_WITH_HOST_SLOTS_TOTAL		( 1 )

#include <stdint.h>
#include <string.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" 
{
#endif

	typedef bool (CommWithHostReadType)( uint8_t* input );
	typedef void (CommWithHostWriteType) ( uint8_t output );

	typedef struct
	{
		uint8_t packet[ COMM_WITH_HOST_MAX_SIZE ];
		uint8_t slots[ COMM_WITH_HOST_SLOTS_TOTAL ][ COMM_WITH_HOST_PAYLOAD_SIZE ];
		bool ready[ COMM_WITH_HOST_SLOTS_TOTAL ];
		uint8_t curr;
		uint8_t size;
		CommWithHostReadType* read;
		CommWithHostWriteType* write;
	}
	CommWithHost;

	void CommWithHostSetup( CommWithHost* ptr, CommWithHostReadType* read, CommWithHostWriteType* write );
	bool CommWithHostReceive( CommWithHost* ptr, uint8_t** data, size_t* len );
	bool CommWithHostGetMotors( CommWithHost* ptr, uint8_t* left, uint8_t* right );
	void CommWithHostSend( CommWithHost* ptr, uint8_t* data, size_t len );

#ifdef __cplusplus
}
#endif

#endif