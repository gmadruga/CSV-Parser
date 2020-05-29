from src.parserCSV.parserFactory import ParserFactory
from src.parserCSV.abstract import ParserResult, ParserConfig
from src.utils import TipoDocumentoNaoIdentificadoException, EmptyDocumentException, ParserStatus
from src.loggerConfig import logger

class ParserAPI:

    def __init__(self, filesToParse):
        self.filesToParse = filesToParse

    def run(self,file):
        try:
            parser = ParserFactory(file).getConstructor()
            if parser is not None:
                result = parser.parse()
                logger.debug(str(result))
                return result
        except EmptyDocumentException as e:
            logger.exception(e)
            result = ParserResult(config=ParserConfig(file=file),message=e.args[0],status=ParserStatus.EMPTY_DOCUMENT.name).getParserResult()
            logger.error(str(result))
            return result
        except TipoDocumentoNaoIdentificadoException as e:
            logger.exception(e)
            result = ParserResult(config=ParserConfig(file=file),message=e.args[0],status=ParserStatus.ERROR_IDENTIFYING_OPERATOR.name).getParserResult()
            logger.error(str(result))
            return result

    def runAll(self):
        parserResults = []
        for file in self.filesToParse:
            parserResults.append(self.run((file)))
        return parserResults



