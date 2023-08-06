from helga.plugins import command


@command('spongebob', aliases=['sb'],
         help='Spongebob Mockery Text. Usage: helga [spongebob|sb] TEXT')
def spongebob(client, channel, nick, message, cmd, args):
    x = ' '.join(args)
    return ''.join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(x))
