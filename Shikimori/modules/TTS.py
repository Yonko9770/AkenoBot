"""
STATUS: Code is working. ✅
"""

"""
BSD 2-Clause License

Copyright (C) 2022, SOME-1HING [https://github.com/SOME-1HING]

Credits:-
    I don't know who originally wrote this code. If you originally wrote this code, please reach out to me. 

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from typing import Optional, List 
 from gtts import gTTS 
 import os 
 import requests 
 import json 
  
 from telegram import ChatAction 
 from telegram.ext import run_async 
  
 from AsukaRobot import dispatcher 
 from AsukaRobot.modules.disable import DisableAbleCommandHandler 
 from AsukaRobot.modules.helper_funcs.alternate import typing_action, send_action 
  
 @send_action(ChatAction.RECORD_AUDIO) 
 def gtts(update, context): 
     msg = update.effective_message 
     reply = " ".join(context.args) 
     if not reply: 
         if msg.reply_to_message: 
             reply = msg.reply_to_message.text 
         else: 
             return msg.reply_text( 
                 "Reply to some message or enter some text to convert it into audio format!" 
             ) 
         for x in "\n": 
             reply = reply.replace(x, "") 
     try: 
         tts = gTTS(reply, lang='en', tld='co.in') 
         tts.save("k.mp3") 
         with open("k.mp3", "rb") as speech: 
             msg.reply_audio(speech) 
     finally: 
         if os.path.isfile("k.mp3"): 
             os.remove("k.mp3") 
  
  
 # Open API key 
 API_KEY = "6ae0c3a0-afdc-4532-a810-82ded0054236" 
 URL = "http://services.gingersoftware.com/Ginger/correct/json/GingerTheText" 
  
  
 @typing_action 
 def spellcheck(update, context): 
     if update.effective_message.reply_to_message: 
         msg = update.effective_message.reply_to_message 
  
         params = dict(lang="US", clientVersion="2.0", apiKey=API_KEY, text=msg.text) 
  
         res = requests.get(URL, params=params) 
         changes = json.loads(res.text).get("LightGingerTheTextResult") 
         curr_string = "" 
         prev_end = 0 
  
         for change in changes: 
             start = change.get("From") 
             end = change.get("To") + 1 
             suggestions = change.get("Suggestions") 
             if suggestions: 
                 sugg_str = suggestions[0].get("Text")  # should look at this list more 
                 curr_string += msg.text[prev_end:start] + sugg_str 
                 prev_end = end 
  
         curr_string += msg.text[prev_end:] 
         update.effective_message.reply_text(curr_string) 
     else: 
         update.effective_message.reply_text( 
             "Reply to some message to get grammar corrected text!" 
         ) 
  
 dispatcher.add_handler(DisableAbleCommandHandler("tts", gtts, pass_args=True, run_async=True)) 
 dispatcher.add_handler(DisableAbleCommandHandler("splcheck", spellcheck, run_async=True)) 
  
 __help__ = """ 
  ‣ `/tts`: Convert Text in Bot Audio  
  *Usage*: reply to text or write message with command. Example `/tts hello` 
  ‣ `/slpcheck`: Check the right spelling of text 
 """ 
 __mod_name__ = "Text To Speech" 
 __command_list__ = ["tts"]
