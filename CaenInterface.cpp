#include "CaenInterface.h"
#include "CaenInterface_p.h"
#include "Connection.h"

#include <sstream>

static Connection m_connection;
static std::string m_json_output;

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
bool set_channel_on( const char* name, bool value )
{ return set_parameter_unsigned( name, "Pw", value ); }

//__________________________________________
bool set_parameter_unsigned( const char* name, const char* parname, unsigned int value )
{
  if( !m_connection.is_connected() ) return false;
  const auto reply = m_connection.get_channel_id( name );
  const auto& slot = reply.first;
  const auto& channel = reply.second;
  if( slot >= 0 ) 
  {
    // assign value, return result
    return set_parameter_value<unsigned int>( m_connection.get_handle(), slot, channel, "Pw", value ) == CAENHV_OK;
  } else {
    // channel not found
    std::cout << "set_parameter_unsigned - channel not found: " << name << std::endl;
    return false;
  }
}

//__________________________________________
bool set_parameter_float( const char* name, const char* parname, float value )
{
  if( !m_connection.is_connected() ) return false;
  const auto reply = m_connection.get_channel_id( name );
  const auto& slot = reply.first;
  const auto& channel = reply.second;
  if( slot >= 0 ) 
  {
    // assign value, return result
    return set_parameter_value<float>( m_connection.get_handle(), slot, channel, "Pw", value ) == CAENHV_OK;
  } else {
    // channel not found
    std::cout << "set_parameter_float - channel not found: " << name << std::endl;
    return false;
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
