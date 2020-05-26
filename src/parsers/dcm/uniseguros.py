from io import StringIO

import pandas as pd

from src.parserCSV.abstract import AbstractPaser


class UnisegurosDCM(AbstractPaser):
    def __init__(self,file,enc):
        super().__init__(file,enc)

    def checkDocumento(self):
        try:
            #   CHECK DOCUMENTO SIMPLES SEM CRIAR DATAFRAME
            fileString = self.file.read_text(self.enc)
            if 'Unimed Seguros' in fileString:
                print('Operadora encontrada: Unimed Seguros - DCM')
                return True
        except Exception as e:
            return False

    def getTipoDocumento(self):
        self.tipoDocumento = ('DEMONSTRATIVO_ANALISE_CONTA','000701','.csv/.txt/.tsv')

    def parseDocument(self):
        self.__read_csv()
        self._set_header()
        self.finalizeDF()

    def __read_csv(self):
        #               INICIALIZACAO DATAFRAME(S)
        #   CONTEUDO
        self.df = pd.read_csv(self.file, sep=r';',
                              engine='python',
                              encoding=self.enc,
                              warn_bad_lines=False,
                              error_bad_lines=False,
                              keep_default_na=False,
                              dtype=str, skiprows=15,
                              header=None)
        #   CABECALHOS
        self.header_df = pd.read_csv(self.file,
                                     sep='\n',
                                     engine='python',
                                     encoding=self.enc,
                                     warn_bad_lines=False,
                                     error_bad_lines=False,
                                     keep_default_na=False,
                                     dtype=str,
                                     skiprows=8,
                                     nrows=5,
                                     header=None
                                     )

    def _set_header(self):
        print('Atribuindo cabecalho ao dataframe')
        self.df.columns = ['Conta', 'Associado', 'Servico', 'Realizacao', 'Qtde',
                           'Val_Informado', 'Val_Glosado', 'Val_Aprovado', 'Glosa', 'Observacao']
        self.__remove_bad_lines()
        self.df['Numero_Credenciado'] = self.header_df.iloc[0, 0].split(": ")[1]
        self.df['Total_Informado'] = self.header_df.iloc[1, 0].split(": ")[1]
        self.df['Total_Glosado'] = self.header_df.iloc[2, 0].split(": ")[1]
        self.df['Total_Aprovado'] = self.header_df.iloc[3, 0].split(": ")[1]
        self.df['NR'] = self.header_df.iloc[4, 0].split(";")[0].split(": ")[1]
        self.df['Fatura'] = self.header_df.iloc[4, 0].split(";")[1].split(": ")[1]
        print('Cabecalho atribuido ao dataframe com sucesso')

    def __remove_bad_lines(self):
        print('Entrando no metodo para remocao de possiveis linhas erradas')
        try:
            self.df = self.df.replace(to_replace='None', value=pd.np.nan).dropna()
        except Exception:
            print('Erro na remocao de linhas')

    def finalizeDF(self):
        self.final_df = self.df