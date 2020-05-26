from src.parserCSV.parserFactory import ParserFactory

class ParserAPI:

    def __init__(self, filesToParse):
        self.filesToParse = filesToParse

    def run(self):
        for file in self.filesToParse:
            parser = ParserFactory(file).getConstructor()
            parser.parse()
            b = 0

