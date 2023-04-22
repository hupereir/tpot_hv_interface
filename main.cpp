#include "Connection.h"
#include "Slot.h"

int main()
{
    Connection connection;
    if( !connection.is_valid() ) 
    {
      std::cout << "main - invalid connection" << std::endl;
      std::cout << "main - reply: " << std::hex << "0x" << connection.get_reply() << std::dec << std::endl;
      return 0;
    }
    
    for(const auto& slot:connection.get_slots())
    { 
      std::cout << "slot: " << slot << std::endl;       
      for( const auto& channel:connection.get_channels( slot ) )
      // { std::cout << "channel: " << channel << std::endl; }
      { std::cout << slot.m_id << " " << channel.m_id << " " << channel.m_name << " " << channel.m_vmon << " " << channel.m_imon << " " << channel.m_status << std::endl; }
    }
}
