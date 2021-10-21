import yaml
from yaml.loader import SafeLoader
import ModuleConfig
import MarkupFilesUtils
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

if __name__ == '__main__':
    modules = get_modules_config()

    mf_utils = MarkupFilesUtils.MarkupFilesUtils(modules)
    mf_utils.check_md_support_files()



