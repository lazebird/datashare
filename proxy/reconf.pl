#!/usr/bin/perl

use strict;

my $filename=$ARGV[0] ? $ARGV[0] : "config.yml";

open F1, '<', $filename or die $filename . " open failed.\n";
my @lines = <F1>;
close F1;
my $str = join "", @lines;
# allow lan
$str =~ s/allow-lan: false/allow-lan: true/mg;
# use auto group instead
$str =~ s/name: Proxy\n  type: select/name: Proxy\n  type: url-test\n  url: http:\/\/www\.gstatic\.com\/generate_204\n  interval: 300/smg;    # about perl multi-line match, refer to zebos/script/rpc*_mod.pl

open F2, '>', $filename or die $filename . " open failed.\n";
print F2 $str;
close F2;
