import os
import sys
import chevron
from pathlib import Path
import logging

class MarkupFilesUtils:
    BASE_PATH = os.environ['BASE_PATH']
    LINK_BASE_PATH = os.environ['LINK_BASE_PATH']
    OUTPUT_DIR = os.environ['OUTPUT_DIR']
    MODULES = None
    # set log level
    logging.basicConfig(level=logging.INFO)

    def __init__(self, modules):
        self.MODULES = modules

    def get_file_content(self, file):
        """
        This method gets content of a file as a string. This method throws an error if the file doesn't exits.
        """
        try:
            if os.path.isfile(file):
                file_txt = Path(file).read_text()
                return file_txt
            else:
                raise Exception("File doesn't exist " + file + ". Check markupFileConfig file.")
        except Exception as e:
            logging.error(e)
            sys.exit(1)

    def check_md_support_files(self):
        """
        This method checks if the supporting files of markup exits. Like example RDF and ShEx files.
        The method throws an error and exit if file doesn't exits.
        """
        for m in self.MODULES:
            rdf_file = self.BASE_PATH + m.EXAMPLE_RDF["file-path"]
            self.get_file_content(rdf_file)

            shex_file = self.BASE_PATH + m.SHEX["file-path"]
            self.get_file_content(shex_file)
        logging.info("All supporting files to generate markup's exits")

    def generate_md_files(self):
        """
        This method generates CDE model's repositories markup files. This methods throws an error if the file doesn't
        exits.
        """
        for m in self.MODULES:
            rdf_figure_path = self.LINK_BASE_PATH + m.EXAMPLE_RDF["figure-file-path"]
            rdf_file = self.BASE_PATH + m.EXAMPLE_RDF["file-path"]
            rdf_txt = self.get_file_content(rdf_file)

            shex_figure_path = self.LINK_BASE_PATH + m.SHEX["figure-file-path"]
            shex_file = self.BASE_PATH + m.SHEX["file-path"]
            shex_txt = self.get_file_content(shex_file)

            markup_files = {}
            # create module markup
            with open(m.TEMPLATE_FILE, 'r') as f:
                md_text = chevron.render(f,
                                         {'text': m.EXAMPLE_RDF["text"], 'semantic-model-figure-path': rdf_figure_path,
                                          'example-rdf': rdf_txt, 'shex-figure-path': shex_figure_path,
                                          'shex': shex_txt, 'title': m.NAME})
                print(md_text)
                output_file = self.OUTPUT_DIR + m.MD_FILE_NAME
                markup_files[output_file] = md_text

            for file_path, content in markup_files.items():
                file = open(file_path, "w")
                file.write(content)
                file.close()