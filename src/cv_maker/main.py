from . import config
from .backend import LatexEngine
from .definitions import MultilangCVData
from .loader import YamlLoader
from .mode import StandaloneMode


def main():
    config.BUILD_DIR.mkdir(parents=True, exist_ok=True)

    engine = LatexEngine()

    data_loader = YamlLoader[MultilangCVData]()
    parser = StandaloneMode(engine, StandaloneMode.init_parser())
    parser.execute(data_loader, parser.parser)

if __name__ == "__main__":
    main()
