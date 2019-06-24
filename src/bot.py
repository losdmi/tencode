import os
import logging

from typing import Dict

from tencode_replacer import replace_tencode_in_message, tencodes_dictionary

from telegram import Update, Message, User, ParseMode, MessageEntity, Chat
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from telegram.bot import Bot

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


def _handle_text_message(bot: Bot, update: Update):
    message: Message = update.message
    original_message = _fill_message_with_entities(message.text, message.parse_entities())
    decoded_message = replace_tencode_in_message(original_message)

    if decoded_message != original_message:
        user: User = message.from_user
        is_group = message.chat.type in [Chat.GROUP, Chat.SUPERGROUP]
        body = "{user} сказал:\n\n{message}" if is_group else '{message}'
        reply = body.format(
            user=user.full_name,
            message=decoded_message
        )
        bot.send_message(
            chat_id=message.chat_id,
            text=reply,
            parse_mode=ParseMode.MARKDOWN
        )


def _fill_message_with_entities(
        message: str,
        entities: Dict[MessageEntity, str]
) -> str:
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


def _handle_show_command(bot: Bot, update: Update):
    response = '\n'.join([
        '`{k}`       {v}'.format(k='{:>7}'.format(k), v=v)
        for k, v in tencodes_dictionary.items()
    ])
    message: Message = update.message
    bot.send_message(
        chat_id=message.chat_id,
        text=response,
        parse_mode=ParseMode.MARKDOWN
    )


dispatcher.add_handler(MessageHandler(Filters.text, _handle_text_message))
dispatcher.add_handler(CommandHandler('show', _handle_show_command))

updater.start_polling()
updater.idle()
