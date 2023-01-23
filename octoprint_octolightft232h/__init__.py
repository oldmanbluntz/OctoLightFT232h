# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import octoprint.plugin
from octoprint.events import Events
import flask
import board
import os
from digitalio import DigitalInOut, Direction, Pull

class OctoLightFT232HPlugin(
		octoprint.plugin.AssetPlugin,
		octoprint.plugin.StartupPlugin,
		octoprint.plugin.TemplatePlugin,
		octoprint.plugin.SimpleApiPlugin,
		octoprint.plugin.SettingsPlugin,
		octoprint.plugin.EventHandlerPlugin,
		octoprint.plugin.RestartNeedingPlugin
	):

	led.value = False

	def get_settings_defaults(self):
		return dict(
			led = DigitalInOut(board.D4),
			lightdirection = Direction.OUTPUT
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
			js=["js/octolightft232h.js"],
			css=["css/octolightft232h.css"],
			#less=["less/octolight.less"]
		)

	def on_after_startup(self):
		self.led.value = False
		self._logger.info("--------------------------------------------")
		self._logger.info("OctoLightFT232H started, listening for GET request")
		self._logger.info("Light pin: {}, inverted_input: {}".format(
			self._settings.get(["led"]),
			self._settings.get(["lightdirection"])
		))
		self._logger.info("--------------------------------------------")

		# Setting the default state of pin
		DigitalInOut(board.D4), Direction.OUTPUT
		if bool(self._settings.get(["lightdirection"])):
			Direction.OUTPUT(int(self._settings.get(["led"])), Pull.UP)
		else:
			Direction.OUTPUT(int(self._settings.get(["led"])), Pull.DOWN)

		#Because light is set to off on startup we don't need to retrieve the current state
		"""
		r = self.led.value = Direction.INPUT(int(self._settings.get(["led"])))
        if r==1:
                self.led.value = False
        else:
                self.led.value = True
        self._logger.info("After Startup. Light state: {}".format(
                self.led.value
        ))
        """

		self._plugin_manager.send_plugin_message(self._identifier, dict(isLightOn=self.led.value))

	def light_toggle(self):
		# Sets the GPIO every time, if user changed it in the settings.
		DigitalInOut(board.D4), Direction.OUTPUT

		self.led.value = not self.led.value

		# Sets the light state depending on the inverted output setting (XOR)
		if self.led.value ^ self._settings.get(["lightdirection"]):
			Direction.OUTPUT(int(self._settings.get(["led"])), Pull.UP)
		else:
			Direction.OUTPUT(int(self._settings.get(["led"])), Pull.DOWN)

		self._logger.info("Got request. Light state: {}".format(
			self.led.value
		))

		self._plugin_manager.send_plugin_message(self._identifier, dict(isLightOn=self.led.value))

	def on_api_get(self, request):
		action = request.args.get('action', default="toggle", type=str)

		if action == "toggle":
			self.light_toggle()

			return flask.jsonify(state=self.led.value)

		elif action == "getState":
			return flask.jsonify(state=self.led.value)

		elif action == "turnOn":
			if not self.led.value:
				self.light_toggle()

			return flask.jsonify(state=self.led.value)

		elif action == "turnOff":
			if self.led.value:
				self.light_toggle()

			return flask.jsonify(state=self.led.value)

		else:
			return flask.jsonify(error="action not recognized")

	def on_event(self, event, payload):
		if event == Events.CLIENT_OPENED:
			self._plugin_manager.send_plugin_message(self._identifier, dict(isLightOn=self.led.value))
			return

	def get_update_information(self):
		return dict(
			octolightft232h=dict(
				displayName="OctoLightFT232H",
				displayVersion=self._plugin_version,

				type="github_release",
				current=self._plugin_version,

				user="OldManBlunTZ",
				repo="OctoLightFT232H",
				pip="https://github.com/oldmanbluntz/OctoLightFT232h/archive/{target}.zip"
			)
		)

__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = OctoLightFT232HPlugin()

__plugin_hooks__ = {
	"octoprint.plugin.softwareupdate.check_config":
	__plugin_implementation__.get_update_information
}
