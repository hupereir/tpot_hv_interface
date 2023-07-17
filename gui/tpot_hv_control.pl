#! /usr/bin/perl

use Tk;
require Tk::Dialog;

$config_path ="/home/phnxrc/hpereira/tpot_hv_interface/config";
$bin_path = "/home/phnxrc/hpereira/tpot_hv_interface/python";

# binaries for LV control
$bin_lv_path = "/home/phnxrc/hpereira/tpot_lv_interface";

##########################################3
sub tpot_go_off
{
    $button_off->configure(-relief => 'sunken' );
    $reply = $mw->Dialog( 
        -text => 'This will turn OFF all TPOT HV channels. Confirm ?', 
        -title => 'TPOT HV OFF', 
        -buttons => ['Yes', 'No'], -default_button => 'No' )->Show( -popover => 'cursor');
    if( uc($reply) eq "YES" )
    { $result = `$bin_path/tpot_hv_off.py --force all`; }
    $button_off->configure(-relief => 'raised' );
}

##########################################3
sub tpot_go_safe
{
    $button_go_safe->configure(-relief => 'sunken' );
    $reply = $mw->Dialog(
        -text => 'This will put TPOT in SAFE state. Confirm ?', 
        -title => 'TPOT HV SAFE', 
        -buttons => ['Yes', 'No'], -default_button => 'No' )->Show( -popover => 'cursor');
    if( uc($reply) eq "YES" )
    {
        $result = `$bin_path/tpot_hv_restore_state.py --force $config_path/tpot_hv_safe_state.json`;
        $result = `$bin_path/tpot_hv_on.py --force --mask $config_path/tpot_mask.json all`;
    }
    $button_go_safe->configure(-relief => 'raised' );
}

##########################################3
sub tpot_go_operating
{
    $button_go_operating->configure(-relief => 'sunken' );
    $reply = $mw->Dialog(
        -text => 'This will turn ON all TPOT HV channels. Confirm ?', 
        -title => 'TPOT HV ON', 
        -buttons => ['Yes', 'No'], -default_button => 'No' )->Show( -popover => 'cursor');
    if( uc($reply) eq "YES" )
    {
        $result = `$bin_path/tpot_hv_restore_state.py --force $config_path/tpot_hv_operating_state.json`;
        $result = `$bin_path/tpot_hv_on.py --force --mask $config_path/tpot_mask.json all`;
    }
    $button_go_operating->configure(-relief => 'raised' );
}

##########################################3
sub tpot_recover_trips
{
    $button_recover_trips->configure(-relief => 'sunken' );
    $reply = $mw->Dialog(
        -text => 'This will recover TPOT tripped channels. Confirm ?', 
        -title => 'TPOT Recover Trips', 
        -buttons => ['Yes', 'No'], -default_button => 'Yes' )->Show( -popover => 'cursor');
    if( uc($reply) eq "YES" )
    {
        $result = `$bin_path/tpot_hv_recover_trips.py --force`;
    }
    $button_recover_trips->configure(-relief => 'raised' );
}

##########################################3
sub tpot_recover_fee_links
{
    $button_recover_fee_links->configure(-relief => 'sunken' );
    $reply = $mw->Dialog(
        -text => 'This will recover TPOT FEE links. Confirm ?', 
        -title => 'TPOT Recover FEE Links', 
        -buttons => ['Yes', 'No'], -default_button => 'Yes' )->Show( -popover => 'cursor');
    if( uc($reply) eq "YES" )
    {
        $result = `$bin_lv_path/tpot_lv_recover_fee_links.py --force`;
    }
    $button_recover_fee_links->configure(-relief => 'raised' );
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

$label{'sline'} = $mw->Label(-text => "TPOT LV and HV Control", -background=>$slinebg, -font =>$bigfont);
$label{'sline'}->pack(-side=> 'top', -fill=> 'x', -ipadx=> '15m', -ipady=> '1m');

$frame{'center'} = $mw->Frame()->pack(-side => 'top', -fill => 'x');
$framebutton = $frame{'center'}->Label(-bg => $color1, -relief=> 'raised')->pack(-side =>'top', -fill=> 'x', -ipadx=>'15m');

$button_off = $framebutton->
    Button(-bg => $buttonbgcolor, -text => "Turn OFF", -command => [\&tpot_go_off, $b],  -relief =>'raised',  -font=> $normalfont)->
    pack(-side =>'top', -fill=> 'x', -ipadx=> '1m',  -ipady=> '1m');

$button_go_safe = $framebutton->
    Button(-bg => $buttonbgcolor, -text => "Go to SAFE", -command => [\&tpot_go_safe, $b],  -relief =>'raised',  -font=> $normalfont)->
    pack(-side =>'top', -fill=> 'x', -ipadx=> '1m',  -ipady=> '1m');

$button_go_operating = $framebutton->
    Button(-bg => $buttonbgcolor, -text => "Turn ON", -command => [\&tpot_go_operating, $b],  -relief =>'raised',  -font=> $normalfont)->
    pack(-side =>'top', -fill=> 'x', -ipadx=> '1m',  -ipady=> '1m');

$button_recover_trips = $framebutton->
    Button(-bg => $buttonbgcolor, -text => "Recover trips", -command => [\&tpot_recover_trips, $b],  -relief =>'raised',  -font=> $normalfont)->
    pack(-side =>'top', -fill=> 'x', -ipadx=> '1m',  -ipady=> '1m');

$button_recover_fee_links = $framebutton->
    Button(-bg => $buttonbgcolor, -text => "Recover FEE links", -command => [\&tpot_recover_fee_links, $b],  -relief =>'raised',  -font=> $normalfont)->
    pack(-side =>'top', -fill=> 'x', -ipadx=> '1m',  -ipady=> '1m');

MainLoop();

