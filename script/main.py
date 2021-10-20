import yaml
from yaml.loader import SafeLoader
import ModuleConfig
import chevron
from pathlib import Path

BASE_PATH = None
LINK_BASE_PATH = None
OUTPUT_DIR = None

def get_modules_config():
    modules = []
    global BASE_PATH
    global LINK_BASE_PATH
    global OUTPUT_DIR

    with open('../markupFilesConfig.yaml') as f:
        data = yaml.load(f, Loader=SafeLoader)

        BASE_PATH = data["base-path"]
        LINK_BASE_PATH = data["links-base-path"]
        OUTPUT_DIR = data["output-dir"]
        modules_config = data["modules"]

        for key, m in modules_config.items():
            module = ModuleConfig.ModuleConfig(m["name"], m["md-file-name"], m["template-file"], m["example-rdf"],
                                               m["shex"])
            modules.append(module)
        print(data)
    return modules

if __name__ == '__main__':
    modules = get_modules_config()

    for m in modules:
        rdf_figure_path = LINK_BASE_PATH + m.EXAMPLE_RDF["figure-file-path"]
        rdf_file = BASE_PATH + m.EXAMPLE_RDF["file-path"]
        rdf_txt = Path(rdf_file).read_text()

        shex_figure_path = LINK_BASE_PATH + m.SHEX["figure-file-path"]
        shex_file = BASE_PATH + m.SHEX["file-path"]
        shex_txt = Path(rdf_file).read_text()

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

