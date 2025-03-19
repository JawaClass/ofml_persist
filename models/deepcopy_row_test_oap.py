from models import generate_session_ctx
from models.base import SqlAlchemyBase
from pprint import pprint

from models.deepcopy_row import deep_copy, make_cache_key, shallow_copy
from models.oap import OapTypeDB, oap_action_object_association_table


with generate_session_ctx() as session:

    cache = {}

    obj = session.get(OapTypeDB, 1)
    print(obj.ref_program)
    new_program = shallow_copy(obj.ref_program)
    from time import time

    new_program.name = f"{new_program.name}_COPY_{time()}"
    cache[make_cache_key(obj.ref_program)] = new_program
    print("new_program...", new_program)
    # input(".")
    new = deep_copy(obj, cache)

    print("OapTypeDB.....")
    print(new)

    print("new.ref_program")
    print(new.ref_program)

    print("new.ref_article2type")
    print(new.ref_article2type)

    print("new.ref_metatype2type")
    print(new.ref_metatype2type)

    print("new.ref_interactor")
    pprint(new.ref_interactor)

    print("new.ref_interactor[0].ref_actions")
    pprint(new.ref_interactor[0].ref_actions)
    print("---")
    pprint(new.ref_interactor[0].ref_actions[0].ref_action)
    print("---")
    pprint(new.ref_interactor[0].ref_actions[0].ref_action.ref_objects)
    print("---")
    pprint(new.ref_interactor[0].ref_actions[0].ref_action.ref_propedit)
    print("---")
    pprint(new.ref_interactor[0].ref_actions[0].ref_action.ref_propedit.ref_program)

    session.add(new)
    session.flush()
    session.commit()

    select_stmt = oap_action_object_association_table.select()
    print("select_stmt...", type(select_stmt))
    print(select_stmt)
    rows = session.execute(select_stmt).all()
    print("rows", type(rows), len(rows))
