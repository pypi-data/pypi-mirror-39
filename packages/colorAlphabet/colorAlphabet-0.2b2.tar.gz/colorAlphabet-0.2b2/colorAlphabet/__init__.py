""" Color Alphabet module

    RV 20161111
    RV 20181119
"""
from collections import OrderedDict
import random

# Paul Green-Armytage: A Colour Alphabet and the Limits of Colour Coding
FULL_COLOR_ALPHABET = OrderedDict((
    ("Black",     (  0,   0,   0)),
    ("Amethyst",  (240, 163, 255)),
    ("Blue",      (  0, 117, 220)),
    ("Caramel",   (153,  63,   0)),
    ("Damson",    ( 76,   0,  92)),
    ("Ebony",     ( 25,  25,  25)),
    ("Forest",    (  0,  92,  49)),
    ("Green",     ( 43, 206,  72)),
    ("Honeydew",  (255, 204, 153)),
    ("Iron",      (128, 128, 128)),
    ("Jade",      (148, 255, 181)),
    ("Khaki",     (143, 124,   0)),
    ("Lime",      (157, 204,   0)),
    ("Mallow",    (194,  0,  136)),
    ("Navy",      (  0,  51, 128)),
    ("Orpiment",  (255, 164,   5)),
    ("Pink",      (255, 168, 187)),
    ("Quagmire",  ( 66, 102,   0)),
    ("Red",       (255,  0,   16)),
    ("Sky",       ( 94, 241, 242)),
    ("Turquoise", (  0, 153, 143)),
    ("Uranium",   (224, 255, 102)),
    ("Violet",    (116,  10, 255)),
    ("Wine",      (153,   0,   0)),
    ("Xanthin",   (255, 255, 128)),
    ("Yellow",    (255, 225,   0)),
    ("Zinnia",    (255,  80,   5)),
    ("White",     (255, 255, 255)),
  ))

COLOR_ALPHABET = FULL_COLOR_ALPHABET.copy()
del COLOR_ALPHABET['Black']
del COLOR_ALPHABET['White']

NORM_COLOR_ALPHABET = OrderedDict()
for c in COLOR_ALPHABET:
    NORM_COLOR_ALPHABET[c] = tuple([i / 255 for i in COLOR_ALPHABET[c]])

FULL_NORM_COLOR_ALPHABET = OrderedDict()
for c in FULL_COLOR_ALPHABET:
    FULL_NORM_COLOR_ALPHABET[c] = tuple([i / 255
        for i in FULL_COLOR_ALPHABET[c]])


#------------------------------------------------------------------------------
def randomColor(full=False):
    """ Return random color name

        Args:
            full (boolean): if True use FULL_COLOR_ALPHABET
                else use COLOR_ALPHABET

        Returns:
            random color name (str)
    """
    if full:
        alphabet = FULL_COLOR_ALPHABET
    else:
        alphabet = COLOR_ALPHABET
    return list(alphabet.keys())[int(random.random() * len(alphabet))]

#------------------------------------------------------------------------------
def colorize(msg, colorname, reset=True, xterm=False, full=False):
    """ Return a colorized version of msg.

        Args:
            msg (string): the message to colorize
            colorname (string): the color to use
            reset (boolean): Do not reset color if False
            xterm (boolean): * True generate RGB control sequence
                                (XTerm and Konsole)
                             * False generate ANSI control sequence
                                (other color terminals)
            full (boolean): if True use also Black and White

        Returns:
            A colorized version of msg.
    """
    if reset:
        if xterm:
            return '%s%s%s' % (setBGColor(colorname, full),
                    msg, resetBGColor())
        else:
            return '%s%s%s' % (setBGColor256(colorname, full),
                    msg, resetBGColor())
    else:
        if xterm:
            return '%s%s' % (setBGColor(colorname, full), msg)
        else:
            return '%s%s' % (setBGColor256(colorname, full), msg)

#------------------------------------------------------------------------------
def needWhiteFont(r, g, b):
    """ Return True if white font is needed based on RGB background color

        Args:
            r: red value of RGB color in [0, 1]
            g: red value of RGB color in [0, 1]
            b: red value of RGB color in [0, 1]

        Returns:
            * True if white font is needed based on RGB background color
            * False if black font is needed based on RGB background color

    """
    # Counting the perceptive luminance - human eye favors green color...
    a = 1 - ( 0.299 * r + 0.587 * g + 0.114 * b) / 255

    if a < 0.5:
        return False # bright colors - black font
    else:
        return True # dark colors - white font

#------------------------------------------------------------------------------
def resetBGColor():
    """ Return XTerm string to reset XTerm color
    """
    return "\x1b[0m"

