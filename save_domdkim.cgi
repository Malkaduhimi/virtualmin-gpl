#!/usr/local/bin/perl
# Save the DKIM key for a virtual server

require './virtual-server-lib.pl';
&ReadParse();
&error_setup($text{'domdkim_err'});
$d = &get_domain($in{'dom'});
&can_edit_domain($d) && &can_edit_mail() || &error($text{'edit_ecannot'});

# Validate inputs
if (!$in{'key_def'}) {
	$in{'key'} =~ s/\r//g;
	$err = &validate_cert_format($in{'key'}, 'key');
	&error($err) if ($err);
	}

&ui_print_unbuffered_header(&domain_in($d), $text{'mail_title'}, "");

# Update the key
# XXX print stuff
$err = &save_domain_dkim_key($d, $in{'key_def'} ? undef : $in{'key'});
&save_domain($d);
&run_post_actions();

# All done
&webmin_log("domdkim", "domain", $d->{'dom'});
&ui_print_footer(&domain_footer_link($d),
		 "", $text{'index_return'});
