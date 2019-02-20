from mox_solr_test.config import settings

page="""<html>
<head>
<meta charset="utf-8">
</head>
<body>
{searchfield}<br>
{examples_table}
</body>
</html>"""



def searchfield(q=""):
    return """
        <form><input value='{value}' name=q>
        <input type=submit name=\"collection\" value=\"employee\">
        <input type=submit name=\"collection\" value=\"orgunit\">
        </form>
        """.format(
            value=q
        )


def rows(results):
    return "\n".join([
        "<tr><td><a href='{_href}'>{name}</a></td></tr>".format(
            **r
        ) for r in results
    ])


def table(rows):
    return "<table>{rows}</table>".format(rows=rows)


examples=[
        { "name":"find 'Peter' i employees name - list name og uuid", "_href":"/?q=name:peter&collection=employee&fl=name,uuid"},
        { "name":"find 'Peter' i employees name - med highlighing, list name og uuid", "_href":"/?hightlightMultiTerm=true&hl.fl=*&hl.requireFieldMatch=true&hl=on&q=name%3Apeter&usePhraseHighLighter=true&collection=employee&fl=name,uuid"},
        { "name":"find 'og' i orgunits name - list alle felter", "_href":"/?q=name:og&collection=orgunit"},
        { "name":"list alle organisationsenheders navn og location", "_href":"/?q=*:*&collection=orgunit&rows=10000000&fl=name,lokation,uuid"},
        { "name":"'og' i name og 'Borgmesterens afdeling' i parent.name - vis name og parent.name", "_href":"/?q=(name%3Aog+AND+parent.name%3A\"Borgmesterens+Afdeling\")&collection=orgunit&fl=uuid,name,parent.name"},
        { "name":"('og' i name og 'Borgmesterens afdeling' i parent.name) - eller 'ansvarlig' vis name og parent.name", "_href":"/?q=(name%3Aog+AND+parent.name%3A\"Borgmesterens+Afdeling\")&collection=orgunit&fl=uuid,name,parent.name"},
        { "name":"Gammel Havnevej 8 i et eller andet addressefelt - (query preprocesseres) - list uuid og alle addressefelter", "_href":"/?q=\"gammel Havnevej 8\"&defType=dismax&qf=details.address.*name&collection=orgunit&fl=uuid,name&hl=on"},

]


def render(_examples=examples):
    _rows = rows(_examples)
    _table = table(_rows)
    return page.format(
        searchfield=searchfield(),
        examples_table=_table
    )




