from . header import head
from .js import js
from .css import css


def list_handler(list_obj, indent):
    '''Write html code for lists in report dictionary'''
    html_string = ''
    for i, _ in enumerate(list_obj):
        if isinstance(list_obj[i], dict):
            if "name" in list_obj[i].keys():
                html_string = html_string + '  '*indent + \
                    '<li><span class="caret">' + str(list_obj[i]["name"]) + \
                    ' : ' + '</span> \n '
            else:
                html_string = html_string + '  '*indent + \
                    '<li><span class="caret">' + str(i) + ' : ' + '</span> \n '
            html_string = html_string + dict_handler(list_obj[i], indent+1)
            html_string = html_string + '  '*indent + '</li> \n '
        elif isinstance(list_obj[i], list):
            html_string = html_string + '  '*indent + \
                '<li><span class="caret">' + str(i) + ' : ' + '</span> \n '
            html_string = html_string + '  '*indent + \
                '<ul class ="nested"> \n '
            html_string = html_string + list_handler(list_obj[i], indent+1)
            html_string = html_string + '  '*indent + '</ul> \n ' + \
                '  '*indent + '</li>\n '
        else:
            html_string = html_string + ' '*indent + '<li>' + \
                '<span class="text-c">' + str(list_obj[i]) + \
                '</span>\n</li> \n '
    return html_string

# pylint: disable=too-many-branches
def dict_handler(dict_obj, indent):
    '''Writes html code for dictionary in report dictionary'''
    html_string = ''
    html_string = html_string + '  '*indent + '<ul class ="nested"> \n'
    for k, v in dict_obj.items():
        if isinstance(v, dict):
            if "name" in v.keys():
                html_string = html_string + '  '*indent + \
                    '<li><span class="caret">' + str(v["name"]) + ' : ' + \
                    '</span> \n '
            else:
                html_string = html_string + '  '*indent + \
                    '<li><span class="caret">' + str(k) + ' : ' + '</span> \n '
            html_string = html_string + dict_handler(v, indent+1) + \
                '  '*indent + '</li> \n '
        elif isinstance(v, list):
            html_string = html_string + '  '*indent + \
                '<li><span class="caret">' + str(k) + ' : ' + \
                '[%d]' % (len(v)) + '</span> \n '
            html_string = html_string + '  '*indent + \
                '<ul class ="nested"> \n ' + list_handler(v, indent+1) + \
                '  '*indent + '</ul> \n ' + '  '*indent + '</li> \n '
        else:
            html_string = html_string + ' '*indent + \
                '<li><span class="text-h">' + str(k) + ' : ' + \
                '</span><span class="text-c">' + str(v) + '</span></li>\n'
    html_string = html_string + '  '*indent + '</ul> \n '
    return html_string


def report_dict_to_html(dict_obj):
    '''Writes html code for report'''
    html_string = ''
    html_string = html_string + '<ul class ="myUL"> \n'
    html_string = html_string + \
        '<li><span class="caret">REPORT</span> \n'
    html_string = html_string + dict_handler(dict_obj, 0)
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