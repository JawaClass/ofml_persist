OAP_INTERACTOR = [
    "interactor",
    "condition",
    "needs_plan_mode",
    "actions",
    "symbol_type",
    "symbol_size",
]

OAP_ARTICLE2TYPE = [
    "manufacturer_id",
    "series_id",
    "article_id",
    "var_type",
    "variant",
    "type_id",
]

OAP_METATYPE2TYPE = [
    "manufacturer",
    "series",
    "metatype_id",
    "var_type",
    "variant",
    "type_id",
]


OAP_OBJECT = [
    "id",
    "category",
    "argument1",
    "argument2",
    "argument3",
]


OAP_METHODCALL = [
    "id",
    "type",
    "context",
    "method",
    "arguments",
]


OAP_DIMCHANGE = [
    "id",
    "dimension",
    "condition",
    "separate",
    "third_dim",
    "property",
    "multiplier",
    "precision",
]


OAP_MESSAGE = [
    "id",
    "arg_type",
    "argument",
]


OAP_PROPCHANGE = [
    "id",
    "type",
    "property",
    "value",
]


OAP_PROPEDIT = [
    "id",
    "title",
    "state_restr",
    "properties",
    "classes",
]


OAP_PROPEDIT2 = [
    "id",
    "title",
    "properties",
    "classes",
]

OAP_TEXT = [
    "id",
    "language",
    "text",
]

OAP_IMAGE = [
    "id",
    "language",
    "dpr",
    "file",
]

OAP_PROPEDITPROPS = [
    "id",
    "property",
    "condition",
    "state_restr",
]


OAP_PROPEDITCLASSES = [
    "id",
    "prop_class",
    "condition",
    "state_restr",
]


OAP_EXTMEDIA = [
    "id",
    "type",
    "media",
]

OAP_CREATEOBJ = [
    "id",
    "parent",
    "art_spec_mode",
    "package",
    "article_id",
    "var_code",
    "pos_rot_mode",
    "pos_rot_arg1",
    "pos_rot_arg2",
    "pos_rot_arg3",
]


OAP_ACTION = [
    "action",
    "condition",
    "type",
    "parameter",
    "objects",
]

OAP_ACTIONCHOICE = [
    "id",
    "title",
    "view_type",
    "argument",
    "list_id",
]

OAP_ACTIONLIST = [
    "id",
    "position",
    "condition",
    "actions",
    "text_id",
    "image_id",
]

OAP_NUMTRIPEL = [
    "id",
    "x",
    "y",
    "z",
]


OAP_SYMBOLDISPLAY = [
    "interactor",
    "hidden_mode",
    "offset_type",
    "symbol_offset",
    "direction",
    "view_angle",
    "orientation_x",
]

OAP_TYPE = [
    "type_id",
    "general_info",
    "prop_change_actions",
    "active_att_areas",
    "passive_att_areas",
    "interactors",
]


OAP_VERSION = [
    "format_version",
]

# field   1	interactor		vstring		delim ; trim hidx link
# field   2	hidden_mode		vstring		delim ; trim
# field   3	offset_type		vstring		delim ; trim
# field   4	symbol_offset		vstring		delim ; trim
# field   5	direction		vstring		delim ; trim
# field   6	view_angle		vstring		delim ; trim
# field   7	orientation_x		vstring		delim ; trim

# table oap_actionlist oap_actionlist.csv mscsv
# fields  6
# field   1	id			vstring		delim ; trim hidx link
# field   2	position		uint16		delim ; trim
# field   3	condition		vstring		delim ; trim
# field   4	actions			vstring		delim ; trim
# field   5	text_id			vstring		delim ; trim
# field   6	image_id		vstring		delim ; trim

# table oap_article2type oap_article2type.csv mscsv
# fields	6
# field	1	manufacturer_id		string 16	delim ; trim
# field	2	series_id		string 16	delim ; trim
# field	3	article_id		vstring		delim ; trim
# field	4	var_type		vstring		delim ; trim
# field	5	variant			vstring		delim ; trim
# field	6	type_id			vstring		delim ; trim
# index	btree	manufacturer_id series_id article_id
# index	btree	manufacturer_id series_id article_id var_type variant

