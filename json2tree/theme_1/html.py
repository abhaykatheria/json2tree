from .header import head
from .js import js
from .css import css
from ..html_base import base_list_handler, base_dict_handler, base_create_html_report

def list_handler(list_obj, indent, current_id_val=0, **kwargs):
    """Writes html code for lists in report dictionary"""
    # Theme 1 does not use item_prefix_func or item_suffix_func, relies on default tag generation.
    # It also doesn't use IDs, so current_id_val is passed but not used for element IDs.
    return base_list_handler(
        data=list_obj,
        indent_level=indent,
        list_item_tag="li",
        list_class="",
        text_class="text-c",
        nested_list_tag="ul",
        nested_list_class="nested",
        dict_handler_func=dict_handler, # Pass the theme's dict_handler
        current_id_val=current_id_val,
        # Pass Theme 1 specific params for dict_handler when it's called by base_list_handler
        # These are kwargs to base_list_handler, which passes them to dict_handler_func
        dict_item_tag="li", # kwarg for dict_handler_func
        dict_key_class="text-h", # kwarg for dict_handler_func
        dict_value_class="text-c", # kwarg for dict_handler_func
        caret_span_class="caret", # kwarg for dict_handler_func
        show_list_len=True # kwarg for dict_handler_func (used in base_dict_handler for lists)
    )

def dict_handler(dict_obj, indent, current_id_val=0, **kwargs):
    """Writes html code for dictionary in report dictionary"""
    html_parts = []
    # This initial <ul class="nested"> is for the current dictionary itself.
    html_parts.append('  ' * indent + '<ul class="nested">\n')

    # Theme 1 does not use item_prefix_func or item_suffix_func
    # It relies on the default key/value rendering in base_dict_handler
    generated_html, next_id = base_dict_handler(
        data=dict_obj,
        indent_level=indent + 1, # Indent for items within this dict's list
        dict_item_tag="li",
        dict_key_class="text-h",
        dict_value_class="text-c",
        nested_list_tag="ul",
        nested_list_class="nested",
        list_handler_func=list_handler, # Pass the theme's list_handler
        caret_span_class="caret",
        current_id_val=current_id_val,
         # Pass Theme 1 specific params for list_handler when it's called by base_dict_handler
        list_item_tag="li", # kwarg for list_handler_func
        list_class="", # kwarg for list_handler_func
        text_class="text-c", # kwarg for list_handler_func
        show_list_len=True # kwarg for list_handler_func (used in base_dict_handler for lists)
    )
    html_parts.append(generated_html)
    html_parts.append('  ' * indent + '</ul>\n')
    return "".join(html_parts), next_id


def body_content_func_theme1(report_dict, indent, current_id_val=0):
    # This function will be called by base_create_html_report.
    # indent will be 0 as passed by the modified lambda.
    if isinstance(report_dict, dict):
        # dict_handler creates its own surrounding <ul class="nested">
        return dict_handler(report_dict, indent, current_id_val=current_id_val)
    elif isinstance(report_dict, list):
        # list_handler returns a string of <li> items.
        # These need to be wrapped in a <ul> if the root itself is a list.
        # The content from this function is placed *inside* the "REPORT" <li>.
        list_html, next_id = list_handler(report_dict, indent, current_id_val=current_id_val)
        # Since list_handler itself does not add the outer ul for the root list case.
        return f"<ul class='nested'>\n{list_html}</ul>\n", next_id
    else:
        # Fallback for simple types as root. Wrap in <li> to fit theme structure.
        # This will be placed inside the "REPORT" <li>.
        escaped_report_dict = str(report_dict).replace('<', '&lt;').replace('>', '&gt;')
        return f"<li><span class='text-c'>{escaped_report_dict}</span></li>", current_id_val


def create_html_report(report_dict, title="Report"):
    """Return the html report as a string"""
    head_content = head % css # Theme specific head

    def root_li_content_theme1(current_id):
        # Theme 1's root is simple, no IDs needed in its content.
        # Returns the HTML for inside the first <li>, and the next id.
        return '<li><span class="caret">REPORT</span>', current_id # This <li> is closed by base_create_html_report

    full_html = base_create_html_report(
        report_dict,
        title=title,
        head_content=head_content,
        # Pass indent as is (0), body_content_func_theme1 now handles it correctly for root elements
        body_content_func=lambda rd, ind, cid: body_content_func_theme1(rd, ind, cid),
        root_ul_tag_and_class='ul class="myUL"', # Tag and class for the outermost <ul>
        root_li_content_func=root_li_content_theme1, # Function to generate root li content
        initial_id=0 # Theme 1 doesn't use IDs, so this is nominal.
    )
    # The base function now creates the full HTML structure.
    # We just need to append the theme-specific JS.
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