# # from pprint import pprint
# # import pandas as pd
# # import ofml_api.repository as ofml
# # from models import engine
# # from models.ocd import (
# #     OcdArticleDB,
# #     OcdPackagingDB,
# #     OcdProgramDB,
# #     OcdRelationDB,
# #     OcdRelationObjDB,
# #     OcdRelationObjRelationAssocDB,
# #     OcdTextDB,
# #     OcdArtbaseDB,
# #     OcdPriceDB,
# #     TextType,
# #     OcdPropertyClassDB,
# #     OcdPropertyDB,
# #     OcdPropertyValueDB,
# #     OcdArticleTaxesDB,
# #     OcdTaxSchemeDB,
# # )
# # from sqlalchemy.orm import Session

# # from ocd_insert.import_program_plaintext_to_db import ofml2dbscheme


# # repo = ofml.Repository("/mnt/knps_testumgebung/ofml_development/repository", "kn")
# # repo.read_profiles()
# # programs_with_errors = []
# # for name in repo.program_names():
# #     if name not in "workplace talos quick3 jet3 s6".split():  #
# #         continue

# #     if "siemen" in name or "test" in name:
# #         continue

# #     p = repo.load_program(name)
# #     print(p)

# #     if isinstance(p, ofml.NotAvailable):
# #         continue

# #     if not p.contains_ofml_part("ocd"):
# #         continue

# #     ocd = p.load_ofml_part("ocd")

# #     if isinstance(ocd, ofml.NotAvailable):
# #         continue

# #     ocd.read_all_tables()

# #     for table_name, table in ocd.tables.items():
# #         if isinstance(table, ofml.NotAvailable):
# #             print("table", table_name, "was NotAvailable!")
# #             input(".")
# #             continue
# #         table.df["db_table_id"] = pd.Series(dtype="Int64")
# #         table.df = table.df.where(table.df.notnull(), None)
# #     # print(ocd.table("ocd_packaging.csv").df.to_string())
# #     # input(".")
# #     session = Session(engine)
# #     try:
# #         ofml2dbscheme(ocd, session, program_name=p.name)
# #         print("session.new::", type(session.new), len(session.new))
# #         # session.commit()
# #     except KeyError as e:
# #         programs_with_errors.append(name)
# #         print("ERROR", e)
# #     session.close()

# # """
# # IMPORT EXPORT VERGLEICH GLEICHHEIT
# # TABLE               BEFORE              AFTER
# # OCD_ARTICLE         216                 216 OK
# # OCD_ARTBASE         502                 502 OK
# # OCD_ARTICLETAXES    208                 208 OK
# # OCD_ARTLONGTEXT     1124                1124 OK
# # OCD_ARTSHORTTEXT    872                 864 ?????????
# # OCD_CLASSIFICATION  0                   0 OK
# # OCD_CODESCHEME      0                   0 OK
# # OCD_PACKAGING       198                 197  OK
# # OCD_PRICE           9357                9357 OK
# # OCD_PRICETEXT       1724                1584 ?????????
# # OCD_PROPCLASSTEXT    29                 32 ?????
# # OCD_PROPERTY        1359                1359 OK
# # OCD_PROPERTYCLASS     403               403 OK
# # OCD_PROPERTYTEXT     658                612 ????
# # OCD_PROPERTYVALUE    6252               6252 OK
# # OCD_PROPHINTTEXT      0                  0  OK
# # OCD_PROPVALUETEXT     2140              2128 ??????
# # OCD_RELATION          15403             12312  ????
# # OCD_RELATIONOBJ       1169              1142 ????
# # OCD_ROUNDING            0               0
# # OCD_TAXSCHEME          16               7 ???? kinda know why...
# # OCD_USERMESSAGE        36                 36 OK
# # OCD_VERSION             1                   1
# # """


# # print("programs_with_errors....")
# # pprint(programs_with_errors)
# # # for key, instance in session.identity_map.items():
# # #     print(key, instance)
# # # print(
# # #     "session.identity_map...",
# # #     type(session.identity_map),
# # #     len(session.identity_map.keys()),
# # # )


# # # df = pd.read_sql(
# # #     session.query(OcdProgramDB).statement,
# # #     engine,
# # # )
# # # print(df.to_string())


