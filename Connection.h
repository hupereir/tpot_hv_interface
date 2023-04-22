#ifndef CONNECTION_H
#define CONNECTION_H

#include "Slot.h"

#include <CAENHVWrapper.h>

class Connection
{
    public:
    
    //! constructor
    Connection();
    
    //! destructor
    ~Connection();
    
    //! get list of non empty slots
    Slot::List get_slots();
    
    //! get all channel names
    using string_list_t  = std::vector<std::string>;
    string_list_t get_channel_names();
    
    //! valid
    bool is_valid() const
    { return m_valid; }
    
    //! reply from last command
    CAENHVRESULT get_reply() const
    { return m_reply; }
    
    private:
    
    //! true if connection is valid
    bool m_valid = false;
    
    //! connection handle
    int m_handle = -1;
    
    //! last command reply
    CAENHVRESULT m_reply = 0;
    
    //!@name connection details
    //@{
    CAENHV_SYSTEM_TYPE_t m_type = SY4527;
    int m_link_type = 0;
    std::string m_ip_address = "10.20.34.154";
    std::string m_username = "admin";
    std::string m_password = "admin";
    //@}
};

#endif
