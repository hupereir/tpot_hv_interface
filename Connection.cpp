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

  // get parameters of a given type and name for all channels in a slot
  template<class T>
  std::vector<T> get_channel_parvalue( int handle, const Slot& slot, const std::string& parname )
  {
 
    // create list of channels for which we want the name
    std::vector<unsigned short> channels;
    for( int i = 0; i < slot.m_nchannels; ++i ) channels.push_back(i);
    
    // create output structure, with automatic deallocation
    std::unique_ptr<void,Deleter> result( malloc( slot.m_nchannels*sizeof(T) ));
    
    // get parameter values
    auto reply = CAENHV_GetChParam( handle, slot.m_id, parname.c_str(), slot.m_nchannels, &channels[0], result.get() );
    if( reply != CAENHV_OK ) { return std::vector<T>(); }

    // store in output
    std::vector<T> out;
    for( int i = 0; i < slot.m_nchannels; ++i )
    { out.push_back( static_cast<T*>( result.get() )[i] ); }

    return out;
  }
 
  // assign parameters of a given type and name to all channels in list
  template<class T, T (Channel::*accessor)>
    void assign( int handle, const Slot& slot, Channel::List& channels, const std::string& parname )
  {
    auto result = get_channel_parvalue<T>( handle, slot, parname );
    if( result.size() == channels.size() )
    {
      for( int i = 0; i < channels.size(); ++i )
      { channels[i].*accessor = result[i]; }
    } else {
      std::cout << "assign - error fetching " << parname << std::endl;
    }
  }
  
}


//_____________________________________________________
Connection::Connection()
{
  //! connection
  m_reply = CAENHV_InitSystem( m_type, m_link_type, 
    const_cast<char*>(m_ip_address.c_str()),
    m_username.c_str(), m_password.c_str(), &m_handle );
  m_valid = (m_reply==CAENHV_OK);
}

//_____________________________________________________
Connection::~Connection()
{ if( m_valid ) CAENHV_DeinitSystem(m_handle); }

//_____________________________________________________
Slot::List Connection::get_slots()
{
  if( !m_valid ) return Slot::List();
  
  unsigned short	n_slots;
  safe_array<unsigned short> n_channels_list;
  safe_array<unsigned short> serial_list;
  safe_array<char> model_list;
  safe_array<char> description_list;
  safe_array<unsigned char> firmware_min_list;
  safe_array<unsigned char> firmware_max_list;
  
  auto out = CAENHV_GetCrateMap(
    m_handle, 
    &n_slots, &n_channels_list.get(), &model_list.get(), 
    &description_list.get(), &serial_list.get(),
    &firmware_min_list.get(), &firmware_max_list.get() );
  
  if( out != CAENHV_OK ) return Slot::List();
  
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
  if( !m_valid ) return Channel::List();

  // create list of channels for which we want the name
  std::vector<unsigned short> channel_ids;
  for( int i = 0; i < slot.m_nchannels; ++i ) channel_ids.push_back(i);

  // create output structure, with automatic deallocation
  using name_t = char[MAX_CH_NAME];  
  std::unique_ptr<name_t, Deleter> names(static_cast<name_t*>(malloc(channel_ids.size()*MAX_CH_NAME)));
  
  // get channel names
  m_reply = CAENHV_GetChName(m_handle, slot.m_id, channel_ids.size(), &channel_ids[0], names.get() );
  if( m_reply != CAENHV_OK ) return Channel::List();
  
  Channel::List channels(channel_ids.size());
  for( int i = 0; i < channels.size(); ++i )
  { 
    channels[i].m_id = i;
    channels[i].m_name = names.get()[i];
  }

  // assign V0Set
  assign<float, &Channel::m_svmax>( m_handle, slot, channels, "SVMax" );
  assign<float, &Channel::m_v0set>( m_handle, slot, channels, "V0Set" );
  assign<float, &Channel::m_i0set>( m_handle, slot, channels, "I0Set" );
  assign<float, &Channel::m_vmon>( m_handle, slot, channels, "Vmon" );
  assign<float, &Channel::m_imon>( m_handle, slot, channels, "Imon" );
  assign<unsigned int, &Channel::m_status>( m_handle, slot, channels, "Status" );
  
  return channels;  
}
