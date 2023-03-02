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

from gpytranslate import Translator

from Shikimori import pbot

from pyrogram import filters, enums

from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

trans = Translator()

LANG_CODES = [

    "af",

    "am",

    "ar",

    "az",

    "be",

    "bg",

    "bn",

    "bs",

    "ca",

    "ceb",

    "co",

    "cs",

    "cy",

    "da",

    "de",

    "el",

    "en",

    "eo",

    "es",

    "et",

    "eu",

    "fa",

    "fi",

    "fr",

    "f",

    "ga",

    "gd",

    "gl",

    "gu",

    "ha",

    "haw",

    "hi",

    "hmn",

    "hr",

    "ht",

    "hu",

    "hy",

    "id",

    "ig",

    "is",

    "it",

    "iw",

    "ja",

    "jw",

    "ka",

    "kk",

    "km",

    "kn",

    "ko",

    "ku",

    "ky",

    "la",

    "lb",

    "lo",

    "lt",

    "lv",

    "mg",

    "mi",

    "mk",

    "ml",

    "mn",

    "mr",

    "ms",

    "mt",

    "my",

    "ne",

    "nl",

    "no",

    "ny",

    "pa",

    "pl",

    "ps",

    "pt",

    "ro",

    "ru",

    "sd",

    "si",

    "sk",

    "sl",

    "sm",

    "sn",

    "so",

    "sq",

    "sr",

    "st",

    "su",

    "sv",

    "sw",

    "ta",

    "te",

    "tg",

    "th",

    "tl",

    "tr",

    "uk",

    "ur",

    "uz",

    "vi",

    "xh",

    "yi",

    "yo",

    "zh",

    "zh_cn",

    "zh_tw",

    "zu",

]

@pbot.on_message(filters.command(["tl", "tr"]))

async def translate(_, message: Message):

    reply_msg = message.reply_to_message

    if not reply_msg:

        await message.reply_text("Reply to a message to translate it!")

        return

    if reply_msg.caption:

        to_translate = reply_msg.caption

    elif reply_msg.text:

        to_translate = reply_msg.text

    try:

        args = message.text.split()[1].lower()

        if "//" in args:

            source = args.split("//")[0]

            dest = args.split("//")[1]

        else:

            source = await trans.detect(to_translate)

            dest = args

        if dest.lower() not in LANG_CODES:

            return await message.reply_text(

                "Click on the button below to see the list of supported language codes.",

                reply_markup=InlineKeyboardMarkup(

                    [

                        [

                            InlineKeyboardButton(

                                text="Language codes",

                                url="https://telegra.ph/Lang-Codes-03-19-3",

                            ),

                        ],

                    ],

                    disable_web_page_preview=True,

                ),

            )

    except IndexError:

        source = await trans.detect(to_translate)

        dest = "en"

    translation = await trans(to_translate, sourcelang=source, targetlang=dest)

    reply = (

        f"<b>Translated from {source} to {dest}</b>:\n"

        f"<code>{translation.text}</code>"

    )

    await message.reply_text(reply, parse_mode=enums.ParseMode.HTML)
