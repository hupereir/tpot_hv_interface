#include "CaenInterface.h"
#include "CaenInterface_p.h"
#include "Channel.h"
#include "Connection.h"

#include <cstring>
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
    return set_parameter_value<unsigned int>( m_connection.get_handle(), slot, channel, parname, value ) == CAENHV_OK;
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
    return set_parameter_value<float>( m_connection.get_handle(), slot, channel, parname, value ) == CAENHV_OK;
  } else {
    // channel not found
    std::cout << "set_parameter_float - channel not found: " << name << std::endl;
    return false;
  }
}

//__________________________________________
unsigned int get_parameter_unsigned( const char* name, const char* parname )
{
  if( !m_connection.is_connected() ) return false;
  const auto reply = m_connection.get_channel_id( name );
  const auto& slot = reply.first;
  const auto& channel = reply.second;
  if( slot >= 0 ) 
  {
    // read value, check result
    const auto result = get_parameter_value<unsigned int>( m_connection.get_handle(), slot, channel, parname);
    const auto reply = result.first;
    if( reply != CAENHV_OK )
    {
      std::cout << "get_parameter_unsigned - parname: " << parname << " failed" << std::endl;
      return 0;
    } else return result.second;
  } else {
    // channel not found
    std::cout << "get_parameter_unsigned - channel not found: " << name << std::endl;
    return 0;
  }
}

//__________________________________________
float get_parameter_float( const char* name, const char* parname )
{
  if( !m_connection.is_connected() ) return false;
  const auto reply = m_connection.get_channel_id( name );
  const auto& slot = reply.first;
  const auto& channel = reply.second;
  if( slot >= 0 ) 
  {
    // read value, check result
    const auto result = get_parameter_value<float>( m_connection.get_handle(), slot, channel, parname);
    const auto reply = result.first;
    if( reply != CAENHV_OK )
    {
      std::cout << "get_parameter_float - parname: " << parname << " failed" << std::endl;
      return 0;
    } else return result.second;
  } else {
    // channel not found
    std::cout << "get_parameter_float - channel not found: " << name << std::endl;
    return false;
  }
}

//___________________________________________
Result<std::vector<std::string>> get_channel_names( int handle, const Slot& slot )
{
  
  // create list of channels for which we want the name
  std::vector<unsigned short> channels;
  for( int i = 0; i < slot.m_nchannels; ++i ) channels.push_back(i);
  
  // create output structure, with automatic deallocation
  using name_t = char[MAX_CH_NAME];  
  std::unique_ptr<name_t, Deleter> names(static_cast<name_t*>(malloc(channels.size()*MAX_CH_NAME)));
  
  // get channel names
  const auto reply = CAENHV_GetChName(handle, slot.m_id, channels.size(), &channels[0], names.get() );
  if( reply != CAENHV_OK ) 
  {
    std::cout << "get_channel_names - failed. reply: " << std::hex << "0x" << reply << std::dec << std::endl;
    return {reply, std::vector<std::string>()};
  }
  
  std::vector<std::string> out;
  for( int i = 0; i < channels.size(); ++i )
  { out.push_back( names.get()[i] ); }
  
  return {reply, out};
}  

//_____________________________________________________
Slot::List get_slots()
{
  if( !m_connection.is_connected() ) return Slot::List();
  
  unsigned short	n_slots;
  safe_array<unsigned short> n_channels_list;
  safe_array<unsigned short> serial_list;
  safe_array<char> model_list;
  safe_array<char> description_list;
  safe_array<unsigned char> firmware_min_list;
  safe_array<unsigned char> firmware_max_list;
  
  const auto reply = CAENHV_GetCrateMap(
    m_connection.get_handle(), 
    &n_slots, &n_channels_list.get(), &model_list.get(), 
    &description_list.get(), &serial_list.get(),
    &firmware_min_list.get(), &firmware_max_list.get() );
  
  if( reply != CAENHV_OK ) 
  {
    std::cout << "get_slots - failed. reply: " << std::hex << "0x" << reply << std::dec << std::endl;
    return Slot::List();
  }
  
  Slot::List slots;
  auto model = model_list.get();
  auto description = description_list.get();
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
Channel::List get_channels( const Slot& slot )
{
  if( !m_connection.is_connected() ) return Channel::List();

  // get all channel names
  const auto handle = m_connection.get_handle();
  const auto result = get_channel_names( handle, slot );
  auto reply = result.first;
  const auto& names = result.second;
  if( !( reply == CAENHV_OK && names.size() == slot.m_nchannels ) )
  { return Channel::List(); }
    
  // create channels, assign id and name
  Channel::List channels(slot.m_nchannels);
  for( int i = 0; i < channels.size(); ++i )
  { 
    channels[i].m_id = i;
    channels[i].m_name = names[i];
  }

  // assign vmax, v0set, i0set, vmon, imon, status and trop, check success at each stage
  if( (reply = assign<float, &Channel::m_svmax>( handle, slot, channels, "SVMax" )) != CAENHV_OK ) return channels;
  if( (reply = assign<float, &Channel::m_v0set>( handle, slot, channels, "V0Set" )) != CAENHV_OK ) return channels;
  if( (reply = assign<float, &Channel::m_i0set>( handle, slot, channels, "I0Set" )) != CAENHV_OK ) return channels;
  if( (reply = assign<float, &Channel::m_vmon>( handle, slot, channels, "VMon" )) != CAENHV_OK ) return channels;
  if( (reply = assign<float, &Channel::m_imon>( handle, slot, channels, "IMon" )) != CAENHV_OK ) return channels;
  if( (reply = assign<unsigned int, &Channel::m_status>( handle, slot, channels, "Status" )) != CAENHV_OK ) return channels;
  if( (reply = assign<unsigned int, &Channel::m_trip_int>( handle, slot, channels, "TripInt" )) != CAENHV_OK ) return channels;
  if( (reply = assign<unsigned int, &Channel::m_trip_ext>( handle, slot, channels, "TripExt" )) != CAENHV_OK ) return channels;
  
  return channels;  
}

//__________________________________________________
const char* get_channel_status()
{
  std::ostringstream out;
  
  // header
  out << "// slot, channel, chname, vset, vmon, imon, status, trip" << std::endl;  
  for(const auto& slot:get_slots() )
  {
    
    for( const auto& channel:get_channels(slot) )
    {
      out 
        << "{ \"slot_id\":" << slot.m_id 
        << ", \"ch_id\":" << channel.m_id 
        << ", \"ch_name\":\"" << channel.m_name << "\""
        << ", \"v0set\":" << channel.m_v0set
        << ", \"vmon\":" << channel.m_vmon 
        << ", \"imon\":" << channel.m_imon
        << ", \"status\":" << channel.m_status
        << ", \"status_Hex\": \"0x" << std::hex << channel.m_status << "\""<< std::dec
	<< ", \"trip\":" << ((channel.m_status&(1<<9))==1<<9)
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
