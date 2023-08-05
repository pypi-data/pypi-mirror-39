import json
import uuid

import ipywidgets as widgets
# from IPython.display import display
from IPython.core.display import display
from IPython.display import display_javascript, display_html, JSON, Javascript


def button(text):
    return widgets.Checkbox(
        value=False,
        description=text,
        disabled=False
    )


def container(stuff):
    return widgets.VBox(stuff)


def to_output(content):
    """
    returns how ipython displays content by default
    """
    x = widgets.Output()
    with x:
        display(content)
    return x


def tab_with_content(content_dict):
    """
    Creates a tab with dicts where keys are tabnames and content are the content of the tab ...
    """
    tab = widgets.Tab()
    keys = list(content_dict.keys())
    tab.children = [content_dict[k] for k in keys]
    for (i,title) in enumerate(keys):
        tab.set_title(i, title)
    return tab


def set_id_for_dom_element_of_output_for_current_cell(_id):
    display(Javascript('console.log(element.get(0)); element.get(0).id = "{}";'.format(_id)))


class RenderJSON(object):
    def __init__(self, json_data):
        if isinstance(json_data, dict):
            self.json_str = json.dumps(json_data)
        elif isinstance(json_data, JSON):
            self.json_str = json_data.data
        else:
            self.json_str = json_data
        self.uuid = str(uuid.uuid4())

    def _ipython_display_(self):
        display_html('<div id="{}" style="height: 600px; width:100%;"></div>'.format(self.uuid), raw=True)
        js = """
            require(["https://rawgit.com/caldwell/renderjson/master/renderjson.js"], function() {{
                renderjson.set_icons('+', '-');
                renderjson.set_show_to_level("2");
                document.getElementById('{}').appendChild(renderjson({}))
            }});
        """
        display_javascript(js.format(self.uuid, self.json_str), raw=True)
