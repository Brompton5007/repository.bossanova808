# -*- coding: utf-8 -*-
"""
Handy utility functions for Kodi Addons
By bossanova808
Free in all senses....
VERSION 0.1.7 2021-03-21
(For Kodi Matrix & later)
"""
import sys
import traceback
import xbmc
import xbmcvfs
import xbmcgui
import xbmcaddon

ADDON = xbmcaddon.Addon()
ADDON_NAME = ADDON.getAddonInfo('name')
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_ICON = ADDON.getAddonInfo('icon')
ADDON_AUTHOR = ADDON.getAddonInfo('author')
ADDON_VERSION = ADDON.getAddonInfo('version')
ADDON_ARGUMENTS = f'{sys.argv}'
CWD = ADDON.getAddonInfo('path')
LANGUAGE = ADDON.getLocalizedString
PROFILE = xbmcvfs.translatePath(ADDON.getAddonInfo('profile'))
KODI_VERSION = xbmc.getInfoLabel('System.BuildVersion')
USER_AGENT = "Mozilla/5.0 (Windows; U; Windows NT 5.1; fr; rv:1.9.0.1) Gecko/2008070208 Firefox/3.6"
HOME_WINDOW = xbmcgui.Window(10000)
WEATHER_WINDOW = xbmcgui.Window(12600)

"""
Determine if we are unit testing outside of Kodi, or actually running within Kodi
Because we're using Kodi stubs https://romanvm.github.io/Kodistubs/ we can't rely on 'import xbmc' failing
So we use this hack - Kodi will return a user agent string, but Kodistrubs just returns and empty string.
If we are unit testing, change logs -> print
"""

unit_testing = False
if not xbmc.getUserAgent():

    xbmc = None
    unit_testing = True
    KODI_VERSION = 'N/A'

    print("No user agent, must be unit testing.")

    def log(message, exception_instance=None, level=None):
        print(f'DEBUG: {message}')
        if exception_instance:
            print(f'EXCPT: {traceback.format_exc(exception_instance)}')

    def log_info(message, exception_instance=None):
        log(f'INFO : {message}')
        if exception_instance:
            print(f'EXCPT: {traceback.format_exc(exception_instance)}')

else:

    def log(message, exception_instance=None, level=xbmc.LOGDEBUG):
        """
        Log a message to the Kodi debug log, if debug logging is turned on.

        :param message: required, the message to log
        :param exception_instance: optional, an instance of some Exception
        :param level: optional, the Kodi log level to use, default LOGDEBUG
        """

        message = f'### {ADDON_NAME} {ADDON_VERSION} - {message}'
        message_with_exception = message + f' ### Exception: {traceback.format_exc(exception_instance)}'

        if exception_instance is None:
            xbmc.log(message, level)
        else:
            xbmc.log(message_with_exception, level)


    def log_info(message, exception_instance=None):
        """
        Log a message at the LOGINFO level, i.e. even if Kodi debugging is not turned on. Use very sparingly.

        :param message: required, the message to log
        :param exception_instance: optional, an instance of some Exception
        """
        log(message, exception_instance, level=xbmc.LOGINFO)

    def set_property(window, name, value=""):
        """
        Set a property on a window.
        To clear a property, provide an empty string

        :param window: Required.  The Kodi window on which to set the property.
        :param name: Required.  Name of the property.
        :param value: Optional (defaults to "").  Set the property to this value.  An empty string clears the property.
        """
        window.setProperty(name, value)


    def get_property(window, name):
        """
        Return the value of a window property
        @param window:
        @param name:
        @return:
        """
        return window.getProperty(name)


    def get_property_as_bool(window, name):
        """
        Return the value of a window property as a boolean
        @param window:
        @param name:
        @return:
        """
        return window.getProperty(name).lower() == "true"


    def send_kodi_json(human_description, json_string):
        """
        Send a JSON command to Kodi, logging the human description, command, and result returned.

        :param human_description: Required. A human sensible description of what the command is aiming to do/retrieve.
        :param json_string: Required. The json command to send.
        """
        log(f'KODI JSON RPC command: {human_description} [{json_string}]')
        result = xbmc.executeJSONRPC(json_string)
        log(f'KODI JSON RPC result: {result}')
        return result


    def get_setting(setting):
        """
        Helper function to get string type from settings

        @param setting:
        @return: setting value
        """
        return ADDON.getSetting(setting).strip()


    def get_setting_as_bool(setting):
        """
        Helper function to get bool type from settings

        @param setting:
        @return: setting value as boolen
        """
        return get_setting(setting).lower() == "true"


    def notify(message, notification_type=xbmcgui.NOTIFICATION_ERROR, duration=5000):
        """
        Send a notification to the user via the Kodi GUI

        @param message: the message to send
        @param notification_type: xbmcgui.NOTIFICATION_ERROR (default), xbmcgui.NOTIFICATION_WARNING, or xbmcgui.NOTIFICATION_INFO
        @param duration: time to display notification in milliseconds, default 5000
        @return: None
        """
        dialog = xbmcgui.Dialog()

        dialog.notification(ADDON_NAME,
                            message,
                            notification_type,
                            duration)


def footprints(startup=True):
    """
    Log the startup of an addon, and key Kodi details that are helpful for debugging

    :param startup: optional, default True.  If true, log the startup of an addon, otherwise log the exit.
    """
    if startup:
        log_info(f'Starting...')
        log_info(f'Kodi Version: {KODI_VERSION}')
        log_info(f'Addon arguments: {ADDON_ARGUMENTS}')
    else:
        log_info(f'Exiting...')

