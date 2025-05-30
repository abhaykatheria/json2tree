def base_list_handler(data, indent_level, list_item_tag, list_class, text_class,
                      nested_list_tag, nested_list_class, dict_handler_func,
                      item_prefix_func=None, item_suffix_func=None, current_id_val=0, **kwargs):
    """
    Base handler for list objects.
    item_prefix_func and item_suffix_func allow themes to inject custom HTML.
    current_id_val is used for themes that need unique IDs.
    """
    html_parts = []
    next_id = current_id_val
    for i, item in enumerate(data):
        item_id = next_id
        next_id +=1

        prefix = item_prefix_func(item_id, str(i) if not isinstance(item, dict) or "name" not in item else item["name"], isinstance(item, (dict,list))) if item_prefix_func else f"<{list_item_tag} class='{text_class if isinstance(item, (str, int, float, bool)) else ''}'>"
        html_parts.append(f"{'  ' * indent_level}{prefix}")

        if isinstance(item, dict):
            # Pass next_id to dict_handler, it returns the next available id
            returned_html, next_id_from_dict = dict_handler_func(item, indent_level + 1, current_id_val=next_id, **kwargs)
            html_parts.append(returned_html)
            next_id = next_id_from_dict # Update next_id with the value returned from the recursive call
        elif isinstance(item, list):
            html_parts.append(f"\n{'  ' * (indent_level + 1)}<{nested_list_tag} class='{nested_list_class}'>\n")
            # Pass next_id to recursive call, it returns the next available id
            returned_html, next_id_from_list = base_list_handler(item, indent_level + 2, list_item_tag, list_class, text_class,
                                                      nested_list_tag, nested_list_class, dict_handler_func,
                                                      item_prefix_func, item_suffix_func, current_id_val=next_id, **kwargs)
            html_parts.append(returned_html)
            next_id = next_id_from_list # Update next_id
            html_parts.append(f"{'  ' * (indent_level + 1)}</{nested_list_tag}>\n{'  ' * indent_level}")
        else:
            html_parts.append(str(item))

        suffix = item_suffix_func(item_id) if item_suffix_func else f"</{list_item_tag}>"
        html_parts.append(f"{suffix}\n")
    return "".join(html_parts), next_id

def base_dict_handler(data, indent_level, dict_item_tag, dict_key_class, dict_value_class,
                      nested_list_tag, nested_list_class, list_handler_func,
                      caret_span_class=None, item_prefix_func=None, item_suffix_func=None, current_id_val=0, **kwargs):
    """
    Base handler for dict objects.
    item_prefix_func and item_suffix_func allow themes to inject custom HTML for each key-value pair.
    current_id_val is used for themes that need unique IDs.
    """
    html_parts = []
    next_id = current_id_val
    for key, value in data.items():
        item_id = next_id
        next_id += 1

        key_display = str(key)
        if isinstance(value, dict) and "name" in value: # Special case from theme1 for list of dicts
            key_display = str(value["name"])

        prefix = item_prefix_func(item_id, key_display, isinstance(value, (dict,list))) if item_prefix_func else f"<{dict_item_tag}>"
        html_parts.append(f"{'  ' * indent_level}{prefix}")

        if not item_prefix_func: # Default rendering of key if no prefix function
            if caret_span_class and isinstance(value, (dict, list)):
                html_parts.append(f"<span class='{caret_span_class}'>{key_display}</span>")
            else:
                html_parts.append(f"<span class='{dict_key_class}'>{key_display}</span>")

        if isinstance(value, dict):
            html_parts.append(f"\n{'  ' * (indent_level + 1)}<{nested_list_tag} class='{nested_list_class}'>\n")
            # Pass next_id, it returns the next available id
            returned_html, next_id_from_dict = base_dict_handler(value, indent_level + 2, dict_item_tag, dict_key_class, dict_value_class,
                                                      nested_list_tag, nested_list_class, list_handler_func,
                                                      caret_span_class, item_prefix_func, item_suffix_func, current_id_val=next_id, **kwargs)
            html_parts.append(returned_html)
            next_id = next_id_from_dict # Update next_id
            html_parts.append(f"{'  ' * (indent_level + 1)}</{nested_list_tag}>\n{'  ' * indent_level}")
        elif isinstance(value, list):
            list_len_display = f" [{len(value)}]" if kwargs.get('show_list_len') else "" # Theme 1 specific
            if item_prefix_func: # If theme handles prefix, it handles the key display
                 pass # key is already in prefix by item_prefix_func
            elif caret_span_class: # Theme 1 specific for list
                html_parts.append(f"{list_len_display}") # Key already added, add length for theme 1 list

            html_parts.append(f"\n{'  ' * (indent_level + 1)}<{nested_list_tag} class='{nested_list_class}'>\n")
            # Pass next_id, it returns the next available id
            # list_handler_func is the THEME's list_handler, which should also return (html, next_id)
            returned_html, next_id_from_list = list_handler_func(value, indent_level + 2, current_id_val=next_id, **kwargs)
            html_parts.append(returned_html)
            next_id = next_id_from_list # Update next_id
            html_parts.append(f"{'  ' * (indent_level + 1)}</{nested_list_tag}>\n{'  ' * indent_level}")
        else:
            if not item_prefix_func: # Default rendering of value if no prefix function
                html_parts.append(f": <span class='{dict_value_class}'>{value}</span>")
            else: # Theme 2 specific for simple value
                # For theme 2, simple values are wrapped in <ul><li><span class="tree_label">value</span></li></ul>
                # The item_prefix_func handles the outer parts. Here we add the specific value formatting.
                 html_parts.append(f"<ul><li><span class='{kwargs.get(\"text_class\", \"\")}'>{value}</span></li></ul>")


        suffix = item_suffix_func(item_id) if item_suffix_func else f"</{dict_item_tag}>"
        html_parts.append(f"{suffix}\n")
    return "".join(html_parts), next_id

def base_create_html_report(report_dict, title, head_content, body_content_func, root_ul_tag_and_class, root_li_content_func, initial_id=0):
    """
    Base function to create an HTML report.
    root_li_content_func is a function that takes the initial_id and returns HTML string for the root li.
    It also returns the next id to be used.
    """
    root_li_html, next_id = root_li_content_func(initial_id)
    html_content, _ = body_content_func(report_dict, 0, current_id_val=next_id) # body_content_func should now also return next_id

    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8"/>
<title>{title}</title>
{head_content}
</head>
<body>
<{root_ul_tag_and_class}>
  {root_li_html}
  {html_content}
</{root_ul_tag_and_class.split(' ')[0]}>
</body>
</html>
"""
