
from typing import Any
from pydantic import BaseModel


def get_simple_model_scheme(model: BaseModel):
    scheme = model.model_json_schema()
    
    scheme_definitions = scheme.get("$defs")
    required_props = set(scheme.get("required")) 
    # output = {k: simplify_propdef(k, v, scheme_definitions, k in required_props) for k, v in scheme["properties"].items()}
    output = [simplify_propdef(k, v, scheme_definitions, k in required_props) for k, v in scheme["properties"].items()]
    
    return output

def simplify_propdef(prop_name: str,
                     propdef: dict[str, Any],
                     scheme_definitions: dict[str, Any],
                     required: bool) -> dict[str, Any]: 
    
    def get_any_of_type(item: dict):
        if t := item.get("type"):
            return t
        if ref := item.get("$ref"):
            ref_key = ref.split("/")[-1] 
            propdef = scheme_definitions[ref_key]
            return propdef["type"]
        else:
            raise ValueError("propdef has unprocessable structure")


    if propdef.get("type"):
        pass
    elif any_of := propdef.get("anyOf"): 
        types = [get_any_of_type(_) for _ in any_of]
        types = [_ for _ in types if _ != "null"]
        propdef["type"] = types[0]
    elif ref := propdef.get("$ref"):
        ref_key = ref.split("/")[-1] 
        propdef = scheme_definitions[ref_key]  
    else:
        print(propdef)
        raise ValueError("propdef has unprocessable structure")
    return {
        "prop_name": prop_name,
        "title": propdef.get("title"),
        "type": propdef["type"],
        "default": propdef.get("default"),
        "enum": propdef.get("enum"),
        "required": required
    }
 