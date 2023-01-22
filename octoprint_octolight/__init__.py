# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import octoprint.plugin
from octoprint.events import Events
import flask
import board
import os
from digitalio import DigitalInOut, Direction, Pull




class OctoLightPlugin(
		octoprint.plugin.AssetPlugin,
		octoprint.plugin.StartupPlugin,
		octoprint.plugin.TemplatePlugin,
		octoprint.plugin.SimpleApiPlugin,
		octoprint.plugin.SettingsPlugin,
		octoprint.plugin.EventHandlerPlugin,
		octoprint.plugin.RestartNeedingPlugin
	):

	light_state = False

	def get_settings_defaults(self):
		return dict(
			light_pin = DigitalInOut(board.D4),
			inverted_output = Direction.OUTPUT
		)

	def get_template_configs(self):
		return [
			dict(type="navbar", custom_bindings=True),
			dict(type="settings", custom_bindings=True)
		]

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/octolight.js"],
			css=["css/octolight.css"],
			#less=["less/octolight.less"]
		)

	def on_after_startup(self):
		self.light_state = False
		self._logger.info("--------------------------------------------")
		self._logger.info("OctoLight started, listening for GET request")
		self._logger.info("Light pin: {}, inverted_input: {}".format(
			self._settings.get(["light_pin"]),
			self._settings.get(["inverted_output"])
		))
		self._logger.info("--------------------------------------------")

		# Setting the default state of pin
		DigitalInOut(int(self._settings.get(["light_pin"])), Direction.OUTPUT)
		if bool(self._settings.get(["inverted_output"])):
			Direction.OUTPUT(int(self._settings.get(["light_pin"])), Pull.UP)
		else:
			Direction.OUTPUT(int(self._settings.get(["light_pin"])), Pull.DOWN)

		#Because light is set to ff on startup we don't need to retrieve the current state
		"""
		r = self.light_state = Direction.INPUT(int(self._settings.get(["light_pin"])))
        if r==1:
                self.light_state = False
        else:
                self.light_state = True
        self._logger.info("After Startup. Light state: {}".format(
                self.light_state
        ))
        """

		self._plugin_manager.send_plugin_message(self._identifier, dict(isLightOn=self.light_state))

	def light_toggle(self):
		# Sets the GPIO every time, if user changed it in the settings.
		DigitalInOut(int(self._settings.get(["light_pin"])), Direction.OUTPUT)

		self.light_state = not self.light_state

		# Sets the light state depending on the inverted output setting (XOR)
		if self.light_state ^ self._settings.get(["inverted_output"]):
			Direction.OUTPUT(int(self._settings.get(["light_pin"])), Pull.UP)
		else:
			Direction.OUTPUT(int(self._settings.get(["light_pin"])), Pull.DOWN)

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
				self.light_toggle()

			return flask.jsonify(state=self.light_state)

		elif action == "turnOff":
			if self.light_state:
				self.light_toggle()

			return flask.jsonify(state=self.light_state)

		else:
			return flask.jsonify(error="action not recognized")

	def on_event(self, event, payload):
		if event == Events.CLIENT_OPENED:
			self._plugin_manager.send_plugin_message(self._identifier, dict(isLightOn=self.light_state))
			return

	def get_update_information(self):
		return dict(
			octolight=dict(
				displayName="OctoLight-FT232H",
				displayVersion=self._plugin_version,

				type="github_release",
				current=self._plugin_version,

				user="OldManBlunTZ",
				repo="OctoLight-FT232H",
				pip="https://github.com/oldmanbluntz/OctoLightFT232h/archive/{target}.zip"
			)
		)

__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = OctoLight-FT232HPlugin()

__plugin_hooks__ = {
	"octoprint.plugin.softwareupdate.check_config":
	__plugin_implementation__.get_update_information
}
