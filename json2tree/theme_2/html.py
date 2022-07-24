from .header import head
from .js import js
from .css import css


def list_handler(list_obj, indent,id):
    '''Write html code for lists in report dictionary'''
    html_string = ''
    for i, _ in enumerate(list_obj):
        if isinstance(list_obj[i], dict):
            if "name" in list_obj[i].keys():
                html_string = html_string + '  '*indent + \
                    '<li><input type="checkbox" checked="checked" id="c%s" /><label for="c%s" class="tree_label">'%(str(id), str(id)) \
                        + str(list_obj[i]["name"]) +  \
                    '</label> \n '
            else:
                html_string = html_string + '  '*indent + \
                    '<li><input type="checkbox" checked="checked" id="c%s" /><label for="c%s" class="tree_label">'%(str(id), str(id)) \
                        + str(i) +  \
                    '</label> \n '
            id = id + 1
            html_string = html_string + dict_handler(list_obj[i], indent+1,id+1)
            
            html_string = html_string + '  '*indent + '</li> \n '
        elif isinstance(list_obj[i], list):
            html_string = html_string + '  '*indent + \
                    '<li><input type="checkbox" checked="checked" id="c%s" /><label for="c%s" class="tree_label">'%(str(id), str(id)) \
                        + str(i) +  \
                    '</label> \n '
            id = id + 1
            html_string = html_string + '  '*indent + \
                '<ul> \n ' + list_handler(list_obj[i], indent+1,id+1) + \
                '  '*indent + '</ul> \n ' + '  '*indent + '</li> \n '
        else:
            html_string = html_string + '  '*indent + \
                    '<li><input type="checkbox" checked="checked" id="c%s" /><label for="c%s" class="tree_label">'%(str(id), str(id)) \
                        + str(i) +  \
                    '</label> \n <ul><li><span class="tree_label">'+str(list_obj[i])+'</span></li></ul> </li>\n'
            id = id + 1
    return html_string

# pylint: disable=too-many-branches
def dict_handler(dict_obj, indent, id):
    '''Writes html code for dictionary in report dictionary'''
    html_string = ''
    html_string = html_string + '  '*indent + '<ul> \n'
    for k, v in dict_obj.items():
        if isinstance(v, dict):
            if "name" in v.keys():
                html_string = html_string + '  '*indent + \
                    '<li><input type="checkbox" checked="checked" id="c%s" /><label for="c%s" class="tree_label">'%(str(id), str(id)) \
                        + str(v["name"]) +  \
                    '</label> \n '
            else:
                html_string = html_string + '  '*indent + \
                    '<li><input type="checkbox" checked="checked" id="c%s" /><label for="c%s" class="tree_label">'%(str(id), str(id)) \
                        + str(k) +  \
                    '</label> \n '
            id = id + 1
            html_string = html_string + dict_handler(v, indent+1, id+1) + \
                '  '*indent + '</li> \n '
            
        elif isinstance(v, list):
            html_string = html_string + '  '*indent + \
                    '<li><input type="checkbox" checked="checked" id="c%s" /><label for="c%s" class="tree_label">'%(str(id), str(id)) \
                        + str(k) +  \
                    '</label> \n '
            id = id + 1
            html_string = html_string + '  '*indent + \
                '<ul> \n ' + list_handler(v, indent+1, id+1) + \
                '  '*indent + '</ul> \n ' + '  '*indent + '</li> \n '
            
        else:
            html_string = html_string + '  '*indent + \
                    '<li><input type="checkbox" checked="checked" id="c%s" /><label for="c%s" class="tree_label">'%(str(id), str(id)) \
                        + str(k) +  \
                    '</label> \n <ul><li><span class="tree_label">'+str(v)+'</span></li></ul> </li>\n'
            id = id + 1
    html_string = html_string + '  '*indent + '</ul> \n '
    return html_string


def report_dict_to_html(dict_obj):
    '''Writes html code for report'''
    html_string = ''
    html_string = html_string + '<ul class ="tree"> \n'
    html_string = html_string + \
        '<li> <input type="checkbox" checked="checked" id="c0"/> <label class="tree_label" for="c0">ROOT</label> \n'
    html_string = html_string + dict_handler(dict_obj, 0, 1)
    html_string = html_string + '</li></ul> \n'
    return html_string

def create_html_report(report_dict):
    '''Return the html report as a string'''
    # logger.debug("Creating HTML report...")
    report = ''
    report = report + '\n' + head % css
    report = report + '\n' + report_dict_to_html(report_dict)
    report = report + '\n' + js
    report = report + '\n' + '</body>\n</html>\n'
    return report


def get_report_dict(image_obj_list):
    '''Given an image object list, return a python dict of the report'''
    image_list = []
    for image in image_obj_list:
        image_list.append({'image': image.to_dict()})
    image_dict = {'images': image_list}
    return image_dict



def generate(self, image_obj_list):
    '''Given a list of image objects, create a html report
    for the images'''
    report_dict = get_report_dict(image_obj_list)
    report = create_html_report(report_dict, image_obj_list)
    return report