from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Generates CSS to animate the class-specific sprite displayed in the UI. Usage: python manage.py generate_gif_keyframes 175 356'

    def add_arguments(self, parser):
        parser.add_argument('width', type=int, help='The width of the sprite')
        parser.add_argument('height', type=int, help='The height of the sprite')

    def handle(self, *args, **options):
        width = options['width']
        height = options['height']

        keyframes = "@keyframes sprite-animation {\n"
        positions = [(i * width, j * height) for j in range(3) for i in range(4)]
        for i, (x, y) in enumerate(positions):
            keyframes += f"  {i / 12 * 100}% {{ background-position: -{x}px -{y}px; }}\n"
        keyframes += "  100% { background-position: 0px 0px; }\n}\n"

        css_class = f""".class_graphic_image {{
        width: {width}px;
        height: {height}px;
        background: url("/static/everbitica/images/class_animations/cleric_class_animation.png") 0 0;
        animation: sprite-animation 3s steps(1) infinite;
        }}"""

        self.stdout.write(keyframes + css_class)

# This is somewhat out of date - it needs 12 frames and then a final 13th frame that takes up 10% to 100% of time. So first twelve should be evenly spread from 0% to 10%
# also the animation time needs to be upped from 3 to probably like 20 or 30 seconds
# also these timings are just rough estimates by me and probably not very accurate to the original animation