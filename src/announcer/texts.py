from announcer.enums import ParseMode

ANNOUNCE = {
    "text": "*{username}* is now live\\.\n"
            "Click to watch: https://twitch\\.tv/{login}\\.\n\n"
            "||\\#{login} • id: {download_id}||",
    "parse_mode": ParseMode.MARKDOWN_V2,
}
