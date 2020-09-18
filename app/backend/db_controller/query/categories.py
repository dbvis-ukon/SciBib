from backend.db_controller.db import SQLAlchemy
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from backend.db_controller.db import Categories, Categories_publications, Publications, Authors, Authors_publications


db = SQLAlchemy()

def getCategories():
    counts = countPubPerCat()
    result = db.engine.execute(
        """
        SELECT CONCAT( REPEAT('  ', COUNT(parent.name) - 1), node.name), node.id AS name
        FROM categories AS node,
            categories AS parent
        WHERE node.lft BETWEEN parent.lft AND parent.rght
        GROUP BY node.name
        ORDER BY node.lft;
        """)
    result = [{'name': r[0].decode('utf-8') if isinstance(r[0], bytes) else str(r[0]), 'id': r[1], 'count': counts.get(r[1], 0)} for r in result]
    return result

def countPubPerCat():
    result = db.session.query(Categories.id, func.count(Categories_publications.id))\
        .filter(Categories_publications.category_id == Categories.id)\
        .group_by(Categories.id)
    result = {r[0]: r[1] for r in result}

    db.session.close()
    return result

def getRelatedCategories(id):
    result = db.engine.execute(
        """
        SELECT node.id, node.name, node.parent_id, (COUNT(parent.name) - (sub_tree.depth + 1)) AS depth, node.description
        FROM categories AS node,
                categories AS parent,
                categories AS sub_parent,
                (
                        SELECT node.name, (COUNT(parent.name) - 1) AS depth
                        FROM categories AS node,
                                categories AS parent
                        WHERE node.lft BETWEEN parent.lft AND parent.rght
                                AND node.id = %s
                        GROUP BY node.name
                        ORDER BY node.lft
                )AS sub_tree
        WHERE node.lft BETWEEN parent.lft AND parent.rght
                AND node.lft BETWEEN sub_parent.lft AND sub_parent.rght
                AND sub_parent.name = sub_tree.name
        GROUP BY node.name
        HAVING depth <= 1
        ORDER BY node.lft;
        """, (id, )
    )
    # skip first one since it is the parent category
    result = [{'id': r[0], 'name': r[1], 'parent_id': r[2], 'description': r[4]} for r in result]
    return result

def getPubsOfCat(id):
    result = db.session.query(
        Publications.id,
        Publications.title,
        func.group_concat(Authors.cleanname.op("ORDER BY")(Authors_publications.position)),
        Publications.thumb,
        Publications.year,
        Publications.journal
    )\
            .filter(Categories_publications.category_id == Categories.id)\
            .filter(Publications.id == Categories_publications.publication_id)\
            .filter(Categories.id == id)\
            .filter(Authors_publications.publication_id == Publications.id)\
            .filter(Authors.id == Authors_publications.author_id)\
            .group_by(Categories.id, Publications.id)\
            .order_by(Publications.year.desc(), Authors.surname)
    result = [{'id': r[0],
               'title': r[1],
               'authors': r[2].replace(',', ', '),
               'thumb': r[3],
               'year': r[4],
               'journal': r[5]
               } for r in result]

    db.session.close()
    return result

def getNameById(id):
    result = db.session.query(Categories)\
        .filter(Categories.id == id).first()

    db.session.close()
    return result.to_dict() if result is not None else None
    # return [{'id': r[0], 'name': r[1]} for r in result]
