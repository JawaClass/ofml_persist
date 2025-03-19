OCD_ARTICLE = [
    "article_nr",
    "art_type",
    "manufacturer",
    "series",
    "short_textnr",
    "long_textnr",
    "rel_obj",
    "fast_supply",
    "discountable",
    "order_unit",
    "scheme_id",
]

OCD_PRICE = [
    "article_nr",
    "var_cond",
    "price_type",
    "price_level",
    "price_rule",
    "price_textnr",
    "price",
    "is_fix",
    "currency",
    "date_from",
    "date_to",
    "scale_quantity",
    "rounding_id",
]

OCD_TEXT = ["textnr", "language", "line_nr", "line_fmt", "text"]

OCD_ARTBASE = ["article_nr", "prop_class", "property", "prop_value"]

OCD_PROPERTYCLASS = ["article_nr", "pos_class", "prop_class", "textnr", "rel_obj"]

OCD_PROPERTY = [
    "prop_class",
    "property",
    "pos_prop",
    "prop_textnr",
    "rel_obj",
    "prop_type",
    "digits",
    "dec_digits",
    "need_input",
    "add_values",
    "restrictable",
    "multi_option",
    "scope",
    "txt_control",
    "hint_text_id",
]


OCD_PROPERTYVALUE = [
    "prop_class",
    "property",
    "pos_pval",
    "pval_textnr",
    "rel_obj",
    "is_default",
    "suppress_txt",
    "op_from",
    "value_from",
    "op_to",
    "value_to",
    "raster",
]

OCD_PACKAGING = [
    "article_nr",
    "var_cond",
    "width",
    "height",
    "depth",
    "measure_unit",
    "volume",
    "volume_unit",
    "tara_weight",
    "net_weight",
    "weight_unit",
    "items_per_unit",
    "pack_units",
]

OCD_ARTICLETAXES = ["article_nr", "tax_id", "date_from", "date_to"]

OCD_TAXSCHEME = ["tax_id", "country", "region", "number", "tax_type", "tax_category"]

OCD_RELATIONOBJ = ["rel_obj", "position", "rel_name", "rel_type", "rel_domain"]

OCD_RELATION = ["rel_name", "rel_blocknr", "rel_block"]
