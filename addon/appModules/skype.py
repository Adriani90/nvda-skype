# -*- coding: utf-8 -*-
import api
import appModuleHandler
import controlTypes
from logHandler import log
import NVDAObjects
import keyboardHandler
from nvdaBuiltin.appModules import skype
import oleacc
import ui
import winUser
import windowUtils

import gettext
import languageHandler
import addonHandler
addonHandler.initTranslation()

# Translators: message presented when there is no active conversation
MSG_NO_ACTIVE_CONVERSATION = _("No active conversation.")

class UnfocusableShellDocObjectView(NVDAObjects.IAccessible.ShellDocObjectView):
    def initOverlayClass(self):
        self.shouldAllowIAccessibleFocusEvent = False
    
    def event_gainFocus(self):
        NVDAObjects.IAccessible.IAccessible.event_gainFocus(self)
        
class AppModule(skype.AppModule):
    scriptCategory = skype.SCRCAT_SKYPE
    def __init__(self, *args, **kwargs):
        super(AppModule, self).__init__(*args, **kwargs)
    
    """
    def chooseNVDAObjectOverlayClasses(self, obj, clsList):
        super(AppModule, self).chooseNVDAObjectOverlayClasses(obj, clsList)
        if obj.windowClassName == "Shell DocObject View":
            clsList.insert(0, UnfocusableShellDocObjectView)
            ui.message("using overlay")     
    
    
    def event_NVDAObject_init(self,obj):
        if  obj.windowClassName in ("Shell DocObject View", "Internet Explorer_Server"):
            ui.message("Disallowing focus event")
            obj.shouldAllowIAccessibleFocusEvent = False
            obj.isFocusable = False
        else:
            super(AppModule, self).event_NVDAObject_init(obj)
    """
    
    def moveFocusTo(self, handle):
        #winUser.sendMessage(api.getForegroundObject().windowHandle, 40, handle, 1)
        winUser.setForegroundWindow(handle)
    
    def script_moveToRecentConversationsList(self, gesture):
        fg = api.getForegroundObject()
        try:
            handle = windowUtils.findDescendantWindow(fg.windowHandle, className="TConversationsControl")
            #w = NVDAObjects.IAccessible.getNVDAObjectFromEvent(handle, winUser.OBJID_CLIENT, 0)
            self.moveFocusTo(handle)
        except LookupError:
            log.debugWarning("Couldn't find recent conversations list")
            ui.message(MSG_NO_ACTIVE_CONVERSATION)
        
        """
        # We use the built-in hotkey to do this and bind a different gesture
        # alt+2 will be used for reviewing recent messages in future
        keyboardHandler.KeyboardInputGesture.fromName("alt+2").send()
        """
    # Translators: Input help mode message for move to recent conversations list command
    script_moveToRecentConversationsList.__doc__ = _("Moves focus to the list of recent conversations.")
    
    # returns the handle of the chat history list window
    # throws: LookupError if the window could not be found
    def getChatHistoryWindow(self):
        fg = api.getForegroundObject()
        lastChild = fg.lastChild
        if controlTypes.STATE_INVISIBLE not in lastChild.states:
            handle = windowUtils.findDescendantWindow(lastChild.windowHandle, className="TChatContentControl")
            return handle
        else:
            raise LookupError("Chat history list not visible.")
    
    def script_moveToChatHistory(self, gesture):
        try:
            handle = self.getChatHistoryWindow()
            #w = NVDAObjects.IAccessible.getNVDAObjectFromEvent(handle, winUser.OBJID_CLIENT, 0)
            self.moveFocusTo(handle)
        except LookupError:
            log.debugWarning("Couldn't find chat history list")
            ui.message(MSG_NO_ACTIVE_CONVERSATION)
    # Translators: Input help mode message for the move to chat history command
    script_moveToChatHistory.__doc__ = _("Moves focus to the chat history for the active conversation.")
    
    def script_moveToChatEntryEdit(self, gesture):
        fg = api.getForegroundObject()
        lastChild = fg.lastChild
        # If there is an active conversation being shown, then it is the last child of fg (which should be visible), and has the class u'TConversationForm'
        if controlTypes.STATE_INVISIBLE not in lastChild.states and lastChild.windowClassName == "TConversationForm":
            try:
                handle = windowUtils.findDescendantWindow(lastChild.windowHandle, None, None, className="TChatRichEdit")
                #w = NVDAObjects.IAccessible.getNVDAObjectFromEvent(handle, winUser.OBJID_CLIENT, 0)
                self.moveFocusTo(handle)
            except LookupError:
                log.debugWarning("Couldn't find chat entry edit.")
                ui.message(MSG_NO_ACTIVE_CONVERSATION)
        else:
            ui.message(MSG_NO_ACTIVE_CONVERSATION)
    # Translators: Input help mode message for move to chat entry field command
    script_moveToChatEntryEdit.__doc__ = _("Moves focus to the message input field for the active conversation.")
    
    def script_displayChatHistoryInVirtualBuffer(self, gesture):
        try:
            handle = self.getChatHistoryWindow()
            chatHistoryObj = NVDAObjects.IAccessible.getNVDAObjectFromEvent(handle, winUser.OBJID_CLIENT, 0).lastChild
            messages = [msg.name for msg in chatHistoryObj.children]
            conversationName = chatHistoryObj.parent.parent.name
            # Translators: brief summary when virtualizing conversation which includes the number of  messages shown
            text = _("Displaying the %d most recent messages chronologically:\n%s") % (len(messages), '\n'.join(messages))
            # Translators: title of the buffer when virtualizing messages, excluding conversation name
            ui.browseableMessage(text, title=_("Chat history for ") + conversationName, isHtml=False)
        except LookupError:
            log.debugWarning("Couldn't find chat history list")
            ui.message(MSG_NO_ACTIVE_CONVERSATION)
    # Translators: Input help mode message for virtualize conversation command
    script_displayChatHistoryInVirtualBuffer.__doc__ = _("Presents the chat history of the active conversation in a virtual document for review.")
    
    __gestures = {
        "kb:control+2" : "moveToRecentConversationsList",
        "kb:control+4" : "moveToChatHistory",
        "kb:control+5" : "moveToChatEntryEdit",
        "kb:control+6" : "displayChatHistoryInVirtualBuffer"
    }