"""
Support for controlling Lutron Homeworks Series 4 and 8 systems.

Michael Dubno - 2018 - New York
"""
import logging
import voluptuous as vol
from homeassistant.const import (
    EVENT_HOMEASSISTANT_STOP, CONF_HOST, CONF_PORT)
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = ['pyhomeworks==0.0.1']

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'homeworks'

HOMEWORKS_CONTROLLER = 'homeworks'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_PORT): cv.port,
    }),
}, extra=vol.ALLOW_EXTRA)


def setup(hass, base_config):
    """Start Homeworks controller."""
    from pyhomeworks.pyhomeworks import Homeworks

    class HomeworksController(Homeworks):
        """Interface between HASS and Homeworks controller."""

        def __init__(self, host, port):
            """Host and port of Lutron Homeworks controller."""
            Homeworks.__init__(self, host, port, self._callback)
            self._subscribers = {}

        def register(self, device):
            """Add a device to subscribe to events."""
            if device.addr not in self._subscribers:
                self._subscribers[device.addr] = []
            self._subscribers[device.addr].append(device)

        def _callback(self, msg_type, values):
            _LOGGER.debug('_callback: %s, %s', msg_type, values)
            addr = values[0]
            for sub in self._subscribers.get(addr,[]):
                _LOGGER.debug("_callback: %s", sub)
                if sub.callback(msg_type, values):
                    sub.schedule_update_ha_state()

    config = base_config.get(DOMAIN)
    host = config[CONF_HOST]
    port = config[CONF_PORT]

    controller = HomeworksController(host, port)
    hass.data[HOMEWORKS_CONTROLLER] = controller

    def cleanup(event):
        controller.close()

    hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, cleanup)
    return True


class HomeworksDevice():
    """Base class of a Homeworks device."""

    def __init__(self, controller, addr, name):
        """Controller, address, and name of the device."""
        self._addr = addr
        self._name = name
        self._controller = controller
        controller.register(self)

    @property
    def addr(self):
        """Device address."""
        return self._addr

    @property
    def name(self):
        """Device name."""
        return self._name

    @property
    def should_poll(self):
        """No need to poll."""
        return False

    def callback(self, msg_type, values):
        """Must be replaced with device callbacks."""
        return False
