import ofml_api.repository
from sqlalchemy import select, delete
from models import generate_session_ctx
from pprint import pprint
from models.deepcopy_row import deep_copy, make_cache_key, shallow_copy
from models.ocd import (
    OcdArtbaseDB,
    OcdArticleDB,
    OcdArticlePropertyclassAssocDB,
    OcdProgramDB,
    OcdRelationObjRelationAssocDB,
    OcdTextDB,
    OcdUtilArticleClonedSourceDB,
)
from ofml_import.ocd.import_program_plaintext_to_db import ofml2dbscheme
import ofml_api.repository as ofml
from time import time

with generate_session_ctx() as session:

    # insert ocd program
    # repo = ofml.Repository("/mnt/knps_testumgebung/ofml_development/repository", "kn")
    # repo.read_profiles()
    # p = repo.load_program("quick3")
    # ocd = p.load_ofml_part("ocd")
    # ocd.read_all_tables()

    # ofml2dbscheme(ocd=ocd, session=session, program_name=f"{p.name}_{time()}")

    # input(",,")

    cache = {}

    new_program = OcdProgramDB(name=f"DEEPCOPY_TEST_{time()}")
    print("new_program..", new_program)

    articles_source = (
        session.execute(select(OcdArticleDB).where(OcdArticleDB.program_id == 13))
        .scalars()
        .all()
    )

    articles_copies = []

    for a in articles_source:
        print(type(a), "::", a)

        cache[make_cache_key(a.ref_program)] = new_program
        a_copy = a.deep_copy(cache)
        a_copy.ref_cloned_src = OcdUtilArticleClonedSourceDB(
            src_article_nr=a.article_nr, src_series=a.ref_program.name
        )
        articles_copies.append(a_copy)

    session.add_all(articles_copies)

    # session.flush()
    new_objects = session.new
    print("session.new...", type(session.new), len(session.new))

    counts = {}
    for obj in new_objects:
        class_name = obj.__class__.__name__
        counts[class_name] = counts.get(class_name, 0) + 1
    print("Counts by type:")
    pprint(counts)

    session.commit()

    print(len(session.scalars(select(OcdArticlePropertyclassAssocDB)).all()))
