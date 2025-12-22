from setuptools import setup

setup(
    name="sce",
    version="0.1.0",
    description="Simple Chess Engine (SCE)",
    py_modules=[
        "board",
        "constants",
        "eval",
        "fen",
        "main",
        "make_move",
        "move_gen",
        "perft",
        "search",
        "uci",
    ],
    python_requires=">=3.11",
    author="I-AM-SENTIENT",
)
