#! /usr/bin/perl

use Tk;
require Tk::Dialog;

$config_path ="/home/phnxrc/operations/TPOT/tpot_hv_interface/config";
$bin_path = "/home/phnxrc/operations/TPOT/tpot_hv_interface/python";

# binaries for LV control
$bin_lv_path = "/home/phnxrc/operations/TPOT/tpot_lv_interface";

##########################################3
sub tpot_hv_go_off
{
    $button_hv_off->configure(-relief => 'sunken' );
    $reply = $mw->Dialog( 
        -text => 'This will turn OFF TPOT High Voltage. Confirm ?', 
        -title => 'TPOT HV OFF', 
	-buttons => ['Yes', 'No'], -default_button => 'No' )->Show( -popover => 'cursor');
    if( uc($reply) eq "YES" )
    { $result = `$bin_path/tpot_hv_off.py --force all`; }
    $button_hv_off->configure(-relief => 'raised' );
}

##########################################3
sub tpot_hv_go_safe
{
    $button_hv_go_safe->configure(-relief => 'sunken' );
    $reply = $mw->Dialog(
        -text => 'This will put TPOT in SAFE state. Confirm ?', 
        -title => 'TPOT HV SAFE', 
        -buttons => ['Yes', 'No'], -default_button => 'No' )->Show( -popover => 'cursor');
    if( uc($reply) eq "YES" )
    {
        $result = `$bin_path/tpot_hv_restore_state.py --force $config_path/tpot_hv_safe_state.json`;
        $result = `$bin_path/tpot_hv_on.py --force --mask $config_path/tpot_mask.json all`;
    }
    $button_hv_go_safe->configure(-relief => 'raised' );
}

##########################################3
sub tpot_hv_go_operating
{
    $button_hv_go_operating->configure(-relief => 'sunken' );
    $reply = $mw->Dialog(
        -text => 'This will turn ON all TPOT HV channels. Confirm ?', 
        -title => 'TPOT HV ON', 
        -buttons => ['Yes', 'No'], -default_button => 'No' )->Show( -popover => 'cursor');
    if( uc($reply) eq "YES" )
    {
        $result = `$bin_path/tpot_hv_restore_state.py --force $config_path/tpot_hv_operating_state.json`;
        $result = `$bin_path/tpot_hv_on.py --force --mask $config_path/tpot_mask.json all`;
    }
    $button_hv_go_operating->configure(-relief => 'raised' );
}

##########################################3
sub tpot_hv_recover_trips
{
    $button_hv_recover_trips->configure(-relief => 'sunken' );
    $reply = $mw->Dialog(
        -text => 'This will recover TPOT tripped channels. Confirm ?', 
        -title => 'TPOT Recover Trips',
        -buttons => ['Yes', 'No'], -default_button => 'Yes' )->Show( -popover => 'cursor');
    if( uc($reply) eq "YES" )
    {
        $result = `$bin_path/tpot_hv_recover_trips.py --force`;
    }
    $button_hv_recover_trips->configure(-relief => 'raised' );
}

##########################################3
sub tpot_lv_go_off
{
    $button_lv_off->configure(-relief => 'sunken' );

    # ask for confirmation
    $reply = $mw->Dialog(
        -text => 'This will turn OFF TPOT Low Voltage. Confirm ?', 
        -title => 'TPOT LV OFF', 
        -buttons => ['Yes', 'No'], -default_button => 'Yes')->Show( -popover => 'cursor');
    if( uc($reply) eq "YES" )
    {
        $result = `$bin_lv_path/tpot_lv_off.py all`;
    }
    $button_lv_off->configure(-relief => 'raised' );
}

##########################################3
sub tpot_lv_go_on
{
    # turning ON the LV is essentially the same as recovering fee links
    # keep button sunken 
    $button_lv_on->configure(-relief => 'sunken' );

    # check if TPOT vgtm is running. Print a warning if yes
    my @result = split( ' ',`gl1_gtm_client gtm_fullstatus`);
    my $vgtm = 12;
    my $vgtm_is_running = hex($result[1]) & (1<<$vgtm);

    if( $vgtm_is_running )
    {
        $reply = $mw->Dialog(
            -text => 'There seems to be a run ongoing. Turning ON LV requires to either stop the current run, or wait for the end of the current run.', 
            -title => 'TPOT LV ON', 
            -bitmap => 'warning',
            -buttons => ['Ok'], -default_button => 'Ok')->Show( -popover => 'cursor');
        $button_lv_on->configure(-relief => 'raised' );
        return;
    } else {
        # ask for confirmation
        $reply = $mw->Dialog(
            -text => 'This will turn ON TPOT Low Voltage. Confirm ?', 
            -title => 'TPOT LV ON', 
            -buttons => ['Yes', 'No'], -default_button => 'Yes')->Show( -popover => 'cursor');
        if( uc($reply) eq "YES" )
        {
            $result = `$bin_lv_path/tpot_lv_recover_fee_links.py --force`;
        }
        $button_lv_on->configure(-relief => 'raised' );
    }
}

