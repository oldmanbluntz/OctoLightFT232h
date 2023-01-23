Just a test to get this plugin to work with CircuitPython's digitalio instead of RPI.GPIO

Forked from Gigibu5/OctoLight

Still trying to figure out the last few things. Any help would be appreciated. It installs. It activates. It won't turn the light on and off. Currently a problem with line 121. Here is thr output in the log. There are 2 parts.

2023-01-23 10:50:34,281 - octoprint.plugin.core - ERROR - Exception while executing injection factory <function settings_plugin_inject_factory.<locals>.f at 0x7ff3febff640>
Traceback (most recent call last):
  File "/home/octo/OctoPrint/venv/lib/python3.10/site-packages/octoprint/plugin/core.py", line 1946, in initialize_implementation
    return_value = factory(name, implementation)
  File "/home/octo/OctoPrint/venv/lib/python3.10/site-packages/octoprint/__init__.py", line 448, in f
    settings.add_overlay(default_settings_overlay, at_end=True)
  File "/home/octo/OctoPrint/venv/lib/python3.10/site-packages/octoprint/settings.py", line 1304, in add_overlay
    overlay_yaml = yaml.dump(overlay)
  File "/home/octo/OctoPrint/venv/lib/python3.10/site-packages/octoprint/util/yaml.py", line 87, in dump
    return _save_to_file_base(data, file=None, pretty=pretty, **kwargs)
  File "/home/octo/OctoPrint/venv/lib/python3.10/site-packages/octoprint/util/yaml.py", line 51, in _save_to_file_base
    return yaml.dump(
  File "/home/octo/OctoPrint/venv/lib/python3.10/site-packages/yaml/__init__.py", line 290, in dump
    return dump_all([data], stream, Dumper=Dumper, **kwds)
  File "/home/octo/OctoPrint/venv/lib/python3.10/site-packages/yaml/__init__.py", line 278, in dump_all
    dumper.represent(data)
  File "/home/octo/OctoPrint/venv/lib/python3.10/site-packages/yaml/representer.py", line 27, in represent
    node = self.represent_data(data)
  File "/home/octo/OctoPrint/venv/lib/python3.10/site-packages/yaml/representer.py", line 48, in represent_data
    node = self.yaml_representers[data_types[0]](self, data)
  File "/home/octo/OctoPrint/venv/lib/python3.10/site-packages/yaml/representer.py", line 207, in represent_dict
    return self.represent_mapping('tag:yaml.org,2002:map', data)
  File "/home/octo/OctoPrint/venv/lib/python3.10/site-packages/yaml/representer.py", line 118, in represent_mapping
    node_value = self.represent_data(item_value)
  File "/home/octo/OctoPrint/venv/lib/python3.10/site-packages/yaml/representer.py", line 48, in represent_data
    node = self.yaml_representers[data_types[0]](self, data)
  File "/home/octo/OctoPrint/venv/lib/python3.10/site-packages/yaml/representer.py", line 207, in represent_dict
    return self.represent_mapping('tag:yaml.org,2002:map', data)
  File "/home/octo/OctoPrint/venv/lib/python3.10/site-packages/yaml/representer.py", line 118, in represent_mapping
    node_value = self.represent_data(item_value)
  File "/home/octo/OctoPrint/venv/lib/python3.10/site-packages/yaml/representer.py", line 48, in represent_data
    node = self.yaml_representers[data_types[0]](self, data)
  File "/home/octo/OctoPrint/venv/lib/python3.10/site-packages/yaml/representer.py", line 207, in represent_dict
    return self.represent_mapping('tag:yaml.org,2002:map', data)
  File "/home/octo/OctoPrint/venv/lib/python3.10/site-packages/yaml/representer.py", line 118, in represent_mapping
    node_value = self.represent_data(item_value)
  File "/home/octo/OctoPrint/venv/lib/python3.10/site-packages/yaml/representer.py", line 58, in represent_data
    node = self.yaml_representers[None](self, data)
  File "/home/octo/OctoPrint/venv/lib/python3.10/site-packages/yaml/representer.py", line 231, in represent_undefined
    raise RepresenterError("cannot represent an object", data)
yaml.representer.RepresenterError: ('cannot represent an object', <digitalio.DigitalInOut object at 0x7ff3feb70340>)
2023-01-23 10:50:34,283 - octoprint.plugin.core - INFO - Initialized 35 plugin implementation(s)
2023-01-23 10:50:34,309 - octoprint - ERROR - Error while trying to migrate settings for plugin octolightft232h, ignoring it
Traceback (most recent call last):
  File "/home/octo/OctoPrint/venv/lib/python3.10/site-packages/octoprint/__init__.py", line 495, in init_settings_plugin_config_migration_and_cleanup
    settings_plugin_config_migration_and_cleanup(
  File "/home/octo/OctoPrint/venv/lib/python3.10/site-packages/octoprint/__init__.py", line 487, in settings_plugin_config_migration_and_cleanup
    implementation.on_settings_cleanup()
  File "/home/octo/OctoPrint/venv/lib/python3.10/site-packages/octoprint/util/__init__.py", line 1688, in wrapper
    return f(*args, **kwargs)
  File "/home/octo/OctoPrint/venv/lib/python3.10/site-packages/octoprint/plugin/types.py", line 1981, in on_settings_cleanup
    config = self._settings.get_all_data(
AttributeError: 'NoneType' object has no attribute 'get_all_data'

and further down in the log:

2023-01-23 10:50:37,622 - octoprint.plugin - ERROR - Error while calling plugin octolightft232h
Traceback (most recent call last):
  File "/home/octo/OctoPrint/venv/lib/python3.10/site-packages/octoprint/plugin/__init__.py", line 273, in call_plugin
    result = getattr(plugin, method)(*args, **kwargs)
  File "/home/octo/OctoPrint/venv/lib/python3.10/site-packages/octoprint/util/__init__.py", line 1688, in wrapper
    return f(*args, **kwargs)
  File "/home/octo/OctoPrint/venv/lib/python3.10/site-packages/octoprint_octolightft232h/__init__.py", line 121, in on_event
    self._plugin_manager.send_plugin_message(self._identifier, dict(isLightOn=self.led.value))
AttributeError: 'OctoLightFT232HPlugin' object has no attribute 'led'
