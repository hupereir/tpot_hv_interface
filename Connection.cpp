#include "Connection.h"
#include "CaenInterface_p.h"

#include <array>
#include <cstring>
#include <memory>

//_____________________________________________________
Connection::~Connection()
{ disconnect(); }
  
//_____________________________________________________
void Connection::connect(
  const std::string& ip_address, 
  const std::string& username,
  const std::string& password)
{
  if( m_connected ) 
  {
    std::cout << "Connection::connect - already connected" << std::endl;
    return;
  }

  std::cout << "connecting to interface at " << ip_address << std::endl;
  m_reply = CAENHV_InitSystem( m_type, m_link_type, 
    const_cast<char*>(ip_address.c_str()),
    username.c_str(), password.c_str(), &m_handle );
  m_connected = (m_reply==CAENHV_OK);
  if( m_connected ) build_channel_map();
}

//_____________________________________________________
void Connection::disconnect()
{ 
  if( m_connected )
  {
    std::cout << "disconnecting from interface" << std::endl;
    CAENHV_DeinitSystem(m_handle); 
  }
  m_connected = false;
}

//_____________________________________________________
Connection::channel_id_t Connection::get_channel_id( const std::string& name ) const
{
  const auto it = m_channel_map.find( name );
  if( it == m_channel_map.end() ) return {-1, 0};
  else return it->second;  
}

//_____________________________________________________
void Connection::build_channel_map() 
{
  m_channel_map.clear();
  
  // get slots
  const auto slots = get_slots();
  
  // loop over slots
  for( const auto& slot:slots )
  {    
    // get channel names
    const auto names = get_channel_names( m_handle, slot ).second;
   
    // loop over names, fill map
    for( size_t i = 0; i < names.size(); ++i )
    { m_channel_map.insert( {names[i], {slot.m_id, i} } ); }
  }  
}
