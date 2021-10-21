import yaml
from yaml.loader import SafeLoader
import ModuleConfig
import chevron
from pathlib import Path
import os
import logging
import sys

BASE_PATH = os.environ['BASE_PATH']
LINK_BASE_PATH = os.environ['LINK_BASE_PATH']
OUTPUT_DIR = os.environ['OUTPUT_DIR']

# set log level
logging.basicConfig(level=logging.INFO)

def get_modules_config():
    modules = []
    with open('../markupFilesConfig.yaml') as f:
        data = yaml.load(f, Loader=SafeLoader)
        modules_config = data["modules"]

        for key, m in modules_config.items():
            module = ModuleConfig.ModuleConfig(m["name"], m["md-file-name"], m["template-file"], m["example-rdf"],
                                               m["shex"])
            modules.append(module)
    return modules

def get_file_content(file):
    try:
        if os.path.isfile(file):
            file_txt = Path(file).read_text()
            return file_txt
        else:
            raise Exception("File doesn't exist " + file + ". Check markupFileConfig file.")
    except Exception as e:
        logging.error(e)
        sys.exit(1)


def generate_md_files(modules):
    for m in modules:
        rdf_figure_path = LINK_BASE_PATH + m.EXAMPLE_RDF["figure-file-path"]
        rdf_file = BASE_PATH + m.EXAMPLE_RDF["file-path"]
        rdf_txt = get_file_content(rdf_file)

        shex_figure_path = LINK_BASE_PATH + m.SHEX["figure-file-path"]
        shex_file = BASE_PATH + m.SHEX["file-path"]
        shex_txt = get_file_content(shex_file)

        # create module markup
        with open(m.TEMPLATE_FILE, 'r') as f:
            md_text = chevron.render(f, {'text': m.EXAMPLE_RDF["text"], 'semantic-model-figure-path': rdf_figure_path,
                                              'example-rdf': rdf_txt, 'shex-figure-path': shex_figure_path,
                                         'shex': shex_txt, 'title': m.NAME})
            print(md_text)

            output_file = OUTPUT_DIR + m.MD_FILE_NAME
            file = open(output_file, "w")
            file.write(md_text)
            file.close()


if __name__ == '__main__':
    modules = get_modules_config()
    generate_md_files(modules)



