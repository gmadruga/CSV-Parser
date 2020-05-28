import glob
import os
import random
import string
import sys
import time
import base64
import hashlib
import re
import unicodedata
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
        timeStart = time.time()
        self.outPutCsvFilePath = Path(str(self.file.parent)+'\\'+str(self.file.stem))
        self.outPutFileName = Path(str(self.file.parent)+'\\'+str(self.file.stem)+'\\'+str(self.file.stem)+'.csv')
        print('Iniciando arquivo no diretorio de saida ' + str(self.outPutCsvFilePath))
        try:
            self.parseDocument()
            if not self.outPutCsvFilePath.exists():
                self.outPutCsvFilePath.mkdir()
            self.saveAndGetHash(self.final_df)
            self.result.setParserHealth(True)
            self.result.setElapsedTime(timeStart)
            print('Arquivo parseado com sucesso!!')
            result = self.result.getParserResult()
            print(str(result))
            return result
        except Exception as e:
            self.result.setMessage(str(e))
            result = self.result.getParserResult()
            print(str(result))
            return result

    def saveAndGetHash(self,finalDataframe):
        buffer = StringIO()
        finalDataframe.to_csv(buffer,index=True, sep=self.csvSeparator)
        self.result.sethHash(self.getHash(buffer=buffer.getvalue(),hash_function='sha256'))
        self.outPutFileName.write_text(data=buffer.getvalue(),encoding=self.enc)
        buffer.close()

    def getHash(self,buffer,hash_function='sha1'):
        if hash_function == 'sha1':
            h = hashlib.sha1()
        else:
            h = hashlib.sha256()
        h.update(buffer.encode(encoding='utf-8'))
        hash_str = base64.b64encode(h.digest()).decode('utf-8')

        return hash_str

