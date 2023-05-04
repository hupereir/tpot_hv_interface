#ifndef CAENINTERFACE_H
#define CAENINTERFACE_H

extern "C" {
  
  bool connect_to_interface( 
    const char* /*ip*/,
    const char* /*user*/,
    const char* /*password*/ ); 
  
  void disconnect_from_interface();
  
  float get_v0set( const char* /*channel name*/ );
  void set_v0set( const char* /*channel name*/, float /*value*/ );
  
  void set_channel_on( const char* /* channel name*/, bool );
  
  const char* get_channel_status();
  
  bool last_command_successful();

}

#endif
