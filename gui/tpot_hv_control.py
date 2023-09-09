#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import subprocess

# configuration
config_path ="/home/phnxrc/operations/TPOT/tpot_hv_interface/config"
bin_path = "/home/phnxrc/operations/TPOT/tpot_hv_interface/python"
bin_lv_path = "/home/phnxrc/operations/TPOT/tpot_lv_interface"

# config_path ="/home/hpereira/sphenix/src/tpot_hv_interface/config"
# bin_path = "/home/hpereira/sphenix/src/tpot_hv_interface/python"
# bin_lv_path = "/home/hpereira/sphenix/src/tpot_lv_interface"

# fonts definitions
fontsize=12
titlefontsize=13
normalfont = ("arial", fontsize )
bigfont = ("arial", titlefontsize )

# color definitions
# buttonbgcolor='#33CCCC'
headerbgcolor='#0099FF'
headerfgcolor='#ffffff'
framebgcolor='#ffffff'
buttonbgcolor='#cccccc'
buttonfgcolor='#000000'
buttonbgcolor_active='#bbbbbb'

framepadx=5
framepady=5
buttonpadx=5
buttonpady=5

##########################################3
def tpot_hv_go_off():
  button_hv_off.configure( relief="sunken" )
  reply = messagebox.askquestion(title="TPOT HV OFF", message="This will turn OFF TPOT High Voltage. Confirm ?")
  if reply == 'yes':
    subprocess.call([bin_path+"/tpot_hv_off.py", "--force", "all"] )
  button_hv_off.configure( relief="raised" )

##########################################3
def tpot_hv_go_safe():
  button_hv_go_safe.configure( relief="sunken" )
  reply = messagebox.askquestion(title="TPOT HV SAFE", message="This will put TPOT in SAFE state. Confirm ?")
  if reply == 'yes':
    subprocess.call([bin_path+"/tpot_hv_restore_state.py", "--force", config_path+"/tpot_hv_safe_state.json"] )
    subprocess.call([bin_path+"/tpot_hv_on.py", "--force", "--mask", config_path+"/tpot_mask.json", "all"] )
  button_hv_go_safe.configure( relief="raised" )

##########################################3
def tpot_hv_go_operating():
  button_hv_go_operating.configure( relief="sunken" )
  reply = messagebox.askquestion(title="TPOT HV ON", message="This will turn ON all TPOT HV channels. Confirm ?")
  if reply == 'yes':
    subprocess.call([bin_path+"/tpot_hv_restore_state.py", "--force", config_path+"/tpot_hv_operating_state.json"] )
    subprocess.call([bin_path+"/tpot_hv_on.py", "--force", "--mask", config_path+"/tpot_mask.json", "all"] )
  button_hv_go_operating.configure( relief="raised" )

##########################################3
def tpot_hv_recover_trips():
  button_hv_recover_trips.configure( relief="sunken" )
  reply = messagebox.askquestion(title="TPOT Recover Trips", message="This will recover TPOT tripped channels. Confirm ?")
  if reply == 'yes':
    subprocess.call([bin_path+"/tpot_hv_recover_trips.py", "--force"] )
  button_hv_recover_trips.configure( relief="raised" )

##########################################3
def tpot_lv_go_off():
  button_lv_off.configure( relief="sunken" )
  reply = messagebox.askquestion(title="TPOT LV OFF", message="This will turn OFF TPOT Low Voltage. Confirm ?")
  if reply == 'yes':
    subprocess.call([bin_lv_path+"/tpot_lv_off.py", "all"] )
  button_lv_off.configure( relief="raised" )

##########################################3
def tpot_lv_go_on():
  # turning ON the LV is essentially the same as recovering fee links
  # keep button sunken 
  button_lv_on.configure( relief="sunken" )

  # check if TPOT vgtm is running. Print a warning if yes
  result = subprocess.run( ["gl1_gtm_client", "gtm_fullstatus"], stdout=subprocess.PIPE)
  output = result.stdout.decode('utf8').split()
  vgtm = 12
  vgtm_is_running = int(output[2],0) & (1<<vgtm)

  if vgtm_is_running:
    messagebox.showinfo( title="TPOT LV ON", message="There seems to be a run ongoing. Turning ON LV requires to either stop the current run, or wait for the end of the current run." )
    button_lv_on.configure( relief="raised" )
    return

  # ask confirmation
  reply = messagebox.askquestion(title="TPOT LV ON", message="This will turn ON TPOT Low Voltage. Confirm ?")
  if reply == 'yes':
    subprocess.call([bin_lv_path+"/tpot_lv_recover_fee_links.py", "--force"] )
  button_lv_on.configure( relief="raised" )

