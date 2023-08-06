from .vars_file import VarsFile


# =============================================================================
# MachineInfoFile
# =============================================================================
class MachineInfoFile(VarsFile):

    def __init__(self, file_name=''):
        VarsFile.__init__(self, file_name)

    @property
    def pretty_host_name(self):
        return self.get_value('PRETTY_HOSTNAME')

    @pretty_host_name.setter
    def pretty_host_name(self, value):
        self.set_value('PRETTY_HOSTNAME', value)

    @property
    def icon_name(self):
        return self.get_value('ICON_NAME')

    @icon_name.setter
    def icon_name(self, value):
        self.set_value('ICON_NAME', value)

    @property
    def chassis(self):
        return self.get_value('CHASSIS')

    @chassis.setter
    def chassis(self, value):
        self.set_value('CHASSIS', value)

    @property
    def deployment(self):
        return self.get_value('DEPLOYMENT')

    @deployment.setter
    def deployment(self, value):
        self.set_value('DEPLOYMENT', value)

    @property
    def location(self):
        return self.get_value('LOCATION')

    @location.setter
    def location(self, value):
        self.set_value('LOCATION', value)
