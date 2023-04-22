#ifndef CHANNEL_H
#define CHANNEL_H

#include <iostream>
#include <vector>

class Channel
{
  public:
  
  //! id
  int m_id = 0;
  
  //! name
  std::string m_name;
  
  //! v0set
  float m_v0set;
  
  //! list of channels alias
  using List = std::vector<Channel>;
  
  //! streamer
  friend std::ostream& operator << ( std::ostream& out, const Channel& channel )
  {
    out << "id: " << channel.m_id << " name: " << channel.m_name;
    return out;
  }

};
#endif
