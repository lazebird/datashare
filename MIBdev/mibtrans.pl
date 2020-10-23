#!/usr/bin/perl
use strict;
use warnings;

our $debug = 0;

sub header_replace {
    my $line = $_[0];
    if ( $line =~ /^#include <net-snmp\/net-snmp-config\.h>/ ) {
        $line = "";
    }
    if ( $line =~ /^#include <net-snmp\/net-snmp-includes\.h>/ ) {
        $line = "";
    }
    if ( $line =~ /^#include <net-snmp\/agent\/net-snmp-agent-includes\.h>/ ) {
        $line = "#include \"pal.h\"\n#include \"lib.h\"\n#include <asn1.h>\n#include \"snmp.h\"\n";
    }
    return $line;
}

sub var_xxx_func_replace {
    my $line = $_[0];
    if ( $line =~ /^\s*WriteMethod \*\*write_method\)/ ) {
        $line =~ s/WriteMethod \*\*write_method\)/WriteMethod **write_method, u_int32_t vr_id)/g;
    }
    return $line;
}

sub write_xxx_func_replace {
    my $line = $_[0];
    if ( $line =~ /^\s*size_t   name_len\)/ ) {
        $line =~ s/size_t   name_len\)/size_t   name_len, struct variable *vp, u_int32_t vr_id)/g;
    }
    return $line;
}

our $validation_flag = 0;
sub validation_del { # header_generic/header_simple_table
    my $line = $_[0];
    if ( $line =~ /if \(header_/ ) {
        $debug && print "start validation\@$line\n";
        $line = "";
        $validation_flag = 1;
    } elsif ( $line =~ /return NULL;/ && $validation_flag == 1) {
        $debug && print "end validation\@$line\n";
        $line = "";
        $validation_flag = 0;
    } elsif ($validation_flag == 1) {
        $line = "";
    }
    return $line;
}

our $comment_flag = 0;
our $commentinfo = "";
sub comment_block_del { # header_generic/header_simple_table
    my $line = $_[0];
    if ( $line =~ /^\s*\/\*/ && $line !~ /\*\// ) {
        $debug && print "start comment\@$line\n";
        $commentinfo = $line;
        $line = "";
        $comment_flag = 1;
    }
    if ( $line =~ /\*\// && $comment_flag == 1) {
        $debug && print "end comment\@$line\n";
        $commentinfo .= $line;
        $line = "";
        $comment_flag = 0;
        if ($commentinfo !~ "This assumes that the table is a 'simple' table.") {
            $line = $commentinfo;
        }
    } elsif ($comment_flag == 1) {
        $commentinfo .= $line;
        $line = "";
    }
    return $line;
}

sub extra_replace {
    my $line = $_[0];
    if ( $line =~ /REGISTER_MIB\(/ ) {
        $line =~ s/REGISTER_MIB\(/REGISTER_MIB\(ZG, /g;
    }
    if ( $line =~ /^\s*DEBUGMSGTL/ ) {
        $line = "";
    }
    if ( $line =~ /^\s*ERROR_MSG\(""\);/ ) {
        $line =~ s/ERROR_MSG\(""\)/break/g;
    }
    if ( $line =~ /^\s*case FREE:/ ) {
        $line =~ s/case FREE:/case FREE_DEL:/g;
    }
    if ( $line =~ /NETSNMP_OLDAPI_/ ) {
        $line =~ s/NETSNMP_OLDAPI_//g;
    }
    if ( $line =~ /variable4/ ) {
        $line =~ s/variable4/variable/g;
    }
    return $line;
}

#get progname/ver value from .h file, and insert more include files
sub proc_file {
    my $infile = $_[0];
    my $outfile = $_[1];
    open FILE_IN,  '<',  $infile or die "$infile open failed.\r\n";
    open FILE_OUT, '>', $outfile or die "$outfile open failed.\r\n";
    while (<FILE_IN>) {
        my $line = $_;
        my $result = $line;
        $result = header_replace($line);
        if ($result ne $line) {
            print FILE_OUT $result;
            next;
        }
        $result = var_xxx_func_replace($line);
        if ($result ne $line) {
            print FILE_OUT $result;
            next;
        }
        $result = write_xxx_func_replace($line);
        if ($result ne $line) {
            print FILE_OUT $result;
            next;
        }
        $result = validation_del($line);
        if ($result ne $line) {
            print FILE_OUT $result;
            next;
        }
        $result = comment_block_del($line);
        if ($result ne $line) {
            print FILE_OUT $result;
            next;
        }
        $result = extra_replace($line);
        if ($result ne $line) {
            print FILE_OUT $result;
            next;
        }
        print FILE_OUT $result;
    }
    close FILE_IN;
    close FILE_OUT;
}

sub usage {
    print "Usage: $_[0] {source-file-path} [destination-file-path]\n";
}

my $srcfile=$ARGV[0];
my $dstfile=$ARGV[1];
if(!defined($srcfile)) {
    usage($0);
    exit(0);
}
if(!defined($dstfile)) {
    $dstfile = $srcfile.".mod";
}
proc_file($srcfile, $dstfile);
