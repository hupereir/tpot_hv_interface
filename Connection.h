#ifndef CONNECTION_H
#define CONNECTION_H

#include "Channel.h"
#include "Slot.h"

#include <CAENHVWrapper.h>

class Connection
{
    public:
    
    //! constructor
    Connection() = default;
    
    //! destructor
    ~Connection();

    //! connect
    void connect(       
      const std::string& /* ip */,
      const std::string& /* user */,
      const std::string& /* password */);
  
    //! disconnect
    void disconnect();
    
    //! get list of non empty slots
    Slot::List get_slots();
    
    //! get list of channels for a given slot
    Channel::List get_channels( const Slot& );
        
    //! valid
    bool is_connected() const
    { return m_connected; }
    
    //! reply from last command
    CAENHVRESULT get_reply() const
    { return m_reply; }
    
    private:
    
    //! true if connection is valid
    bool m_connected = false;
    
    //! connection handle
    int m_handle = -1;
    
    //! last command reply
    CAENHVRESULT m_reply = 0;
    
    //!@name connection details
    //@{
    CAENHV_SYSTEM_TYPE_t m_type = SY4527;
    int m_link_type = 0;
    //@}
};

#endif
