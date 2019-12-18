from feature_tree import *

# def gen_markdown_readme(ft, directory):

#     def gen_table(ft):

#         def gen_feature(feature, tree_level=0):

#             out = "|{}|{}|{}|{}|{}|{}|{}|{}| \n".format(
                
#                         "&nbsp; &nbsp; "*tree_level + feature.longname,
#                         feature.description,
#                         feature.stage_mask if feature.is_leaf_node() else "",
#                         feature.combine if not feature.is_leaf_node() else "",
#                         feature.weight,
#                         feature.scale if feature.is_leaf_node() else "",
#                         feature.num_dims if feature.is_leaf_node() else "",
#                         feature.bdc)

#             for f in feature.sub_features:
#                 out += gen_feature(f, tree_level+1)

#             return out
        
#         return  ("<div style='width:290px'><font size='+1'>\n\n" + 
#                     "|Feature Name|Description|Stage Mask|Combine|Weight|Scale|# Dims|BDC| \n" +
#                     "|---|---|---|---|---|---|---|---| \n" +
#                     gen_feature(ft.root, 0) + "</font></div>")

#     # Read details template
#     with open(directory + "/details.md", 'r') as file:
#         details = file.read()

#     # Generate file
#     with open(directory + "/README.md", "w+") as file:
#         file.write(details.replace("<table_placeholder>", gen_table(ft)))


def gen_markdown_readme(ft, directory):

    def gen_table(ft):

        eval_done = ft.is_eval_done()

        def gen_feature(feature, tree_level=0, prefix_str=""):

            anchor = ""
            if tree_level > 0:
                if prefix_str:
                    anchor += prefix_str + "--"
                anchor += feature.longname.strip().lower().replace(" ", "-")

            out = ( "{}**{}**{}" + 
                    " {}{}</br>" + 
                    " {} {} {}{} \n").format(

                        "  "*tree_level + "- ",
                        "[{}](#{})".format(feature.longname.strip(), anchor),
                        (": " + feature.description.strip())
                            if feature.description else "",
                        ("</br>*num_dims =* " + str(feature.num_dims) + "; ")
                            if eval_done and feature.is_leaf_node() else "",
                        ("*BDC =* **" + str(feature.bdc) + "**")
                            if eval_done else "",
                        ("*stage_mask =* " + str(feature.stage_mask) + "; ")
                            if feature.is_leaf_node() else "",
                        ("*combine =* " + str(feature.combine) + "; ")
                            if not feature.is_leaf_node() else "",
                        ("*scale =* " + str(feature.scale) + "; ")
                            if feature.is_leaf_node() else "",
                        ("*weight =* " + str(feature.weight)))

            for f in feature.sub_features:
                out += gen_feature(f, tree_level+1, anchor)

            return out
        
        return  ("\n\n" + gen_feature(ft.root, 0) + "")

    # Read details template
    with open(directory + "/.template.md", 'r') as file:
        details = file.read()

    # Generate file
    with open(directory + "/README.md", "w+") as file:
        file.write(details.replace("<table_placeholder>", gen_table(ft)))

    logging.info("Generated markdown files at: " + directory)
