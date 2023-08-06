import argparse
#configuration utilities
class ArgsUtil(object):

    @staticmethod
    def loadArgumentParseModule(params = []):
        parser = argparse.ArgumentParser()
        #default params
        parser.add_argument("--debug", default='0', help="debug level", required=False)
        parser.add_argument("--test", default='0', help="test run", required=False)
        if params:
            for item in params:
                if 'name' in item and 'default' in item and 'help' in item and 'required' in item:
                    if 'choices' in item:
                        parser.add_argument('--' + item['name'] , default=item['default'], help=item['help'], required=item['required'], choices=item['choices'])
                    else:
                        parser.add_argument('--' + item['name'] , default=item['default'], help=item['help'], required=item['required'])
                else:
                    return False
        args = parser.parse_args()
        return args

