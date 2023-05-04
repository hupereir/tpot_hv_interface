#include "CaenInterface.h"
#include "Connection.h"

#include <sstream>

static Connection m_connection;
static std::string m_json_output;

extern "C" {
  
  bool connect_to_interface( 
    const char* /*ip*/,
    const char* /*user*/,
    const char* /*password*/ ); 
  
  void disconnect_from_interface();
  
  float get_v0set( const char* /*channel name*/ );
  void set_v0set( const char* /*channel name*/, float /*value*/ );
  
  void set_channel_on( const char* /* channel name*/, bool );
  
  const char* get_channel_status();
  
  bool last_command_successful();

}

//___________________________________________
bool connect_to_interface( 
  const char* ip,
  const char* user,
  const char* password )
{ 
  std::cout << "connect_to_interface - connecting to " << ip << std::endl;
  m_connection.connect( ip, user, password ); 
  return m_connection.is_connected();
}

//___________________________________________
void disconnect_from_interface() 
{
  std::cout << "disconnect_from_interface" << std::endl;
  m_connection.disconnect(); 
}

//__________________________________________
float get_v0set( const char* name )
{ 
  if( !m_connection.is_connected() ) return 0;
  const auto reply = m_connection.get_channel_id( name );
  const auto& slot = reply.first;
  const auto& channel = reply.second;
  if( slot >= 0 ) {
    return get_parameter_value<float>( m_connection.get_handle(), slot, channel, "V0Set" ).second; 
  } else {
    std::cout << "get_v0Set - channel not found: " << name << std::endl;
    return -1;
  }
}

//__________________________________________
void set_v0set( const char* name, float value )
{ 
  if( !m_connection.is_connected() ) return;
  const auto reply = m_connection.get_channel_id( name );
  const auto& slot = reply.first;
  const auto& channel = reply.second;
  if( slot >= 0 ) {
    set_parameter_value<float>( m_connection.get_handle(), slot, channel, "V0Set", value );
  } else {
    std::cout << "get_v0Set - channel not found: " << name << std::endl;
  }
}

//__________________________________________
void set_channel_on( const char* name, bool value )
{ 
  std::cout << "set_channel_on - name: " << name << " value: " << value << std::endl;

  if( !m_connection.is_connected() ) return;
  const auto reply = m_connection.get_channel_id( name );
  const auto& slot = reply.first;
  const auto& channel = reply.second;
  if( slot >= 0 ) {
    set_parameter_value<unsigned int>( m_connection.get_handle(), slot, channel, "Pw", value );
  } else {
    std::cout << "set_channel_on - channel not found: " << name << std::endl;
  }
}

//__________________________________________________
const char* get_channel_status()
{
  std::ostringstream out;
  
  // header
  out << "// slot, channel, chname, vset, vmon, imon, status, trip" << std::endl;  
  for(const auto& slot:m_connection.get_slots() )
  {
    
    for( const auto& channel:m_connection.get_channels( slot ) )
    {
      out 
        << "{ \"slot_id\":" << slot.m_id 
        << ", \"ch_id\":" << channel.m_id 
        << ", \"ch_name\":\"" << channel.m_name << "\""
        << ", \"v0set\":" << channel.m_v0set
        << ", \"vmon\":" << channel.m_vmon 
        << ", \"imon\":" << channel.m_imon
        << ", \"status\":" << channel.m_status
        << ", \"trip\":" << channel.m_trip_int 
        << " }"
        << std::endl;
    }
  }
  
  m_json_output = out.str();
  return m_json_output.c_str();
}

//__________________________________________________
bool last_command_successful() 
{ return m_connection.is_connected() && m_connection.get_reply() == CAENHV_OK; }
