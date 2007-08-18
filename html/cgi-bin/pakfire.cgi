#!/usr/bin/perl
#
# IPFire CGIs
#
# This file is part of the IPFire Project
# 
# This code is distributed under the terms of the GPL
#
#

use strict;

# enable only the following on debugging purpose
#use warnings;
#use CGI::Carp 'fatalsToBrowser';

require '/var/ipfire/general-functions.pl';
require "${General::swroot}/lang.pl";
require "${General::swroot}/header.pl";
require "/opt/pakfire/lib/functions.pl";

my %pakfiresettings=();
my $errormessage = '';
my %color = ();
my %mainsettings = ();

&Header::showhttpheaders();

$pakfiresettings{'ACTION'} = '';
$pakfiresettings{'VALID'} = '';

$pakfiresettings{'INSPAKS'} = '';
$pakfiresettings{'DELPAKS'} = '';
$pakfiresettings{'AUTOUPDATE'} = 'off';
$pakfiresettings{'UUID'} = 'on';

&Header::getcgihash(\%pakfiresettings);
&General::readhash("${General::swroot}/main/settings", \%mainsettings);
&General::readhash("/srv/web/ipfire/html/themes/".$mainsettings{'THEME'}."/include/colors.txt", \%color);

&Header::openpage($Lang::tr{'pakfire configuration'}, 1);
&Header::openbigbox('100%', 'left', '', $errormessage);

if ($pakfiresettings{'ACTION'} eq 'install'){
	$pakfiresettings{'INSPAKS'} =~ s/\|/\ /g;
	if ("$pakfiresettings{'FORCE'}" eq "on") {
		my $command = "/usr/local/bin/pakfire install --non-interactive --no-colors $pakfiresettings{'INSPAKS'} &>/dev/null &";
		system("$command");
		sleep(2);
	} else {
		&Header::openbox("100%", "center", "Abfrage");
  	my @output = `/usr/local/bin/pakfire resolvedeps --no-colors $pakfiresettings{'INSPAKS'}`;
		print <<END;
		<table><tr><td colspan='2'>$Lang::tr{'pakfire install package'}.$pakfiresettings{'INSPAKS'}.$Lang::tr{'pakfire possible dependency'}
		<pre>		
END
		foreach (@output) {
			print "$_\n";
		}
		print <<END;
		</pre>
		<tr><td colspan='2'>$Lang::tr{'pakfire accept all'}
		<tr><td colspan='2'>&nbsp;
		<tr><td align='right'><form method='post' action='$ENV{'SCRIPT_NAME'}'>
							<input type='hidden' name='INSPAKS' value='$pakfiresettings{'INSPAKS'}' />
							<input type='hidden' name='FORCE' value='on' />
							<input type='hidden' name='ACTION' value='install' />
							<input type='image' alt='$Lang::tr{'install'}' src='/images/go-next.png' />
						</form>
				<td align='left'>
						<form method='post' action='$ENV{'SCRIPT_NAME'}'>
							<input type='hidden' name='ACTION' value='' />
							<input type='image' alt='$Lang::tr{'abort'}' src='/images/dialog-error.png' />
						</form>
		</table>
END
		&Header::closebox();
		&Header::closebigbox();
		&Header::closepage();
		exit;
	}
} elsif ($pakfiresettings{'ACTION'} eq 'remove') {

	$pakfiresettings{'DELPAKS'} =~ s/\|/\ /g;
	if ("$pakfiresettings{'FORCE'}" eq "on") {
		my $command = "/usr/local/bin/pakfire remove --non-interactive --no-colors $pakfiresettings{'DELPAKS'} &>/dev/null &";
		system("$command");
		sleep(2);
	} else {
		&Header::openbox("100%", "center", "Abfrage");
  	my @output = `/usr/local/bin/pakfire resolvedeps --no-colors $pakfiresettings{'DELPAKS'}`;
		print <<END;
		<table><tr><td colspan='2'>$Lang::tr{'pakfire uninstall package'}.$pakfiresettings{'DELPAKS'}.$Lang::tr{'pakfire possible dependency'}
		<pre>		
END
		foreach (@output) {
			print "$_\n";
		}
		print <<END;
		</pre>
		<tr><td colspan='2'>$Lang::tr{'pakfire accept all'}
		<tr><td colspan='2'>&nbsp;
		<tr><td align='right'><form method='post' action='$ENV{'SCRIPT_NAME'}'>
							<input type='hidden' name='DELPAKS' value='$pakfiresettings{'DELPAKS'}' />
							<input type='hidden' name='FORCE' value='on' />
							<input type='hidden' name='ACTION' value='remove' />
							<input type='image' alt='$Lang::tr{'uninstall'}' src='/images/go-next.png' />
						</form>
				<td align='left'>
						<form method='post' action='$ENV{'SCRIPT_NAME'}'>
							<input type='hidden' name='ACTION' value='' />
							<input type='image' alt='$Lang::tr{'abort'}' src='/images/dialog-error.png' />
						</form>
		</table>
END
		&Header::closebox();
		&Header::closebigbox();
		&Header::closepage();
		exit;
	}

} elsif ($pakfiresettings{'ACTION'} eq 'update') {
	
	system("/usr/local/bin/pakfire update --force --no-colors");

} elsif ($pakfiresettings{'ACTION'} eq 'upgrade') {
	
	system("/usr/local/bin/pakfire upgrade -y --no-colors");
	
} elsif ($pakfiresettings{'ACTION'} eq "$Lang::tr{'save'}") {

	&General::writehash("${General::swroot}/pakfire/settings", \%pakfiresettings);

}

