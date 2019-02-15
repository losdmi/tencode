import os
import re
from pprint import pprint
import logging

from typing import Dict

from tencode_replacer import replace_tencode_in_message

from telegram import Update, Message, User, ParseMode, MessageEntity
from telegram.ext import Updater, MessageHandler, Filters

updater = Updater(token=os.getenv('BOT_TOKEN'))
dispatcher = updater.dispatcher

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

_entity_type_to_symbols = {
    MessageEntity.BOLD: '*',
    MessageEntity.ITALIC: '_',
    MessageEntity.CODE: '`',
    MessageEntity.PRE: '```'
}


def _handle(bot, update: Update):
    message: Message = update.message
    user: User = message.from_user
    original_message = _fill_message_with_entities(message.text, message.parse_entities())
    decoded_message = replace_tencode_in_message(original_message)

    pprint(original_message)
    print()
    print()
    pprint(decoded_message)
    print()
    print()
    pprint(str(update))
    print()
    print()
    print()

    if decoded_message != original_message:
        reply = "{user} сказал:\n\n{message}".format(
            user=user.full_name,
            message=decoded_message
        )
        reply = re.sub(
            r'(?<![{symbols}])\['.format(
                symbols=re.escape(''.join(_entity_type_to_symbols.values()))
            ),
            r'\[',
            reply
        )
        print(reply)
        print()
        print()
        bot.send_message(
            chat_id=message.chat_id,
            text=reply,
            parse_mode=ParseMode.MARKDOWN
        )


def _fill_message_with_entities(message: str, entities: Dict[MessageEntity, str]) -> str:
    result = ''
    border = 0

    for entity, text in entities.items():
        wrapper = _entity_type_to_symbols.get(entity.type)
        if wrapper:
            result += '{before}{wrapper}{text}{wrapper}'.format(
                before=message[border:entity.offset],
                wrapper=wrapper,
                text=text
            )
            border = entity.offset + entity.length

    result += message[border:len(message)]

    return result


dispatcher.add_handler(MessageHandler(Filters.text, _handle))

updater.start_polling()
updater.idle()
