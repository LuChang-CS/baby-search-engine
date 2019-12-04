class Configuration:
    """Configuration class
    """
    def __init__(self, config=None):
        """Initialize the configuration

        @param config: dict, key value pairs for configuration, like
                       {
                           'key': value
                       }
        """
        if config is not None:
            assert type(config) is dict

            for key, value in config.items():
                assert type(key) is str
                setattr(self, key, value)
