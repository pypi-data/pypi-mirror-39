# Scripter

Make a script using Python!

## Installing

Currently, you can do:
```
git clone https://github.com/NCPlayz/Scripter
cd Scripter
python3 -m pip install -U .
```

## Example

```python
from scripter import Script

my_script = Script("Macbeth", "Shakespeare")

act1 = my_script.add_act()

act1.add_scene("A Desert Place. Thunder and lightning. Enter three Witches.")

act1.add_dialogue("When shall we three meet again\nIn thunder lightning, or in rain?", author="First Witch")
# Rest of Act 1 Scene 1

if __name__ == '__main__':
    my_script.create("Macbeth")
    # Result in ./tests
```

## Requirements
- `Python` language - version `3.0.0+`
- `python-docx` library - version `0.8.7`

