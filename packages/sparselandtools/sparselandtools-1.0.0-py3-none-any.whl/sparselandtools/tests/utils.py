import os


class Example:
    output_dir = "outputs"

    def __init__(self, no: str, name: str):
        self.no = no
        self.name = name

    def path(self):
        fname = self.no + "-" + self.name + '.npy'
        return os.path.join(Example.output_dir, fname)
