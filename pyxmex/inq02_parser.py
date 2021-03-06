from yaml import load, FullLoader
from six import iteritems
import os
from . import utils
from .parser import Parser

class INQ02Parser(Parser):
    def __init__(self, config_file=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config/inq02.yml')):
        super(self.__class__, self).__init__()

        with open(config_file) as file:
            config = load(file, Loader=FullLoader)

        self.inq02_generic_config = config['INQUIRY_DETAIL_RECORD_GENERIC']
        self.inq02_case_config = config['INQUIRY_DETAIL_RECORD_CASE_TYPE_SPECIFIC']

    def process_lines(self, content):
        result = []

        # remove the unneeded header and footer
        del content[0]
        del content[-1]

        for line in content:
            fields = self._parse_line(self.inq02_generic_config['FIELDS'], line)
            case_type = utils.range_from_list(line, *self.inq02_case_config['TYPE_FIELD'])
            fields.update(self._parse_line(self.inq02_case_config['TYPES'][case_type]['FIELDS'], line))

            result.append(fields)

        return result
