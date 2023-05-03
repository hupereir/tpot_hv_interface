#include "CaenInterface.h"
#include "Connection.h"

static Connection m_connection;
  
extern "C" {
  
//   bool connect_to_interface( 
//     const std::string&,
//     const std::string&,
//     const std::string& ); 
  
  bool connect_to_interface();
  float get_v0set( int slot, int channel );
 
}

//___________________________________________
bool connect_to_interface( 
  const std::string& ip,
  const std::string& user,
  const std::string& password )
{ 
  m_connection.connect( ip, user, password ); 
  return m_connection.is_connected();
}

//___________________________________________
bool connect_to_interface()
{ 
  return connect_to_interface( "10.20.34.154", "admin", "admin" ); 
}

//___________________________________________
void disconnect_from_insterface() 
{ m_connection.disconnect(); }

//__________________________________________
float get_v0set( int slot, int channel )
{ return get_parameter_value<float>( m_connection.get_handle(), slot, channel, "V0Set" ); }

//__________________________________________
void set_v0( int slot, int channel, float value )
{ set_parameter_value( m_connection.get_handle(), slot, channel, "V0Set", value ); }