#------------------------------------------------------------------------------
def rgb2short(rgb):
    """ Return the closest xterm-256 approximation to the given RGB value.

        Args:
            rgb (string): Hex code representing an RGB value, eg, 'abcdef'

        Returns:
            String between 0 and 255, compatible with xterm.

    """
    rgb2short_dict = {
        '000000': '16',  '00005f': '17',  '000080': '04',  '000087': '18',
        '0000af': '19',  '0000d7': '20',  '0000ff': '21',  '005f00': '22',
        '005f5f': '23',  '005f87': '24',  '005faf': '25',  '005fd7': '26',
        '005fff': '27',  '008000': '02',  '008080': '06',  '008700': '28',
        '00875f': '29',  '008787': '30',  '0087af': '31',  '0087d7': '32',
        '0087ff': '33',  '00af00': '34',  '00af5f': '35',  '00af87': '36',
        '00afaf': '37',  '00afd7': '38',  '00afff': '39',  '00d700': '40',
        '00d75f': '41',  '00d787': '42',  '00d7af': '43',  '00d7d7': '44',
        '00d7ff': '45',  '00ff00': '46',  '00ff5f': '47',  '00ff87': '48',
        '00ffaf': '49',  '00ffd7': '50',  '00ffff': '51',  '080808': '232',
        '121212': '233', '1c1c1c': '234', '262626': '235', '303030': '236',
        '3a3a3a': '237', '444444': '238', '4e4e4e': '239', '585858': '240',
        '5f0000': '52',  '5f005f': '53',  '5f0087': '54',  '5f00af': '55',
        '5f00d7': '56',  '5f00ff': '57',  '5f5f00': '58',  '5f5f5f': '59',
        '5f5f87': '60',  '5f5faf': '61',  '5f5fd7': '62',  '5f5fff': '63',
        '5f8700': '64',  '5f875f': '65',  '5f8787': '66',  '5f87af': '67',
        '5f87d7': '68',  '5f87ff': '69',  '5faf00': '70',  '5faf5f': '71',
        '5faf87': '72',  '5fafaf': '73',  '5fafd7': '74',  '5fafff': '75',
        '5fd700': '76',  '5fd75f': '77',  '5fd787': '78',  '5fd7af': '79',
        '5fd7d7': '80',  '5fd7ff': '81',  '5fff00': '82',  '5fff5f': '83',
        '5fff87': '84',  '5fffaf': '85',  '5fffd7': '86',  '5fffff': '87',
        '626262': '241', '6c6c6c': '242', '767676': '243',  '800000': '01',
        '800080': '05',  '808000': '03',  '808080': '08',  '870000': '88',
        '87005f': '89',  '870087': '90',  '8700af': '91',  '8700d7': '92',
        '8700ff': '93',  '875f00': '94',  '875f5f': '95',  '875f87': '96',
        '875faf': '97',  '875fd7': '98',  '875fff': '99',  '878700': '100',
        '87875f': '101', '878787': '102', '8787af': '103', '8787d7': '104',
        '8787ff': '105', '87af00': '106', '87af5f': '107', '87af87': '108',
        '87afaf': '109', '87afd7': '110', '87afff': '111', '87d700': '112',
        '87d75f': '113', '87d787': '114', '87d7af': '115', '87d7d7': '116',
        '87d7ff': '117', '87ff00': '118', '87ff5f': '119', '87ff87': '120',
        '87ffaf': '121', '87ffd7': '122', '87ffff': '123', '8a8a8a': '245',
        '949494': '246', '9e9e9e': '247', 'a8a8a8': '248', 'af0000': '124',
        'af005f': '125', 'af0087': '126', 'af00af': '127', 'af00d7': '128',
        'af00ff': '129', 'af5f00': '130', 'af5f5f': '131', 'af5f87': '132',
        'af5faf': '133', 'af5fd7': '134', 'af5fff': '135', 'af8700': '136',
        'af875f': '137', 'af8787': '138', 'af87af': '139', 'af87d7': '140',
        'af87ff': '141', 'afaf00': '142', 'afaf5f': '143', 'afaf87': '144',
        'afafaf': '145', 'afafd7': '146', 'afafff': '147', 'afd700': '148',
        'afd75f': '149', 'afd787': '150', 'afd7af': '151', 'afd7d7': '152',
        'afd7ff': '153', 'afff00': '154', 'afff5f': '155', 'afff87': '156',
        'afffaf': '157', 'afffd7': '158', 'afffff': '159', 'b2b2b2': '249',
        'bcbcbc': '250', 'c0c0c0': '07',  'c6c6c6': '251', 'd0d0d0': '252',
        'd70000': '160', 'd7005f': '161', 'd70087': '162', 'd700af': '163',
        'd700d7': '164', 'd700ff': '165', 'd75f00': '166', 'd75f5f': '167',
        'd75f87': '168', 'd75faf': '169', 'd75fd7': '170', 'd75fff': '171',
        'd78700': '172', 'd7875f': '173', 'd78787': '174', 'd787af': '175',
        'd787d7': '176', 'd787ff': '177', 'd7af00': '178', 'd7af5f': '179',
        'd7af87': '180', 'd7afaf': '181', 'd7afd7': '182', 'd7afff': '183',
        'd7d700': '184', 'd7d75f': '185', 'd7d787': '186', 'd7d7af': '187',
        'd7d7d7': '188', 'd7d7ff': '189', 'd7ff00': '190', 'd7ff5f': '191',
        'd7ff87': '192', 'd7ffaf': '193', 'd7ffd7': '194', 'd7ffff': '195',
        'dadada': '253', 'e4e4e4': '254', 'eeeeee': '255', 'ff0000': '196',
        'ff005f': '197', 'ff0087': '198', 'ff00af': '199', 'ff00d7': '200',
        'ff00ff': '201', 'ff5f00': '202', 'ff5f5f': '203', 'ff5f87': '204',
        'ff5faf': '205', 'ff5fd7': '206', 'ff5fff': '207', 'ff8700': '208',
        'ff875f': '209', 'ff8787': '210', 'ff87af': '211', 'ff87d7': '212',
        'ff87ff': '213', 'ffaf00': '214', 'ffaf5f': '215', 'ffaf87': '216',
        'ffafaf': '217', 'ffafd7': '218', 'ffafff': '219', 'ffd700': '220',
        'ffd75f': '221', 'ffd787': '222', 'ffd7af': '223', 'ffd7d7': '224',
        'ffd7ff': '225', 'ffff00': '226', 'ffff5f': '227', 'ffff87': '228',
        'ffffaf': '229', 'ffffd7': '230', 'ffffff': '231'
    }
    res = []
    incs = (0x00, 0x5f, 0x87, 0xaf, 0xd7, 0xff)
    for part in rgb:
        i = 0
        while i < len(incs) - 1:
            s, b = incs[i], incs[i + 1]  # smaller, bigger
            if s <= part <= b:
                s1 = abs(s - part)
                b1 = abs(b - part)
                if s1 < b1:
                    closest = s
                else:
                    closest = b
                res.append(closest)
                break
            i += 1
    res = ''.join([ ('%02.x' % i) for i in res ])
    equiv = rgb2short_dict[res]
    return equiv, res

