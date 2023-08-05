import inspect
import os
import pandas as pd
import sys
from collections import OrderedDict
from incolumepy.utils.files import realfilename
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

try:
    import src.incolumepy.saj_projects.legis as legis
    from src.incolumepy.saj_projects import logger
except ModuleNotFoundError:
    import incolumepy.saj_projects.legis as legis
    from incolumepy.saj_projects import logger


def __lista_atos_xlsx_todataframe(xlsx_file='../../../data/DECRETOS_REVOGADOS_COM_LINK_VAZIO.xlsx',
                                  columns: list=['nome', 'data', 'ementa', 'total'], sheet_name=0):
    '''

    :param xlsx_file: xlsx xlsx_file name
    :param columns: title of columns sheet
    :param sheet_name: sheet position or name sheet
    :return: pandas.DataFrame
    '''
    excel_file = os.path.abspath(os.path.join(os.path.dirname(__file__), *xlsx_file.split(os.sep)))
    assert os.path.exists(excel_file), f"Arquivo {excel_file} indisponível."
    dataframe = pd.read_excel(excel_file, sheet_name=sheet_name, names=columns)

    logger.debug(type(dataframe))
    result = dataframe.dropna(subset=['nome', 'data'], how='all')
    result.to_csv('/tmp/asdfasdfasdfasdfadf.csv')
    return result


def listar_atos_por_ano(ano: str='1985',
                        df: pd.DataFrame=__lista_atos_xlsx_todataframe,
                        dir_output: str=None, **kwargs) -> pd.DataFrame:
    '''
    Gera um DataFrame a partir do resultado lista_atos_xlsx_todataframe
    :param ano: str
    :return: pandas.DataFrame
    '''
    if dir_output:
        filename = os.path.join(os.path.abspath(os.sep), *dir_output.split(os.sep), f'lista-{ano}-0.csv')
    else:
        filename = os.path.join(os.path.abspath(os.sep), 'tmp', inspect.stack()[0][3], f'lista-{ano}-0.csv')

    dict_num_ano = OrderedDict()

    df = __lista_atos_xlsx_todataframe(sheet_name=ano, **kwargs)
    df['NUM'], df['ANO'] = df.nome.str.split('/').str

    # remove ponto de milhar
    df['NUM'] = df.NUM.str.replace('.', '')  # modo lento

    # acrescenta num no dicionário e remove string 'DEC ' no inicio do numero
    dict_num_ano['NUM'] = [x[4:] for x in df.NUM]  # rapido

    # acrescenta ano no dicionário
    dict_num_ano['ANO'] = [x for x in df.ANO]

    df = pd.DataFrame(dict_num_ano)
    df.to_csv(realfilename(filename), index=False)
    return df


def relatorio_progresso(csv_file_0: str=None, csv_file: str = None, outputfile=None, ano='1975', **kwargs)->bool:
    #csv_file = os.path.abspath(os.path.join(os.path.dirname(__file__), *csv_file.split(os.sep)))
    assert os.path.exists(csv_file), f"Arquivo inexistente: {csv_file}"
    assert os.path.exists(csv_file_0), f"Arquivo inexistente: {csv_file_0}"
    logger.debug(csv_file)

    if csv_file_0:
        df = pd.read_csv(csv_file_0)
        df.columns = df.columns.str.lower()
        # df.sort_values(by='num', ascending=False)
    else:
        df = listar_atos_por_ano(ano, **kwargs)
        df.columns = df.columns.str.lower()

    df1 = pd.read_csv(csv_file)
    df1.columns = df1.columns.str.lower()
    df1 = df1.sort_values(by='num', ascending=False)

    df.ano = df.ano.astype('int64')
    df.num = df.num.astype('int64')
    df1.ano = df1.ano.astype('int64')
    df1.num = df1.num.astype('int64')

    df2 = df.merge(df1, left_on=['num', 'ano'], right_on=['num', 'ano'], how='outer', sort=False)
    if not outputfile:
        outputfile = realfilename(f'/tmp/teste_{inspect.stack()[0][3]}.csv')
    logger.debug(f'outputfile: {outputfile}')
    df2.to_csv(outputfile, index=False)
    return True


