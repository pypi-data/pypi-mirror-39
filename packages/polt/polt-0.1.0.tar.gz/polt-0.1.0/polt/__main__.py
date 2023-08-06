#!/usr/bin/env python3
# system modules
import argparse
import logging
import os
import sys
import itertools
import select
import datetime
import multiprocessing
import subprocess
import shlex
import configparser
import time
import re
import importlib

# internal modules
import polt

# external modules
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import xdgspec


def existing_file(arg):
    if os.path.isfile(arg):
        return arg
    else:
        raise argparse.ArgumentTypeError(
            "File {} does not exist".format(repr(arg))
        )


parser_aliases = {"numbers": polt.parser.NumberParser}


def source_spec(arg):
    parts = arg.split(":")
    if len(parts) == 1:
        cmd = parts[0]
        parser_spec = "numbers"
    elif len(parts) >= 2:
        parser_spec, cmd = parts[0], ":".join(parts[1:])
    else:
        raise argparse.ArgumentTypeError("You should never see this...")
    if not polt.utils.normalize_cmd(cmd):
        raise argparse.ArgumentTypeError("Empty source ({})".format(repr(cmd)))
    parser_cls = parser_aliases.get(parser_spec)
    if not parser_cls:
        parts = parser_spec.split(".")
        try:
            package, classname = ".".join(parts[:-1]), parts[-1]
            module = importlib.import_module(package)
            parser_cls = getattr(module, classname)
        except (IndexError, ImportError, AttributeError, ValueError) as e:
            raise argparse.ArgumentTypeError(
                "parser specification {p} (for source {s}) "
                "is neither an alias (like {aliases}) "
                "nor an importable class specification ({err})"
                "".format(
                    p=repr(parser_spec),
                    s=repr(cmd),
                    aliases=", ".join(map(repr, parser_aliases)),
                    err=e,
                )
            )
    return (parser_spec, cmd)


user_config_file = os.path.join(
    xdgspec.XDGPackageDirectory("XDG_CONFIG_HOME", "polt").path, "polt.conf"
)
local_config_file = ".polt.conf"

argparser = argparse.ArgumentParser(
    prog="python3 -m polt",
    description="polt - Live Data Visualisation via Matplotlib",
)
configgroup = argparser.add_argument_group(
    title="Configuration Options",
    description="These options control how configuration is managed",
)
configgroup.add_argument(
    "--no-config",
    action="store_true",
    help="Don't read default configuration file(s) ({} and {})".format(
        repr(user_config_file), repr(local_config_file)
    ),
)
configgroup.add_argument(
    "-c",
    "--config",
    metavar="file",
    nargs="+",
    help="Extra configuration file(s) to read (after {} and {})".format(
        repr(user_config_file), repr(local_config_file)
    ),
    type=existing_file,
    default=[],
)
configgroup.add_argument(
    "--save-config",
    metavar="file",
    nargs="?",
    help="Save the current configuration into this file. "
    "If this option is specified without further arguments, "
    "{} is used.".format(repr(local_config_file)),
    const=local_config_file,
)
loggroup = argparser.add_argument_group(
    title="Logging Options",
    description="These options control the amount of output verbosity",
)
logoptions = loggroup.add_mutually_exclusive_group()
logoptions.add_argument(
    "-v", "--verbose", help="verbose output", action="store_true"
)
logoptions.add_argument(
    "-q", "--quiet", help="only show warnings", action="store_true"
)
inputgroup = argparser.add_argument_group(
    title="Input Options",
    description="These options control from where and how data is read",
)
inputgroup.add_argument(
    "--source",
    metavar=("[parser:]source"),
    type=source_spec,
    action="append",
    help="Add a 'source' to read numbers from by parsing with 'parser'. "
    "Specify a dash (-) for 'source' to read from stdin. "
    "The 'parser' may either be one of the aliases {} "
    "or a class path specification (like 'mypackage.MyParser') pointing to "
    "a subclass of 'poly.parser.Parser'. "
    "When 'parser' is left out, the default (polt.parser.NumberParser) "
    "is used to just extract any numbers.".format(
        ", ".join(map(repr, parser_aliases))
    ),
    default=[],
)
inputgroup.add_argument(
    "--soft-shutdown",
    help="Shut down input threads gracefully",
    action="store_true",
)
plotoptions = argparser.add_argument_group(
    title="Plot Options", description="These options control the plot"
)
plotoptions.add_argument(
    "--interval",
    metavar=("milliseconds"),
    help="plot update interval [default:200]",
    type=lambda x: max(int(x), 1),  # minimum 1ms, below does not work
)
argparser.add_argument(
    "--version", action="version", version="polt v{}".format(polt.__version__)
)
args = argparser.parse_args()


