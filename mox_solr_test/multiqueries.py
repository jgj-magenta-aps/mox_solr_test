from mox_solr_test.config import settings
from mox_solr_test import queries

def name_in_subtree_via_employee(params):
    department_children = queries.department_children(params["department"])
    result, params = queries.lucenequery("employee", {"q": "name:%s" % params["name"], "fq":"details.engagement.org_unit.uuid:(IN %s )" % " ".join(department_children), "fl":"name,uuid"})
    return result, params

multiqueries={
    "name_in_subtree_via_employee": name_in_subtree_via_employee
}


page="""<html>
<head>
<meta charset="utf-8">
</head>
<body>

<form>
<input type=hidden name=multiquery value=name_in_subtree_via_employee>
Find alle med navn A i undertræet under afdeling B: - slår først op i department og derefter employees<br>
Navn: <select name=name>{employee_name_options}</select><select name=department>{department_name_options}</select><input type=submit>
</form>

<hr>
</body>
</html>"""



def render():
    return page.format(
        employee_name_options = queries.employee_name_options(),
        department_name_options = queries.department_name_options(),
    )




