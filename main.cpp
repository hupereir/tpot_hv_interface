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
    { 
      std::cout << "slot: " << slot << std::endl;       
      for( const auto& channel:connection.get_channels( slot ) )
      { std::cout << "channel: " << channel << std::endl; }
    }
}
