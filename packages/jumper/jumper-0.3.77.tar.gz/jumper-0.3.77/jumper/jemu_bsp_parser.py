"""
:copyright: (c) 2017 by Jumper Labs Ltd.
:license: Apache 2.0, see LICENSE.txt for more details.
"""
import os
import json
from .jemu_button import JemuButton
from .jemu_i2c_master import JemuI2cMaster
from .jemu_i2c_slave import JemuI2cSlave
from .jemu_mem_peripheral import JemuMemPeripheral
from .jemu_bma280 import JemuBMA280
from .jemu_sudo import JemuSudo
from .jemu_bq24160 import JemuBQ24160
from .jemu_bq27421 import JemuBQ27421
from .platforms import platforms_list_upper


class JemuBspParser:
    _EXTERNAL_PERIPHERAL = "External"
    _bsp_json_path = None

    def __init__(self, bsp_json_path):
        self._bsp_json_path = bsp_json_path
        self._platform = None

    # def get_platform(self):
    #     return self._platform

    def get_components(self, jemu_connection, gdb_mode):
        components_list = []

        if not os.path.isfile(self._bsp_json_path):
            raise Exception(self._bsp_json_path + ' is not found')
        elif not os.access(self._bsp_json_path, os.R_OK):
            raise Exception(self._bsp_json_path + ' is not readable')
        else:
            with open(self._bsp_json_path) as bsp_json_file:
                bsp_json = json.load(bsp_json_file)

                for component in bsp_json["components"]:
                    component_id = component["id"]
                    component_obj = None

                    if ("config" in component) and ("generators" in component["config"]):
                        generators = component["config"]["generators"]
                    else:
                        generators = None

                    if 'class' in component:
                        if component["class"] == "Button":
                            component_obj = JemuButton(jemu_connection, component_id)

                        elif component["class"] == "I2cSlaveSdk":
                            component_obj = JemuI2cSlave(jemu_connection, component_id)

                        elif component["class"] == "I2cMasterSdk":
                            component_obj = JemuI2cMaster(jemu_connection, component_id)

                        elif component["class"] == "BME280":
                            component_obj = JemuMemPeripheral(jemu_connection, component_id, self._EXTERNAL_PERIPHERAL, generators)

                        elif component["class"] == "BQ24160":
                            component_obj = JemuBQ24160(jemu_connection, component_id, self._EXTERNAL_PERIPHERAL, generators)

                        elif component["class"] == "BQ27421":
                            component_obj = JemuBQ27421(jemu_connection, component_id, self._EXTERNAL_PERIPHERAL, generators)

                        elif component["class"] == "BMA280":
                            component_obj = JemuBMA280(jemu_connection, component_id, self._EXTERNAL_PERIPHERAL, generators)

                        elif any(component["class"] in p for p in platforms_list_upper):
                            name = component["class"].lower()
                            name = 'stm32f411' if name == 'stm32f4' else 'nrf52832' if name == 'mcu' else name  # backward compatibility
                            peripheral_obj = JemuSudo(jemu_connection, 39, name, gdb_mode)
                            components_list.append({"obj": peripheral_obj, "name": "SUDO"})
                            self._platform = name
                    elif 'type' in component:
                        if component["type"] == "Peripheral":
                            component_obj = JemuMemPeripheral(jemu_connection, component_id, self._EXTERNAL_PERIPHERAL, generators)

                    if component_obj is not None:
                        components_list.append({"obj": component_obj, "name": component["name"]})

            return components_list, self._platform
