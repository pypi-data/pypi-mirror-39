

class Parameters:

    def __init__(self, first_approach_param):
        self.param = first_approach_param

    def build(self):
        if self.is_loading_from_file():
            self.check_commands_from_file()
        return self.param

    def is_loading_from_file(self):
        return self.check_param("ext_config", False)

    def check_param(self, param, default):
        if param in self.param.keys():
            return self.param[param]
        return default

    def check_commands_from_file(self):
        with open('./cronably.txt', 'r') as crx:
            for value in crx:
                command = value.strip().split('=')
                key = command[0]
                value = command[1].upper() if key=='name' else command[1].lower()
                self.param[command[0].lower()] = value

    def has_to_make_reports(self):
        return self.check_param('report', 'N').upper() == 'Y'
