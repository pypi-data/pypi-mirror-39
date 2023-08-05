from .download import getJson
from .githelper import has_uncommit
from codegenhelper import put_folder, log, get_tag, put_folder
import os
from fn import F
from code_engine import publish
import demjson
from deep_mapper import process_mapping
from .template_data import TemplateData

def run(root, url, project_name, template_repo, template_tag, username = None, password = None, jsonstr = None, datafile = None, template_path = None):

    def fetch_template():
        return get_tag(template_repo, template_tag, log(__name__)("template_folder").debug(put_folder(".template", root)))
    
    def gen_code(app_data, project_folder, template_path):
        def gen_with_template(template_path):
            try:
                publish(template_path, app_data, project_folder)
            except Exception as e:
                log(__name__)("gen_code_error").debug(e)
                log(__name__)("gen_code_app_data").debug(app_data)
                log(__name__)("gen_code_project_folder").debug(project_folder)
                log(__name__)("gen_code_template_path").debug(template_path)
                raise e
                
                
        
        if len(os.listdir(project_folder)) == 0 or not has_uncommit(project_folder):
            gen_with_template(template_path)
        else:
            raise ValueError("the git is not configured or there is uncommitted changes in %s" % project_folder)


    
    (lambda folder_path, template_path, template_data: \
     [gen_code(log(__name__)("app_data").debug(app_data),
               log(__name__)("project_path").debug(put_folder(template_data.get_project_name(app_data, template_path), folder_path)),
               log(__name__)("template_path").debug(template_path)) for app_data in template_data.get_data(url, project_name, username, password, jsonstr, datafile)])(put_folder(root), template_path or fetch_template(), TemplateData())


