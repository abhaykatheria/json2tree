from .header import head
from .js import js
from .css import css
from ..html_base import base_list_handler, base_dict_handler, base_create_html_report

# Theme 2 Specific: Prefix function for list items and dict items
def item_prefix_theme2(item_id, item_name, is_expandable):
    # is_expandable helps decide if the checkbox is needed or if it's a leaf node in terms of interaction
    # However, theme2 seems to put checkboxes on all items.
    # For simple values (not dict/list), they are wrapped in <ul><li><span class="tree_label">value</span></li></ul>
    # The base_dict_handler or base_list_handler will handle the value itself if not is_expandable.
    # This prefix should then only create the part before the value or nested list/dict.
    return f'<li><input type="checkbox" checked="checked" id="c{item_id}" /><label for="c{item_id}" class="tree_label">{item_name}</label>'

# Theme 2 Specific: Suffix function for list items and dict items
def item_suffix_theme2(item_id):
    return f'</li>'

def list_handler(list_obj, indent, current_id_val=0, **kwargs):
    """Writes html code for lists in report dictionary for Theme 2"""
    return base_list_handler(
        data=list_obj,
        indent_level=indent,
        list_item_tag="li", # Not strictly used if item_prefix_func is comprehensive
        list_class="",
        text_class="tree_label", # Class for simple text items if not handled by prefix/suffix
        nested_list_tag="ul",
        nested_list_class="", # Theme 2 uses plain <ul> for nesting
        dict_handler_func=dict_handler, # Pass the theme's dict_handler
        item_prefix_func=item_prefix_theme2,
        item_suffix_func=item_suffix_theme2,
        current_id_val=current_id_val,
        # Kwargs for dict_handler_func when called from base_list_handler
        # None needed specifically for dict_handler that are not already params of base_dict_handler itself
    )

def dict_handler(dict_obj, indent, current_id_val=0, **kwargs):
    """Writes html code for dictionary in report dictionary for Theme 2"""
    html_parts = []
    # Theme 2 wraps dictionary content directly in <ul>.
    # The base_dict_handler will then call item_prefix_theme2 for each <li>.
    html_parts.append('  ' * indent + '<ul>\n')
    generated_html, next_id = base_dict_handler(
        data=dict_obj,
        indent_level=indent + 1,
        dict_item_tag="li", # Not strictly used due to item_prefix_func
        dict_key_class="tree_label", # Fallback if prefix func not used
        dict_value_class="tree_label", # Fallback if prefix func not used
        nested_list_tag="ul",
        nested_list_class="", # Theme 2 uses plain <ul>
        list_handler_func=list_handler, # Pass the theme's list_handler
        item_prefix_func=item_prefix_theme2,
        item_suffix_func=item_suffix_theme2,
        current_id_val=current_id_val,
        text_class="tree_label", # Passed to base_dict_handler for simple values
        # Kwargs for list_handler_func when called from base_dict_handler
        # None needed specifically for list_handler that are not already params of base_list_handler itself
    )
    html_parts.append(generated_html)
    html_parts.append('  ' * indent + '</ul>\n')
    return "".join(html_parts), next_id


def body_content_func_theme2(report_dict, indent, current_id_val=0):
    # This function will be called by base_create_html_report.
    # It needs to match the expected signature: (data, indent_level, current_id_val, **kwargs)
    return dict_handler(report_dict, indent, current_id_val=current_id_val)


def create_html_report(report_dict, title="Report"):
    """Return the html report as a string for Theme 2"""
    head_content = head % css # Theme specific head

    def root_li_content_theme2(current_id):
        # Theme 2's root. current_id is c0 for the root.
        # Returns the HTML for the root <li>, and the next id (c1).
        html = f'<li><input type="checkbox" checked="checked" id="c{current_id}"/> <label class="tree_label" for="c{current_id}">ROOT</label>'
        return html, current_id + 1

    full_html = base_create_html_report(
        report_dict,
        title=title,
        head_content=head_content,
        body_content_func=lambda rd, ind, cid: body_content_func_theme2(rd, ind, cid),
        root_ul_tag_and_class='ul class="tree"', # Tag and class for the outermost <ul>
        root_li_content_func=root_li_content_theme2,
        initial_id=0 # Start ID generation from 0 for "c0"
    )
    # Append theme-specific JS before closing body and html tags
    return full_html.replace("</body>", js + "\n</body>")


# def get_report_dict(image_obj_list):
#     '''Given an image object list, return a python dict of the report'''
#     image_list = []
#     for image in image_obj_list:
#         image_list.append({'image': image.to_dict()})
#     image_dict = {'images': image_list}
#     return image_dict


# def generate(self, image_obj_list):
#     '''Given a list of image objects, create a html report
#     for the images'''
#     report_dict = get_report_dict(image_obj_list)
#     report = create_html_report(report_dict, image_obj_list)
#     return report