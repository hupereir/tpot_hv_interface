#include "Connection.h"

#include <array>
#include <cstring>
#include <memory>

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
Connection::string_list_t Connection::get_channel_names()
{
  if( !m_valid ) return string_list_t();

  string_list_t out;
  
  // get all valid slots
  const auto slots = get_slots();
  for( const auto& slot:slots )
  {
    std::vector<unsigned short> channels = {0, 1, 2, 3 };
    char (*names)[MAX_CH_NAME];
    m_reply = CAENHV_GetChName(m_handle, slot.m_id, channels.size(), &channels[0], names );
    for( int i = 0; i < channels.size(); ++i )
    { out.push_back(names[i]); }
  }
  
  return out;
}
