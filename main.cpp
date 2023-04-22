#include "Connection.h"
#include "Slot.h"

int main()
{
    Connection connection;
    if( !connection.is_valid() ) 
    {
      std::cout << "main - invalid connection" << std::endl;
      return 0;
    }
    
    for(const auto& slot:connection.get_slots())
    { std::cout << "main - " << slot << std::endl; }
    
    for( const auto& channel_name:connection.get_channel_names() )
    { std::cout << "main - channel name: " << channel_name << std::endl; }
    return 0;
}
