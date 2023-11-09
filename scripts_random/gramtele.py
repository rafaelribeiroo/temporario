from requests import get, post
from decouple import config
from random import randint

quotes = (
    'Ilyena, my love, forgive me!',
    'A man who trusts everyone is a fool, and a man who trusts no one is a '
    'fool. We are all fools, if we live long enough.',
    'What you want is what you cannot have. What you cannot have is what '
    'you want.',
    'The Wheel of Time and the wheel of a man\'s life turn alike without '
    'pity or mercy.',
    'What makes you think you can keep anyone safe? We are all going to die. '
    'Just hope that you aren\'t the one who kills them.',
    'Mustn\'t use that. Threatens the fabric of the pattern. Not even for '
    'Ilyena? I would burn the world and use my soul for tinder to hear her'
    ' laugh again.',
    'Break it break them all must break them must must must break them all '
    'break them and strike must strike quickly must strike now break it '
    'break it break it...',
    'He\'s insane and I\'m not. Besides, he failed and I won\'t',
    'Kill him, kill him now!',
    '"The end of time?" Ba\'alzamon mocked. "You live like a beetle under a '
    'rock, and you think your slime is the universe. The death of time will '
    'bring me power such as you could not dream of, worm."',
    'There is a different beauty in simplicity, in a single line placed just '
    'so, a single flower among the rocks. The harshness of the stone makes '
    'the flower more precious. We try not to dwell too much on what is '
    'gone. The strongest heart will break under that strain.',
    'What is done in dreams can be more dangerous than what is done awake.',
    'If you don\'t know everything, you must go on with what you do know.',
    'Better watching than fighting.',
    'The weak must be bold cautiously.',
    'I don\'t hand out penance for telling the truth, daughter.',
    '"Do not trouble trouble till trouble troubles you." Mark it well, child.',
    'Smooth words make smooth companions.',
    'When you can\'t win a big victory, sheepherder, learn to settle for the '
    'small ones.',
    'Look at it from every side, Mat thought wearily. Half the trouble I get '
    'into is from not doing that. I have to think.',
    'We must be concerned with what concerns us.',
    'If I can\'t keep up with you, girl, how will I be able to tend '
    'Elayne\'s babes? Do you mean to stand there? "Dragging feet '
    'never finish a journey".',
    'A woman is no less a woman because she carries a spear.',
    '"Sift enough sand," Taim said stiffly, "and you will find a few grains '
    'of gold eventually".',
    'First things first; take care of what can be done now before worrying '
    'too long over what might never be.',
    '"Watch sharp," Ingtar commanded, gathering his reins. And do not believe '
    'that they\'re friendly just because they smile.',
    '“There\'s an old saying in the Two Rivers," Rand said dryly. "The louder '
    'a man tells you he\'s - honest, the harder you must hold on to your '
    'purse." Another said, "The fox often offers to give the duck its pond."',
    'Lini always said "Waiting turns men into bears in a barn, and women into '
    'cats in a sack".',
    '"You lost concentration," Lan told him. "You must hold on to that even '
    'when your muscles turn to water. Lose it, and that is the day you die. '
    'And it will probably be a farmboy who has his hands on a sword for the '
    'first time who does it.-"',
    'Take what you can have. Rejoice in what you can save, and do not\' mourn '
    'your losses too long. It was not his thought, but he took it.',
    'Elayne\'s mouth tightened. That was about what she had expected, but not '
    'what she wanted to hear. "Wish" and "want" trip the fret, but "is" makes '
    'the path smoother. That was what Lini said. You had to deal with what '
    'was, not what you wished was.',
    'Yet to achieve greatly, a man must believe something. Belief and '
    'knowledge pave the road to greatness. Knowledge is perhaps the most '
    'valuable of all. We all seek the coin of knowledge',
    '"I have heard it said," Rand told him, "that you should believe nothing '
    'you hear, and only half of what you see."',
    'Sometimes he thought women all belonged to a guild, the way craftsmen in '
    'cities did. Put a foot wrong with one, and the next ten you met knew of '
    'it, and disapproved.',
    '"Not the whole world," he replied. But if they can see, they can hear as '
    'well. You have made a place in my heart where I thought there was no '
    'room for anything else. You have made flowers grow where I cultivated '
    'dust and stones. Remember this, on this journey you insist on making. '
    'If you die, I will not survive you long.'
)

token = config('BOT_TOKEN')
last_update_id = 0


def getUpdates():
    url = f'https://api.telegram.org/bot{token}/getUpdates?offset=-1'
    res = get(url=url)
    update = res.json()["result"]
    return update


def last():
    url = f'https://api.telegram.org/bot{token}/getUpdates?offset=-1'
    res = get(url=url)
    # import pdb; pdb.set_trace()
    update = res.json()["result"]
    return update[-1]


def parse_message():
    current_update_id = last()['update_id']
    try:
        chat_id = last()['message']['chat']['id']
        txt = last()['message']['text']
        txt_id = last()['message']['message_id']
    except KeyError:
        txt = ''
        txt_id = ''
        chat_id = ''
    return current_update_id, chat_id, txt, txt_id


def reply_markup(ids, txt_id):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': ids,
        'text': f'<i>{quotes[randint(0, len(quotes) - 1)]}</i>',
        'reply_to_message_id': txt_id,
        'parse_mode': 'HTML'
    }

    r = post(url, json=payload)
    return r.json()


while True:
    current_update_id, chat_id, txt, txt_id = parse_message()

    # import pdb; pdb.set_trace()
    if last_update_id != current_update_id:
        last_update_id = current_update_id

        if not txt:
            continue

        if ' rand' in txt.lower():
            reply_markup(chat_id, txt_id)
