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
    regex = r"(.{0,50})" + re.escape(txt) + r"(.{0,50})"

    ret = []
    for result in results:
        found = re.findall(regex, result["content"])
        for f in  found:
            ret.append({
                "file": result["path"],
                "content": "{} {} {}".format(f[0].strip(), txt, f[1]).strip()
            })
    
    return {"result": ret}, 200
    





