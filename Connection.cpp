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

  // get parameters of a given type and name for all channels in a slot
  template<class T>
  std::vector<T> get_channel_parvalue( int handle, const Slot& slot, const std::string& parname )
  {
 
    // create list of channels for which we want the name
    std::vector<unsigned short> channels;
    for( int i = 0; i < slot.m_nchannels; ++i ) channels.push_back(i);
    
    auto result = malloc( slot.m_nchannels*sizeof(T) );
    auto reply = CAENHV_GetChParam( handle, slot.m_id, parname.c_str(), slot.m_nchannels, &channels[0], result );
    if( reply != CAENHV_OK )
    {
      free( result );
      return std::vector<T>();
    }
    
    std::vector<T> out;
    for( int i = 0; i < slot.m_nchannels; ++i )
    { out.push_back( static_cast<T*>( result )[i] ); }
    return out;
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
  std::vector<unsigned short> channels;
  for( int i = 0; i < slot.m_nchannels; ++i ) channels.push_back(i);

  // get channel names
  auto names = static_cast<char (*)[MAX_CH_NAME]>(malloc(channels.size()*MAX_CH_NAME));
  m_reply = CAENHV_GetChName(m_handle, slot.m_id, channels.size(), &channels[0], names );
  if( m_reply != CAENHV_OK ) return Channel::List();
  
  Channel::List out(channels.size());
  for( int i = 0; i < channels.size(); ++i )
  { 
    out[i].m_id = i;
    out[i].m_name = names[i];
  }
  free( names );
  
  auto v0set_list = get_channel_parvalue<float>( m_handle, slot, "V0Set" );
  if( v0set_list.size() == out.size() )
  {
    for( int i = 0; i < out.size(); ++i )
    { out[i].m_v0set = v0set_list[i]; }
  } else {
    std::cout << "Connection::get_channels - error fetching V0Set" << std::endl;
  }
    
  return out;  
}