##########################################3
sub tpot_lv_recover_fee_links
{
    # keep button sunken
    $button_lv_recover_fee_links->configure(-relief => 'sunken' );

    # check if TPOT vgtm is running. Print a warning if yes
    my @result = split( ' ',`gl1_gtm_client gtm_fullstatus`);
    my $vgtm = 12;
    my $vgtm_is_running = hex($result[1]) & (1<<$vgtm);

    if( $vgtm_is_running )
    {
        $reply = $mw->Dialog(
            -text => 'There seems to be a run ongoing. Recovering FEE links requires to either stop the current run, or wait for the end of the current run.', 
            -title => 'TPOT Recover FEE Links', 
            -bitmap => 'warning',
            -buttons => ['Ok'], -default_button => 'Ok')->Show( -popover => 'cursor');
        $button_lv_recover_fee_links->configure(-relief => 'raised' );
        return;
    } else {
        # ask for confirmation
        $reply = $mw->Dialog(
            -text => 'This will recover TPOT FEE links. Confirm ?', 
            -title => 'TPOT Recover FEE Links', 
            -buttons => ['Yes', 'No'], -default_button => 'Yes')->Show( -popover => 'cursor');
        if( uc($reply) eq "YES" )
        {
            $result = `$bin_lv_path/tpot_lv_recover_fee_links.py --force`;
        }
        $button_lv_recover_fee_links->configure(-relief => 'raised' );
    }
}

#$color1 = "#cccc99";
#$color1 = "#999900";
$color1 = "#CCCC99";
$graycolor = "#666666";

$buttonbgcolor='#33CCCC';

$smalltextfg = '#00CCFF';
$smalltextbg = '#333366';

$slinebg='#cccc00';

$titlefontsize=13;
$fontsize=12;
$subtitlefontsize=10;
$smallfont = ['arial', $subtitlefontsize];
$normalfont = ['arial', $fontsize];
$bigfont = ['arial', $titlefontsize, 'bold'];

$mw = MainWindow->new();

$smallfont = $mw->fontCreate('code', -family => 'fixed',-size => 10);


$mw->title("TPOT LV and HV Control");

# HV controls
$label = $mw->Label(-text => "TPOT High Voltage (HV) Control", -background=>$slinebg, -font =>$bigfont);
$label->pack(-side=> 'top', -fill=> 'x', -ipadx=> '15m', -ipady=> '1m');

$framebutton = $mw->Frame()->pack(-side => 'top', -fill => 'x');
$button_hv_off = $framebutton->
    Button(-bg => $buttonbgcolor, -text => "Turn OFF  High Voltage", -command => [\&tpot_hv_go_off, $b],  -relief =>'raised',  -font=> $normalfont)->
    pack(-side =>'top', -fill=> 'x', -ipadx=> '1m',  -ipady=> '1m');

$button_hv_go_safe = $framebutton->
    Button(-bg => $buttonbgcolor, -text => "Go to SAFE", -command => [\&tpot_hv_go_safe, $b],  -relief =>'raised',  -font=> $normalfont)->
    pack(-side =>'top', -fill=> 'x', -ipadx=> '1m',  -ipady=> '1m');

$button_hv_go_operating = $framebutton->
    Button(-bg => $buttonbgcolor, -text => "Turn ON High Voltage", -command => [\&tpot_hv_go_operating, $b],  -relief =>'raised',  -font=> $normalfont)->
    pack(-side =>'top', -fill=> 'x', -ipadx=> '1m',  -ipady=> '1m');

$button_hv_recover_trips = $framebutton->
    Button(-bg => $buttonbgcolor, -text => "Recover High Voltage trips", -command => [\&tpot_hv_recover_trips, $b],  -relief =>'raised',  -font=> $normalfont)->
    pack(-side =>'top', -fill=> 'x', -ipadx=> '1m',  -ipady=> '1m');

# LV controls
$label = $mw->Label(-text => "TPOT Low Voltage (LV) Control", -background=>$slinebg, -font =>$bigfont);
$label->pack(-side=> 'top', -fill=> 'x', -ipadx=> '15m', -ipady=> '1m');

$framebutton= $mw->Frame()->pack(-side => 'top', -fill => 'x');

$button_lv_off = $framebutton->
    Button(-bg => $buttonbgcolor, -text => "Turn OFF Low Voltage", -command => [\&tpot_lv_go_off, $b],  -relief =>'raised',  -font=> $normalfont)->
    pack(-side =>'top', -fill=> 'x', -ipadx=> '1m',  -ipady=> '1m');

$button_lv_on = $framebutton->
    Button(-bg => $buttonbgcolor, -text => "Turn ON Low Voltage", -command => [\&tpot_lv_go_on, $b],  -relief =>'raised',  -font=> $normalfont)->
    pack(-side =>'top', -fill=> 'x', -ipadx=> '1m',  -ipady=> '1m');

$button_lv_recover_fee_links = $framebutton->
    Button(-bg => $buttonbgcolor, -text => "Recover FEE links", -command => [\&tpot_lv_recover_fee_links, $b],  -relief =>'raised',  -font=> $normalfont)->
    pack(-side =>'top', -fill=> 'x', -ipadx=> '1m',  -ipady=> '1m');

MainLoop();

