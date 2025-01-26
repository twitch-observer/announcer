from enums import ParseMode

ANNOUNCE = {
    "text": "*{username}* is now live\\.\n"
            "{title}\n\n"
            "_Category: *{game}*_\n"
            "https://twitch\\.tv/{login}\n\n"
            "||\\#{login} • id: {download_id}||",
    "parse_mode": ParseMode.MARKDOWN_V2,
}

USER_NOT_FOUND = {
    "text": "The user with username *{login}* was not found\\.",
    "parse_mode": ParseMode.MARKDOWN_V2,
}

USER_ADDED = {
    "text": "The user with username *{username}* has been successfully added to the list of tracked users\\.",
    "parse_mode": ParseMode.MARKDOWN_V2,
}

USER_ALREADY_ADDED = {
    "text": "The user with username *{username}* was already added to the list of tracked users\\.",
    "parse_mode": ParseMode.MARKDOWN_V2,
}
