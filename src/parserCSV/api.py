from src.parserCSV.parserFactory import ParserFactory
from src.parserCSV.abstract import ParserResult, ParserConfig

class ParserAPI:

    def __init__(self, filesToParse):
        self.filesToParse = filesToParse

    def run(self,file):
        try:
            parser = ParserFactory(file).getConstructor()
            if parser is not None:
                return parser.parse()
        except Exception as e:
            print(e)
            config= ParserConfig(file=file)
            return ParserResult(config=config)

    def runAll(self):
        parserResults = []
        for file in self.filesToParse:
            parserResults.append(self.run((file)))
        return parserResults



