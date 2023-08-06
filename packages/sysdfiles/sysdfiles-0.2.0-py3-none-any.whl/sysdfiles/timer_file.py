from .unit_file import UnitFile


# =============================================================================
# TimerFile
# =============================================================================
class TimerFile(UnitFile):

    def __init__(self, file_name=''):
        UnitFile.__init__(self, file_name)
        self.add_properties('timer',
                            [['accuracy_sec', 'ns'],
                             ['on_active_sec', 'ns'],
                             ['on_boot_sec', 'ns'],
                             ['on_calendar', 'l', '', 1],
                             ['on_startup_sec', 'ns'],
                             ['on_unit_active_sec', 'ns'],
                             ['on_unit_inactive_sec', 'ns'],
                             ['persistent', 'b'],
                             ['randomized_delay_sec', 'ns'],
                             ['remain_after_elapse', 'b'],
                             ['unit'],
                             ['wake_system', 'b']])
