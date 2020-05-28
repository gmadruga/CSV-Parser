from src.parserCSV.parserFactory import ParserFactory
from src.parserCSV.abstract import ParserResult, ParserConfig
from src.utils import TipoDocumentoNaoIdentificadoException, EmptyDocumentException, ParserStatus

class ParserAPI:

    def __init__(self, filesToParse):
        self.filesToParse = filesToParse

    def run(self,file):
        try:
            parser = ParserFactory(file).getConstructor()
            if parser is not None:
                result = parser.parse()
                print(str(result))
                return result
        except EmptyDocumentException as e:
            print(e)
            result = ParserResult(config=ParserConfig(file=file),message=e.args[0],status=ParserStatus.EMPTY_DOCUMENT.name).getParserResult()
            print(str(result))
            return result
        except TipoDocumentoNaoIdentificadoException as e:
            print(e)
            result = ParserResult(config=ParserConfig(file=file),message=e.args[0],status=ParserStatus.ERROR_IDENTIFYING_OPERATOR.name).getParserResult()
            print(str(result))
            return result

    def runAll(self):
        parserResults = []
        for file in self.filesToParse:
            parserResults.append(self.run((file)))
        return parserResults



