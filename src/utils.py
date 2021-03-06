import json
from pathlib import Path
import time
from enum import Enum, auto


class ParserResult:

    def __init__(self,config,tipoDocumento=None,message=None,status=None):
        self.enc = config.getParserConfig()["encoding"]
        self.csvSeparator = config.getParserConfig()["csvSeparator"]
        self.file = Path(config.getParserConfig()["originFilePath"])
        self.config = config.getConfigJson()
        self.hash = ''
        self.health = False
        self.message = message
        self.elapsedTime = 0
        self.result = None
        self.status = status
        self.tipoDocumento = tipoDocumento

    def getParserResult(self):
        self.result = json.dumps({"tipoDocumento":self.tipoDocumento,"health":self.health,"message":self.message,
                                 "config":self.config,"hash":self.hash,"status":self.status,"elapsedTime":self.elapsedTime})
        return self.result


    def setParserHealth(self,bol):
        self.health = bol

    def setMessage(self,e):
        self.message = e

    def setTipoDocumento(self,tipoDocumento):
        self.tipoDocumento = tipoDocumento

    def sethHash(self,hash):
        self.hash = hash

    def setElapsedTime(self,timeStart):
        timeFinish = time.time()
        self.elapsedTime = timeFinish - timeStart

    def setStatus(self, status):
        self.status = status.name

class ParserConfig:
    def __init__(self,file=None,enc='',csvSeparator=r';'):
        self.file = file
        self.enc = enc
        self.csvSeparator = csvSeparator
        self.config = {"csvSeparator": self.csvSeparator, "originFilePath": str(self.file), "encoding": self.enc}

    def getParserConfig(self):
        return self.config

    def getConfigJson(self):
        return json.dumps(self.config)

    def setParserConfig(self,file,enc,csvSeparator):
        self.file = file
        self.enc = enc
        self.csvSeparator = csvSeparator
        self.config= {"csvSeparator": self.csvSeparator, "originFilePath": str(self.file), "encoding": self.enc}

    def setFile(self,file):
        self.file=file

    def setEnc(self,enc):
        self.enc = enc

    def setCsvSeparator(self,csvSeparator):
        self.csvSeparator = csvSeparator

class TipoDocumento:
    def __init__(self,tipoDocumento=None):
        self.tipo = tipoDocumento
        self.tipoDocumento = tipoDocumento[0]
        self.tipoDocumento_complemento1 = tipoDocumento[1]
        self.tipoDocumento_complemento2 = tipoDocumento[2]

    def getTipoDocumento(self):
        return self.tipo

    def getTipoDocumento1(self):
        return self.tipoDocumento

    def getTipoDocumentoC1(self):
        return self.tipoDocumento_complemento1

    def getTipoDocumentoC2(self):
        return self.tipoDocumento_complemento2

class ParserStatus(Enum):
#               STATUS PADRAO PARA TODOS OS PARSERS
    PARSED = auto()
    ERROR = auto()
    INVALID = auto()
    INPROGRESS = auto()
    ENCODING_ERROR = auto()
    INVALID_TISS = auto()
    EMPTY_DOCUMENT = auto()
    ERRROR_RUNNING_REGEX = auto()
    SCHEMA_TISS_DESCONHECIDO = auto()
    VERSAO_TISS_DESCONHECIDA = auto()
    ERROR_IDENTIFYING_OPERATOR = auto()


#                       EXCEPTIONS CUSTOMIZADAS

class EmptyDocumentException(Exception):
    pass

class TipoDocumentoNaoIdentificadoException(Exception):
    pass