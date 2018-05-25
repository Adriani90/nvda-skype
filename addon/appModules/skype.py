# -*- coding: utf-8 -*-
import api
import appModuleHandler
import controlTypes
import datetime
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

# Used in a failed attempt to prevent focus from being trapped by annoying ads
class UnfocusableShellDocObjectView(NVDAObjects.IAccessible.ShellDocObjectView):
    def initOverlayClass(self):
        self.shouldAllowIAccessibleFocusEvent = False
    
    def event_gainFocus(self):
        NVDAObjects.IAccessible.IAccessible.event_gainFocus(self)
        
# since  commands to review recent messages are moved to  app module  so they work anywhere in Skype (not just in a conversation), 
# we need to use a Conversation overlay without these gestures
class ConversationWithoutMessageReviewGestures(skype.Conversation):
    def initOverlayClass(self):
        super( ConversationWithoutMessageReviewGestures, self).initOverlayClass()
        # Undo the gesture binding
        for n in xrange(0, 10):
			self.removeGestureBinding("kb:NVDA+control+%d" % n)
        self.script_speakOrCopyRecentMessage = None
    
class AppModule(skype.AppModule):
    scriptCategory = skype.SCRCAT_SKYPE
    def __init__(self, *args, **kwargs):
        super(AppModule, self).__init__(*args, **kwargs)
        # keep track of the index of the message and the time when a review recent message command is pressed
        self.lastIndexOfRecentMessageReviewed = 0
        self.timeOfLastMessageReviewGesture = datetime.datetime.now()
        
        for i in xrange(0, 10):
            self.bindGesture("kb:control+%d" % i, "speakOrCopyRecentMessage")
    
    def chooseNVDAObjectOverlayClasses(self, obj, clsList):
        super(AppModule, self).chooseNVDAObjectOverlayClasses(obj, clsList)
        if isinstance(obj, NVDAObjects.IAccessible.IAccessible) and obj.windowClassName == "TConversationForm" and obj.IAccessibleRole == oleacc.ROLE_SYSTEM_CLIENT:
            clsList.remove(skype.Conversation)
            clsList.insert(0, ConversationWithoutMessageReviewGestures)
        """
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
                self.moveFocusTo(handle)
            except LookupError:
                log.debugWarning("Couldn't find chat entry edit.")
                ui.message(MSG_NO_ACTIVE_CONVERSATION)
        else:
            ui.message(MSG_NO_ACTIVE_CONVERSATION)
    # Translators: Input help mode message for move to chat entry field command
    script_moveToChatEntryEdit.__doc__ = _("Moves focus to the message input field for the active conversation.")
    
    def script_virtualizeConversation(self, gesture):
        try:
            chatOutputList = NVDAObjects.IAccessible.getNVDAObjectFromEvent(self.getChatHistoryWindow(), winUser.OBJID_CLIENT, 0).lastChild
            messages = [msg.name for msg in chatOutputList.children]
            conversationName = chatOutputList.parent.parent.name
            # Translators: brief summary when virtualizing conversation which includes the number of  messages shown
            text = _("Displaying the {n} most recent messages chronologically:\n{messageText}").format(n=len(messages), messageText='\n'.join(messages))
            # Translators: title of the buffer when virtualizing messages, excluding conversation name
            ui.browseableMessage(text, title=_("Chat history for ") + conversationName, isHtml=False)
        except LookupError:
            log.debugWarning("Couldn't find chat history list")
            ui.message(MSG_NO_ACTIVE_CONVERSATION)
    # Translators: Input help mode message for virtualize conversation command
    script_virtualizeConversation.__doc__ = _("Virtualizes recent messages for the active conversation for convenient review and copying.")
    
    def script_speakOrCopyRecentMessage(self, gesture):
        try:
            index = int(gesture.mainKeyName[-1])
        except (AttributeError, ValueError):
            return
        if index == 0:
            index = 10
        
        try:
            chatOutputList = NVDAObjects.IAccessible.getNVDAObjectFromEvent(self.getChatHistoryWindow(), winUser.OBJID_CLIENT, 0).lastChild
            count = chatOutputList._getMessageCount()
            if index > count:
                # Translators: notify users that not that many messages were received
                ui.message(_("Not that many messages received."))
                return
            message = chatOutputList.getChild(count - index)
            
            # is the gesture pressed consecutively withint a short time (0.5 seconds)? E.g pressing ctrl+2 twice quickly
            # scriptHandler.getLastScriptRepeatCount() can't be used, reviewing different messages count as repetitions;  different keys invoke this gesture
            timeElapsed = datetime.datetime.now() - self.timeOfLastMessageReviewGesture
            isRepeat = index == self.lastIndexOfRecentMessageReviewed and timeElapsed.seconds == 0 and timeElapsed.microseconds <= 500000
            if not isRepeat:
                chatOutputList.reportMessage(message.name)
            else:
                if api.copyToClip(message.name):
                    # Translators: recent message was successfully copied to clipboard
                    ui.message(_("Copied."))
                else:
                    # Translators: recent message text not successfully copied to clipboard
                    ui.message(_("There was an unknown error copying the message to the clipboard."))
            
            self.lastIndexOfRecentMessageReviewed = index
            self.timeOfLastMessageReviewGesture = datetime.datetime.now() 
        except LookupError:
            log.debugWarning("Couldn't find recent message list")
            
    # Translators: Input help mode message for reviewing recent message commands
    script_speakOrCopyRecentMessage.__doc__ = _("Speaks one of the 10 most recent  messages  for the active conversation. Press twice quickly to copy it to the clipboard.")
    
    __gestures = {
        "kb:alt+4" : "moveToChatHistory",
        "kb:alt+5" : "moveToChatEntryEdit",
        "kb:NVDA+alt+w" : "virtualizeConversation"
    }