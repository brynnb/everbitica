def generate_css(width, height):
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

  return keyframes + css_class

# Usage:
print(generate_css(175, 356))


# This is somewhat out of date - it needs 12 frames and then a final 13th frame that takes up 10% to 100% of time. So first twelve should be evenly spread from 0% to 10%
# also the animation time needs to be upped from 3 to probably like 20 or 30 seconds