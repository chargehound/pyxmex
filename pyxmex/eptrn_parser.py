from yaml import load, FullLoader
from six import iteritems
import os
from . import utils
from .parser import Parser

class EPTRNParser(Parser):
    def __init__(self, config_file=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config/eptrn.yml')):
        super(self.__class__, self).__init__()

        with open(config_file) as file:
            config = load(file, Loader=FullLoader)

        self.eptrn_config = config['DETAIL_RECORD']
        self.section_types = [v for k, v in iteritems(self.eptrn_config['TYPE_MAPPING'])]

    def process_lines(self, content):
        result = {}

        for section_type in self.section_types:
            result[section_type] = []

        # remove the unneeded header and footer
        del content[0]
        del content[-1]

        for line in content:
            # find out what type of information this line contains
            section_type_mapping_key = utils.range_from_list(line, *self.eptrn_config['TYPE_FIELD'])
            section_type_name = self.eptrn_config['TYPE_MAPPING'][section_type_mapping_key]
            field_formats = self.eptrn_config['TYPES'][section_type_name]['FIELDS']

            # parse this line according to what type it is
            result[section_type_name].append(self._parse_line(field_formats, line))

        return result