# # # df = pd.read_sql(
# # #     session.query(OcdArticleDB).limit(5).statement,
# # #     engine,
# # # )
# # # print(df.to_string())

# from typing import Any, TypedDict
# from pprint import pprint
# from api_models.oap.interactor import OapInteractorOut
# from api_models.oap.action import OapActionOut
# from api_models.oap.propedit import OapPropEditOut

# scheme = OapPropEditOut.model_json_schema()

# def simplify_propdef(prop_name: str,
#                      propdef: dict[str, Any],
#                      scheme_definitions: dict[str, Any],
#                      required: bool) -> dict[str, Any]: 
#     if propdef.get("type"):
#         pass
#     elif any_of := propdef.get("anyOf"):
#         types = [_["type"] for _ in any_of if _["type"] != "null"]
#         propdef["type"] = types[0]
#     elif ref := propdef.get("$ref"):
#         ref_key = ref.split("/")[-1] 
#         propdef = scheme_definitions[ref_key]  
#     else:
#         print(propdef)
#         raise ValueError("propdef has unprocessable structure")
#     return {
#         "prop_name": prop_name,
#         "title": propdef.get("title"),
#         "type": propdef["type"],
#         "default": propdef.get("default"),
#         "enum": propdef.get("enum"),
#         "required": required
#     }

# scheme_definitions = scheme.get("$defs")
# required_props = set(scheme.get("required"))
# # for prop_name, prop_def in scheme["properties"].items():
# #     # print(prop_name, "......")
# #     prop_def = simplify_propdef(prop_name, prop_def, scheme_definitions, prop_name in required_props)
# #     print(prop_def)
    

# output = {k: simplify_propdef(k, v, scheme_definitions, k in required_props) for k, v in scheme["properties"].items()}

# pprint(output)

import ofml_api.repository as ofml

repo = ofml.Repository("/mnt/knps_testumgebung/Testumgebung/EasternGraphics", "kn")
repo.read_profiles()

p = repo.load_program("basic4")
p.load_ofml_part("go")
print(p)

properties = p.go.read_table("go_properties.csv")

print("properties", properties.df.shape)
print(properties.df.columns)

df = properties.df[properties.df.id == "MT_B4_CombiExt"]
print("df...", df.shape)
# MT_B4_CombiExt

print(df.head().to_string())

# all groups have same length OK
# print(df.groupby("key").count().to_string())

# print(df.groupby("key").apply(lambda group: group["name"] + "___" + group["value"]).to_string())
import pandas as pd
# x: pd.Series = df.groupby("key").apply(lambda group: group["name"] + "___" + group["value"])
seen_articles = set()
seen = set() 
seen_values = set()
#df = df.sort_values(by=["id", "key", "name", "value"])
for key, group_df in df.groupby("key"):
    assert key not in seen_articles
    seen_articles.add(key)
    # print("::::", key)
    # print(group_df.to_string())
    x = (group_df["name"] + "___" + group_df["value"])
    assert x.shape[0] == 5
    block = "::".join(x.array)
    assert block not in seen, f"{key} duplicate def"
    seen.add(block)
    # print(block)
    print("::", key)
    print("_".join(group_df["name"].array))
    props = group_df["name"].tolist()
    print("props:", props)
    assert props[0] == "GB4_PriceGroup", f"props[0] was {props[0]}"
    assert props[1] == "GB4_ExtType", f"props[1] was {props[1]}"
    assert props[2] == "GB4_Width", f"props[2] was {props[2]}"
    assert props[3] == "GB4_Depth", f"props[3] was {props[3]}"
    assert props[4] == "GB4_TopThickness", f"props[4] was {props[4]}"

    values = group_df["value"].tolist()

    print("values.", values)
    key = "".join(values)
    assert key not in seen_values
    seen_values.add(key)


    
    # assert props[0] == "GB4_PriceGroup"
    # assert props[0] == "GB4_PriceGroup"

    # print(group_df[["name", "value"]].to_string())

articles = p.go.read_table("go_articles.csv")

print(articles.df.columns)

df = articles.df
df = df[df["id"] == "MT_B4_CombiExt"]

print(df.shape)
print(df.drop_duplicates(["prm_key"]).shape)

print(df.shape)
print(df.drop_duplicates(["article_nr"]).shape)