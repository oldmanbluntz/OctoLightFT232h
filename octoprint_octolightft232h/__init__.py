# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import octoprint.plugin
from octoprint.events import Events
import flask
import board
import os
import digitalio

class OctoLightFT232HPlugin(
		octoprint.plugin.AssetPlugin,
		octoprint.plugin.StartupPlugin,
		octoprint.plugin.TemplatePlugin,
		octoprint.plugin.SimpleApiPlugin,
		octoprint.plugin.SettingsPlugin,
		octoprint.plugin.EventHandlerPlugin,
		octoprint.plugin.RestartNeedingPlugin
	):
	
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
		self._logger.info("Loading OctoLight-FT232H, Setting LED to Off")
		
		led = digitalio.DigitalInOut(board.D4)
		led.direction = digitalio.Direction.OUTPUT
		led.value = False


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
