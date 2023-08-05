import logging

import voluptuous as vol

from esphomeyaml import core
import esphomeyaml.config_validation as cv
from esphomeyaml.const import CONF_ID, CONF_OTA, CONF_PASSWORD, CONF_PORT, CONF_SAFE_MODE, \
    ESP_PLATFORM_ESP32, ESP_PLATFORM_ESP8266
from esphomeyaml.core import ESPHomeYAMLError
from esphomeyaml.helpers import App, Pvariable, add, esphomelib_ns, Component

_LOGGER = logging.getLogger(__name__)

OTAComponent = esphomelib_ns.class_('OTAComponent', Component)

CONFIG_SCHEMA = vol.Schema({
    cv.GenerateID(): cv.declare_variable_id(OTAComponent),
    vol.Optional(CONF_SAFE_MODE, default=True): cv.boolean,
    vol.Optional(CONF_PORT): cv.port,
    vol.Optional(CONF_PASSWORD): cv.string,
})


def to_code(config):
    rhs = App.init_ota()
    ota = Pvariable(config[CONF_ID], rhs)
    if CONF_PASSWORD in config:
        add(ota.set_auth_password(config[CONF_PASSWORD]))
    if CONF_PORT in config:
        add(ota.set_port(config[CONF_PORT]))
    if config[CONF_SAFE_MODE]:
        add(ota.start_safe_mode())


def get_port(config):
    if CONF_PORT in config[CONF_OTA]:
        return config[CONF_OTA][CONF_PORT]
    if core.ESP_PLATFORM == ESP_PLATFORM_ESP32:
        return 3232
    elif core.ESP_PLATFORM == ESP_PLATFORM_ESP8266:
        return 8266
    raise ESPHomeYAMLError(u"Invalid ESP Platform for ESP OTA port.")


def get_auth(config):
    return config[CONF_OTA].get(CONF_PASSWORD, '')


BUILD_FLAGS = '-DUSE_OTA'
REQUIRED_BUILD_FLAGS = '-DUSE_NEW_OTA'


def lib_deps(config):
    if core.ESP_PLATFORM == ESP_PLATFORM_ESP32:
        return ['ArduinoOTA', 'Update', 'ESPmDNS']
    return ['Hash', 'ESP8266mDNS', 'ArduinoOTA']
