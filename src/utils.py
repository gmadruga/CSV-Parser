import json
from pathlib import Path


class ParserResult:

    def __init__(self,config,tipoDocumento=None):
        self.enc = config.getParserConfig()["encoding"]
        self.csvSeparator = config.getParserConfig()["csvSeparator"]
        self.file = Path(config.getParserConfig()["originFilePath"])
        self.config = config.getConfigJson()
        self.hash = ''
        self.health = False
        self.message = None
        self.elapsedTime = 0
        self.result = None
        self.tipoDocumento = tipoDocumento

    def getParserResult(self):
        self.result = json.dumps({"tipoDocumento":self.tipoDocumento,"health":self.health,"message":self.message,
                                 "config":self.config,"hash":self.hash,"status":"","elapsedTime":self.elapsedTime})
        return self.result


    def setParserHealth(self,bol):
        self.health = bol

    def setMessage(self,e):
        self.message = e

    def setTipoDocumento(self,tipoDocumento):
        self.tipoDocumento = tipoDocumento

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
