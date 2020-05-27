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
import json

class AbstractPaser:
    def __init__(self,file,enc,csvSeparator):
        #       INICIALIZANDO OS ATRIBUTOS
        self.csvSeparator = csvSeparator
        self.file = file
        self.enc = enc
        self.config = json.dumps({"csvSeparator": self.csvSeparator,"originFilePath":str(self.file),"encoding":self.enc})
        self.outPutCsvFilePath = None
        self.hash = ''
        self.tipoDocumento = None
        self.final_df = None
        self.result = None
        self.health = False
        self.message = None
        self.elapsedTime = 0

    def checkDocumento(self):
        pass

    def finalizeDF(self):
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
            self.getTipoDocumento()
            self.setParserHealth(True)
            print('Arquivo parseado com sucesso!!')
            self.getParserResult()
            print(self.result)
            return self.result
        except Exception as e:
            print('Erro ao parsear documento: '+e)
            self.setMessage(e)
            return self.getParserResult()


    def getParserResult(self):
        self.result= json.dumps({"tipoDocumento":self.tipoDocumento,"health":self.health,"message":self.message,
                                 "config":self.config,"hash":self.hash,"status":"","elapsedTime":self.elapsedTime})

    def setParserHealth(self,bol):
        self.health = bol

    def setMessage(self,e):
        self.message = e