from .controlmanager import ControlInterface, ControlManager


def with_ctrl_manager(klass):
    """
    A decorator to be used with ``MagicRobot`` robot classes which
    automatically processes :class:`ControlInterface` members

    Any :class:`ControlInterface` with a ``_DISPLAY_NAME`` variable
    defined will be added to a chooser on the dashboard and its associated
    methods will be automatically called
    """
    from robotpy_ext.misc.annotations import get_class_annotations

    def empty_execute(self):
        pass

    for m, ctyp in get_class_annotations(klass).items():
        if not hasattr(ctyp, "execute"):
            ctyp.execute = empty_execute

    def robotInit(_self):
        _self.__old_robotInit_ctrlmgnr()

        components = []
        for m in dir(_self):
            if m.startswith("_") or isinstance(getattr(type(_self), m, True), property):
                continue

            ctyp = getattr(_self, m, None)
            if ctyp is None:
                continue

            if not issubclass(ctyp.__class__, ControlInterface):
                continue

            components.append(ctyp)

        assert (
            len(components) > 0
        ), "No valid control components found. Do they subclass ControlInterface?"

        _self.__control_manager = ControlManager(*components)

    klass.__old_robotInit_ctrlmgnr = klass.robotInit
    klass.robotInit = robotInit

    def teleopPeriodic(_self):
        _self.__control_manager.teleopPeriodic()
        _self.__old_teleopPeriodic()

    klass.__old_teleopPeriodic = klass.teleopPeriodic
    klass.teleopPeriodic = teleopPeriodic

    return klass


def provide_setup(klass):
    """
        As the ``MagicRobot`` class uses the ``robotInit()`` method, this decorator
        provides ``MagicRobot`` classes with a ``setup()`` function that is called
        after the ``createObjects()`` function is called

        For more information, see `robotpy/robotpy-wpilib-utilities#21
        <https://github.com/robotpy/robotpy-wpilib-utilities/issues/21>`_
    """

    def robotInitSetup(_self):
        _self.__old_robotInit_setup()

        if hasattr(klass, "setup"):
            _self.setup()
        else:
            logger.warning(
                "{} was wrapped with @provide_setup but no setup() function was found".format(
                    klass
                )
            )

    klass.__old_robotInit_setup = klass.robotInit
    klass.robotInit = robotInitSetup

    return klass