# set up logging
loglevel = logging.DEBUG if args.verbose else logging.INFO
loglevel = logging.WARNING if args.quiet else loglevel
logging.basicConfig(
    level=loglevel,
    format="%(processName)s %(threadName)s  "
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("polt-cli")
for n, l in logger.manager.loggerDict.items():
    if not n.startswith("polt"):
        l.propagate = False

# initialise the configuration
config = polt.config.Configuration()
# read configuration files
config.read(
    ([] if args.no_config else [user_config_file, local_config_file])
    + args.config
)
# merge command-line arguments into the configuration
if "plot" not in config:
    config.add_section("plot")
if args.interval is None:
    if "interval" not in config["plot"]:
        config["plot"]["interval"] = str(200)
else:
    config["plot"]["interval"] = str(args.interval)
# merge command-line source commands into the configuration
for parser_spec, cmd in polt.utils.flatten(args.source):
    matching_sections = list(config.matching_source_section(command=cmd))
    for section in matching_sections:
        logger.warning(
            "Removing configuration section {section} because it matches "
            "the given command-line source command {clicmd}.".format(
                clicmd=repr(cmd),
                section="{} (parsing {} from {})".format(
                    repr(section.name),
                    section.get("parser"),
                    repr(section.get("command")),
                ),
            )
        )
        config.remove_section(section.name)
    section_name = "{}:{}".format(
        config.SOURCE_SECTION_PREFIX,
        "stdin" if cmd == "-" else polt.utils.normalize_cmd(cmd),
    )
    config.add_section(section_name)
    config[section_name]["command"] = cmd
    config[section_name]["parser"] = parser_spec


# save configuration if desired
if args.save_config is not None:
    config_file = args.save_config
    directory, name = os.path.split(config_file)
    directory = os.path.expanduser(directory)
    logger.info(
        "Saving current configuration to file {}".format(repr(config_file))
    )
    if directory:
        if not os.path.exists(directory):
            logger.warning("Create nonexistent directory {}".format(directory))
            os.makedirs(directory)
    with open(config_file, "w") as f:
        config.write(f)
    logger.debug(
        "Current configuration successfully saved to file {}".format(
            config_file
        )
    )


def input_parser(section):
    parser_spec = section.get("parser")
    if parser_spec:
        parser_cls = parser_aliases.get(parser_spec)
        if not parser_cls:
            logger.debug(
                "{} is not a parser alias. "
                "Trying to interpret it as a class path specification".format(
                    parser_spec
                )
            )
            parts = parser_spec.split(".")
            try:
                package, classname = ".".join(parts[:-1]), parts[-1]
                module = importlib.import_module(package)
                parser_cls = getattr(module, classname)
            except (IndexError, ImportError, AttributeError):
                logger.error(
                    "parser specification {p} in section {s} "
                    "is neither an alias (like {aliases}) "
                    "nor an importable class specification".format(
                        p=repr(parser_spec),
                        s=repr(section.name),
                        aliases=", ".join(map(repr, parser_aliases)),
                    )
                )
                sys.exit(1)
            if not isinstance(parser_cls, polt.parser.Parser):
                logger.warning(
                    "Specified parser class {} is not a subclass "
                    "of {} and might not work.".format(
                        parser_cls, polt.parser.Parser
                    )
                )
    else:
        logger.error(
            "Section {} does not specify a 'parser'".format(repr(section.name))
        )
        sys.exit(1)
    cmd = section.get("command")
    if cmd:
        if cmd == "-":  # stdin
            f = sys.stdin
        else:  # a command
            process = subprocess.Popen(
                shlex.split(cmd),
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
            )
            try:
                returncode = process.wait(timeout=0.5)
                if returncode == 0:
                    logger.warning(
                        "Command {} is already done".format(repr(cmd))
                    )
                else:
                    logger.error(
                        "Running {} did not work (return code {})".format(
                            repr(cmd), returncode
                        )
                    )
                    sys.exit(1)
            except subprocess.TimeoutExpired:  # still running
                logger.info("Successfully started {}".format(repr(cmd)))
            f = process.stdout
    else:
        logger.error(
            "Section {} does not specify a 'command'".format(
                repr(section.name)
            )
        )
        sys.exit(1)
    return parser_cls(f)


# set up parsers from configuration
parsers = list(map(input_parser, config.source_section))

with multiprocessing.Manager() as manager:

    def animate_process(buf):
        logger.debug("Creating figure")
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        now = datetime.datetime.now()
        ax.set_xlim(now, now + datetime.timedelta(minutes=1))
        fig.autofmt_xdate()

        logger.debug("Creating Animator")
        animator = polt.animator.Animator(
            figure=fig, buffer=buf, interval=config["plot"]["interval"]
        )

        logger.info("Running Animator")
        animator.run()
        logger.info("Animator is done")

    buf = manager.list()
    streamers = [polt.streamer.Streamer(parser, buf) for parser in parsers]
    p = multiprocessing.Process(
        target=animate_process, daemon=True, kwargs={"buf": buf}
    )
    try:
        logger.debug("Starting plot process")
        p.start()
        logger.info("plot process started")
        logger.debug("starting parsing threads")
        for streamer in streamers:
            logger.debug("starting parsing thread {}".format(streamer.name))
            streamer.start()
        logger.info("parsing threads started")
        p.join()
        logger.debug("Plot process exited")
    except KeyboardInterrupt:
        logger.info("User wants to stop")
    if args.soft_shutdown:
        logger.info("shutting down gracefully")
        try:
            for streamer in streamers:
                streamer.stop()
                logger.debug(
                    "Waiting for thread {} to close".format(streamer.name)
                )
                streamer.join()
        except KeyboardInterrupt:
            logger.info("Okay, okay, stopping now...")

logger.info("done")
