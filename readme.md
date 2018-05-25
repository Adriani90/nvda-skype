# Skype Add-on Users Guide

This add-on enhances the built-in app module by porting some features from Doug Lee's excellent [jaws scripts for Skype](http://www.dlee.org/skype/skypeman6.php) to NVDA. 

This add-on only works with the classic version of Skype desktop, not the Electron or UWP apps. You can download  the [latest Skype classic from this direct link](http://www.skype.com/go/getskype-full), version 7.41.0.101 at time of writing. If other versions of Skype are installed, you may have to uninstall them first before installing Skype classic.

## Configuring Skype for Use with the Add-on

1. The add-on currently only works with single window view, which uses a single window to display one conversation at a time, instead of using a window for each active conversation. Press Alt+V for the view menu, and press up arrow thrice. 
    * If you hear "split window view", you are already in single window view. 
    * Otherwise, you are in split window view and should   press enter when you hear "single window view". 
2. Optionally, enable more accessible mode in Skype. Press Alt+T, then O to open the Skype options. Press end to move to the Accessibility category. Using tab to explore the dialog, check the "Enable accessible mode" check box, and choose save.

## Available Commands

* Ctrl+0 through 9: read the 10 most recent messages for the active conversation. Press twice quickly to copy  the message to the clipboard.
* Alt+1: moves focus to the contacts list. This functionality is built into Skype itself.
* Alt+2: moves focus to the  recent conversations list. This functionality is built into Skype itself.
* Alt+3 (unimplemented): Moves focus to the list of active calls, if any. Active calls actually appear at the top of the recent conversations list, and are not in a separate list.
* Alt+4: moves focus to the message history for the active conversation.
* Alt+5: moves focus to the message input field for the active conversation.
* NVDA+Alt+w: virtualizes the message history for the active conversation for convenient review and copying. To load more earlier messages so they can be virtualized, move to the message history,   press home to move to the first message in the list, and press up arrow.

## Support

Please send bug reports, feature requests, or other feedback to the  [NVDA Add-ons list](https://nvda-addons.groups.io/g/nvda-addons). Alternatively, use the issue tracker on the [Github repository](https://github.com/Neurrone/nvda-skype).

## Changelog

### V0.2

* All commands now have different key bindings to better match the shortcuts that Skype itself provides. Alt is now the modifier for commands that move focus, instead of Ctrl.
* Ctrl+0 through 9 reads recent messages in the active conversation. Pressing twice quickly copies it to the clipboard.
* The hotkey for virtualization is now NVDA+Alt+w.
* Fix the built-in app module's gestures for reading recent messages for the active conversation (NVDA+Ctrl+n) not being cleared properly during initialization.
* Minor string updates and documentation improvements.

### V0.1.1

* The hotkeys for reviewing the 10 most recent messages, NVDA+ctrl+0 through 9 now work anywhere in Skype, instead of only when your focus is already in the conversation.
* Added details about the Skype version and Skype configuration required for this add-on to work.
* Many fixes to enable translation to other languages.

### V0.1

Initial release