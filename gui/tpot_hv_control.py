#!/usr/bin/env python3
from tkinter import *
from tkinter import messagebox

import os.path
import subprocess
import sys

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
bigfont = ("arial", titlefontsize, "bold" )

# color definitions
headerbgcolor='#0099FF'
headerfgcolor='#ffffff'
framebgcolor='#ffffff'

buttonbgcolor='#dddddd'
buttonfgcolor='#000000'
buttonbgcolor_active='#bbbbbb'

framepadx=5
framepady=5
buttonpadx=3
buttonpady=3

##########################################3
class generic_button( Button ):
  def __init__(self, parent, text):
    Button.__init__( self, parent )
    self.configure( text = text, \
      border = 0, \
      padx = 9, pady = 9, \
      font = normalfont, bg = buttonbgcolor, fg = buttonfgcolor, \
      activebackground = buttonbgcolor_active, activeforeground = buttonfgcolor )

##########################################3
class yes_no_dialog( Toplevel ):
    def __init__(self, parent, title, message ):
      Toplevel.__init__(self, parent)
      self.parent=parent
      self.title( title )
      self.configure( bg = framebgcolor, padx=10, pady=10 )

      self.headerframe = Frame( self, bg = framebgcolor )
      self.headerframe.pack( side=TOP, fill=Y )

      try:
        l1=Label(self.headerframe,bg = framebgcolor, image="::tk::icons::question")
        l1.grid(row=0, column=0, pady=(7, 0), padx=(10, 30), sticky="e")
      except:
        pass

      self.label=Label(self.headerframe,text=message,bg = framebgcolor, \
        font = normalfont, wraplength = 500,\
        padx=10, pady=10)
      self.label.grid( row=0, column=1, pady=(7, 10), sticky="w")

      self.buttonframe = Frame( self, bg = framebgcolor )
      self.buttonframe.pack( side=TOP, fill=Y )

      self.yes_button = generic_button( self.buttonframe, "Yes" )
      self.yes_button.configure( command = self.on_yes, width=10 )
      self.yes_button.grid( row=0, column=0, padx=35 )

      self.no_button = generic_button( self.buttonframe, "No" )
      self.no_button.configure( command = self.on_no, width=10 )
      self.no_button.grid( row=0, column=1, padx=35 )

      self.reply = "no"

    def on_yes(self):
      self.reply = "yes"
      self.destroy()

    def on_no(self):
      self.reply = "no"
      self.destroy()

    def show(self):
      root.eval( f"tk::PlaceWindow .{self.winfo_name()} widget ." )
      self.wm_transient( root )
      self.wm_deiconify()
      self.grab_set()
      self.wait_window()
      return self.reply

##########################################3
class information_dialog( Toplevel ):
    def __init__(self, parent, title, message ):
      Toplevel.__init__(self, parent)
      self.parent=parent
      self.title( title )
      self.configure( bg = framebgcolor, padx=10, pady=10 )

      self.headerframe = Frame( self, bg = framebgcolor )
      self.headerframe.pack( side=TOP, fill=Y )

      try:
        l1=Label(self.headerframe,bg = framebgcolor, image="::tk::icons::information")
        l1.grid(row=0, column=0, pady=(7, 0), padx=(10, 30), sticky="e")
      except:
        pass

      self.label=Label(self.headerframe,text=message,bg = framebgcolor,\
        font = normalfont, wraplength = 500,\
        padx=10, pady=10)
      self.label.grid( row=0, column=1, pady=(7, 10), sticky="w")

      self.yes_button = generic_button( self, "Ok" )
      self.yes_button.configure( command = self.destroy, width=10 )
      self.yes_button.pack( side=TOP, fill=Y )

    def show(self):
      root.eval( f"tk::PlaceWindow .{self.winfo_name()} widget ." )
      self.wm_transient( root )
      self.wm_deiconify()
      self.grab_set()
      self.wait_window()

##########################################3
def tpot_hv_go_off():
  button_hv_off.configure( relief="sunken" )

  reply = yes_no_dialog(root, "TPOT HV OFF", "This will turn OFF all TPOT HV channels. Confirm ?").show()

  if reply == 'yes':
    subprocess.call([bin_path+"/tpot_hv_off.py", "--force", "all"] )
  button_hv_off.configure( relief="raised" )

##########################################3
def tpot_hv_go_safe():
  button_hv_go_safe.configure( relief="sunken" )
  reply = yes_no_dialog(root, "TPOT HV SAFE", "This will put TPOT in SAFE state. Confirm ?").show()
  if reply == 'yes':
    subprocess.call([bin_path+"/tpot_hv_restore_state.py", "--force", config_path+"/tpot_hv_safe_state.json"] )
    subprocess.call([bin_path+"/tpot_hv_on.py", "--force", "--mask", config_path+"/tpot_mask.json", "all"] )
  button_hv_go_safe.configure( relief="raised" )

##########################################3
def tpot_hv_go_operating():
  button_hv_go_operating.configure( relief="sunken" )
  reply = yes_no_dialog(root, "TPOT HV ON", "This will turn ON all TPOT HV channels. Confirm ?").show()
  if reply == 'yes':
    subprocess.call([bin_path+"/tpot_hv_restore_state.py", "--force", config_path+"/tpot_hv_operating_state.json"] )
    subprocess.call([bin_path+"/tpot_hv_on.py", "--force", "--mask", config_path+"/tpot_mask.json", "all"] )
  button_hv_go_operating.configure( relief="raised" )

