#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import subprocess

# configuration
# config_path ="/home/phnxrc/operations/TPOT/tpot_hv_interface/config";
# bin_path = "/home/phnxrc/operations/TPOT/tpot_hv_interface/python";
# bin_lv_path = "/home/phnxrc/operations/TPOT/tpot_lv_interface";

config_path ="/home/hpereira/sphenix/src/tpot_hv_interface/config";
bin_path = "/home/hpereira/sphenix/src/tpot_hv_interface/python";
bin_lv_path = "/home/hpereira/sphenix/src/tpot_lv_interface";

##########################################3
def tpot_hv_go_off():
  button_hv_off.configure( relief="sunken" );
  reply = messagebox.askquestion(title="TPOT HV OFF", message="This will turn OFF TPOT High Voltage. Confirm ?")
  if reply:
    subprocess.call([bin_path+"/tpot_hv_off.py", "--force", "all"] )
  button_hv_off.configure( relief="raised" );

##########################################3
def tpot_hv_go_safe():
  button_hv_go_safe.configure( relief="sunken" );
  reply = messagebox.askquestion(title="TPOT HV SAFE", message="This will put TPOT in SAFE state. Confirm ?")
  if reply:
    subprocess.call([bin_path+"/tpot_hv_restore_state.py", "--force", config_path+"/tpot_hv_safe_state.json"] );
    subprocess.call([bin_path+"/tpot_hv_on.py", "--force", "--mask", config_path+"/tpot_mask.json", "all"] );
  button_hv_go_safe.configure( relief="raised" );

##########################################3
def tpot_hv_go_operating():
  button_hv_go_operating.configure( relief="sunken" );
  reply = messagebox.askquestion(title="TPOT HV ON", message="This will turn ON all TPOT HV channels. Confirm ?")
  if reply:
    subprocess.call([bin_path+"/tpot_hv_restore_state.py", "--force", config_path+"/tpot_hv_operating_state.json"] );
    subprocess.call([bin_path+"/tpot_hv_on.py", "--force", "--mask", config_path+"/tpot_mask.json", "all"] );
  button_hv_go_operating.configure( relief="raised" );

##########################################3
def tpot_hv_recover_trips():
  button_hv_recover_trips.configure( relief="sunken" );
  reply = messagebox.askquestion(title="TPOT Recover Trips", message="This will recover TPOT tripped channels. Confirm ?")
  if reply:
    subprocess.call([bin_path+"/tpot_hv_recover_trips.py", "--force"] )
  button_hv_recover_trips.configure( relief="raised" );

##########################################3
def tpot_lv_go_off():
  button_lv_off.configure( relief="sunken" );
  reply = messagebox.askquestion(title="TPOT LV OFF", message="This will turn OFF TPOT Low Voltage. Confirm ?")
  if reply:
    subprocess.call([bin_lv_path+"/tpot_lv_off.py", "all"] )
  button_lv_off.configure( relief="raised" );

##########################################3
def tpot_lv_go_on():
  # turning ON the LV is essentially the same as recovering fee links
  # keep button sunken 
  button_lv_on.configure( relief="sunken" );

  # check if TPOT vgtm is running. Print a warning if yes
  result = subprocess.run( ["gl1_gtm_client", "gtm_fullstatus"], stdout=subprocess.PIPE)
  output = result.stdout.decode('utf8').split();
  vgtm = 12
  vgtm_is_running = hex(output[1]) & (1<<vgtm);

  if vgtm_is_running:
    messagebox.showinfo( title="TPOT LV ON", message="There seems to be a run ongoing. Turning ON LV requires to either stop the current run, or wait for the end of the current run." )
    button_lv_on.configure( relief="raised" );
    return

  # ask confirmation
  reply = messagebox.askquestion(title="TPOT LV ON", message="This will turn ON TPOT Low Voltage. Confirm ?")
  if reply:
    subprocess.call([bin_lv_path+"/tpot_lv_recover_fee_links.py", "--force"] )
  button_lv_on.configure( relief="raised" );

