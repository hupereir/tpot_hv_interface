#include "Connection.h"
#include "CaenInterface.h"

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
  
  m_reply = CAENHV_InitSystem( m_type, m_link_type, 
    const_cast<char*>(ip_address.c_str()),
    username.c_str(), password.c_str(), &m_handle );
  m_connected = (m_reply==CAENHV_OK);
}

//_____________________________________________________
void Connection::disconnect()
{ if( m_connected ) CAENHV_DeinitSystem(m_handle); }

//_____________________________________________________
Slot::List Connection::get_slots()
{
  if( !m_connected ) return Slot::List();
  
  unsigned short	n_slots;
  safe_array<unsigned short> n_channels_list;
  safe_array<unsigned short> serial_list;
  safe_array<char> model_list;
  safe_array<char> description_list;
  safe_array<unsigned char> firmware_min_list;
  safe_array<unsigned char> firmware_max_list;
  
  m_reply = CAENHV_GetCrateMap(
    m_handle, 
    &n_slots, &n_channels_list.get(), &model_list.get(), 
    &description_list.get(), &serial_list.get(),
    &firmware_min_list.get(), &firmware_max_list.get() );
  
  if( m_reply != CAENHV_OK ) 
  {
    std::cout << "Connection::get_slots - failed. reply: " << std::hex << "0x" << m_reply << std::dec << std::endl;
    return Slot::List();
  }
  
  Slot::List slots;
  char* model = model_list.get();
  char* description = description_list.get();
  for( int i = 0; i < n_slots; ++i, model+=strlen(model)+1, description+=strlen(description)+1 )
  {
    if( *model == '\0' ) continue;
    
    Slot current;
    current.m_id = i;
    current.m_model = model;
    current.m_nchannels = n_channels_list.get()[i];
    if( *description != '\0' ) current.m_description = description;
    
    slots.push_back( current );
  }
  
  return slots;        
}

//_____________________________________________________
Channel::List Connection::get_channels( const Slot& slot )
{
  if( !m_connected ) return Channel::List();

  const auto names = get_channel_names( m_handle, slot );
  if( names.size() != slot.m_nchannels )
  { return Channel::List(); }
    
  // create channels, assign id and name
  Channel::List channels(slot.m_nchannels);
  for( int i = 0; i < channels.size(); ++i )
  { 
    channels[i].m_id = i;
    channels[i].m_name = names[i];
  }

  // assign V0Set
  assign<float, &Channel::m_svmax>( m_handle, slot, channels, "SVMax" );
  assign<float, &Channel::m_v0set>( m_handle, slot, channels, "V0Set" );
  assign<float, &Channel::m_i0set>( m_handle, slot, channels, "I0Set" );
  assign<float, &Channel::m_vmon>( m_handle, slot, channels, "VMon" );
  assign<float, &Channel::m_imon>( m_handle, slot, channels, "IMon" );
  assign<unsigned int, &Channel::m_status>( m_handle, slot, channels, "Status" );
  assign<unsigned int, &Channel::m_trip_int>( m_handle, slot, channels, "TripInt" );
  assign<unsigned int, &Channel::m_trip_ext>( m_handle, slot, channels, "TripExt" );
  
  return channels;  
}
