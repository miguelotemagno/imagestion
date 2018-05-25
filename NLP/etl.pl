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

sub extract2 {
	my ($txt) = @_;
	my @verb;
	# mas pruebas, hacer en: https://regexr.com/
	for ($txt =~ /(infinitivo|gerundio|participio pasado)\s+(\w+)\s+/g) {
		s/((infinitivo|gerundio|participio pasado))//;
		s/\W//;
		s/compuesto//;
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
	
	my $YO = join("|",@yo);
	my $TU = join("|",@tu);
	my $EL_LA = join("|",@el_la);
	my $NOS = join("|",@nos);
	my $UDS = join("|",@uds);
	my $ELLOS = join("|",@ellos);
	
	my @ip = (shift(@yo), shift(@tu), shift(@el_la), shift(@nos), shift(@uds), shift(@ellos));
	my @ipi = (shift(@yo), shift(@tu), shift(@el_la), shift(@nos), shift(@uds), shift(@ellos));
	my @if = (shift(@yo), shift(@tu), shift(@el_la), shift(@nos), shift(@uds), shift(@ellos));
	my @ic = (shift(@yo), shift(@tu), shift(@el_la), shift(@nos), shift(@uds), shift(@ellos));
	my @ipps = (shift(@yo), shift(@tu), shift(@el_la), shift(@nos), shift(@uds), shift(@ellos));
	
	my @sf = (pop(@yo), pop(@tu), pop(@el_la), pop(@nos), pop(@uds), pop(@ellos));
	my @spi2 = (pop(@yo), pop(@tu), pop(@el_la), pop(@nos), pop(@uds), pop(@ellos));
	my @spi = (pop(@yo), pop(@tu), pop(@el_la), pop(@nos), pop(@uds), pop(@ellos));
	my @sp = (pop(@yo), pop(@tu), pop(@el_la), pop(@nos), pop(@uds), pop(@ellos));
	
	my @i = (pop(@yo), pop(@tu), pop(@el_la), pop(@nos), pop(@uds), pop(@ellos));
	
	my $IP = join("|",@ip);
	my $IPI = join("|",@ipi);
	my $IF = join("|",@if);
	my $IC = join("|",@ic);
	my $I = join("|",@i);
	my $IPPS = join("|",@ipps);
	my $SF = join("|",@sf);
	my $SPI2 = join("|",@spi2);
	my $SPI = join("|",@spi);
	my $SP = join("|",@sp);
	
	#TODO /(infinitivo|gerundio|participio pasado)\s+(\w+)\s+/g	
	my @igp = extract2($txt);
	my ($ger,$par,$inf) = @igp;
	
	print qq{"inf"   : "$inf",\n};
	print qq{"ger"   : "$ger",\n};
	print qq{"par"   : "$par",\n};

	print qq{"ipi"   : "$IPI",\n};
	print qq{"if"    : "$IF",\n};
	print qq{"ic"    : "$IC",\n};
	print qq{"ipps"  : "$IPPS",\n};

	print qq{"i"     : "$I",\n};

	print qq{"sp"    : "$SP",\n};
	print qq{"spi"   : "$SPI",\n};
	print qq{"spi2"  : "$SPI2",\n};
	print qq{"sf"    : "$SF",\n};
	
	print qq{"yo"    : "$YO",\n};
	print qq{"tu"    : "$TU",\n};
	print qq{"el_la" : "$EL_LA",\n};
	print qq{"nos"   : "$NOS",\n};
	print qq{"uds"   : "$UDS",\n};
	print qq{"ellos" : "$ELLOS"\n};
}

my ($verb) = @ARGV;
chomp $verb;

Main ($verb);
