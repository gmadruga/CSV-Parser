from io import StringIO

import pandas as pd
from src.utils import TipoDocumento
from src.loggerConfig import logger

from src.parserCSV.abstract import AbstractPaser


#       COLOCAR O NOME DA CLASSE CONFORME O NOME DO PARSER
#   Será usado também no ParserFactory
class TemplateDCM(AbstractPaser):
    def __init__(self,config):
        #  COLOCAR AQUI O SEPARADOR DESSE ARQUIVO
        # ---------------------------------------#
        config.setCsvSeparator(csvSeparator=r'<csvSeparator>')
        #---------------------------------------#
        super().__init__(config)

    def checkDocumento(self):
        try:
            #   CHECK DOCUMENTO SIMPLES SEM CRIAR DATAFRAME
            #   Pode ser feito tambem com dataframe
            fileString = self.file.read_text(self.enc)
            #   Condição para verificar presença de identificador único do doc dessa operadora
            if '' in fileString:
                logger.debug('Operadora encontrada: <ic_operadora> - <tipo documento>')
                return True
        except Exception as e:
            return False

    def getTipoDocumento(self):
        return TipoDocumento(("<tipo documento>","<ic_operadora>",".csv/.txt/.tsv"))

    def parseDocument(self):
        #       GERACAO DATAFRAME
        self.__read_csv()
        #       INSIRA AQUI METODOS PARA O TRATAMENTO DO(S) DATAFRAMES

        #       DATAFRAME FINAL
        self.finalizeDF()

    def __read_csv(self):
        #               INICIALIZACAO DATAFRAME(S)
        #   DATAFRAME COM CONTEUDO DO CSV
        self.df = pd.read_csv(self.file, sep=self.csvSeparator,
                              engine='python',
                              encoding=self.enc,
                              warn_bad_lines=False,
                              error_bad_lines=False,
                              keep_default_na=False,
                              dtype=str, skiprows=15, # Colocar a qtde de linhas a serem puladas de cabeçalhos
                              header=None)

    def finalizeDF(self):
        self.final_df = self.df