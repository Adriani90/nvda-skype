# Skype Addon Users Guide

This addon enhances the built-in app module by porting some features from Dug Lee's excellent [jaws scripts for Skype](http://www.dlee.org/skype/skypeman6.php) to NVDA. 

This addon only works with the classic version of Skype desktop, not the Electron or UWP apps. You can download  the [latest Skype classic from this direct link](http://www.skype.com/go/getskype-full), version 7.41.0.101 at time of writing. If other versions of Skype are installed, you may have to uninstall them first before installing Skype classic.

## Configuring Skype for Use with the Addon

1. The addon currently only works with single window view, which uses a single window to display one conversation at a time, instead of using a window for each active conversation. Press Alt+V for the view menu, and press up arrow thrice. 
    * If you hear "split window view", you are already in single window view. 
    * Otherwise, you are in split window view and should   press enter when you hear "single window view". 
2. Optionally, enable more accessible mode in Skype. Press Alt+T, then O to open the Skype options. Press end to move to the Accessibility category. Using tab to explore the dialog, check the "Enable accessible mode" check box, and choose save.

## Available Commands

All commands match those in the jaws scripts as closely as possible.

* NVDA+Ctrl+0 through 9: read the 10 most recent messages when focus is on a conversation. This is implemented by the built-in app module, but has been enhanced so that it works  anywhere in Skype, not just when focus is inside the active conversation. This will be changed to alt+0 through 9 in the future.
* Ctrl+1: moves focus to the contacts list.
* Ctrl+2: moves focus to the  recent conversations list.
* Ctrl+3 (unimplemented): Moves focus to the list of active calls, if any. Active calls actually appear at the top of the recent conversations list, and are not in a separate list.
* Ctrl+4: moves focus to the message history for the active conversation.
* Ctrl+5: moves focus to the message input field for the active conversation.
* Ctrl+6: virtualizes the message history for the active conversation for convenient review and copying. This is subject to change.

## Changelog

### V0.1.1

* The hotkeys for reviewing the 10 most recent messages, NVDA+ctrl+0 through 9 now work anywhere in Skype, instead of only when your focus is already in the conversation.
* Added details about the Skype version and Skype configuration required for this addon to work.
* Many fixes to enable translation to other languages.

### V0.1

Initial release