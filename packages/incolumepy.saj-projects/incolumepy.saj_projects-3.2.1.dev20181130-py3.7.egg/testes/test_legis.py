import os
import shutil
import logging
import chardet
from collections import namedtuple
from unittest import TestCase, main
from incolumepy.saj_projects import legis, logger
from incolumepy.saj_projects.legis import Legis
from incolumepy.saj_projects.legis import BeautifulSoup
from unittest.mock import mock_open, patch, MagicMock, call, DEFAULT, Mock, sentinel
# from incolumepy.utils.decorators import time_it
# from contextlib import contextmanager
# from io import StringIO


class TestLegis(TestCase):
    def setUp(self):
        self.valores = namedtuple('teste', 'entrada saida')
        # caminho de gravação
        self.arquivos = {
            '/tmp/file.html': '/tmp/file.html',
            '/tmp/teste/file.txt': '/tmp/teste/',
            '~/tmp/file.txt': os.path.expanduser('~/tmp/'),
            '~/file.txt': os.path.expanduser('~/file.txt'),
            'teste/file.txt': 'teste/',
            'file.txt': 'file.txt'
        }
        self.leg = legis.Legis()
        self.soup1 = BeautifulSoup('<div><p><b><i>teste</i></b></p></div>', 'html5lib')
        self.soup2 = BeautifulSoup('''<head>
        <meta name="GENERATOR" content="Microsoft FrontPage 6.0">
        <title>L8666consol</title>
        </head>
        <body bgcolor="#FFFFFF">
        <div align="center"><center>
        <table border="0" cellpadding="0" cellspacing="0" width="70%">
        <tr>
        <td width="14%"><p align="center">
        <img src="../Brastra.gif" alt="Brastra.gif (4376 bytes)" width="74" height="82"></td>
        <td width="86%"><p align="center"><font color="#808000" face="Arial">
        <strong><big><big>Presidência da República</big></big><br>
        <big>Casa Civil<br>
        </big>Subchefia para Assuntos Jurídicos</strong></font></td>
        </tr>
        </table>
        </center></div>
        <p align="center">
        <a 
        href="http://legislacao.planalto.gov.br/legisla/legislacao.nsf/Viw_Identificacao/lei%208.666-1993?OpenDocument">
        <font face="Arial" color="#000080">
        <strong><small>LEI Nº 8.666, DE 21 DE JUNHO DE 1993</small></strong></font></a></p>
        <table border="0" width="100%" cellspacing="0" cellpadding="0"><tr>
        <td width="51%"><font face="Arial"><small><a href="L8666compilado.htm">Texto compilado</a></small><br>
        <a href="Mensagem_Veto/anterior_98/Vep335-L8666-93.pdf">
        <small>Mensagem de veto</small></a></font><p>
        <font face="Arial">
        <font size="2"><a href="../decreto/Antigos/D99658.htm">(Vide Decreto nº 99.658, de 1990)</a></font><br>
        <font size="2"><a href="../decreto/Antigos/D1054.htm">(Vide Decreto nº 1.054, de 1994)</a></font><br>
        <font size="2"><a href="../_Ato2007-2010/2010/Decreto/D7174.htm">(Vide Decreto nº 7.174, de 2010)</a></font>
        <br></font><font face="Arial" style="font-size: smaller">
        <a href="../_Ato2011-2014/2011/Mpv/544.htm#art15">
        (Vide Medida Provisória nº 544, de 2011)</a></font><font FACE="Arial" SIZE="2"><br>
        <span style="color:black">
        <a href="../_Ato2011-2014/2012/Lei/L12598.htm#art15">(Vide Lei nº 12.598, de 2012)</a></span></font></td>
        <td width="49%"><p ALIGN="JUSTIFY"><font face="Arial" color="#800000"><small>Regulamenta o
        art. 37, inciso XXI, da Constituição Federal, institui normas para licitações e
        contratos da Administração Pública e dá outras providências.</small></font></td>
        </tr></table><p ALIGN="JUSTIFY" style="text-indent: 30px"><small><font face="Arial">
        <strong>O&nbsp;PRESIDENTE DA REPÚBLICA </strong>Faço&nbsp;saber&nbsp;que&nbsp;o Congresso 
        Nacional decreta e eu sanciono&nbsp;a&nbsp;seguinte Lei:</font></small></p>
        <p ALIGN="CENTER"><font face="Arial"><small>Capítulo I</small><br>
        <small>DAS DISPOSIÇÕES GERAIS</small></font></p>
        <p ALIGN="CENTER"><b><font face="Arial"><small>Seção I</small><br>
        <small>Dos Princípios</small></font></b></p>

        <p ALIGN="JUSTIFY" style="text-indent: 30px"><small><font face="Arial">
        <a name="art1"></a>Art.&nbsp;1<sup><u>o</u></sup>&nbsp;&nbsp;Esta Lei estabelece normas gerais sobre
        licitações e contratos administrativos pertinentes a obras, serviços, inclusive de
        publicidade, compras, alienações e locações no âmbito dos Poderes da União, dos
        Estados, do Distrito Federal e dos Municípios.</font></small></p>
        <p ALIGN="JUSTIFY" style="text-indent: 30px"><small>
        <font face="Arial">
        Brasília,&nbsp;21&nbsp;de junho&nbsp;de 1993, 172<sup><u>o</u></sup> da Independência e 105
        <sup><u>o</u></sup> da República.</font></small></p>
        <p ALIGN="JUSTIFY"><font face="Arial"><small>ITAMAR FRANCO</small><br>
        <em><small>Rubens Ricupero</small><br>
        <small>Romildo Canhim</small></em></font></p>
        <p ALIGN="JUSTIFY"><font face="Arial" color="#FF0000"><small>Este texto não substitui o
        publicado no DOU de 22.6.1993, 
        <font color="#FF0000">republicado em 6.7.1994 e </font>
        <a href="1989_1994/RET/rlei-8666-93.pdf">
        <font color="#FF0000">retificado em&nbsp; 6.7.1994</font></a></small></font></p>
        <p align="center"><font color="#FF0000">*</font></p>''', 'html5lib')

    def tearDown(self):
        del self.leg
        del self.soup1
        for arquivo in self.arquivos.values():
            try:
                if os.path.exists(arquivo):
                    os.remove(arquivo)
                    logging.debug(f'removido: {arquivo}')
            except IsADirectoryError:
                shutil.rmtree(arquivo)
                logging.debug(f'removido: {arquivo}')
            except Exception as e:
                logging.debug(f'{arquivo}: {e}')

    def test_instance(self):
        self.assertTrue(isinstance(self.leg, legis.Legis))

    def test_link(self):
        e = '<link href="http://www.planalto.gov.br/ccivil_03/css/legis_3.css" rel="stylesheet" type="text/css"/>'
        e += '<link href="https://www.planalto.gov.br/ccivil_03/css/legis_3.css" rel="stylesheet" type="text/css"/>'
        self.assertEqual(type(self.leg.link_css()), BeautifulSoup)
        self.assertEqual(BeautifulSoup(e, 'html.parser'), self.leg.link_css())

    def test_header(self):
        h = '<header>'
        h += '<h1>Presidência da República</h1>'
        h += '<h2>Casa Civil</h2>'
        h += '<h3>Subchefia para Assuntos Jurídicos</h3>'
        h += '</header>'
        self.assertEqual(type(self.leg.header()), BeautifulSoup)
        self.assertEqual(BeautifulSoup(h, 'html.parser'), self.leg.header())

    def test_baseUrl(self):
        with self.assertRaisesRegex(ValueError, 'href nao definido'):
            self.leg.baseurl()
        href = "http://www.planalto.gov.br/ccivil_03/"
        result = '<base href="{}" target="{}"/>'
        self.assertEqual(type(self.leg.baseurl(href=href)), BeautifulSoup)

        result0 = BeautifulSoup(result.format(href, '_blank'), 'html.parser')
        self.assertEqual(result0, self.leg.baseurl(href=href, target='_blank'))

        result1 = BeautifulSoup(result.format(href, 'novajanela'), 'html.parser')
        self.assertEqual(result1, self.leg.baseurl(href=href, target='novajanela'))

    def test_nav(self):
        txt = '<nav><ul>'
        txt += '<input id="something" type="checkbox"/>'
        txt += '<li class="fixo"><a class="hide-action" href="#view">Texto compilado</a>'
        txt += '<a class="show-action" href="#">Texto atualizado</a></li>'
        txt += '<li class="fixo"><a class="textoimpressao" href="#textoimpressao">Texto para impressão</a></li>'
        txt += '<li class="fixo last"><label class="abrir" for="something">Ver mais..</label></li>'
        txt += '<li class="last"><label for="something">Ocultar</label></li><li class="fixo"></li>'
        txt += '<li class="fixo"></li><li class="fixo"></li></ul></nav>'

        result = BeautifulSoup(txt, 'html.parser')
        self.assertEqual(result, self.leg.nav())

    def test_comentario(self):
        from incolumepy.saj_projects.legis import Comment
        result1 = 'Comentario de teste.'
        op = self.leg.comment(result1)
        self.assertEqual(Comment, type(op))
        self.assertEqual(result1, op)

    def test_doctype(self):
        from incolumepy.saj_projects.legis import Doctype

        self.assertEqual(Doctype, type(self.leg.doctype()))

        self.assertEqual('html', self.leg.doctype())

        self.assertEqual('html', self.leg.doctype(default='html5'))

        r1 = 'HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"'
        self.assertEqual(r1, self.leg.doctype(default='html_401s'))
        self.assertEqual(r1, self.leg.doctype(r1))

        r2 = 'HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"'
        self.assertEqual(r2, self.leg.doctype(default='html_401t'))
        self.assertEqual(r2, self.leg.doctype(r2))

        r3 = 'HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd"'
        self.assertEqual(r3, self.leg.doctype(default='html_401f'))
        self.assertEqual(r3, self.leg.doctype(r3))

        r4 = 'html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"'
        self.assertEqual(r4, self.leg.doctype(default='xhtml_11'))
        self.assertEqual(r4, self.leg.doctype(r4))

        r5 = 'html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd"'
        self.assertEqual(r5, self.leg.doctype(default='xhtml_10f'))
        self.assertEqual(r5, self.leg.doctype(r5))

        r6 = 'html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" '
        r6 += '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"'
        self.assertEqual(r6, self.leg.doctype(default='xhtml_10t'))
        self.assertEqual(r6, self.leg.doctype(r6))

        r7 = 'html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"'
        self.assertEqual(r7, self.leg.doctype(default='xhtml_10s'))
        self.assertEqual(r7, self.leg.doctype(r7))

    def test_date_conv(self):
        print(self.leg.date_conv('de 8 de maio de 2018'))

        self.assertEqual('2018/05/08', self.leg.date_conv(' DE 8 DE MAIO DE 2018'))
        self.assertEqual('2018/06/01', self.leg.date_conv(' DE 1º DE JUNHO DE 2018'))
        self.assertEqual('2018/12/01', self.leg.date_conv(' DE 1º DE dezembro DE 2018'))

    def test_date_conv_raises(self):
        self.assertRaises(ValueError, self.leg.date_conv, ' de 29 de fevereiro de 1900')
        with self.assertRaisesRegex(ValueError,
                                    "de 29 de fevereiro de 1891' does not match format 'de %dº de %B de %Y'"):
            self.leg.date_conv(' de 29 de fevereiro de 1891')

    def test_dou(self):
        from bs4.element import Tag
        r1 = '<p class="dou">Este texto não substitui o publicado no D.O.U.</p>'
        expected = BeautifulSoup(r1, 'html.parser').p
        self.assertEqual(type(self.leg.dou()), Tag)
        self.assertTrue(isinstance(self.leg.dou(), Tag))
        self.assertEqual(expected, self.leg.dou())

    def test_locate_parent(self):
        from incolumepy.saj_projects.legis import Tag, NavigableString
        q = self.soup1.find_all(string='teste')
        self.assertEqual(q[0], 'teste')
        self.assertEqual(type(q[0]), NavigableString)
        self.assertEqual(q[0].name, None)
        self.assertEqual(q[0].parent.name, 'i')
        self.assertEqual(Tag, type(legis.locate_parent(soup=q[0], tag_name='div')))
        self.assertEqual('<div><p><b><i>teste</i></b></p></div>',
                         str(legis.locate_parent(soup=q[0], tag_name='div')))

        with self.assertRaisesRegex(AssertionError, 'Not instance bs4'):
            legis.locate_parent(soup='<div><p><b><i>teste</i></b></p></div>', tag_name='div')

    def test_change_parent0(self):
        s = BeautifulSoup('<div><span><b><i><u>oi</div>', 'html5lib')

        with self.assertRaisesRegex(TypeError, 'Soup must be instance bs4'):
            legis.change_parent(soup='<div>oi</div>', tag_name='div', new_tag_name='p')
            legis.change_parent(soup='oi', tag_name='div', new_tag_name='p')

        with self.assertRaisesRegex(ValueError, 'atributo tag_name deverá ser informado'):
            legis.change_parent(soup=s, new_tag_name='div')

        with self.assertRaisesRegex(ValueError, "atributo new_tag_name deverá ser informado"):
            legis.change_parent(soup=s, tag_name='div')

        a = legis.change_parent(soup=s.find(string='oi'), tag_name='div', new_tag_name='p')
        self.assertNotRegex(s.prettify(), 'div')

    def test_change_parent1(self):
        with self.assertRaises(TypeError):
            legis.change_parent(soup='<div>oi</div>', tag_name='div')

        q = self.soup1.find(string='teste')
        result = legis.change_parent(soup=q, tag_name='div', new_tag_name='blockquote')
        self.assertEqual('blockquote', result.name)
        self.assertNotRegex(self.soup1.prettify(), 'div')
        self.assertRegex(self.soup1.prettify(), 'blockquote')

    def test_check_parent(self):
        with self.assertRaisesRegex(AssertionError, 'Not instance bs4'):
            legis.check_parent(soup='<div>oi</div>', tag_name='div')

        q = self.soup1.find_all(string='teste')
        result = legis.check_parent(soup=q[0], tag_name='p', key='id', value='date')
        self.assertEqual('<p id="date"><b><i>teste</i></b></p>', str(result))
        self.assertEqual('date', self.soup1.p['id'])

    def test_save_html_file(self):
        # verificação dos parametros de entrada
        mock_save_html_file = Mock(spec=legis.save_html_file)
        mock_save_html_file(conteudo=self.soup1, filename='/tmp/file.html')
        esperado = call(conteudo=self.soup1, filename='/tmp/file.html')
        self.assertEqual(esperado, mock_save_html_file.call_args)

        texto = '<p>açaí é brasileiro!</p>'
        soup = BeautifulSoup(texto, 'html5lib')
        # test encoding ISO8859-1
        mock_save_html_file.return_value = soup.prettify(encoding='iso8859-1')
        self.assertRegex(r'ISO-8859-1', chardet.detect(mock_save_html_file('file')).get('encoding'))

        # test encoding utf-8
        mock_save_html_file.return_value = soup.prettify(encoding='utf-8')
        self.assertRegex(r'utf-8', chardet.detect(mock_save_html_file('file')).get('encoding'))

        mock_save_html_file.return_value = soup.prettify(encoding='iso8859-1')
        # verificação dos tipos de entrada
        with self.assertRaisesRegex(ValueError, '"conteudo" deve ser um código HTML de tipo "str"'):
            legis.save_html_file(conteudo=self.soup1, filename='/tmp/file.html')
            legis.save_html_file(conteudo=1, filename='/tmp/file.html')
            legis.save_html_file(conteudo=1.1, filename='/tmp/file.html')
            legis.save_html_file(conteudo=object(), filename='/tmp/file.html')
            legis.save_html_file(conteudo=object, filename='/tmp/file.html')

        with self.assertRaisesRegex(ValueError,'"filename" deve ser um caminho válido no sistemas de arquivo de tipo "str"'):
            legis.save_html_file(conteudo=self.soup1.prettify(), filename=object)
            legis.save_html_file(conteudo=self.soup1.prettify(), filename=object())
            legis.save_html_file(conteudo=self.soup1.prettify(), filename=1)
            legis.save_html_file(conteudo=self.soup1.prettify(), filename=1.1)
            legis.save_html_file(conteudo=self.soup1.prettify(), filename=self.soup1)

        ## caminhos inexistentes
        for arquivo in self.arquivos.keys():
            self.assertFalse(os.path.exists(arquivo))
            _, file = legis.save_html_file(self.soup1.prettify(), arquivo)
            logging.debug(f'{os.path.exists(file)}, {file}')
            self.assertTrue(os.path.exists(file))

    def test_presidente_identify(self):
        self.assertEqual('', legis.presidente_em_exercicio(soup='', json_file=''))

    def test_loc_epigrafe_lei(self):
        t = []
        v = self.valores

        t.append(v('''<p><a href="#"><b>LEI  Nº10.406,  DE  10  DE  JANEIRO  DE  2002.</b></a></p>''',''))
        t.append(v(
            '<p align="CENTER"><a href="#"><font face="Arial" color="#000080"><small><strong>LEI N<sup>o</sup> '
            '8.156, DE 28 DE DEZEMBRO DE1990.</strong></small></font></a></p>',
            ''))
        t.append(v('<p align="CENTER"><a href="#"><font color="#000080" face="Arial">'
                 '<small><strong>LEI N<sup>o</sup>10.406, DE 10 DE JANEIRO DE2002.</strong></small></font></a></p>',
                 ''))


        for elem in t:
            soup = BeautifulSoup(elem.entrada, 'html.parser')
            print(soup.prettify())
            legis.Legis.loc_epigrafe(soup)
            print(soup.prettify())
            self.assertIn('class="epigrafe"', str(soup))

    def test_president_exerc(self):
        def loc_president_exerc(*args, **kwargs):
            return legis.loc_president_exerc(*args, **kwargs)

        self.assertEqual([], loc_president_exerc(soup=self.soup1))
        self.assertRaisesRegex(AssertionError,
                               'Arquivo /home/brito/projetos/saj_projects/src/testes/data/base_presidentes.cvs indisponível',
                               loc_president_exerc, self.soup1,
                               '../data/base_presidentes.cvs')
        self.assertRaisesRegex(AssertionError,
                               '"soup" deverá ser instancia de bs4',
                               loc_president_exerc, '', '')
        self.assertEqual([], loc_president_exerc(soup=self.soup2))

        # self.assertEqual(['ITAMAR FRANCO'], legis.loc_president_exerc(soup=self.soup2))

    def test_loc_presidente_exercicio(self):
        self.assertEqual(['ITAMAR FRANCO'], legis.loc_presidente_exercicio(soup=self.soup2))

    def test_vice_identify(self):
        self.assertEqual([], legis.vice_identify(json_file='../../data/presidentes.json', ano='1993'))

    def test_loc_data_assinatura(self):
        datas_teste = [
            '<p>Brasília, 10 de janeiro de 2002; 181º da Independência e 114º da República.</p>',
            '<p>Brasília, 11 de janeiro de 1973; 152o da Independência e 85o da República.</p>',
            '<p>Brasília, 16 de março de 2015; 194o da Independência e 127o da República.</p>',
            '<p>Rio de Janeiro, 10 de janeiro de 1902; 18º da Independência e 1º da República.</p>',
            '<p> Senado Federal, 1º de dezembro de 1978; 99º da República e 99º da Independência.</p>'
        ]
        for item in datas_teste:
            s = BeautifulSoup(item, 'html.parser')
            Legis.loc_data_assinatura(soup=s)
            self.soup2.select('[class="data"]')
            logging.debug(s.prettify())
            self.assertEqual('p', s.p.name)
            self.assertEqual({'class': 'data'}, s.p.attrs)

    def test_loc_dou(self):
        self.assertEqual(None, Legis.loc_dou(soup=self.soup2))
        s = self.soup2.select('[class="dou"]')
        self.assertEqual('p', s[0].name)
        self.assertEqual({'align': 'JUSTIFY', 'class': 'dou'}, s[0].attrs)

    def test_charset(self):
        codigo_html = '''
                        <html lang="pt-br">
                        <head>
                        <link href="//s7.addthis.com/static/r07/widget/css/widget005.old.css" media="all" rel="stylesheet" type="text/css"/>
                        <link href="http://www.planalto.gov.br/ccivil_03/css/legis_3.css" rel="stylesheet" type="text/css"/>
                        <link href="https://www.planalto.gov.br/ccivil_03/css/legis_3.css" rel="stylesheet" type="text/css"/>
                        <meta content="pt-br" http-equiv="Content-Language"/>
                        <meta content="text/html; charset=UTF-8" http-equiv="Content-Type"/>
                        <meta charset="UTF-8"/>
                        '''

        soup_test = legis.Legis.charset()

        soup = BeautifulSoup(codigo_html, 'html.parser')

        metas = soup.find_all('meta')
        soup_test = soup.find_all('meta')

        self.assertEqual(soup.find_all('meta'), soup_test)

    def test_meta(self):
        from datetime import datetime as dt

        soup = legis.Legis.meta()
        names = {'numero': '', 'tipo': 'decreto', 'ano': dt.today().strftime('%Y'),
            'situacao': "vigente ou revogado", 'origem': 'Poder Executivo', 'chefe_de_governo': '',
            'referenda': '', 'correlacao': '', 'veto': '', 'dataassinatura': '', "generator_user": "@britodfbr",
            'publisher': 'Centro de Estudos Jurídicos da Presidência da República',
            "Copyright": 'PORTARIA Nº 1.492 DE 5/10/2011. http://www.planalto.gov.br/ccivil_03/Portaria/P1492-11-ccivil.htm',
            'fonte': '', 'presidente_em_exercicio': '', 'vice_presidente': '',
            'revised': dt.today().strftime('%Y-%m-%d %X %z'), 'description': 'Atos Normativos Federais do Governo Brasileiro',
            'keywords':'', 'robots': 'index, nofollow', 'googlebot': 'index, follow',
            'generator': 'Centro de Estudos Juridicos (CEJ/SAJ/CC/PR)',
            'reviewer': ''}

        cont = 0

        for i in names:
            metas = soup.select('meta[name]')
            self.assertIsNotNone(str(soup.find('meta', names[i])))
            self.assertEqual(str('<meta content="'+names[i]+'" name="'+i+'"/>'), str(metas[cont]))
            cont += 1


    def test_governo_ano(self):
        results = {
            '1889': 'MANUEL DEODORO DA FONSECA',
            1894: 'FLORIANO VIEIRA PEIXOTO',
            1908: 'AFONSO AUGUSTO MOREIRA PENA',
            '1905': 'FRANCISCO DE PAULA RODRIGUES ALVES',
            1955: 'JOÃO FERNANDES CAMPOS CAFÉ FILHO',
            '1956': 'NEREU DE OLIVEIRA RAMOS',
            1961: 'JUSCELINO KUBITSCHEK DE OLIVEIRA',
            '1978': 'ERNESTO BECKMANN GEISEL',
            1985: 'JOÃO BAPTISTA DE OLIVEIRA FIGUEIREDO',
            '2009': 'LUIZ INÁCIO LULA DA SILVA',
            '2011': 'DILMA VANA ROUSSEFF',
            '2018': 'MICHEL MIGUEL ELIAS TEMER LULIA',
            2019: 'JAIR MESSIAS BOLSONARO'
        }
        file = os.path.abspath("../../data/presidentes.json")
        assert open(file).read(), f"Arquivo {file} indisponível!"
        for item in results.keys():
            logging.debug(f"{type(item)} {item} {legis.governo_ano(json_file=file, ano=item)}")
            self.assertEqual(results[item], legis.governo_ano(json_file=file, ano=item))


    def test_loc_ministro(self):
        ministros = list(sorted((legis.loc_ministro(self.soup2))))

        #print(ministros)

        self.assertEqual('Romildo Canhim', ministros[0])
        self.assertEqual('Rubens Ricupero', ministros[1])

    def test_presidente_em_exercicio(self):
        raise NotImplementedError

    def test_file(self):
        raise NotImplementedError

    def test_replace_brastra(self):
        lista = [
            '''<table width="70%" cellspacing="0" cellpadding="0" border="0">
            <tbody><tr>
            <td width="14%">
            <p align="center"><font size="2">
            <img src="../../../_Ato2007-2010/2008/Decreto/Image4.gif" width="76" height="82"></font></p></td>
            <td width="86%"><p align="center"><font face="Arial" color="#808000"><strong><big><big>
            Presidência da República</big></big><br>
            <big>Casa Civil<br>
            </big>Subchefia para Assuntos Jurídicos</strong></font></p></td>
            </tr>
            </tbody></table>''',
            '''<table width="76%" cellspacing="0" cellpadding="0" border="0">
            <tbody><tr>
            <td width="14%"><p align="center">
            <img src="../decreto/Brastra.gif" alt="Brastra.gif (4376 bytes)" width="74" height="82"></p></td>
            <td width="86%"><p align="center"><font face="Arial" color="#808000"><strong><big><big>Presidência
            da República</big></big><br>
            <big>Casa Civil<br>
            </big>Subchefia para Assuntos Jurídicos</strong></font></p></td>
            </tr>
            </tbody></table>'''
        ]
        for item in lista:
            s = BeautifulSoup(item, 'html5lib')
            a = Legis(soup=s)
            a.replace_brastra(str_busca='Image4')
            a.replace_brastra()

            self.assertIn('Brasão da República do Brasil', s.prettify())
            self.assertEqual('Brasão da República do Brasil', s.img['alt'])
            self.assertRegex(s.img['src'], 'http://www.planalto.gov.br/ccivil_03/img/Brastra.png')

    def test_set_date(self):
        epigrafes = {
            '<p class="epigrafe">LEI Nº 7.565, DE 1º DE Maio DE 1956.</p>': '1956/05/01',
            '<p class="epigrafe">DECRETO-LEI Nº 7.565, DE 19 DE DEZEMBRO DE 1986</p>': '1986/12/19',
            '<p class="epigrafe">DECRETO-LEI Nº 7.565 - DE 19 DE DEZEMBRO DE 1986</p>': '1986/12/19',
            '<p class="epigrafe">DECRETO-LEI Nº 7.565 – DE 19 DE DEZEMBRO DE 1986</p>': '1986/12/19',
            '<p class="epigrafe">DECRETO-LEI Nº 7.565. DE 19 DE DEZEMBRO DE 1986</p>': '1986/12/19',
            '<p class="epigrafe">DECRETO Nº 7.565, DE 9 DE Junho DE 1978.</p>': '1978/06/09'
        }
        for item in epigrafes.keys():
            logging.debug(item)
            s = BeautifulSoup(item, 'html5lib')
            # print(s.prettify())
            o = Legis(soup=s)
            # print(o.soup.prettify())
            o.set_date()
            self.assertIsInstance(o.date, str)
            self.assertEqual(epigrafes[item], o.date)

    def test_set_tag_class(self):
        raise NotImplementedError

    def test_get_conteudo_url(self):
        url = 'http://www.planalto.gov.br/ccivil_03/_Ato2004-2006/2004/Lei/L10.973.htm'
        tag = '<p>áàãâäÁÀÃÂÄ! Çç éèêëÉÈẼÊË? íìîïÍÌĨÎÏ, óòõôöÓÒÕÔÖ; úùûüÚÙŨÛÜ.</p>'
        soup = BeautifulSoup(tag, 'html5lib')
        # print(soup.prettify(encoding='iso8859-1'))
        with patch.object(legis, 'get_conteudo_requests_url') as mock_requests:
            # verificação iso8859-1
            mock_requests.return_value = soup.prettify(encoding='iso8859-1')
            content = legis.get_conteudo_url(url)
            assert content == soup.prettify(encoding='iso8859-1')
            # verificação utf-8
            mock_requests.return_value = soup.prettify(encoding='utf-8')
            content = legis.get_conteudo_url(url)
            assert content == soup.prettify(encoding='utf-8')

        with patch.object(legis, 'get_conteudo_requests_url', side_effect=[ConnectionError]) as mock_requests:
            content = legis.get_conteudo_url(url)
            assert content == soup.prettify(encoding='iso8859-1')

    def test_get_conteudo_requests_url(self):
        url = 'http://www.planalto.gov.br/ccivil_03/_Ato2004-2006/2004/Lei/L10.973.htm'
        text = '<!DOCTYPE html><html><head></head><body><h1>Título</h1><p>Olá o amanhã é açaí áàâãõoóò</p></body></html>'
        soup = BeautifulSoup(text, 'html5lib')
        with patch.object(legis.requests, 'get') as get_mock:
            get_mock.return_value = mock_response = Mock()
            mock_response.content = soup.prettify(encoding='iso8859-1')
            content = legis.get_conteudo_requests_url(url)
            assert content, "Conteudo indisponível"
            self.assertRegex(chardet.detect(content).get('encoding'), 'ISO-8859-\d')

        with patch.object(legis.requests, 'get') as get_mock:
            get_mock.return_value = mock_response = Mock()
            mock_response.content = soup.prettify(encoding='utf8')
            content = legis.get_conteudo_requests_url(url)
            assert content, "Conteudo indisponível"
            self.assertEqual(chardet.detect(content).get('encoding'), 'utf-8')

    def test_get_conteudo_selenium_url(self):
        url = 'http://www.planalto.gov.br/ccivil_03/_Ato2004-2006/2004/Lei/L10.973.htm'
        conteudo = legis.get_conteudo_selenium_url(url)
        assert 'L10973' in conteudo, "Conteúdo legis.get_conteudo_selenium_url inválido."

    def test_definir_titulos(self):
        raise NotImplementedError

    def test_replaceLineThrough2Del(self):
        raise NotImplementedError

    def test_get_conteudo_file(self):
        raise NotImplementedError

    def test_get_conteudo(self):
        # raise NotImplementedError
        tag = '<p>áàãâäÁÀÃÂÄ! Çç éèêëÉÈẼÊË? íìîïÍÌĨÎÏ, óòõôöÓÒÕÔÖ; úùûüÚÙŨÛÜ.</p>'
        soup = BeautifulSoup(tag, 'html5lib')

        with self.assertRaises(Exception):
            # exceptions filename invalido
            legis.get_conteudo(filename='')
            # exception url invalida
            legis.get_conteudo(url=None)

        with patch.object(legis, 'get_conteudo_file') as mock_get_conteudo_file:
            mock_get_conteudo_file.return_value = soup.prettify(encoding='iso8859-1')
            content = legis.get_conteudo(filename='file_mock')
            assert content, "Conteúdo iso8859-1 não apresentado"
            # teste encode iso8859-1
            self.assertRegex(chardet.detect(content).get('encoding'), 'ISO-8859-')

            mock_get_conteudo_file.return_value = soup.prettify(encoding='utf-8')
            content = legis.get_conteudo(filename='file_mock')
            assert content, "Conteúdo utf-8 não apresentado"
            self.assertRegex(chardet.detect(content).get('encoding'), 'utf-8')

        with patch.object(legis, 'get_conteudo_url') as mock_get_conteudo_url:
            mock_get_conteudo_url.return_value = soup.prettify(encoding='iso8859-1')
            content = legis.get_conteudo(url='url')
            assert content, "Conteúdo não apresentado"

            # test encode iso8859-1
            self.assertRegex(chardet.detect(content).get('encoding'), 'ISO-8859-')
            mock_get_conteudo_url.return_value = soup.prettify(encoding='utf-8')
            content = legis.get_conteudo(url='url')
            assert content, "Conteúdo não apresentado"

            # test encode utf-8
            self.assertRegex(chardet.detect(content).get('encoding'), 'utf-8')

    def test_get_soup_from_file(self):
        a = Legis()
        with patch('builtins.open', mock_open(read_data='<br />')):
            a.file = 'file.html'

            # html.parser
            a.get_soup_from_file()
            self.assertIsInstance(a.soup, BeautifulSoup)
            self.assertEqual('<br/>', str(a.soup))

            # lxml
            a.get_soup_from_file(parser_index=1)
            self.assertIsInstance(a.soup, BeautifulSoup)
            self.assertEqual('<html><body><br/></body></html>', str(a.soup))

            # 'lxml-xml'
            a.get_soup_from_file(parser_index=2)
            self.assertIsInstance(a.soup, BeautifulSoup)
            self.assertEqual('<?xml version="1.0" encoding="utf-8"?>\n<br/>', str(a.soup))

            # 'xml'
            a.get_soup_from_file(parser_index=3)
            self.assertIsInstance(a.soup, BeautifulSoup)
            self.assertEqual('<?xml version="1.0" encoding="utf-8"?>\n<br/>', str(a.soup))

            # 'html5lib'
            a.get_soup_from_file(parser_index=4)
            self.assertIsInstance(a.soup, BeautifulSoup)
            self.assertEqual('<html><head></head><body><br/></body></html>', str(a.soup))

    def test_replace_tag(self):
        codigo_html = '''
                        <html lang="pt-br">
                        <head>
                        <link href="//s7.addthis.com/static/r07/widget/css/widget005.old.css" media="all" rel="stylesheet" type="text/css"/>
                        <link href="http://www.planalto.gov.br/ccivil_03/css/legis_3.css" rel="stylesheet" type="text/css"/>
                        <link href="https://www.planalto.gov.br/ccivil_03/css/legis_3.css" rel="stylesheet" type="text/css"/>
                        <meta content="pt-br" http-equiv="Content-Language"/>
                        <meta content="text/html; charset=UTF-8" http-equiv="Content-Type"/>
                        <meta charset="UTF-8"/>
                        </head>
                        </html>
                    '''
        resultado = '''
                        <html lang="pt-br">
                        <head>
                        <link href="//s7.addthis.com/static/r07/widget/css/widget005.old.css" media="all" rel="stylesheet" type="text/css"/>
                        <link href="http://www.planalto.gov.br/ccivil_03/css/legis_3.css" rel="stylesheet" type="text/css"/>
                        <link href="https://www.planalto.gov.br/ccivil_03/css/legis_3.css" rel="stylesheet" type="text/css"/>
                        <p content="pt-br" http-equiv="Content-Language"/>
                        <p content="text/html; charset=UTF-8" http-equiv="Content-Type"/>
                        <p charset="UTF-8"/>
                        </head>
                        </html>
                    '''
        soup = BeautifulSoup(codigo_html, 'html.parser')

        legis.Legis.replace_tag(soup, 'meta', 'p')
        self.assertEqual(soup, BeautifulSoup(resultado, 'html.parser'))

    def test_extract_soup_set_tag_class(self):
        raise NotImplementedError

    def test_acrescentado(self):
        raise NotImplementedError

    def test_iconv(self):
        mock_iconv = Mock(spec=legis.iconv)
        content = "<h1> Título</h1> <p>á à é í ó ò ü ú açaí </p>"
        soup = BeautifulSoup(content, 'html5lib')

        mockFile = MagicMock(return_value=soup.prettify(encoding='utf-8'))

        assert os.path.exists(mockFile), "Arquivo Indisponível"
        # assert False, type(mockFile)

        self.assertIn('utf-8', chardet.detect(mockFile.return_value).values())
        self.assertEqual('utf-8', chardet.detect(mockFile.return_value)['encoding'])
        result = mock_iconv(filein=mockFile, encode_in='utf-8', encode_out='iso8859-1',fileout=None)

        self.assertEqual([call(encode_in='utf-8', encode_out='iso8859-1',
                              filein=mockFile, fileout=None)], mock_iconv.mock_calls)

        with patch('builtins.open', mockFile) as file:
            mock_iconv(file, encode_in='utf-8', encode_out='iso8859-1')


        # print(soup)
        #print(f'>>{result}')
        # print(mockFile.return_value)
        # self.assertIn('iso8859-1', chardet.detect(mockFile.return_value).values())
        # self.assertEqual('iso8859-1', chardet.detect(mockFile.return_value)['encoding'])


if __name__ == '__main__':
    main()
