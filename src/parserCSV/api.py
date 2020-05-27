from src.parserCSV.parserFactory import ParserFactory
import json

class ParserAPI:

    def __init__(self, filesToParse):
        self.filesToParse = filesToParse

    def run(self,file):
        try:
            parser = ParserFactory(file).getConstructor()
            if parser is not None:
                result = parser.parse()
                return result
        except Exception as e:
            print(e)


    def runAll(self):
        parserResults = []
        for file in self.filesToParse:
            parserResults.append(self.run((file)))



