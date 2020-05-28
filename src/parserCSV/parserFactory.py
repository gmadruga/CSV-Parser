from src.parsers.dcm.uniseguros import UnisegurosDCM
from src.utils import ParserConfig
import src.parsers.dp
import src.parsers.erp
import src.parsers.rrg

class ParserFactory:
    def __init__(self, file):
        self.file = file
        #       ENCODINGS
        self.acceptedEncodings = ['utf-8','latin1']
        #       CLASSES DOS PARSERS EXISTENTES
        self.Parsers = {'ParserUnisegurosDCM':UnisegurosDCM}

    def getConstructor(self):
        bol = False
        for enc in self.acceptedEncodings:
            for p in self.Parsers:
                parser = self.Parsers[p](ParserConfig(file=self.file,enc=enc))
                bol = parser.checkDocumento()
                if bol:
                    return parser

        print('Operadora nao encontrada para '+self.file.name)