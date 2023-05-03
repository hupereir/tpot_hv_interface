#ifndef CAENINTERFACE_H
#define CAENINTERFACE_H

#include "Slot.h"
#include "Channel.h"

#include <CAENHVWrapper.h>

#include <iostream>
#include <memory>
#include <vector>

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

// get parameter for given slot, channel
template<class T>
  T get_parameter_value( int handle, int slot, unsigned short channel, const std::string& parname )
{
  // create output structure, with automatic deallocation
  std::unique_ptr<void,Deleter> result( malloc( sizeof(T) ));    
  auto reply = CAENHV_GetChParam( handle, slot, parname.c_str(), 1, &channel, result.get() );
  if( reply != CAENHV_OK ) { 
    std::cout << "get_parameter_value - failed. reply: " << std::hex << "0x" << reply << std::dec << std::endl;
    return T(); 
  }
  return static_cast<T*>(result.get())[0];
}

// get parameters of a given type and name for several channels in a slot
template<class T>
  std::vector<T> get_parameter_values( int handle, int slot, const std::vector<unsigned short>& channels, const std::string& parname )
{
  // create output structure, with automatic deallocation
  std::unique_ptr<void,Deleter> result( malloc( channels.size()*sizeof(T) ));
  
  // get parameter values
  auto reply = CAENHV_GetChParam( handle, slot, parname.c_str(), channels.size(), &channels[0], result.get() );
  if( reply != CAENHV_OK ) { 
    std::cout << "get_parameter_values - failed. reply: " << std::hex << "0x" << reply << std::dec << std::endl;
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
  std::vector<T> get_parameter_values( int handle, const Slot& slot, const std::string& parname )
{ 
  // create list of channels for which we want the value
  std::vector<unsigned short> channels;
  for( int i = 0; i < slot.m_nchannels; ++i ) channels.push_back(i);
  return get_parameter_values<T>( handle, slot.m_id, channels, parname );
}

// assign parameters of a given type and name to all channels in list
template<class T, T (Channel::*accessor)>
  void assign( int handle, const Slot& slot, Channel::List& channels, const std::string& parname )
{
  auto result = get_parameter_values<T>( handle, slot, parname );
  if( result.size() == channels.size() )
  {
    for( int i = 0; i < channels.size(); ++i )
    { channels[i].*accessor = result[i]; }
  }
}

// set parameter value of a given type for given slot, channel
template<class T>
  CAENHVRESULT set_parameter_value( int handle, int slot, unsigned short channel, const std::string& parname, T value )
{
  auto reply = CAENHV_SetChParam( handle, slot, parname.c_str(), 1, &channel, &value );
  if( reply != CAENHV_OK ) std::cout << "set_pararameter_value - failed. reply: " << std::hex << "0x" << reply << std::dec << std::endl;
  return reply;
}

// set parameter value of a given type for given slot, several channels
template<class T>
  CAENHVRESULT set_parameter_value( int handle, int slot, const std::vector<unsigned short>& channels, const std::string& parname, T value )
{
  auto reply = CAENHV_SetChParam( handle, slot, parname.c_str(), channels.size(), &channels[0], &value );
  if( reply != CAENHV_OK ) std::cout << "set_pararameter_value - failed. reply: " << std::hex << "0x" << reply << std::dec << std::endl;
  return reply;
}

#endif
