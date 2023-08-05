import voluptuous as vol

import esphomeyaml.config_validation as cv
from esphomeyaml import pins
from esphomeyaml.const import CONF_BAUD_RATE, CONF_ID, CONF_RX_PIN, CONF_TX_PIN
from esphomeyaml.helpers import App, Pvariable, esphomelib_ns, setup_component, Component

UARTComponent = esphomelib_ns.class_('UARTComponent', Component)
UARTDevice = esphomelib_ns.class_('UARTDevice')

UART_SCHEMA = vol.All(vol.Schema({
    cv.GenerateID(): cv.declare_variable_id(UARTComponent),
    vol.Optional(CONF_TX_PIN): pins.output_pin,
    vol.Optional(CONF_RX_PIN): pins.input_pin,
    vol.Required(CONF_BAUD_RATE): cv.positive_int,
}).extend(cv.COMPONENT_SCHEMA.schema), cv.has_at_least_one_key(CONF_TX_PIN, CONF_RX_PIN))

CONFIG_SCHEMA = vol.All(cv.ensure_list, [UART_SCHEMA])


def to_code(config):
    for conf in config:
        tx = conf.get(CONF_TX_PIN, -1)
        rx = conf.get(CONF_RX_PIN, -1)
        rhs = App.init_uart(tx, rx, conf[CONF_BAUD_RATE])
        var = Pvariable(conf[CONF_ID], rhs)

        setup_component(var, conf)


BUILD_FLAGS = '-DUSE_UART'
