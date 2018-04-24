import re

class GrammarRules:
    def __init__(self):
        self.verbs = {
            'comer' : '^com(o|e[sn]?|mos)$',
            'ir' : '^(v(oy|a(mos|[sn])?)$',
            'escribir' : '^escrib(o|e[sn]?|imos)$',
            'tomar' : '^tom(o|a([sn]|mos)?)$',
            'conocer' : '^cono(zco|ce([sn]|mos)?)$',
            'jugar' : '^ju(gamos|eg[oa][sn]?)$',
            'volver' : '^v(olvemos|uelv(o|e[sn]?))$',
            'leer' : '^le(o|e(mos|[sn])?)$',
            'estudiar' : '^estudi(o|a(mos|[sn])?)$',
            'recorrer' : '^recorr(o|[ae](mos|[sn])?)$'
        }

    def isVerb(self):
        return re.compile('^(\w+[ae]r|\w*ir|\w+(mos|is|[sn]|ron|[ni]do))$')

    def isArticle(self):
        return re.compile('^([d]?el|la[s]?|lo[s]?|un(a[s]?|os)?|al)$')

    def isAdjetive(self):
        return re.compile('^(simple|mayor|\w{3,}[^n]d[oa][s]?|\w+ble|(generos|antigu|cuant|blanc|negr|baj|alt|medi)'+
                          '[ao][s]?|tan|mas|dulce|cada|\w+isim[oa]|a(ca|hi|quel(l[oa][s]?)?))$')

    def isSustantive(self):
        return re.compile('^(\w+(ac[oa]|ach([oa]|uelo)|ot[ea]|(ich|ecez|ez)uelo|or(ri[ao]|r[oa]|i[oa])|'+
                          '(uz|asc|astr|ang|[au]j|[at|[z]?uel|uch)[oa])|\w{3,}(es[a]?|[mt]an[a]?|[iea]n[oa])[s]?)$')

    def isPreposition(self):
        return re.compile('^(segun|tras|(par|vi)?a|ha(cia|sta)|de(sde)?|(dur|medi)?ante|en(tre)?|so(bre)?|con(tra)?|por|sin)$')

    def isAdverb(self):
        return re.compile('^(\w+mente|si|no|mu(y|cho)|ade(mas|lante)|poco|hoy|ayer|manana|ahora|despues|aqui|encima|'+
                          'delante|debajo|tam(bien|poco)|jamaz|nunca|siempre)$')

    def isPronom(self):
        return re.compile('^(donde|(aqu)?el((lo|la)[s]?)?|l[aeo][s]?|yo|[tsc]u(y[oa][s]?)?|[vn]os(otr[oa]s)?|[vn]uestr[oa][s]?|'+
                          '(cual|quien)(quier[a]?|(es)?)?|alg(o|uien|un[oa]?)|si|(es[t]?|vari|much)(e|[oa][s]?)|es([ao][s]?|e)?|'+
                          'con[mst]igo|bastante[s]?|cardinal(es)?|(mi|otr)[ao][s]?|m[ie]|t[eiu]|ningun[oa]?|os|otr[oa][s]?|nadie)$')

    def getVerb(self, text):
        for expr, verb in self.verbs.iteritems():
            eval = re.compile(expr)
            if eval.match(text):
                return verb

        return None