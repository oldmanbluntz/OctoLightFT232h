# coding=utf-8
from __future__ import absolute_import



import octoprint.plugin

class OctoLightFT232HPlugin(
		octoprint.plugin.AssetPlugin,
		octoprint.plugin.StartupPlugin,
		octoprint.plugin.TemplatePlugin,
		octoprint.plugin.SimpleApiPlugin,
		octoprint.plugin.SettingsPlugin,
		octoprint.plugin.EventHandlerPlugin,
		octoprint.plugin.RestartNeedingPlugin
	):

  
	light_state = False
	

	# put your plugin's default settings here
	def get_settings_defaults(self):
        return dict(
		self.led = DigitalInOut(board.D4),
		self.led_direction = Direction.OUTPUT,
		
           
        )

  
	def get_template_configs(self):
	return [
		dict(type="navbar", custom_bindings=True),
		dict(type="settings", custom_bindings=True),
	]    

	def get_assets(self):
        return dict(
            "js": ["js/octolightft232h.js"],
            "css": ["css/octolightft232h.css"],
            "less": ["less/octolightft232h.less"]
        )

	def on_after_startup(self):
		led.value = False
		self._logger.info("--------------------------------------------")
		self._logger.info("OctoLightFT232H Started")
		self._logger.info("--------------------------------------------")

		# Setting the default state of pin
		DigitalInOut(board.D4)
		
		if bool Direction.OUTPUT:
			self.led.value = True
		else:
			self.led.value = False

		self._plugin_manager.send_plugin_message(self._identifier, dict(isLightOn=self.light_state))

	def light_toggle(self):
		# Sets the GPIO every time, if user changed it in the settings.
		Direction.OUTPUT
		self.light_state = not self.light_state

		# Sets the light state depending on the inverted output setting (XOR)
		if self.light_state ^ Direction.OUTPUT:
			self.led.value = True
		else:
			self.led.value = False

		self._logger.info("Got request. Light state: {}".format(
			self.light_state
		))

		self._plugin_manager.send_plugin_message(self._identifier, dict(isLightOn=self.light_state))

def on_api_get(self, request):
		action = request.args.get('action', default="toggle", type=str)

		if action == "toggle":
			self.light_toggle()

			return flask.jsonify(state=self.light_state)

		elif action == "getState":
			return flask.jsonify(state=self.light_state)

		elif action == "turnOn":
			if not self.light_state:
				self.led.value = True

			return flask.jsonify(state=self.light_state)

		elif action == "turnOff":
			if self.light_state:
				self.led.value = False

			return flask.jsonify(state=self.light_state)

		else:
			return flask.jsonify(error="action not recognized")

	def on_event(self, event, payload):
		if event == Events.CLIENT_OPENED:
			self._plugin_manager.send_plugin_message(self._identifier, dict(isLightOn=self.light_state))
			return

   
    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "octolightft232h": {
                "displayName": "Octolightft232h Plugin",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "OldMaNBlunTZ",
                "repo": "OctoPrint-Octolightft232h",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/OldMaNBlunTZ/OctoPrint-Octolightft232h/archive/{target_version}.zip",
            }
        }



__plugin_pythoncompat__ = ">=3,<4"  # Only Python 3

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = Octolightft232hPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
