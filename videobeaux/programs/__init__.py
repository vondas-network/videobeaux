import os

available_programs = [
    f[:-3] for f in os.listdir(os.path.dirname(__file__))
    if f.endswith(".py") and not f.startswith("_")
]