##########################################3
def tpot_lv_recover_fee_links():
  # turning ON the LV is essentially the same as recovering fee links
  # keep button sunken 
  button_lv_recover_fee_links.configure( relief="sunken" );

  # check if TPOT vgtm is running. Print a warning if yes
  result = subprocess.run( ["gl1_gtm_client", "gtm_fullstatus"], stdout=subprocess.PIPE)
  output = result.stdout.decode('utf8').split();
  vgtm = 12
  vgtm_is_running = hex(output[1]) & (1<<vgtm);

  if vgtm_is_running:
    messagebox.showinfo( title="TPOT Recover FEE Links", message="There seems to be a run ongoing. Turning ON LV requires to either stop the current run, or wait for the end of the current run." )
    button_lv_recover_fee_links.configure( relief="raised" );
    return

  # ask confirmation
  reply = messagebox.askquestion(title="TPOT Recover FEE Links", message="This will turn ON TPOT Low Voltage. Confirm ?")
  if reply:
    subprocess.call([bin_lv_path+"/tpot_lv_recover_fee_links.py", "--force"] )
  button_lv_recover_fee_links.configure( relief="raised" );

def main():

  # fonts definitions
  fontsize="12"
  titlefontsize="13"
  normalfont = ("arial", fontsize )
  bigfont = ("arial", titlefontsize, "bold" )

  # color definitions
  buttonbgcolor='#33CCCC';
  labelbgcolor='#cccc00';

  root = Tk()
  root.title("TPOT LV and HV Control")

  ## HV controls  
  Label( root, text= "TPOT High Voltage (HV) Control", font = bigfont, bg = labelbgcolor ).pack( side=TOP, fill=X, ipadx="15m", ipady="1m" )
  
  global button_hv_off
  button_hv_off = Button( root, text= "Turn OFF High Voltage", command=tpot_hv_go_off, font = normalfont, bg = buttonbgcolor )
  button_hv_off.pack( side = TOP, fill=X, ipadx="1m", ipady="1m" )

  global  button_hv_go_safe
  button_hv_go_safe = Button( root, text= "Go to SAFE High Voltage", command=tpot_hv_go_safe, font = normalfont, bg = buttonbgcolor )
  button_hv_go_safe.pack( side = TOP, fill=X, ipadx="1m", ipady="1m" )

  global button_hv_go_operating
  button_hv_go_operating = Button( root, text= "Turn ON High Voltage", command=tpot_hv_go_operating, font = normalfont, bg = buttonbgcolor )
  button_hv_go_operating.pack( side = TOP, fill=X, ipadx="1m", ipady="1m" )

  global button_hv_recover_trips
  button_hv_recover_trips = Button( root, text= "Recover High Voltage Trips", command=tpot_hv_recover_trips, font = normalfont, bg = buttonbgcolor )
  button_hv_recover_trips.pack( side = TOP, fill=X, ipadx="1m", ipady="1m" )

  ## LV controls  
  Label( root, text= "TPOT Low Voltage (LV) Control", font = bigfont, bg = labelbgcolor ).pack( side=TOP, fill=X, ipadx="15m", ipady="1m" )

  global button_lv_off
  button_lv_off = Button( root, text= "Turn OFF Low Voltage", command=tpot_lv_go_off, font = normalfont, bg = buttonbgcolor )
  button_lv_off.pack( side = TOP, fill=X, ipadx="1m", ipady="1m" )

  global button_lv_on
  button_lv_on = Button( root, text= "Turn ON Low Voltage", command=tpot_lv_go_on, font = normalfont, bg = buttonbgcolor )
  button_lv_on.pack( side = TOP, fill=X, ipadx="1m", ipady="1m" )

  global button_lv_recover_fee_links
  button_lv_recover_fee_links = Button( root, text= "Recover FEE links", command=tpot_lv_recover_fee_links, font = normalfont, bg = buttonbgcolor )
  button_lv_recover_fee_links.pack( side = TOP, fill=X, ipadx="1m", ipady="1m" )

  root.mainloop()  

if __name__ == '__main__':
  main()
