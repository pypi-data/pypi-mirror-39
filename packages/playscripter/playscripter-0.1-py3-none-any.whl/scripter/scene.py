from scripter.dialogue import Dialogue, StageDirection


class Act:
    """
    The script's act.
    """
    def __init__(self):
        self.scenes = []

    def add_scene(self, description: str):
        """
        Append a new instance of `Scene` to
        `Act.scenes`.
        :param description: The scene description
        :return: The newly created `Scene`
        """
        self.scenes.append(Scene(description))
        return self.scenes[-1]

    def add_dialogue(self, description: str, *, author: str=None):
        """
        Short-hand for `Scene.add_dialogue`.
        Gets the last `Scene` and calls its
        `Scene.add_dialogue`.
        :param author: The author of the dialogue
        :param description: What the author will say
        """
        self.scenes[-1].add_dialogue(description, author=author)

    def add_direction(self, description: str):
        """
        Short-hand for `Scene.add_direction`.
        Gets the last `Scene` and call its
        `Scene.add_dialogue`.
        :param description: What the author will say
        """
        self.scenes[-1].add_dialogue(description)


class Scene:
    """
    The script's scene
    """
    def __init__(self, description: str):
        """
        New instance of `Scene`
        :param description: The scene description
        """
        self.description = description
        self.dialogue = []

    def add_dialogue(self, description: str, *, author: str=None):
        """
        Appends a `Dialogue` or `StageDirection`
        to the `Scene.dialogue`
        :param author: The author of the dialogue
        :param description: What the author will say
        """
        if author:
            self.dialogue.append(Dialogue(author, description))
        else:
            self.dialogue.append(StageDirection(description))

    def add_direction(self, description: str):
        """
        Calls `add_dialogue` without the `author`.
        This means it will become a `StageDirection`.
        :param description:
        :return:
        """
        self.add_dialogue(description)
