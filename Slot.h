#ifndef SLOT_H
#define SLOT_H

#include <iostream>
#include <string>
#include <vector>
class Slot
{
  public: 
  
  //! slot id
  int m_id = 0;
  
  //! model
  std::string m_model;
  
  //! description
  std::string m_description;
  
  //! number of channels
  unsigned short m_nchannels = 0;

  //! list of slot alias
  using List = std::vector<Slot>;
  
  //! streamer
  friend std::ostream& operator << ( std::ostream& out, const Slot& slot )
  {
    out << "id: " << slot.m_id << " model: " << slot.m_model << " description: " << slot.m_description << " channels: " << slot.m_nchannels;
    return out;
  }

};
#endif
