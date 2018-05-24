#!/usr/bin/perl

sub getText {
	my ($url) = @_;
	chomp $url;
	my @text = qx{sh loadFromWeb2.sh $url};
	return @text
}


sub extract {
	my ($pron, @text) = @_;
	my $txt = join("\n", @text);
	my @verb = ();
	
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

	@text = getText($url);
	@yo = extract('yo',@text);
	@tu = extract('tu',@text);
	print "yo:\n".join("|",@yo)."\n";
	print "tu:\n".join("|",@tu)."\n";
}

my ($verb) = @ARGV;
chomp $verb;

Main ($verb);
