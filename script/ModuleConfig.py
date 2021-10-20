class ModuleConfig:
    NAME = None
    MD_FILE_NAME = None
    TEMPLATE_FILE = None
    EXAMPLE_RDF = {}
    SHEX = {}

    def __init__(self, name, md_file_name, template_file, example_rdf, shex):
        self.NAME = name
        self.MD_FILE_NAME = md_file_name
        self.TEMPLATE_FILE = template_file
        self.EXAMPLE_RDF = example_rdf
        self.SHEX = shex