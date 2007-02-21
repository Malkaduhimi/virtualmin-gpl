#!/usr/local/bin/perl
# Switch the login to a domain's admin

require './virtual-server-lib.pl';
&ReadParse();
$d = &get_domain($in{'dom'});
&can_edit_domain($d) || &error($text{'edit_ecannot'});
&can_switch_user($d) || &error($text{'switch_ecannot'});

if ($in{'admin'}) {
	# Switch is to an extra admin .. make sure he exists
	&can_edit_admins($d) || &error($text{'admins_ecannot'});
	@admins = &list_extra_admins($d);
	($admin) = grep { $_->{'name'} eq $in{'admin'} } @admins;
	$admin || &error($text{'switch_eadmin'});
	$user = $admin->{'name'};
	}
else {
	# To domain owner
	$user = $d->{'user'};
	}

&require_acl();
&get_miniserv_config(\%miniserv);
&acl::open_session_db(\%miniserv);
($olduser, $oldtime) = split(/\s+/, $acl::sessiondb{$main::session_id});
$olduser || &error($acl::text{'switch_eold'});
$acl::sessiondb{$main::session_id} = "$user $oldtime $ENV{'REMOTE_ADDR'}";
dbmclose(%acl::sessiondb);
&reload_miniserv();
if ($in{'admin'}) {
	&webmin_log("switch", "admin", $user);
	}
else {
	&webmin_log("switch", "domain", $d->{'dom'}, $d);
	}
&redirect("/");

