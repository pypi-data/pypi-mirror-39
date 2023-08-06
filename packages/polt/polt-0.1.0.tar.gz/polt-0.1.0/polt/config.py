# system modules
import configparser
import shlex

# internal modules
from polt.utils import normalize_cmd

# external modules


class Configuration(configparser.ConfigParser):
    """
    Class for configurations.
    """

    SOURCE_SECTION_PREFIX = "source"
    """
    Prefix for sections specifying a source
    """

    @property
    def source_section(self):
        """
        Generator yielding source sections

        Yields:
            configparser.SectionProxy: the next source section
        """
        for name, section in self.items():
            if name.startswith(self.SOURCE_SECTION_PREFIX):
                yield section

    def matching_source_section(self, command=None, parser=None):
        """
        Generator yielding source sections with a similar specification

        Args:
            cmd (str, optional): the command to check for
            parser (str, optional): the parser to check for

        Yields:
            configparser.SectionProxy: the next matching source section
        """
        for section in self.source_section:
            command_matches = False
            if command is not None:
                this_cmd = section.get("command")
                if not this_cmd:  # pragma: no cover
                    continue
                if normalize_cmd(this_cmd) == normalize_cmd(command):
                    command_matches = True
            else:
                command_matches = True
            parser_matches = False
            if parser is not None:
                this_parser = section.get("parser")
                parser_matches = this_parser == parser
            else:
                parser_matches = True
            if command_matches and parser_matches:
                yield section
