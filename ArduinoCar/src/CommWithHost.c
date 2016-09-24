#include "CommWithHost.h"

static bool CommWithHostFillSlot( CommWithHost* ptr )
{
	uint8_t* payload;
	size_t len;
	if ( CommWithHostReceive( ptr, &payload, &len ) )
	{
		uint8_t id = payload[ COMM_WITH_HOST_PAYLOAD_LOC ];
		if ( id<COMM_WITH_HOST_SLOTS_TOTAL )
		{
			memcpy( ptr->slots[ id ], payload, sizeof( ptr->packet ) );
			ptr->ready[ id ] = true;
			return true;
		}
	}
	return false;
}

void CommWithHostSetup( CommWithHost* ptr, CommWithHostReadType* read, CommWithHostWriteType* write )
{
	ptr->curr = 0;
	ptr->size = 0;
	ptr->read = read;
	ptr->write = write;
	memset( ptr->slots, 0, sizeof( ptr->slots ) );
	memset( ptr->ready, 0, sizeof( ptr->ready) );
}

bool CommWithHostReceive( CommWithHost* ptr, uint8_t** data, size_t* len )
{
	CommWithHostReadType* read;
	uint8_t b;
	
	read = ptr->read;
	if ( read==NULL )
		return false;
	
	while ( read( &b ) )
	{
		switch ( ptr->curr )
		{
		case COMM_WITH_HOST_START_LOC:
			{
				ptr->curr++;
			}
			break;
		case COMM_WITH_HOST_SIZE_LOC:
			{
				if ( b>COMM_WITH_HOST_MAX_SIZE )
				{
					ptr->curr = 0;
				}
				else
				{
					ptr->size = b;
					ptr->curr++;
				}
			}
			break;
		default:
			{
				if ( ( ptr->curr>=(ptr->size-1) ) && ( b==COMM_WITH_HOST_END_BYTE ) )
				{
					*len = ptr->size-COMM_WITH_HOST_CONTROL_SIZE;
					*data = &ptr->packet[ COMM_WITH_HOST_DATA_LOC ];
					ptr->curr = 0;
					return true;
				}
				else if ( ptr->curr>COMM_WITH_HOST_MAX_SIZE )
				{
					ptr->curr = 0;
				}
				else
				{
					ptr->packet[ ptr->curr++ ] = b;
				}
			}
			break;
		}
	}
	
	return false;
}

void CommWithHostSend( CommWithHost* ptr, uint8_t* data, size_t len )
{
	CommWithHostWriteType* write = ptr->write;
	uint8_t each_byte = 0;
	
	if ( write==NULL )
		return false;
	write( COMM_WITH_HOST_START_BYTE );
	write( COMM_WITH_HOST_CONTROL_SIZE+len );
	for ( each_byte=0; each_byte<len; each_byte++ )
		write( data[ each_byte ] );
	write( COMM_WITH_HOST_END_BYTE );
}

bool CommWithHostGetMotors( CommWithHost* ptr, uint8_t* left, uint8_t* right )
{
	CommWithHostFillSlot( ptr );
	
	if ( ptr->ready[ COMM_WITH_HOST_MOTORS_ID ]==true )
	{
		ptr->ready[ COMM_WITH_HOST_MOTORS_ID ]=false;
		*left = ptr->slots[ COMM_WITH_HOST_MOTORS_ID ][ COMM_WITH_HOST_MOTORS_LEFT_LOC ];
		*right = ptr->slots[ COMM_WITH_HOST_MOTORS_ID ][ COMM_WITH_HOST_MOTORS_RIGHT_LOC ];
		return true;
	}
	return false;
}