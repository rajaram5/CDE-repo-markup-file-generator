import yaml
from yaml.loader import SafeLoader
import ModuleConfig
import MarkupFilesUtils
import os
import logging

# set log level
logging.basicConfig(level=logging.INFO)

def get_modules_config():
    modules = []
    markup_config_file = os.environ['MARKUP_CONFIG_FILE']
    with open(markup_config_file) as f:
        data = yaml.load(f, Loader=SafeLoader)
        modules_config = data["modules"]

        for key, m in modules_config.items():
            module = ModuleConfig.ModuleConfig(m["name"], m["md-file-name"], m["template-file"], m["example-rdf"],
                                               m["shex"])
            modules.append(module)
    return modules

if __name__ == '__main__':
    job = os.environ['JOB_TO_RUN']
    job = job.upper()
    modules = get_modules_config()
    mf_utils = MarkupFilesUtils.MarkupFilesUtils(modules)

    if job == "CHECK SUPPORTING FILES":
        logging.info("Check if markup supporting files exits")
        mf_utils.check_md_support_files()
    elif job == "UPDATE MD FILES":
        logging.info("Update markup files")
        mf_utils.check_md_support_files()
        mf_utils.generate_md_files()
    else:
        logging.info("Unknown job. Please use of these jobs [CHECK SUPPORTING FILES, UPDATE MD FILES]")




