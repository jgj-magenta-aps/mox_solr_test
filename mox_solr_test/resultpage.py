from mox_solr_test.config import settings
from pprint import pformat


page="""<html>
<head>
<meta charset="utf-8">
</head>
<body><a href="/">forfra</a>
<table border=2>
<tr><th>query</th><th>query sent to solr-url</th></tr>
<tr><td><pre>{orgparams}</pre></td><td><pre>{expparams}</pre></td></tr>
<tr><td colspan=2>Solr-url: {solrurl}</td></tr>
</table>
<p>
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


def render(orgparams, expparams, result, solrurl):
    #import pdb; pdb.set_trace()
    _rows = rows(result["response"]["docs"])
    _table = table(_rows)
    return page.format(
        orgparams=pformat(dict(orgparams)),
        expparams=pformat(dict(expparams)),
        solrurl=solrurl,
        result_table=_table,
    )