# comment

# table oap_attacharea oap_attacharea.csv mscsv
# fields  6
# field   1	type_id			vstring		delim ; trim
# field   2	area_id			vstring		delim ; trim
# field   3	geo_type		vstring		delim ; trim
# field   4	geometry		vstring		delim ; trim
# field   5	cursor_pos		vstring		delim ; trim
# field   6	linked_areas		vstring		delim ; trim
# index	btree	type_id area_id

# table oap_attareamatch oap_attareamatch.csv mscsv
# fields  16
# field   1	active_id		vstring		delim ; trim
# field   2	passive_id		vstring		delim ; trim
# field   3	rot_axis		vstring		delim ; trim
# field   4	rotation		vstring		delim ; trim
# field   5	free_width_plus		vstring		delim ; trim
# field   6	free_width_minus	vstring		delim ; trim
# field   7	free_height_plus	vstring		delim ; trim
# field   8	free_height_minus	vstring		delim ; trim
# field   9	free_depth_plus		vstring		delim ; trim
# field  10	free_depth_minus	vstring		delim ; trim
# field  11	reverse_order		uint8		delim ; trim
# field  12	connect_type		vstring		delim ; trim
# field  13	translation_dof		vstring		delim ; trim
# field  14	rotation_dof		vstring		delim ; trim
# field  15	attach_actions		vstring		delim ; trim
# field  16	detach_actions		vstring		delim ; trim
# index  btree	active_id passive_id

# end comment

# table oap_createobj oap_createobj.csv mscsv
# fields 10
# field   1	id			vstring		delim ; trim hidx
# field   2	parent			vstring		delim ; trim
# field   3	art_spec_mode		vstring		delim ; trim
# field   4	package			vstring		delim ; trim
# field   5	article_id		vstring		delim ; trim
# field   6	var_code		vstring		delim ; trim
# field   7	pos_rot_mode		vstring		delim ; trim
# field   8	pos_rot_arg1		vstring		delim ; trim
# field   9	pos_rot_arg2		vstring		delim ; trim
# field  10	pos_rot_arg3		vstring		delim ; trim

# table oap_dimchange oap_dimchange.csv mscsv
# fields  8
# field   1	id			vstring		delim ; trim hidx link
# field   2	dimension		vstring		delim ; trim
# field   3	condition		vstring		delim ; trim
# field   4	separate		vstring		delim ; trim
# field   5	third_dim		vstring		delim ; trim
# field   6	property		vstring		delim ; trim
# field   7	multiplier		vstring		delim ; trim
# field   8	precision		vstring		delim ; trim

# table oap_extmedia oap_extmedia.csv mscsv
# fields  3
# field   1	id			vstring		delim ; trim hidx
# field   2	type			vstring		delim ; trim
# field   3	media			vstring		delim ; trim

# table oap_image oap_image.csv mscsv
# fields  4
# field   1	id			vstring		delim ; trim hidx
# field   2	language		string 5	delim ; trim
# field   3	dpr			uint8		delim ; trim
# field   4	file			vstring		delim ; trim
# index	btree	id language

# table oap_interactor oap_interactor.csv mscsv
# fields  6
# field   1	interactor		vstring		delim ; trim hidx
# field   2	condition		vstring		delim ; trim
# field   3	needs_plan_mode		vstring		delim ; trim
# field   4	actions			vstring		delim ; trim
# field   5	symbol_type		vstring		delim ; trim
# field   6	symbol_size		vstring		delim ; trim

# table oap_metatype2type oap_metatype2type.csv mscsv
# fields	6
# field	1	manufacturer		vstring		delim ; trim
# field	2	series			vstring		delim ; trim
# field	3	metatype_id		vstring		delim ; trim
# field	4	var_type		vstring		delim ; trim
# field	5	variant			vstring		delim ; trim
# field	6	type_id			vstring		delim ; trim
# index	btree	manufacturer series metatype_id
# index	btree	manufacturer series metatype_id var_type variant

