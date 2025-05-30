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
    # It needs to match the expected signature: (data, indent_level, current_id_val, **kwargs)
    # For theme 1, dict_handler starts with its own <ul class="nested">
    return dict_handler(report_dict, indent, current_id_val=current_id_val)


def create_html_report(report_dict, title="Report"):
    """Return the html report as a string"""
    head_content = head % css # Theme specific head

    def root_li_content_theme1(current_id):
        # Theme 1's root is simple, no IDs needed in its content.
        # Returns the HTML for inside the first <li>, and the next id.
        return '<li><span class="caret">REPORT</span>', current_id

    # Adjust body_content_func to match new signature if necessary
    # dict_handler for theme1 already returns html_string, next_id
    # The lambda below ensures correct parameters are passed.
    # indent + 1 because dict_handler expects to be inside a list item.

    # The base_create_html_report now handles the full page up to </html>
    # It also handles the outermost <ul> itself.
    # body_content_func (dict_handler for theme1) will be placed inside the root <li>

    full_html = base_create_html_report(
        report_dict,
        title=title,
        head_content=head_content,
        body_content_func=lambda rd, ind, cid: body_content_func_theme1(rd, ind + 1, cid),
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