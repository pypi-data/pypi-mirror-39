from .download import getJson
from .githelper import has_uncommit
from codegenhelper import put_folder, log, get_tag, put_folder
import os
from fn import F
from code_engine import publish
import demjson
from deep_mapper import process_mapping

def run(root, url, project_name, template_repo, template_tag, username = None, password = None, jsonstr = None, datafile = None):
    def get_data():
        def get_from_data(data):
            return data if data and isinstance(data, list) else [data] if data else None

        def get_from_file():
            return get_from_data(demjson.decode_file(datafile) if datafile and os.path.exists(datafile) else None)

        return get_from_data(demjson.decode(jsonstr) if jsonstr else None) or get_from_file()

    def fetch_template():
        return get_tag(template_repo, template_tag, log(__name__)("template_folder").debug(put_folder(".template", root)))
    
    def gen_code(app_data, project_folder, template_path):
        def gen_with_template(template_path):
            publish(template_path, app_data, project_folder)
        
        if len(os.listdir(project_folder)) == 0 or not has_uncommit(project_folder):
            gen_with_template(template_path)
        else:
            raise ValueError("the git is not configured or there is uncommitted changes in %s" % project_folder)

    def get_project_name(jsonData, template_path):
        def map_project_name(project_name_map_file):
            if not os.path.exists(project_name_map_file):
                raise ValueError("the map file is not available--%s" % project_name_map_file)

            return process_mapping(jsonData, demjson.decode_file(project_name_map_file), "/")["project_name"]
        
        return jsonData["project_name"] if "project_name" in jsonData else map_project_name(os.path.join(template_path, ".mapper"))
        
    
    (lambda folder_path, template_path: \
     [gen_code(log(__name__)("app_data").debug(app_data),
               put_folder(get_project_name(app_data, template_path), folder_path), template_path) for app_data in get_data() or getJson(url, project_name, username, password)])(put_folder(root), fetch_template())


