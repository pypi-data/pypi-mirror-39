import voluptuous as vol

import esphomeyaml.config_validation as cv
from esphomeyaml import pins
from esphomeyaml.components import display, spi
from esphomeyaml.components.spi import SPIComponent
from esphomeyaml.const import CONF_CS_PIN, CONF_DC_PIN, CONF_EXTERNAL_VCC, \
    CONF_ID, CONF_MODEL, \
    CONF_RESET_PIN, CONF_SPI_ID, CONF_LAMBDA
from esphomeyaml.helpers import App, Pvariable, add, get_variable, \
    gpio_output_pin_expression, process_lambda, setup_component, PollingComponent

DEPENDENCIES = ['spi']

SSD1306 = display.display_ns.class_('SSD1306', PollingComponent, display.DisplayBuffer)
SPISSD1306 = display.display_ns.class_('SPISSD1306', SSD1306, spi.SPIDevice)
SSD1306Model = display.display_ns.enum('SSD1306Model')

MODELS = {
    'SSD1306_128X32': SSD1306Model.SSD1306_MODEL_128_32,
    'SSD1306_128X64': SSD1306Model.SSD1306_MODEL_128_64,
    'SSD1306_96X16': SSD1306Model.SSD1306_MODEL_96_16,
    'SSD1306_64X48': SSD1306Model.SSD1306_MODEL_64_48,
    'SH1106_128X32': SSD1306Model.SH1106_MODEL_128_32,
    'SH1106_128X64': SSD1306Model.SH1106_MODEL_128_64,
    'SH1106_96X16': SSD1306Model.SH1106_MODEL_96_16,
    'SH1106_64X48': SSD1306Model.SH1106_MODEL_64_48,
}

SSD1306_MODEL = vol.All(vol.Upper, vol.Replace(' ', '_'), cv.one_of(*MODELS))

PLATFORM_SCHEMA = display.FULL_DISPLAY_PLATFORM_SCHEMA.extend({
    cv.GenerateID(): cv.declare_variable_id(SPISSD1306),
    cv.GenerateID(CONF_SPI_ID): cv.use_variable_id(SPIComponent),
    vol.Required(CONF_CS_PIN): pins.gpio_output_pin_schema,
    vol.Required(CONF_DC_PIN): pins.gpio_output_pin_schema,
    vol.Required(CONF_MODEL): SSD1306_MODEL,
    vol.Optional(CONF_RESET_PIN): pins.gpio_output_pin_schema,
    vol.Optional(CONF_EXTERNAL_VCC): cv.boolean,
}).extend(cv.COMPONENT_SCHEMA.schema)


def to_code(config):
    for spi_ in get_variable(config[CONF_SPI_ID]):
        yield
    for cs in gpio_output_pin_expression(config[CONF_CS_PIN]):
        yield
    for dc in gpio_output_pin_expression(config[CONF_DC_PIN]):
        yield

    rhs = App.make_spi_ssd1306(spi_, cs, dc)
    ssd = Pvariable(config[CONF_ID], rhs)
    add(ssd.set_model(MODELS[config[CONF_MODEL]]))

    if CONF_RESET_PIN in config:
        for reset in gpio_output_pin_expression(config[CONF_RESET_PIN]):
            yield
        add(ssd.set_reset_pin(reset))
    if CONF_EXTERNAL_VCC in config:
        add(ssd.set_external_vcc(config[CONF_EXTERNAL_VCC]))
    if CONF_LAMBDA in config:
        for lambda_ in process_lambda(config[CONF_LAMBDA],
                                      [(display.DisplayBufferRef, 'it')]):
            yield
        add(ssd.set_writer(lambda_))

    display.setup_display(ssd, config)
    setup_component(ssd, config)


BUILD_FLAGS = '-DUSE_SSD1306'
