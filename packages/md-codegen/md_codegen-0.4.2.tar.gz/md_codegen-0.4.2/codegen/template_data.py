from .download import getJson
import os
import demjson
from  deep_mapper import process_mapping

class TemplateData:
    def __init__(self):
        def func(project_name):
            def get_project_name(jsonData, template_path):
                def map_project_name(project_name_map_file):
                    if not os.path.exists(project_name_map_file):
                        raise ValueError("the map file is not available--%s" % project_name_map_file)

                    return process_mapping(jsonData, demjson.decode_file(project_name_map_file), "/")[project_name]

                return jsonData[project_name] if project_name in jsonData else map_project_name(os.path.join(template_path, ".mapper"))

            self.get_project_name = get_project_name


            # get_project_name

            def get_data(url, project, username, password, jsonstr, datafile):
                    def get_local_data():
                        def get_from_data(data):
                            return data if data and isinstance(data, list) else [data] if data else None

                        def get_from_file():
                            if datafile and not os.path.exists(datafile):
                                raise ValueError("the data file is not existing. Please check %s" % datafile)

                            return get_from_data(demjson.decode_file(datafile) if datafile and os.path.exists(datafile) else None)

                        return get_from_data(demjson.decode(jsonstr) if jsonstr else None) or get_from_file()

                    def get_default_data():
                        return [{project_name: project}]


                    return get_local_data() or getJson(url, project, username, password) or get_default_data()

            self.get_data = get_data
            
            # get_data
        func("project_name")
