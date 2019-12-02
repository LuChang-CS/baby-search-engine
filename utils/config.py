class Configuration:
    def __init__(self, config=None):
        if config is not None:
            assert type(config) is dict

            for key, value in config.items():
                assert type(key) is str
                setattr(self, key, value)
