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
  
  //! vmax
  float m_svmax = 0;
  
  //! v0set
  float m_v0set = 0;

  //! i0set
  float m_i0set = 0;
  
  //! vmon
  float m_vmon = 0;
  
  //! imon
  float m_imon = 0;
  
  //! status
  unsigned int m_status = 0;
  
  //! list of channels alias
  using List = std::vector<Channel>;
  
  //! streamer
  friend std::ostream& operator << ( std::ostream& out, const Channel& channel )
  {
    out 
      << "id: " << channel.m_id 
      << " name: " << channel.m_name 
      << " v0set: " << channel.m_v0set
      << " i0set: " << channel.m_i0set
      << " vmon: " << channel.m_vmon
      << " imon: " << channel.m_imon
      << " status: " << channel.m_status
      ;
    return out;
  }

};
#endif
