from mox_solr_test.frontpage import searchfield as _field
from mox_solr_test.config import settings


page="""<html>
<head>
<meta charset="utf-8">
</head>
<body><a href="/">forfra</a>
{searchfield}<br>
{result_table}
</body>
</html>"""

def rows(docs, ):
    _rows = []
    for d in docs:
        text = [
            "<a href='{_href}'>{name}</a>".format(**d)
        ]
        d.pop("_href")
        for field, value in d.pop("_hl",{}).items():
            text.append("highlight %s: %s" % (field, ",".join(value)))
        for field, value in d.items():
            if isinstance(value, list):
                text.append("%s: %s" % (field, ",".join(value)))
        _rows.append("<tr>{cells}</tr>".format(
            cells="<td>" + "</td><td>".join(text) + "</td>"
        ))
    return "\n".join(_rows)

def table(rows):
    return "<table>{rows}</table>".format(rows=rows)


def render(q, result):
    #import pdb; pdb.set_trace()
    _rows = rows(result["response"]["docs"])
    _table = table(_rows)
    return page.format(
        searchfield=_field(q),
        result_table=_table
    )


