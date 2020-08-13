from light_aligner import __version__
from light_aligner.light_scores import light_scores
from light_aligner.light_aligner import light_aligner


def test_version():
    assert __version__ == "0.1.0"
