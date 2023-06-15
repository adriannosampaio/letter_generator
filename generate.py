from PIL import Image, ImageFont, ImageDraw
import textwrap
from pathlib import Path
import random
import argparse
import codecs

parser = argparse.ArgumentParser(
     "generate", 
     description="Allow the creation of an image containing a letter from the given text"
)
parser.add_argument('-i', '--input', type=Path, required=True)
parser.add_argument('-o', '--output', type=Path, required=True)
parser.add_argument('-mx', type=int)
parser.add_argument('-my', type=int)
parser.add_argument('--font-size', type=int)
parser.add_argument('-f', '--font-file', type=Path)

def text_wrap(text : str, font : ImageFont, max_width):
    """Wrap text base on specified width. 
    This is to enable text of width more than the image width to be display
    nicely.
    @params:
        text: str
            text to wrap
        font: obj
            font of the text
        max_width: int
            width to split the text with
    @return
        lines: list[str]
            list of sub-strings
    """
    lines = []
    
    # If the text width is smaller than the image width, then no need to split
    # just add it to the line list and return
    if font.getlength(text) <= max_width:
        lines.append(text)
    else:
        #split the line by spaces to get words
        words = text.split(' ')
        pointer = 0
        # append every word to a line while its width is shorter than the image width
        while pointer < len(words):
            line = ''
            while pointer < len(words) and font.getlength(line + words[pointer]) <= max_width:
                line = line + words[pointer]+ " "
                pointer += 1
            if not line:
                line = words[pointer]
                pointer += 1
            lines.append(line)
    res : str = '\n'.join(lines)
    return res


if __name__ == '__main__':
    try:
        backgrounds = list(Path('textures').glob('**/*'))
        chosen =  random.choice(backgrounds)
        img = Image.open(chosen)

        args = parser.parse_args()

        margin = (args.mx or 100, args.my or 100)
        font_size = args.font_size or 20
        size = [x - m for x, m in zip(img.size, margin)]
        text = open(args.input, 'r', encoding='utf8').read()
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(args.font_file or Path('fonts/OldLondon.ttf'), font_size)
        sentences = ' \n '.join([sentence for sentence in text.split('\n') if not sentence.isspace()])
        draw.text(margin, text_wrap(text, font, size[0] - margin[0]),fill=(0, 0, 0, 250), font=font)
        img.save(args.output)
    except Exception as e:
        print(e)