def query_ato_num_ano(num: int=90786,
                      ano: int=1985,
                      alias: str = 'dec',
                      url_consulta: str='http://legis.senado.leg.br/sicon/#/basica',
                      firefoxbin: str = None):
    pkg = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src', 'incolumepy', 'saj_projects')
    )
    if not firefoxbin:
        firefoxbin = os.path.abspath(os.path.join(pkg, 'drivers', 'geckodriver'))
    else:
        firefoxbin = os.path.abspath(os.path.join(os.path.abspath(os.sep), os.path.join(*firefoxbin.split(os.sep))))

    assert os.path.isfile(firefoxbin), f'Driver "{firefoxbin}" não disponível.'
    navegador = webdriver.Firefox(executable_path=firefoxbin)
    navegador.get(url_consulta)
    logger.debug(navegador.current_url)
    sleep(5)
    result, pub_original, ato_url = None, None, None
    try:
        # Verifica renderização inicial
        assert 'SICON' in navegador.title, "Carregamento não iniciado.."
        logger.debug(f'Título carregado -> {navegador.title}')

        # Verifica a estruturação
        assert 'Informe o argumento' in navegador.page_source
        logger.debug(f"conteudo carregado:\n\n{navegador.page_source}")

        # Pesquisa no formulário
        elemento = navegador.find_element_by_tag_name('input')
        logger.debug(elemento)
        elemento.send_keys(f'{alias}-{num}-{ano}')
        elemento.send_keys(Keys.RETURN)

        # Página de resultado
        logger.debug(f'Metadados url: {navegador.current_url}')

        # Delay para carregamento
        sleep(7)
        # wait = WebDriverWait(navegador, 5)
        # wait.until(EC.element_to_be_clickable((By.TAG_NAME, "Button")))

        # Verificação de carregamento do resultado
        assert 'Gestão de Normas Jurídicas' in navegador.page_source

        # Verificação de resultado
        assert 'Não foi encontrado documentos com os parâmetros' \
            'informados.' not in navegador.page_source, "Não encontrado"

        # captura DOU
        elem_pub_original = navegador.find_element(
            By.XPATH,
            '/html/body/div[1]/div/div/div/div[2]/div/div[4]/div[4]/div[3]/span/div/div/div[7]/div[2]/div')
        logger.debug(elem_pub_original)
        pub_original = elem_pub_original.text
        logger.debug(pub_original)

        # Navegar para texto original
        elemento = navegador.find_element_by_css_selector('button.btn-primary:nth-child(2)')
        elemento.click()

        # Delay para carregamento
        sleep(7)
        logger.debug(navegador.window_handles)
        navegador.switch_to_window(navegador.window_handles[-1])
        try:
            assert 'Este texto não substitui o original publicado no Diário Oficial.' in navegador.page_source, \
                "Texto original falhou"
            assert 'PublicacaoSigen.action' in navegador.current_url, \
                "URL Texto original falhou"
        except AssertionError:
            # Página intermediária
            elemento = navegador.find_element(By.PARTIAL_LINK_TEXT, 'PUB')
            elemento.click()
            logger.debug(navegador.window_handles)
            navegador.switch_to_window(navegador.window_handles[-1])

        logger.debug(navegador.current_url)
        ato_url = navegador.current_url

    except Exception as e:
        logger.error(e)
        raise
    else:
        logger.debug('Executado com sucesso')
        logger.debug(f'return -> {pub_original}, {ato_url}')
        return pub_original, ato_url
    finally:
        navegador.quit()


def discover_url(csv_file: str = None, dir_output: str = None, **kwargs):
    '''

    :param csv_file: CSV no formato ['num', 'ano', 'dou', 'url']
    :param dir_output: Diretório de saída, onde será gravado o CSV ['num', 'ano', 'dou', 'url'] com resultado
    :param kwargs:  alias: str = 'dec|del|lei' default dec;
                    url_consulta: str='http://legis.senado.leg.br/sicon/#/basica';
                    firefoxbin: str = None, path absoluto para geckodriver;
    :return: Grava um arquivo para cada iteração dos itens presentes no csv_file.
    '''
    # csv_file = os.path.abspath(os.path.join(os.path.dirname(__file__), *csv_file.split(os.sep)))
    assert os.path.exists(csv_file), f"{csv_file} indisponível!"
    df = pd.read_csv(csv_file)
    assert df.shape[1] == 4, "csv diferente do formato ['num', 'ano', 'dou', 'url']"
    assert set(df.columns).issubset(set('num ano dou url'.split())), "formato esperado: ['num', 'ano', 'dou', 'url']"
    req = df[df.url.isnull()]
    logger.debug(req)
    result = None

    for i, (num, ano, _, _) in enumerate(req.values):
        atos = []
        num, ano = int(num), int(ano)
        kwargs['num'], kwargs['ano'] = num, ano
        try:
            logger.debug(f'{i} [{num}/{ano}]')
            logger.debug(f'kwargs: {kwargs}')
            dou, url = query_ato_num_ano(**kwargs)
            atos.append((num, ano, dou, url))
            result = pd.DataFrame(atos, columns=['num', 'ano', 'dou', 'url'])
        except (AssertionError,
                NoSuchElementException,
                TimeoutException,
                UnexpectedAlertPresentException,
                WebDriverException
                ) as e:
            logger.error(f"{i} {num}/{ano}: ({e}) {sys.exc_info()}")
        else:
            file_output = realfilename(f'/tmp/{inspect.stack()[0][3]}/{ano}/{num}.csv')
            if dir_output:
                file_output = realfilename(os.path.join(dir_output, f'{ano}', f'{num}.csv'))
            result.to_csv(file_output, index=False)
            logger.debug(f"SUCESSO: {file_output} {(num, ano, dou, url)}")

    return result


