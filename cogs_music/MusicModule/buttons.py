import disnake
from disnake.ext import commands

btns = {
    'back': {
        'label': 'back',    
        'emoji': '⏮',
        'disabled': None
    },
    'pause': {
        'label': 'pause',
        'emoji': '⏸️',
        'disabled': False
    },
    'forward': {
        'label': 'forward',
        'emoji': '⏭️',
        'disabled': None
    },
    'stop': {
        'label': 'stop',
        'emoji': '⏹️',
        'disabled': False
    },
    'repeat': {
        'label': 'repeat',
        'emoji': '🔁',
        'disabled': False
    },
    'quieter': {
        'label': 'quieter',
        'emoji': '🔉',
        'disabled': False
    },
    'louder': {
        'label': 'louder',
        'emoji': '🔊',
        'disabled': False
    },
    'playlist': {
        'label': 'playlist',
        'emoji': '📜',
        'disabled': False
    }
}


async def create_button_view(inter, queue, server_id):
    btn = []

    length_of_queue = len(queue[server_id])
    print(length_of_queue)

    for key, value in btns.items():

        if length_of_queue == 0:
            btns['back']['disabled'] = True
            btns['forward']['disabled'] = True

        button = disnake.ui.Button(style=disnake.ButtonStyle.gray, emoji=value['emoji'], custom_id=value['label'], disabled=value['disabled'])
        btn.append(button)

    return btn

