# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import octoprint.plugin
from octoprint.events import Events
import flask
import board
import os
import digitalio
from digitalio import DigitalInOut, Direction, DriveMode, Pull

class OctoLightFT232HPlugin(
		octoprint.plugin.AssetPlugin,
		octoprint.plugin.StartupPlugin,
		octoprint.plugin.TemplatePlugin,
		octoprint.plugin.SimpleApiPlugin,
		octoprint.plugin.SettingsPlugin,
		octoprint.plugin.EventHandlerPlugin,
		octoprint.plugin.RestartNeedingPlugin
	):
	

	def __init__(self):
		self.light_state = False
		self.led = None

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
		self._logger.info("Loading OctoLight-FT232H, and Getting current LED state")
		
		self.led = digitalio.DigitalInOut(board.D4) 
		self.led.direction = digitalio.Direction.OUTPUT
		self.light_state = self.led.value

		self._plugin_manager.send_plugin_message(self._identifier, dict(isLightOn=self.light_state))

	def light_toggle(self):
		if self.led is not None:
			self.light_state = not self.led.value
			self.led.value = self.light_state

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

__plugin_pythoncompat__ = ">=3,<4"
__plugin_implementation__ = OctoLightFT232HPlugin()

__plugin_hooks__ = {
	"octoprint.plugin.softwareupdate.check_config":
	__plugin_implementation__.get_update_information
}