#------------------------------------------------------------------------------
def setBGColor(colorname, full=False):
    """ Return XTerm string to set the background color to `colorname`

        Args:
            colorname (str): color name from COLOR_ALPHABET
                or FULL_COLOR_ALPHABET
            full (boolean): if True use FULL_COLOR_ALPHABET
    """
    try:
        if full:
            r, g, b = FULL_COLOR_ALPHABET[colorname]
        else:
            r, g, b = COLOR_ALPHABET[colorname]
    except KeyError:
        r, g, b = colorname
        #raise NotImplementedError("Color '%s' not implemented, sorry :-("
                #% str(colorname))
    # Set background color
    colorstring = ("\x1b[%d;2;%d;%d;%dm" % (48, r, g, b))
    if needWhiteFont(r, g, b):
        colorstring += ("\x1b[%d;2;%d;%d;%dm" % (38, 255, 255, 255))
    else:
        colorstring += ("\x1b[%d;2;%d;%d;%dm" % (38, 0, 0, 0))
    return colorstring

#------------------------------------------------------------------------------
def setBGColor256(colorname, full=False):
    """ Return ANSI term string to set the background color to `colorname`

        Args:
            colorname (str): color name from COLOR_ALPHABET
                or FULL_COLOR_ALPHABET
            full (boolean): if True use FULL_COLOR_ALPHABET
    """
    try:
        if full:
            r, g, b = FULL_COLOR_ALPHABET[colorname]
        else:
            r, g, b = COLOR_ALPHABET[colorname]
    except KeyError:
        r, g, b = colorname
        #raise NotImplementedError("Color '%s' not implemented, sorry :-("
                #% str(colorname))
    # Set background color
    short, rgb = rgb2short((r, g, b))

    # 48 ==> BG color
    # 38 ==> FG color
    # 30 ==> BLACK FG
    # 97 ==> WHITE FG
    colorstring = ("\x1b[48;5;%sm" % short)
    if needWhiteFont(r, g, b):
        colorstring += "\x1b[97m"
    else:
        colorstring += "\x1b[30m"
    return colorstring

#------------------------------------------------------------------------------
if __name__ == '__main__':
    import os
    import  sys
    import argparse
    #print('***', res, equiv)
    parser = argparse.ArgumentParser(
        description="\nShow colorAlphabet palette.",
        add_help=True,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog=os.path.basename(sys.argv[0]))

    parser.add_argument('-f', '--full',
        help=("Show full color Alphabet (i.e. with black and white)"),
        action='store_true',
        default=False,
        )
    options = parser.parse_args(sys.argv[1:])

    if options.full:
        alphabet = FULL_COLOR_ALPHABET
    else:
        alphabet = COLOR_ALPHABET
    for i, color in enumerate(alphabet):
        print(colorize("%2d XTerm %15s " % (i, color), color,
                full=True, xterm=True))
        print(colorize("%2d ANSI  %15s " % (i, color), color, full=True))
