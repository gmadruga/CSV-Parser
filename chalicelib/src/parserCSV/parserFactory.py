from chalicelib.src.parsers.dcm.uniseguros import UnisegurosDCM
from chalicelib.src.utils import ParserConfig, EmptyDocumentException, TipoDocumentoNaoIdentificadoException
from chalicelib.src.loggerConfig import logger

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
        logger.error('Operadora nao encontrada para ' + self.file.name)
    ##      VERIFICANDO SE ARQUIVO ESTA VAZIO
        string = self.file.read_text()
        if not string:
            raise EmptyDocumentException('Documento vazio: '+self.file.name)
        else:
            raise TipoDocumentoNaoIdentificadoException('Erro ao identificar operadora: '+self.file.name)