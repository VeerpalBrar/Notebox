import re
from flask import Blueprint, request
from ..elastic.elasticClient import ElasticClient

bp = Blueprint("search", __name__)

elastic = ElasticClient()
@bp.route("/search")
def get_post():
    """Search for files with certain content"""
    txt = request.args.get('txt')
    results = elastic.search(txt)
    regex = r"(.{0,25})" + re.escape(txt) + r"(.{0,25})"

    ret = []
    for result in results:
        found = re.findall(regex, str(result))
        for f in  found:
            ret.append("{} {} {}".format(f[0], txt, f[1]))
    
    return ret
    





