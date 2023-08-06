class Dialogue:
    """
    Dialogue for the `Scene`
    """
    def __init__(self, character: str, description: str):
        """
        New instance of `Dialogue`
        :param character: The character's name
        :param description: What the character says
        """
        self.character = character
        self.description = description


class StageDirection:
    """
    Stage directions for the `Scene`
    """
    def __init__(self, direction: str):
        """
        New instance of `StageDirection`
        :param direction: What the direction should say
        """
        self.direction = direction

    def __str__(self):
        """
        Formated version of `StageDirection.direction`
        for the creation of a Word document.
        :return: `"(YOUR STAGE DIRECTION HERE)"`
        """
        return '({})'.format(self.direction)
