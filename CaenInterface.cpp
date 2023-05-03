#include "CaenInterface.h"
#include "Connection.h"

static Connection m_connection;

//___________________________________________
void connect( 
  const std::string& ip,
  const std::string& user,
  const std::string& password )
{ m_connection.connect( ip, user, password ); }

//___________________________________________
void disconnect() 
{ m_connection.disconnect(); }

//__________________________________________
float get_v0set( int slot, int channel )
{ return get_parameter_value<float>( m_connection.get_handle(), slot, channel, "V0Set" ); }

//__________________________________________
void set_v0( int slot, int channel, float value )
{ set_parameter_value( m_connection.get_handle(), slot, channel, "V0Set", value ); }
