from typing import List

import wpilib
from networktables.util import ChooserControl

import logging

logger = logging.getLogger("marsutils")

__all__ = ["ControlManager", "ControlInterface", "with_ctrl_manager"]


class ControlInterface:
    _DISPLAY_NAME: str
    _SORT = 0

    def teleopPeriodic(self):
        pass

    def enabled(self):
        pass

    def disabled(self):
        pass


class ControlManager:
    __slots__ = [
        "control_mode",
        "control_interfaces",
        "control_chooser",
        "control_chooser_control",
    ]

    def __init__(
        self, *interfaces: ControlInterface, dashboard_key: str = "Control Mode"
    ):
        assert len(interfaces) > 0, "No control interfaces given"

        # Sort the interfaces by their _SORT values
        interfaces = tuple(sorted(interfaces, key=lambda x: x._SORT, reverse=True))

        self.control_mode = None
        self.control_interfaces: List[ControlInterface] = []

        self.control_chooser = wpilib.SendableChooser()

        for i, mode in enumerate(interfaces):
            if not hasattr(mode, "_DISPLAY_NAME"):
                logger.error(
                    f'Control interface {mode.__class__.__name__} has no "_DISPLAY_NAME" attr, \
                    skipping'
                )
                continue
            if not isinstance(mode._DISPLAY_NAME, str):
                logger.error(
                    f'Control interface {mode.__class__.__name__} has non-string "_DISPLAY_NAME" \
                    attr'
                )
                continue
            self.control_interfaces.append(mode)
            # Make the first entry the default
            # TODO: Configurable?
            if i == 0:
                self.control_chooser.addDefault(mode._DISPLAY_NAME, i)
            else:
                self.control_chooser.addObject(mode._DISPLAY_NAME, i)

        wpilib.SmartDashboard.putData(dashboard_key, self.control_chooser)

        self.control_chooser_control = ChooserControl(
            dashboard_key, on_selected=self.control_mode_changed
        )

    def teleopPeriodic(self):
        if self.control_mode is not None:
            self.control_mode.teleopPeriodic()

    def control_mode_changed(self, new_value):
        """
            Network tables callback to update control mode
        """
        new_selected: int = self.control_chooser.getSelected()
        if new_selected is None:
            return
        if new_selected >= len(self.control_interfaces):
            logger.error(f"Invalid control mode: {new_selected}")
            return
        if self.control_mode != self.control_interfaces[new_selected]:
            if self.control_mode is not None:
                self.control_mode.disabled()
            self.control_mode = self.control_interfaces[new_selected]
            if self.control_mode is not None:
                self.control_mode.enabled()


def with_ctrl_manager(klass):
    from robotpy_ext.misc.annotations import get_class_annotations

    def empty_execute(self):
        pass

    for m, ctyp in get_class_annotations(klass).items():
        if not hasattr(ctyp, "execute"):
            ctyp.execute = empty_execute

    def robotInit(_self):
        _self.__old_robotInit()

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

    klass.__old_robotInit = klass.robotInit
    klass.robotInit = robotInit

    def teleopPeriodic(_self):
        _self.__control_manager.teleopPeriodic()
        _self.__old_teleopPeriodic()

    klass.__old_teleopPeriodic = klass.teleopPeriodic
    klass.teleopPeriodic = teleopPeriodic

    return klass