# table oap_methodcall oap_methodcall.csv mscsv
# fields  5
# field   1	id			vstring		delim ; trim hidx
# field   2	type			string 8	delim ; trim
# field   3	context			vstring		delim ; trim
# field   4	method		 	vstring		delim ; trim
# field   5	arguments	 	vstring		delim ; trim

# table	oap_message oap_message.csv mscsv
# fields	3
# field	1	id			vstring		delim ; trim hidx
# field	2	arg_type		vstring		delim ; trim
# field	3	argument		vstring		delim ; trim

# table oap_numtripel oap_numtripel.csv mscsv
# fields  4
# field   1	id			vstring		delim ; trim hidx
# field   2	x			vstring		delim ; trim
# field   3	y			vstring		delim ; trim
# field   4	z			vstring		delim ; trim

# table oap_object oap_object.csv mscsv
# fields  5
# field   1	id			vstring		delim ; trim hidx
# field   2	category		vstring		delim ; trim
# field   3	argument1		vstring		delim ; trim
# field   4	argument2		vstring		delim ; trim
# field   5	argument3		vstring		delim ; trim

# table oap_propchange oap_propchange.csv mscsv
# fields  4
# field   1	id			vstring		delim ; trim hidx
# field   2	type			vstring		delim ; trim
# field   3	property		vstring		delim ; trim
# field   4	value			vstring		delim ; trim

# comment

# table oap_propedit oap_propedit.csv mscsv
# fields  5
# field   1	id			vstring		delim ; trim hidx
# field   2	title			vstring		delim ; trim
# field   3	state_restr		vstring		delim ; trim
# field   4	properties		vstring		delim ; trim
# field   5	classes			vstring		delim ; trim

# end comment

# table oap_propedit2 oap_propedit2.csv mscsv
# fields  4
# field   1	id			vstring		delim ; trim hidx
# field   2	title			vstring		delim ; trim
# field   3	properties		vstring		delim ; trim
# field   4	classes			vstring		delim ; trim

# table oap_propeditprops oap_propeditprops.csv mscsv
# fields  4
# field   1	id			vstring		delim ; trim hidx link
# field   2	property		vstring		delim ; trim
# field   3	condition		vstring		delim ; trim
# field   4	state_restr		vstring		delim ; trim

# table oap_propeditclasses oap_propeditclasses.csv mscsv
# fields  4
# field   1	id			vstring		delim ; trim hidx link
# field   2	prop_class		vstring		delim ; trim
# field   3	condition		vstring		delim ; trim
# field   4	state_restr		vstring		delim ; trim

# table oap_symboldisplay oap_symboldisplay.csv mscsv
# fields  7
# field   1	interactor		vstring		delim ; trim hidx link
# field   2	hidden_mode		vstring		delim ; trim
# field   3	offset_type		vstring		delim ; trim
# field   4	symbol_offset		vstring		delim ; trim
# field   5	direction		vstring		delim ; trim
# field   6	view_angle		vstring		delim ; trim
# field   7	orientation_x		vstring		delim ; trim

# table oap_text oap_text.csv mscsv
# fields  3
# field   1	id			vstring		delim ; trim hidx
# field   2	language		string 5	delim ; trim
# field   3	text			vstring		delim ; trim
# index	btree	id language

# table oap_type oap_type.csv mscsv
# fields	6
# field	1	type_id			vstring		delim ; trim hidx
# field	2	general_info		vstring		delim ; trim
# field	3	prop_change_actions	vstring		delim ; trim
# field	4	active_att_areas	vstring		delim ; trim
# field	5	passive_att_areas	vstring		delim ; trim
# field	6	interactors		vstring		delim ; trim

# table oap_version oap_version.csv mscsv
# fields  1
# field   1       format_version		vstring         delim ;
