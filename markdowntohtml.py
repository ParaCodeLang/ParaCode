import markdown

inputFile = input('Input File >> ')
outputFile = input('Output File >> ')

markdown.markdownFromFile(
    input=inputFile
    output=outputFile,
    encoding='utf8',
    extensions=['fenced_code', 'codehilite'],
)