##########################################3
def tpot_hv_recover_trips():
  button_hv_recover_trips.configure( relief="sunken" )
  reply = yes_no_dialog(root, "TPOT Recover Trips", "This will recover TPOT tripped channels. Confirm ?").show()
  if reply == 'yes':
    subprocess.call([bin_path+"/tpot_hv_recover_trips.py", "--force"] )
  button_hv_recover_trips.configure( relief="raised" )

##########################################3
def tpot_lv_go_off():
  button_lv_off.configure( relief="sunken" )
  reply = yes_no_dialog(root, "TPOT LV OFF", "This will turn OFF TPOT Low Voltage. Confirm ?").show()
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
    information_dialog( root, "TPOT LV ON", "There seems to be a run ongoing. Turning ON LV requires to either stop the current run, or wait for the end of the current run." ).show()
    button_lv_on.configure( relief="raised" )
    return

  # ask confirmation
  reply = yes_no_dialog(root, "TPOT LV ON", "This will turn ON TPOT Low Voltage. Confirm ?").show()
  if reply == 'yes':
    subprocess.call([bin_lv_path+"/tpot_lv_turn_on_and_configure.py", "--force"] )
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
    information_dialog( root, "TPOT Recover FEE Links", "There seems to be a run ongoing. Turning ON LV requires to either stop the current run, or wait for the end of the current run." ).show()
    button_lv_recover_fee_links.configure( relief="raised" )
    return


  # ask confirmation
  reply = yes_no_dialog(root, "TPOT Recover FEE Links", "This will recover lost FEE links. Confirm ?").show()
  if reply == 'yes':
    subprocess.call([bin_lv_path+"/tpot_lv_recover_fee_links.py", "--force"] )
  button_lv_recover_fee_links.configure( relief="raised" )

##########################################3
def main():

  global root
  root = Tk()
  root.title("TPOT LV and HV Control")
  root.minsize( 450, 400 )

  # sphenix logo
  # get script directory 
  script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
  img_file = f"{script_directory}/sphenixlogo.png"
  try:
    img = PhotoImage(file=img_file)
  except :
    img = PhotoImage()

  ## HV controls
  frame = Frame( root, bg = framebgcolor )
  frame.pack( side=TOP, fill=BOTH )

  headerframe = Frame( frame, bg = headerbgcolor )
  headerframe.pack( side=TOP, fill=X )
  Label( headerframe, text= "TPOT High Voltage (HV) Control", font = bigfont, anchor=W, fg=headerfgcolor, bg = headerbgcolor, padx=10, pady=10 ).pack(side=LEFT, fill=X)
  Label( headerframe, image=img, bg = headerbgcolor ).pack(side=RIGHT, fill=X)

  buttonframe = Frame( frame, bg = framebgcolor )
  buttonframe.pack( side=TOP, fill=X, padx=buttonpadx, pady=buttonpady)  

  global button_hv_off
  button_hv_off = generic_button( buttonframe, "Turn OFF High Voltage" )
  button_hv_off.configure( command=tpot_hv_go_off )
  button_hv_off.pack( side = TOP, fill=X, padx=buttonpadx, pady=buttonpady )

  global button_hv_go_safe
  button_hv_go_safe = generic_button( buttonframe, text= "Go to SAFE High Voltage" )
  button_hv_go_safe.configure( command=tpot_hv_go_safe )
  button_hv_go_safe.pack( side = TOP, fill=X, padx=buttonpadx, pady=buttonpady )

  global button_hv_go_operating
  button_hv_go_operating = generic_button( buttonframe, text= "Turn ON High Voltage" )
  button_hv_go_operating.configure( command=tpot_hv_go_operating )
  button_hv_go_operating.pack( side = TOP, fill=X, padx=buttonpadx, pady=buttonpady )

  global button_hv_recover_trips
  button_hv_recover_trips = generic_button( buttonframe, text= "Recover High Voltage Trips" )
  button_hv_recover_trips.configure( command=tpot_hv_recover_trips )
  button_hv_recover_trips.pack( side = TOP, fill=X, padx=buttonpadx, pady=buttonpady )

  ## LV controls
  frame = Frame( root, bg = framebgcolor )
  frame.pack( side=TOP, fill=BOTH )

  headerframe = Frame( frame, bg = headerbgcolor )
  headerframe.pack( side=TOP, fill=X )
  Label( headerframe, text= "TPOT Low Voltage (LV) Control", font = bigfont, anchor=W, fg=headerfgcolor, bg = headerbgcolor, padx=10, pady=10 ).pack(side=LEFT, fill=X)
  Label( headerframe, image=img, bg = headerbgcolor ).pack(side=RIGHT, fill=X)

  buttonframe = Frame( frame, bg = framebgcolor )
  buttonframe.pack( side=TOP, fill=X, padx=buttonpadx, pady=buttonpady)  

  global button_lv_off
  button_lv_off = generic_button( buttonframe, text= "Turn OFF Low Voltage" )
  button_lv_off.configure( command=tpot_lv_go_off )
  button_lv_off.pack( side = TOP, fill=X, padx=buttonpadx, pady=buttonpady )

  global button_lv_on
  button_lv_on = generic_button( buttonframe, text= "Turn ON Low Voltage" )
  button_lv_on.configure( command=tpot_lv_go_on )
  button_lv_on.pack( side = TOP, fill=X, padx=buttonpadx, pady=buttonpady )

  global button_lv_recover_fee_links
  button_lv_recover_fee_links = generic_button( buttonframe, text= "Recover FEE links" )
  button_lv_recover_fee_links.configure( command=tpot_lv_recover_fee_links )
  button_lv_recover_fee_links.pack( side = TOP, fill=X, padx=buttonpadx, pady=buttonpady )

  root.mainloop()

if __name__ == '__main__':
  main()
