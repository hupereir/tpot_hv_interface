#include "Connection.h"
#include "Slot.h"

void usage() 
{
  std::cout << "Usage: " << std::endl;
  std::cout << "  caen_hv_reader --ip <ip adress> --user <username> --password <password>" << std::endl;
}

int main(int argc, char *argv[])
{
  
  // parse arguments
  if( argc < 7 ) 
  {
    usage();
    return 0;
  }
  
  std::string ip;
  std::string user;
  std::string password;
  
  for( int iarg = 1; iarg < argc; ++iarg )
  {
    std::string value( argv[iarg]);
    if( value == "--ip" ) ip = argv[++iarg]; 
    else if( value == "--user" ) user = argv[++iarg];
    else if( value == "--password" ) password = argv[++iarg];
  }
  
  Connection connection( ip, user, password );
  if( !connection.is_valid() ) 
  {
    std::cout << "main - invalid connection" << std::endl;
    std::cout << "main - reply: " << std::hex << "0x" << connection.get_reply() << std::dec << std::endl;
    return 0;
  }
  
  // header
  std::cout << "// slot, channel, chname, vset, vmon, imon, status, trip" << std::endl;
  
  for(const auto& slot:connection.get_slots())
  { 
    //       std::cout << "slot: " << slot << std::endl;       
    //       for( const auto& channel:connection.get_channels( slot ) )
    //       { std::cout << "channel: " << channel << std::endl; }
    for( const auto& channel:connection.get_channels( slot ) )
    {
      std::cout 
        << "{ \"slot_id\":" << slot.m_id 
        << ", \"ch_id\":" << channel.m_id 
        << ", \"ch_name\":\"" << channel.m_name << "\""
        << ", \"v0set\":" << channel.m_v0set
        << ", \"vmon\":" << channel.m_vmon << ", \"imon\":" << channel.m_imon
        << ", \"status\":" << channel.m_status
        << ", \"trip\":" << channel.m_trip_int 
        << "}"
        << std::endl;
    }
  }
}
