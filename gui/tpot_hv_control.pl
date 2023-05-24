#! /usr/bin/perl

use Tk;

$config_path ="/home/phnxrc/hpereira/tpot_hv_interface/config";
$bin_path = "/home/phnxrc/hpereira/tpot_hv_interface/python";

sub tpot_on
{

    $result = `$bin_path/tpot_hv_on.py all`;
}

sub tpot_off
{
    $result = `$bin_path/tpot_hv_off.py all`;
}

sub tpot_go_safe
{
    $result = `$bin_path/tpot_hv_restore_state.py $config_path/tpot_hv_safe_state.json`;
}

sub tpot_go_operating
{
    $result = `$bin_path/tpot_hv_restore_state.py $config_path/tpot_hv_operating_state.json`;
}

sub tpot_recover_trips
{
    $result = `$bin_path/tpot_hv_recover_trips`;
}

#$color1 = "#cccc99";
#$color1 = "#999900";
$color1 = "#CCCC99";
$okcolor = "#00cc99";
$errorcolor= "#ff6666";
$neutralcolor ="#cc9900";
$panelcolor = "#336633";
$warncolor = "IndianRed4";
$graycolor = "#666666";

$buttonbgcolor='#33CCCC';

$smalltextfg = '#00CCFF';
$smalltextbg = '#333366';

$slinebg='#cccc00';
#$sline2bg='#ffb90f';

$oncolor = "orange2";
$offcolor = "yellow4";


#$bgcolor = "#cccc66";
$bgcolor = "#990000";

$runstatcolor = "aquamarine";
$stopstatcolor = "palegreen";
$neutralcolor = "khaki";

#$smallfont = "6x10";

$titlefontsize=13;
$fontsize=12;
$subtitlefontsize=10;
$smallfont = ['arial', $subtitlefontsize];
$normalfont = ['arial', $fontsize];
$bigfont = ['arial', $titlefontsize, 'bold'];

$mw = MainWindow->new();

$smallfont = $mw->fontCreate('code', -family => 'fixed',-size => 10);


$mw->title("TPOT HV Control");


$label{'sline'} = $mw->Label(-text => "TPOT HV Control", -background=>$slinebg, -font =>$bigfont);
$label{'sline'}->pack(-side=> 'top', -fill=> 'x', -ipadx=> '15m', -ipady=> '1m');

$frame{'center'} = $mw->Frame()->pack(-side => 'top', -fill => 'x');
$framename = $frame{'center'}->Label(-bg => $color1, -relief=> 'raised')->pack(-side =>'left', -fill=> 'x', -ipadx=>'15m');

$outerlabel = $framename->Label(-bg => $color1)->pack(-side =>'top', -fill=> 'x', -padx=> '1m',  -pady=> '1m');

$button_open = $outerlabel->
    Button( -bg => $buttonbgcolor, -text => "Turn TPOT ON", -command => [\&tpot_on,$b],  -relief =>'raised',  -font=> $normalfont)->
    pack(-side =>'top', -fill=> 'x', -ipadx=> '1m',  -ipady=> '1m');

$button_begin = $outerlabel->
    Button(-bg => $buttonbgcolor, -text => "Turn TPOT OFF", -command => [\&tpot_off, $b],  -relief =>'raised',  -font=> $normalfont)->
    pack(-side =>'top', -fill=> 'x', -ipadx=> '1m',  -ipady=> '1m');

$button_begin = $outerlabel->
    Button(-bg => $buttonbgcolor, -text => "Go to SAFE state", -command => [\&tpot_go_safe, $b],  -relief =>'raised',  -font=> $normalfont)->
    pack(-side =>'top', -fill=> 'x', -ipadx=> '1m',  -ipady=> '1m');

$button_begin = $outerlabel->
    Button(-bg => $buttonbgcolor, -text => "Go to OPERATING state", -command => [\&tpot_go_operating, $b],  -relief =>'raised',  -font=> $normalfont)->
    pack(-side =>'top', -fill=> 'x', -ipadx=> '1m',  -ipady=> '1m');

$button_begin = $outerlabel->
    Button(-bg => $buttonbgcolor, -text => "Recover trips", -command => [\&tpot_recover_trips, $b],  -relief =>'raised',  -font=> $normalfont)->
    pack(-side =>'top', -fill=> 'x', -ipadx=> '1m',  -ipady=> '1m');


MainLoop();

