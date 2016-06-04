# packages required for framework integration
import core.module
# module specific packages
import lib.dns.resolver


class Module(core.module.Module):
    def __init__(self, params):
        # initialize the module
        # the "query" parameter is optional and determines the "default" source of input
        # the "SOURCE" option is only avilable if the "query" parameter is provided
        core.module.Module.__init__(self, params, query='SELECT DISTINCT host FROM hosts WHERE host IS NOT NULL')
        # register local options
        # the "register_option" method expects 4 arguments:
        # 1. the name of the option
        # 2. the default value of the option (strings, integers and boolean values are allowed)
        # 3. "yes" or "no" for whether or not the option is mandatory
        # 4. a description of the option
        self.register_option('nameserver', '8.8.8.8', 'yes', 'ip address of a valid nameserver')
        # define descriptive metadata
        # all items are optional and may be omitted
        self.info = {
            'Name': 'Hostname Resolver',
            'Author': 'Tim Tomes (@LaNMaSteR53)',
            'Version': 'v0.0.1',
            'Description': 'Resolves IP addresses to hosts and updates the database with the results.',
            'Comments': [
                'Note: Nameserver must be in IP form.',
                ],
            }

    # optional method
    def module_pre(self):
        value=None
        # override this method to execute code prior to calling the "module_run" method
        # returned values are passed to the "module_run" method and must be captured in a parameter
        return value

    # mandatory method
    # the second parameter is required to capture the result of the "SOURCE" option, which means that it is only required if the query parameter is provided in the __init__ method
    # the third parameter is required if a value is returned from the "module_pre" method
    def module_run(self, hosts, value):
        # do something leveraging the api methods discussed below
        # local option values can be accessed via self.options['name']
        # global option values can be accessed via self.global_options['name']
        # use the 'self.workspace' class property to access the workspace location
        return