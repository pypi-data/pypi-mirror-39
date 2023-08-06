from .vars_file import VarsFile


# =============================================================================
# OSReleaseFile
# =============================================================================
class OSReleaseFile(VarsFile):

    def __init__(self, file_name=''):
        VarsFile.__init__(self, file_name)

    @property
    def name(self):
        return self.get_value('NAME')

    @name.setter
    def name(self, value):
        self.set_value('NAME', value)

    @property
    def version(self):
        return self.get_value('VERSION')

    @version.setter
    def version(self, value):
        self.set_value('VERSION', value)

    @property
    def id(self):
        return self.get_value('ID')

    @id.setter
    def id(self, value):
        self.set_value('ID', value)

    @property
    def id_like(self):
        return self.get_value('ID_LIKE')

    @id_like.setter
    def id_like(self, value):
        self.set_value('ID_LIKE', value)

    @property
    def version_code_name(self):
        return self.get_value('VERSION_CODENAME')

    @version_code_name.setter
    def version_code_name(self, value):
        self.set_value('VERSION_CODENAME', value)

    @property
    def version_id(self):
        return self.get_value('VERSION_ID')

    @version_id.setter
    def version_id(self, value):
        self.set_value('VERSION_ID', value)

    @property
    def pretty_name(self):
        return self.get_value('PRETTY_NAME')

    @pretty_name.setter
    def pretty_name(self, value):
        self.set_value('PRETTY_NAME', value)

    @property
    def ansi_color(self):
        return self.get_value('ANSI_COLOR')

    @ansi_color.setter
    def ansi_color(self, value):
        self.set_value('ANSI_COLOR', value)

    @property
    def cpe_name(self):
        return self.get_value('CPE_NAME')

    @cpe_name.setter
    def cpe_name(self, value):
        self.set_value('CPE_NAME', value)

    @property
    def home_url(self):
        return self.get_value('HOME_URL')

    @home_url.setter
    def home_url(self, value):
        self.set_value('HOME_URL', value)

    @property
    def support_url(self):
        return self.get_value('SUPPORT_URL')

    @support_url.setter
    def support_url(self, value):
        self.set_value('SUPPORT_URL', value)

    @property
    def bug_report_url(self):
        return self.get_value('BUG_REPORT_URL')

    @bug_report_url.setter
    def bug_report_url(self, value):
        self.set_value('BUG_REPORT_URL', value)

    @property
    def privacy_policy_url(self):
        return self.get_value('PRIVACY_POLICY_URL')

    @privacy_policy_url.setter
    def privacy_policy_url(self, value):
        self.set_value('PRIVACY_POLICY_URL', value)

    @property
    def build_id(self):
        return self.get_value('BUILD_ID')

    @build_id.setter
    def build_id(self, value):
        self.set_value('BUILD_ID', value)

    @property
    def variant(self):
        return self.get_value('VARIANT')

    @variant.setter
    def variant(self, value):
        self.set_value('VARIANT', value)

    @property
    def variant_id(self):
        return self.get_value('VARIANT_ID')

    @variant_id.setter
    def variant_id(self, value):
        self.set_value('VARIANT_ID', value)
