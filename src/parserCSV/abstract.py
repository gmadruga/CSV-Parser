import glob
import os
import random
import string
import sys
import time
from io import StringIO
from multiprocessing.pool import ThreadPool
from pathlib import Path
import pandas as pd
from src.utils import ParserResult, ParserConfig, TipoDocumento
import json

class AbstractPaser:
    def __init__(self,config):
        self.enc = config.getParserConfig()["encoding"]
        self.csvSeparator = config.getParserConfig()["csvSeparator"]
        self.file = Path(config.getParserConfig()["originFilePath"])
        self.config = config.getConfigJson()
        self.outPutCsvFilePath = None
        self.tipoDocumento = self.getTipoDocumento()
        self.final_df = None
        self.result = ParserResult(config,tipoDocumento=self.tipoDocumento.getTipoDocumento())

    def checkDocumento(self):
        pass

    def finalizeDF(self):
        pass

    def getTipoDocumento(self):
        pass

    def parse(self):
        #           CRIA DIRETORIO E ARQUIVO DE SAIDA
        self.outPutCsvFilePath = Path(str(self.file.parent)+'\\'+str(self.file.stem))
        self.outPutFileName = Path(str(self.file.parent)+'\\'+str(self.file.stem)+'\\'+str(self.file.stem)+'.csv')
        print('Iniciando arquivo no diretorio de saida ' + str(self.outPutCsvFilePath))
        try:
            self.parseDocument()
            if not self.outPutCsvFilePath.exists():
                self.outPutCsvFilePath.mkdir()
            self.final_df.to_csv(self.outPutFileName,index=True, sep=self.csvSeparator)
            self.result.setParserHealth(True)
            print('Arquivo parseado com sucesso!!')
            result = self.result.getParserResult()
            print(str(result))
            return result
        except Exception as e:
            self.result.setMessage(str(e))
            result = self.result.getParserResult()
            print(str(result))
            return result