##########################################3
def tpot_lv_recover_fee_links():
  # turning ON the LV is essentially the same as recovering fee links
  # keep button sunken 
  button_lv_recover_fee_links.configure( relief="sunken" )

  # check if TPOT vgtm is running. Print a warning if yes
  result = subprocess.run( ["gl1_gtm_client", "gtm_fullstatus"], stdout=subprocess.PIPE)
  output = result.stdout.decode('utf8').split()
  vgtm = 12
  vgtm_is_running = int(output[2],0) & (1<<vgtm)
  
  if vgtm_is_running:
    messagebox.showinfo( title="TPOT Recover FEE Links", message="There seems to be a run ongoing. Turning ON LV requires to either stop the current run, or wait for the end of the current run." )
    button_lv_recover_fee_links.configure( relief="raised" )
    return

  # ask confirmation
  reply = messagebox.askquestion(title="TPOT Recover FEE Links", message="This will turn ON TPOT Low Voltage. Confirm ?")
  if reply == 'yes':
    subprocess.call([bin_lv_path+"/tpot_lv_recover_fee_links.py", "--force"] )
  button_lv_recover_fee_links.configure( relief="raised" )

##########################################3
def generic_button( parent, text ):
  return Button( parent, text = text, font = normalfont, bg = buttonbgcolor, fg = buttonfgcolor, activebackground = buttonbgcolor_active, activeforeground = buttonfgcolor )

##########################################3
def main():

  root = Tk()
  root.title("TPOT LV and HV Control")
  
  ## HV controls  
  baseframe = Frame(root)
  baseframe.pack( side=TOP, fill=BOTH, padx=framepadx, pady=framepady )
  
  frame = Frame( baseframe, bg = framebgcolor )
  frame.pack( side=TOP, fill=BOTH, padx=framepadx, pady=framepady )
  Label( frame, text= "TPOT High Voltage (HV) Control", font = bigfont, anchor=W, bg = headerbgcolor, fg=headerfgcolor, padx=10, pady=10 ).pack( side=TOP, fill=X )
  
  global button_hv_off
  button_hv_off = generic_button( frame, "Turn OFF High Voltage" )
  button_hv_off.configure( command=tpot_hv_go_off )
  button_hv_off.pack( side = TOP, fill=X, ipadx=5, ipady=5, padx=buttonpadx, pady=buttonpady )

  global button_hv_go_safe
  button_hv_go_safe = generic_button( frame, text= "Go to SAFE High Voltage" )
  button_hv_go_safe.configure( command=tpot_hv_go_safe )
  button_hv_go_safe.pack( side = TOP, fill=X, ipadx=5, ipady=5, padx=buttonpadx, pady=buttonpady )

  global button_hv_go_operating
  button_hv_go_operating = generic_button( frame, text= "Turn ON High Voltage" )
  button_hv_go_operating.configure( command=tpot_hv_go_operating )
  button_hv_go_operating.pack( side = TOP, fill=X, ipadx=5, ipady=5, padx=buttonpadx, pady=buttonpady )

  global button_hv_recover_trips
  button_hv_recover_trips = generic_button( frame, text= "Recover High Voltage Trips" )
  button_hv_recover_trips.configure( command=tpot_hv_recover_trips )
  button_hv_recover_trips.pack( side = TOP, fill=X, ipadx=5, ipady=5, padx=buttonpadx, pady=buttonpady )

  ## LV controls  
  frame = Frame( baseframe, bg = framebgcolor )
  frame.pack( side=TOP, fill=BOTH, padx=framepadx, pady=framepady )
  Label( frame, text= "TPOT Low Voltage (HV) Control", font = bigfont, anchor=W, bg = headerbgcolor, fg=headerfgcolor, padx=10, pady=10 ).pack( side=TOP, fill=X )

  global button_lv_off
  button_lv_off = generic_button( frame, text= "Turn OFF Low Voltage" )
  button_lv_off.configure( command=tpot_lv_go_off )
  button_lv_off.pack( side = TOP, fill=X, ipadx=5, ipady=5, padx=buttonpadx, pady=buttonpady )

  global button_lv_on
  button_lv_on = generic_button( frame, text= "Turn ON Low Voltage" )
  button_lv_on.configure( command=tpot_lv_go_on )
  button_lv_on.pack( side = TOP, fill=X, ipadx=5, ipady=5, padx=buttonpadx, pady=buttonpady )

  global button_lv_recover_fee_links
  button_lv_recover_fee_links = generic_button( frame, text= "Recover FEE links" )
  button_lv_recover_fee_links.configure( command=tpot_lv_recover_fee_links )
  button_lv_recover_fee_links.pack( side = TOP, fill=X, ipadx=5, ipady=5, padx=buttonpadx, pady=buttonpady )

  root.mainloop()  

if __name__ == '__main__':
  main()
