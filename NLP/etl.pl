#!/usr/bin/perl

sub getText {
	my ($url) = @_;
	chomp $url;
	my @text = qx{sh loadFromWeb2.sh $url};
	return @text
}


sub extract {
	my ($pron, $txt) = @_;
	my @verb;
	# mas pruebas, hacer en: https://regexr.com/
	for ($txt =~ /(presente|imperfecto( \(2\))?|futuro|condicional|simple)\n(\s|\w|[\(\)])+\($pron\)\s*(\w+)|imperativo\n(\s|\w|[\(\)])+\s(\w+)\s+\($pron\)/g) {
		s/(presente|imperfecto( \(2\))?|\(2\)|futuro|condicional|simple|imperativo)//;
		s/\W//;
		push(@verb,$_) if($_ =~ /\w+/);
	}
	
	return @verb;
}

sub Main {
	my ($verb) = @_;
	my $url = "http://conjugador.reverso.net/conjugacion-espanol.html?verb=$verb";

	my @text = getText($url);
	my $txt = join("\n", @text);
	$txt =~ s/(presente|preterito|futuro|condicional|imperativo|subjuntivo)/\(. . .\)\n $1/g;
	$txt =~ s/el ella ud[.]/el_la/g;
	$txt =~ s/ellos ellas uds[.]/elloas_uds/g;
	#print "$txt\n";
	
	my @yo = extract('yo',$txt);
	my @tu = extract('tu',$txt);
	my @el_la = extract('el_la',$txt);
	my @nos = extract('nosotros',$txt);
	my @uds = extract('vosotros',$txt);
	my @ellos = extract('elloas_uds',$txt);
	
	my @ip = ($yo[0],$tu[0],$el_la[0],$nos[0],$uds[0],@ellos[0]);
	my @ipi = ($yo[1],$tu[1],$el_la[1],$nos[1],$uds[1],@ellos[1]);
	my @if = ($yo[2],$tu[2],$el_la[2],$nos[2],$uds[2],@ellos[2]);
	
	#TODO /(infinitivo|gerundio|participio pasado)\s+(\w+)\s+/g	
	
	print "\"ip\" : \"".join("|",@ip)."\",\n";
	print "\"ipi\" : \"".join("|",@ipi)."\",\n";
	print "\"if\" : \"".join("|",@if)."\",\n";
	print "\"yo\" : \"".join("|",@yo)."\",\n";
	print "\"tu\" : \"".join("|",@tu)."\",\n";
	print "\"el_la\" : \"".join("|",@el_la)."\",\n";
	print "\"nos\" : \"".join("|",@nos)."\",\n";
	print "\"uds\" : \"".join("|",@uds)."\",\n";
	print "\"ellos\" : \"".join("|",@ellos)."\"\n";
}

my ($verb) = @ARGV;
chomp $verb;

Main ($verb);
