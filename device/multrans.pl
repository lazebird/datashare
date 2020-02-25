#!/usr/bin/perl

my $srcfile="picker.txt";
my $transfile="trans.txt";
my $outputfile="table.json";
my $fist_flag=1;

open(FSRC, "<$srcfile") or die "$srcfile open failed: $!.";
open(FTRANS, "<$transfile") or die "$transfile open failed: $!.";
open(FOUT, ">$outputfile") or die "$outputfile open failed: $!.";

print FOUT "{\n";
while(<FSRC>) {
    my $src_str=($_);
    my $trans_str=<FTRANS>;
    chomp($src_str);
    chomp($trans_str);
    $trans_str=~ s/“//g; # remove extra quotation marks
    $trans_str=~ s/”//g; # remove extra quotation marks
    $src_str=~ s/[\[\]]/&quot;/g; # restore [] to &quot;
    $trans_str=~ s/[\[\]]/&quot;/g; # restore [] to &quot;
    if ($fist_flag == 1) {
        print FOUT "\t\"$src_str\": \"$trans_str\"";
        $fist_flag = 0;
    } else {
        print FOUT ",\n\t\"$src_str\": \"$trans_str\"";
    }
}
print FOUT "\n}\n";

close(FSRC);
close(FTRANS);
close(FOUT);
