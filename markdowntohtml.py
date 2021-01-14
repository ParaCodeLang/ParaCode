import markdown

markdown.markdownFromFile(
    input='README.md',
    output='README.html',
    encoding='utf8',
    extensions=['fenced_code', 'codehilite'],
)