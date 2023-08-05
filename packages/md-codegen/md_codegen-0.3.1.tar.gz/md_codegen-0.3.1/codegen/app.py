from .download import getJson
from .githelper import has_uncommit
from codegenhelper import put_folder, log, get_tag, put_folder
import os
from fn import F
from code_engine import publish

def run(root, url, project_name, template_repo, template_tag,  username = None, password = None):
    def gen_code(app_data, project_folder):
        def fetch_template():
            return get_tag(template_repo, template_tag, log(__name__)("template_folder").debug(put_folder(".template", project_folder)))

        def gen_with_template(template_path):
            publish(template_path, app_data, project_folder)
        
        if len(os.listdir(project_folder)) == 0 or not has_uncommit(project_folder):
            (F(fetch_template) >>
            F(gen_with_template))()
        else:
            raise ValueError("the git is not configured or there is uncommitted changes in %s" % project_folder)
            
    (lambda folder_path: \
     [gen_code(log(__name__)("app_data").debug(app_data),
          put_folder(app_data["deployConfig"]["instanceName"], folder_path)) for app_data in getJson(url, project_name, username, password)])(put_folder(root))


