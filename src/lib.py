from telegram import MessageEntity

entity_type_to_symbols = {
    MessageEntity.BOLD: '*',
    MessageEntity.ITALIC: '_',
    MessageEntity.CODE: '`',
    MessageEntity.PRE: '```'
}
