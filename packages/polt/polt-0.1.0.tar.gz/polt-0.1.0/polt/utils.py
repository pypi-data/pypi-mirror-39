# system modules
import shlex

# internal modules

# external modules


def flatten(S):
    """
    Function to recursively flatten a list

    Args:
        S (list): the list of nested lists to flatten

    Returns:
        list : the flattened list
    """
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])


def normalize_cmd(cmd):
    """
    Normalise a command

    Args:
        cmd (str): the command to normalize

    Returns:
        str : the normalized command
    """
    return " ".join(map(shlex.quote, shlex.split(cmd)))
