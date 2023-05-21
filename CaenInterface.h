#ifndef CAENINTERFACE_H
#define CAENINTERFACE_H

extern "C" {
  
  //! connect
  bool connect_to_interface( 
    const char* /*ip*/,
    const char* /*user*/,
    const char* /*password*/ ); 
  
  //! disconnect
  void disconnect_from_interface();
  
  //! turn on/off channel
  bool set_channel_on( const char* /* channel name*/, bool );

  //! assign unsigned parameter value to given channel
  bool set_parameter_unsigned( const char* /* channel name*/, const char* /* parname */, unsigned int /* value */ );

  //! assign float parameter value to given channel
  bool set_parameter_float( const char* /* channel name*/, const char* /* parname */, float /* value */ );
  
  //! get unsigned parameter value for a given channel
  unsigned int get_parameter_unsigned( const char* /* channel name*/, const char* /* parname */ );

  //! get float parameter value for a given channel
  float get_parameter_float( const char* /* channel name*/, const char* /* parname */ );
  
  //! get status for all channels
  const char* get_channel_status();
  
  /// return true if last command was successful
  /** note: this is misleading. For now it only refers to commands as run by Connection object */
  bool last_command_successful();

}

#endif
