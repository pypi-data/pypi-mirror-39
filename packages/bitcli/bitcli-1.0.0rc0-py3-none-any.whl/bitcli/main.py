
from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import BitCLIError
from .controllers.base import Base

# configuration defaults
CONFIG = init_defaults('bitcli')
CONFIG['bitcli']['foo'] = 'bar'


class BitCLI(App):
    """Bitpanda prices CLI primary application."""

    class Meta:
        label = 'bitcli'

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        close_on_exit = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'tabulate',
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'tabulate'

        # register handlers
        handlers = [
            Base
        ]


class BitCLITest(TestApp,BitCLI):
    """A sub-class of BitCLI that is better suited for testing."""

    class Meta:
        label = 'bitcli'


def main():
    with BitCLI() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except BitCLIError as e:
            print('BitCLIError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
