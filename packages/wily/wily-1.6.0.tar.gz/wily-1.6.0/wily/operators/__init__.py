"""Models and types for "operators" the basic measure of a module that measures code."""

from collections import namedtuple
from enum import Enum


class MetricType(Enum):
    """Type of metric, used in trends."""

    AimLow = 1  # Low is good, high is bad
    AimHigh = 2  # High is good, low is bad
    Informational = 3  # Doesn't matter


Metric = namedtuple("Metric", "name description type measure")

GOOD_COLORS = {
    MetricType.AimHigh: 32,
    MetricType.AimLow: 31,
    MetricType.Informational: 33,
}

BAD_COLORS = {
    MetricType.AimHigh: 31,
    MetricType.AimLow: 32,
    MetricType.Informational: 33,
}


class OperatorLevel(Enum):
    """Level of operator."""

    File = 1
    Object = 2


class BaseOperator(object):
    """Abstract Operator Class."""

    """Name of the operator."""
    name = "abstract"

    """Default settings."""
    defaults = {}

    """Available metrics as a list of tuple ("name"<str>, "description"<str>, "type"<type>, "metric_type"<MetricType>)."""
    metrics = ()

    """Which metric is the default to display in the report command."""
    default_metric_index = None

    """Level at which the operator goes to."""
    level = OperatorLevel.File

    def run(self, module, options):
        """
        Run the operator.

        :param module: The target module path.
        :type  module: ``str``

        :param options: Any runtime options.
        :type  options: ``dict``

        :return: The operator results.
        :rtype: ``dict``
        """
        raise NotImplementedError


from wily.operators.cyclomatic import CyclomaticComplexityOperator
from wily.operators.maintainability import MaintainabilityIndexOperator
from wily.operators.raw import RawMetricsOperator

"""Type for an operator."""
Operator = namedtuple("Operator", "name cls description level")

OPERATOR_CYCLOMATIC = Operator(
    name="cyclomatic",
    cls=CyclomaticComplexityOperator,
    description="Cyclomatic Complexity of modules",
    level=OperatorLevel.Object,
)

OPERATOR_RAW = Operator(
    name="raw",
    cls=RawMetricsOperator,
    description="Raw Python statistics",
    level=OperatorLevel.File,
)

OPERATOR_MAINTAINABILITY = Operator(
    name="maintainability",
    cls=MaintainabilityIndexOperator,
    description="Maintainability index (lines of code and branching)",
    level=OperatorLevel.File,
)


"""Set of all available operators."""
ALL_OPERATORS = {OPERATOR_CYCLOMATIC, OPERATOR_MAINTAINABILITY, OPERATOR_RAW}


def resolve_operator(name):
    """
    Get the :namedtuple:`wily.operators.Operator` for a given name.

    :param name: The name of the operator
    :return: The operator type
    """
    r = [operator for operator in ALL_OPERATORS if operator.name == name.lower()]
    if not r or len(r) == 0:
        raise ValueError(f"Operator {name} not recognised.")
    else:
        return r[0]


def resolve_operators(operators):
    """
    Resolve a list of operator names to their corresponding types.

    :param operators: The list of operators
    :type  operators: iterable or ``str``

    :rtype: ``list`` of :class:`Operator`
    """
    return [resolve_operator(operator) for operator in operators]


def resolve_metric(metric):
    """
    Resolve metric key to a given target.

    :param metric: the metric name.
    :type  metric: ``str``

    :rtype: :class:`Metric`
    """
    operator, key = metric.split(".")
    r = [
        metric for metric in resolve_operator(operator).cls.metrics if metric[0] == key
    ]
    if not r or len(r) == 0:
        raise ValueError(f"Metric {metric} not recognised.")
    else:
        return r[0]


def get_metric(revision, operator, path, key):
    """
    Get a metric from the cache.

    :param revision: The revision id.
    :type  revision: ``str``

    :param operator: The operator name.
    :type  operator: ``str``

    :param path: The path to the file/function
    :type  path: ``str``

    :param key: The key of the data
    :type  key: ``str``

    :return: Data from the cache
    :rtype: ``dict``
    """
    if ":" in path:
        part, entry = path.split(":")
        val = revision[operator][part][entry][key]
    else:
        val = revision[operator][path][key]
    return val