&General::readhash("${General::swroot}/pakfire/settings", \%pakfiresettings);

my %selected=();
my %checked=();

$checked{'AUTOUPDATE'}{'off'} = '';
$checked{'AUTOUPDATE'}{'on'} = '';
$checked{'AUTOUPDATE'}{$pakfiresettings{'AUTOUPDATE'}} = "checked='checked'";
$checked{'UUID'}{'off'} = '';
$checked{'UUID'}{'on'} = '';
$checked{'UUID'}{$pakfiresettings{'UUID'}} = "checked='checked'";

# DPC move error message to top so it is seen!
if ($errormessage) {
	&Header::openbox('100%', 'left', $Lang::tr{'error messages'});
	print "<font class='base'>$errormessage&nbsp;</font>\n";
	&Header::closebox();
}

my $return = `pidof pakfire`;
chomp($return);
if ($return) {
	&Header::openbox( 'Waiting', 1, "<meta http-equiv='refresh' content='5;'>" );
	print <<END;
	<table>
		<tr><td>
				<img src='/images/indicator.gif' alt='$Lang::tr{'aktiv'}' />&nbsp;
			<td>
				$Lang::tr{'pakfire working'}
		<tr><td colspan='2' align='center'>
			<form method='post' action='$ENV{'SCRIPT_NAME'}'>
				<input type='image' alt='$Lang::tr{'reload'}' src='/images/view-refresh.png' />
			</form>
		<tr><td colspan='2' align='left'><pre>
END
	my @output = `tail -20 /var/log/pakfire.log`;
	foreach (@output) {
		print "$_";
	}
	print <<END;
			</pre>
		</table>
END
	&Header::closebox();
	&Header::closebigbox();
	&Header::closepage();
	exit;
}

&Header::openbox("100%", "center", "Pakfire");

system("pakfire update &>dev/null");

print <<END;
	<table width='100%'>
		<tr><td bgcolor='$color{'color20'}' align="center"><b>$Lang::tr{'pakfire available addons'}</b></td><td bgcolor='$color{'color20'}'></td><td bgcolor='$color{'color20'}' align="center"><b>$Lang::tr{'pakfire installed addons'}</b>
		<tr><td width='40%' align="center">
			<form method='post' action='$ENV{'SCRIPT_NAME'}'>
				<select name="INSPAKS" size="10" multiple>
END
			&Pakfire::dblist("notinstalled", "forweb");
		
print <<END;
				</select>
		</td>
		<td width='20%' align="center">
				<input type='hidden' name='ACTION' value='install' />
				<input type='image' alt='$Lang::tr{'install'}' src='/images/list-add.png' />
			</form><br />
			
			<form method='post' action='$ENV{'SCRIPT_NAME'}'>
				<input type='hidden' name='ACTION' value='update' />
				<input type='submit' value='Liste aktualisieren' /><br />
			</form>
			
			<form method='post' action='$ENV{'SCRIPT_NAME'}'>
				<input type='hidden' name='ACTION' value='remove' />
				<input type='image' alt='$Lang::tr{'remove'}' src='/images/list-remove.png' />
		</td>
		<td width='40%' align="center">
			<select name="DELPAKS" size="10" multiple>
END

			&Pakfire::dblist("installed", "forweb");

print <<END;
		</select>
	</table></form>
	<br />
	<form method='post' action='$ENV{'SCRIPT_NAME'}'>
	<table width='100%'>
		<tr><td colspan='3' bgcolor='$color{'color20'}'><b>$Lang::tr{'pakfire updates'}</b></br>
		<tr><td width='20%'>&nbsp;<td width='60%' align='center'>
			<select name="UPDPAKS" size="5" disabled>
END

			&Pakfire::dblist("upgrade", "forweb");

print <<END;
			</select>
		<td width='20%' align='center' valign='middle'><input type='hidden' name='ACTION' value='upgrade' />
			<input type='image' alt='$Lang::tr{'upgrade'}' src='/images/document-save.png' />
	</table></form>
	<br />
	<form method='post' action='$ENV{'SCRIPT_NAME'}'>
		<table width='100%'>
			<tr><td colspan='4' bgcolor='$color{'color20'}'><b>$Lang::tr{'basic options'}</b></br>
			<tr><td width='40%' align="right">$Lang::tr{'pakfire update daily'}
					<td width='10%' align="left"><input type="checkbox" name="AUTOUPDATE" $checked{'AUTOUPDATE'}{'on'} />
					<td width='40%' align="right">$Lang::tr{'pakfire register'} 
					<td width='10%' align="left"><input type="checkbox" name="UUID" $checked{'UUID'}{'on'} />
			<tr><td width='100%' colspan="4" align="center"><input type="submit" name="ACTION" value="$Lang::tr{'save'}" />
		</table>
	</form>
END

&Header::closebox();
&Header::closebigbox();
&Header::closepage();
