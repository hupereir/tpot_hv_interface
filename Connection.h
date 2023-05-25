#ifndef CONNECTION_H
#define CONNECTION_H

#include <CAENHVWrapper.h>

#include <map>
#include <string>

class Connection
{
    public:
    
    //! constructor
    Connection() = default;
    
    //! destructor
    ~Connection();

    //! connect
    CAENHVRESULT connect(       
      const std::string& /* ip */,
      const std::string& /* user */,
      const std::string& /* password */);
  
    //! disconnect
    void disconnect();
            
    //! valid
    bool is_connected() const
    { return m_connected; }
         
    //! get handle
    int get_handle() const 
    { return m_handle; }
    
    //! get channel matching name
    using channel_id_t = std::pair<int, unsigned short>;
    channel_id_t get_channel_id( const std::string& /*name*/ ) const;
    
    private:
    
    //! map channel names to slot, id
    void build_channel_map();
    
    //! true if connection is valid
    bool m_connected = false;
    
    //! connection handle
    int m_handle = -1;
    
    //!@name connection details
    //@{
    CAENHV_SYSTEM_TYPE_t m_type = SY4527;
    int m_link_type = 0;
    //@}
    
    //! channel map
    using channel_map_t = std::map<std::string, channel_id_t>;
    channel_map_t m_channel_map;
    
};

#endif
