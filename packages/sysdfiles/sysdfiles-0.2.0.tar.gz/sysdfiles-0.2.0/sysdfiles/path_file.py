from .unit_file import UnitFile


# =============================================================================
# PathFile
# =============================================================================
class PathFile(UnitFile):

    def __init__(self, file_name=''):
        UnitFile.__init__(self, file_name)
        self.add_properties('path',
                            [['directory_mode', 'fm'],
                             ['directory_not_empty', 'l', '', 1],
                             ['make_directory', 'b'],
							 ['path_changed', 'l', '', 1],
                             ['path_exists', 'l', '', 1],
                             ['path_exists_glob', 'l', '', 1],
                             ['path_modified', 'l', '', 1],
                             ['unit']])