def merge_csv_files(dir_in: str=None):
    assert dir_in, "O diretório deve ser informado"
    assert os.path.exists(dir_in), "O diretório informado não foi encontrado"
    assert os.access(dir_in, os.X_OK), "O diretório informado não pode ser acessado"
    assert os.access(dir_in, os.R_OK), "O diretório informado não pode ser lido"
    assert os.access(dir_in, os.W_OK), "O diretório informado não se pode gravar"
    files = [os.path.join(path, file) for path, _, x in os.walk(dir_in) for file in x if not file.startswith('lista-')]
    file_output = os.path.join(dir_in, f"lista-{os.path.basename(dir_in)}-1.csv")
    dataframes = []

    if file_output in files:
        files.remove(file_output)

    for file in files:
        df = pd.read_csv(file)
        df.columns = df.columns.str.lower()
        dataframes.append(df)

    result = pd.concat(dataframes, sort=False)
    result = result[['num', 'ano', 'dou', 'url']]
    result = result.sort_values(by=['num', 'ano'])
    result.to_csv(file_output, index=False)
    return result


def aferir_csv_final(csv_in: str) -> bool:
    assert csv_in, "O arquivo CSV deve ser informado"
    assert os.path.exists(csv_in), f"{csv_in} indisponível!"
    assert os.access(csv_in, os.R_OK), f"O arquivo {csv_in} não pode ser lido"
    df = pd.read_csv(csv_in)
    assert df.shape[1] == 4, "csv diferente do formato ['num', 'ano', 'dou', 'url']"
    assert set(df.columns).issubset(set('num ano dou url'.split())), "formato esperado: ['num', 'ano', 'dou', 'url']"
    return True


def elencar_atos_por_ano(ano: str, dir_output: str=None, **kwargs):
    dir_output = os.path.join('/tmp', inspect.stack()[0][3], ano) if not dir_output else dir_output

    df = listar_atos_por_ano(ano=ano, dir_output=dir_output)

    # print(df)
    for i, ato in enumerate(df.values):
        try:
            print(i, ato)
            logger.debug(f'{i} {ato}')
            n, a = ato
            dou, url = query_ato_num_ano(num=n, ano=a, **kwargs)
            result = pd.DataFrame({'num': [n], 'ano': [a], 'dou': [dou], 'url': [url]})
            print(result.columns)
            logger.debug(result)
        except (AssertionError,
                NoSuchElementException,
                TimeoutException,
                UnexpectedAlertPresentException,
                WebDriverException, IndexError
                ) as e:

            logger.error(f'{i} {ato}: {e}')
        else:
            filename = f'{n}.csv'
            file_output = realfilename(os.path.join(dir_output, filename))
            result.to_csv(file_output, index=False)
    return True


def get_lista_atos_tocsv(ano: str='', path_output: str='/tmp/elencar_atos_revogados/', loop: int=2, **kwargs):
    assert ano.isalnum(), '"ano" dever ser informato em formato str (ex: "2018")'
    assert int(ano), '"ano" dever ser informato em formato str (ex: "2018")'
    assert ano.isdigit(), '"ano" dever ser informato em formato str (ex: "2018")'
    assert len(ano) == 4, '"ano" dever ser informato em formato str (ex: "2018")'

    dir_output = os.path.join(path_output, ano)

    if not os.path.exists(f'{dir_output}/lista-{ano}-0.csv'):
        elencar_atos_por_ano(ano=ano, dir_output=dir_output, **kwargs)
        logger.debug('sucesso: elencar_atos_por_ano')

    for i in range(loop):
        merge_csv_files(f'{path_output}/{ano}')
        logger.debug('sucesso: merge_csv_files')
        relatorio_progresso(
            f'{dir_output}/lista-{ano}-0.csv',
            f'{dir_output}/lista-{ano}-1.csv',
            f'{dir_output}/lista-progresso.csv',
        )
        logger.debug('sucesso: relatorio_progresso')
        discover_url(f'{dir_output}/lista-progresso.csv',
                     dir_output=f'{path_output}')
        logger.debug('sucesso: discover_url')
        logger.debug(f"return: {aferir_csv_final(f'{dir_output}/lista-progresso.csv')}")
    return aferir_csv_final(f'{dir_output}/lista-progresso.csv')


if __name__ == '__main__':
    pass
