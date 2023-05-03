#include "Connection.h"

#include <array>
#include <cstring>
#include <memory>
namespace 
{
  // ensures proper deallocation of arrays as filled by CAEN interface
  template<class T> 
    class safe_array
  {
    public:
    
    // default constructor
    safe_array() = default;
    
    // destructor
    /* calls CAEN de-allocator */
    ~safe_array()
    { CAENHV_Free( m_p ); }
    
    // accessor
    typename std::add_lvalue_reference<T*>::type get()
    { return m_p; }
    
    // copy constructor and assignment operator are deleted
    safe_array( const safe_array<T>& ) = delete;
    safe_array<T>& operator = ( const safe_array<T>& ) = delete;
    
    private:
    T* m_p = nullptr;
    
  };

  //! custom deleter that uses "free" to deallocate
  class Deleter
  {
    public:
    template<class T>
      void operator() ( T* ptr )
    { free(ptr); }
  };
  
  // get channel names
  std::vector<std::string> get_channel_names( int handle, const Slot& slot )
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
      return std::vector<std::string>();
    }
    
    std::vector<std::string> out;
    for( int i = 0; i < channels.size(); ++i )
    { out.push_back( names.get()[i] ); }
    
    return out;
  }

  // get parameter for given slot, channel
  template<class T>
  T get_parvalue( int handle, int slot, unsigned short channel, const std::string& parname )
  {
    // create output structure, with automatic deallocation
    std::unique_ptr<void,Deleter> result( malloc( sizeof(T) ));    
    auto reply = CAENHV_GetChParam( handle, slot, parname.c_str(), 1, &channel, result.get() );
    if( reply != CAENHV_OK ) { 
      std::cout << "get_parvalue - failed. reply: " << std::hex << "0x" << reply << std::dec << std::endl;
      return T(); 
    }
    return static_cast<T*>(result.get())[0];
  }
  
  // get parameters of a given type and name for several channels in a slot
  template<class T>
  std::vector<T> get_parvalues( int handle, int slot, const std::vector<unsigned short>& channels, const std::string& parname )
  {
    // create output structure, with automatic deallocation
    std::unique_ptr<void,Deleter> result( malloc( channels.size()*sizeof(T) ));
    
    // get parameter values
    auto reply = CAENHV_GetChParam( handle, slot, parname.c_str(), channels.size(), &channels[0], result.get() );
    if( reply != CAENHV_OK ) { 
      std::cout << "get_parvalues - failed. reply: " << std::hex << "0x" << reply << std::dec << std::endl;
      return std::vector<T>(); 
    }

    // store in output
    std::vector<T> out;
    for( int i = 0; i < channels.size(); ++i )
    { out.push_back( static_cast<T*>( result.get() )[i] ); }
  
    return out;
  }
  
  // get parameters of a given type and name for all channels in a slot
  template<class T>
  std::vector<T> get_parvalues( int handle, const Slot& slot, const std::string& parname )
  { 
    // create list of channels for which we want the value
    std::vector<unsigned short> channels;
    for( int i = 0; i < slot.m_nchannels; ++i ) channels.push_back(i);
    return get_parvalues<T>( handle, slot.m_id, channels, parname );
  }
  
  // assign parameters of a given type and name to all channels in list
  template<class T, T (Channel::*accessor)>
    void assign( int handle, const Slot& slot, Channel::List& channels, const std::string& parname )
  {
    auto result = get_parvalues<T>( handle, slot, parname );
    if( result.size() == channels.size() )
    {
      for( int i = 0; i < channels.size(); ++i )
      { channels[i].*accessor = result[i]; }
    }
  }
  
}

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
