# -*- coding: utf-8 -*-
from sklearn.base import BaseEstimator
from sktime.performance_metrics.forecasting._functions import (
    mean_asymmetric_error,
    mean_absolute_scaled_error,
    median_absolute_scaled_error,
    mean_squared_scaled_error,
    median_squared_scaled_error,
    mean_absolute_error,
    mean_squared_error,
    median_absolute_error,
    median_squared_error,
    mean_absolute_percentage_error,
    median_absolute_percentage_error,
    mean_squared_percentage_error,
    median_squared_percentage_error,
    mean_relative_absolute_error,
    median_relative_absolute_error,
    geometric_mean_relative_absolute_error,
    geometric_mean_relative_squared_error,
)

__author__ = ["Markus Löning", "Tomasz Chodakowski", "Ryan Kuhns"]
__all__ = [
    "MetricFunctionWrapper",
    "PercentageMetricFunctionWrapper",
    "SquaredMetricFunctionWrapper",
    "SquaredPercentageMetricFunctionWrapper",
    "make_forecasting_scorer",
    "MeanAbsoluteScaledError",
    "MedianAbsoluteScaledError",
    "MeanSquaredScaledError",
    "MedianSquaredScaledError",
    "MeanAbsoluteError",
    "MeanSquaredError",
    "MedianAbsoluteError",
    "MedianSquaredError",
    "MeanAbsolutePercentageError",
    "MedianAbsolutePercentageError",
    "MeanSquaredPercentageError",
    "MedianSquaredPercentageError",
    "MeanRelativeAbsoluteError",
    "MedianRelativeAbsoluteError",
    "GeometricMeanRelativeAbsoluteError",
    "GeometricMeanRelativeSquaredError",
]


class MetricFunctionWrapper(BaseEstimator):
    def __init__(self, func, name=None, greater_is_better=False):
        self._func = func
        self.name = name if name is not None else func.__name__
        self.greater_is_better = greater_is_better

    def __call__(self, y_true, y_pred):
        return self._func(y_true, y_pred)


class _PercentageErrorMixIn:
    def __call__(self, y_true, y_pred):
        return self._func(y_true, y_pred, symmetric=self.symmetric)


class _SquaredErrorMixIn:
    def __call__(self, y_true, y_pred):
        return self._func(y_true, y_pred, square_root=self.square_root)


class _SquaredPercentageErrorMixIn:
    def __call__(self, y_true, y_pred):
        return self._func(
            y_true, y_pred, symmetric=self.symmetric, square_root=self.square_root
        )


class _AsymmetricErrorMixIn:
    def __call__(self, y_true, y_pred):
        return self._func(
            y_true,
            y_pred,
            asymmetric_threshold=self.asymmetric_treshold,
            left_error_function=self.left_error_function,
            right_error_function=self.right_error_function,
        )


class PercentageMetricFunctionWrapper(_PercentageErrorMixIn, MetricFunctionWrapper):
    def __init__(self, func, name=None, greater_is_better=False, symmetric=True):
        self.symmetric = symmetric
        super().__init__(func=func, name=name, greater_is_better=greater_is_better)


class SquaredMetricFunctionWrapper(_SquaredErrorMixIn, MetricFunctionWrapper):
    def __init__(self, func, name=None, greater_is_better=False, square_root=False):
        self.square_root = square_root
        super().__init__(func=func, name=name, greater_is_better=greater_is_better)


class SquaredPercentageMetricFunctionWrapper(
    _SquaredPercentageErrorMixIn, MetricFunctionWrapper
):
    def __init__(
        self,
        func,
        name=None,
        greater_is_better=False,
        square_root=False,
        symmetric=True,
    ):
        self.square_root = square_root
        self.symmetric = symmetric
        super().__init__(func=func, name=name, greater_is_better=greater_is_better)


class AsymmetricMetricFunctionWrapper(_AsymmetricErrorMixIn, MetricFunctionWrapper):
    def __init__(
        self,
        func,
        name=None,
        greater_is_better=False,
        asymmetric_threshold=0,
        left_error_function="squared",
        right_error_function="absolute",
    ):
        self.asymmetric_threshold = asymmetric_threshold
        self.left_error_function = left_error_function
        self.right_error_function = right_error_function
        super().__init__(func=func, name=name, greater_is_better=greater_is_better)


def make_forecasting_scorer(
    func, name=None, greater_is_better=False, symmetric=None, square_root=None
):
    """Factory method for creating metric classes from metric functions

    Parameters
    ----------
    func:
        Loss function to convert to a forecasting scorer class

    name: str, default=None
        Name to use for the forecasting scorer loss class

    greater_is_better: bool, default=False
        If True then maximizing the metric is better.
        If False then minimizing the metric is better.

    symmetric: bool, default=None
        Whether to calculate symmetric percentage error.
            If None then created metric class does not include a `symmetric`
                parameter
            If True, created metric class includes has `symmetric` attribute
                equal to True. Metric calculates symmetric version of
                percentage error loss function.
            If False, created metric class includes has `symmetric` attribute
                equal to False. Metric calculates standard version of
                percentage error loss function

    square_root: bool, default=None
        Whether to take the square root of the calculated metric.
            If None then created metric class does not include a `square_root`
                parameter
            If True, created metric class includes has `square_root` attribute
                equal to True. Metric calculates square root of provided loss function.
            If False, created metric class includes has `square_root` attribute
                equal to False. Metric calculates provided loss function.

    Returns
    -------
    scorer:
        Metric class that can be used as forecasting scorer.
    """
    # Create base
    if symmetric is None and square_root is None:
        return MetricFunctionWrapper(
            func, name=name, greater_is_better=greater_is_better
        )
    elif symmetric is not None and square_root is None:
        return PercentageMetricFunctionWrapper(
            func, name=name, greater_is_better=greater_is_better, symmetric=symmetric
        )
    elif symmetric is None and square_root is not None:
        return SquaredMetricFunctionWrapper(
            func,
            name=name,
            greater_is_better=greater_is_better,
            square_root=square_root,
        )

    elif symmetric is not None and square_root is not None:
        return SquaredPercentageMetricFunctionWrapper(
            func,
            name=name,
            greater_is_better=greater_is_better,
            symmetric=symmetric,
            square_root=square_root,
        )


class MeanAbsoluteScaledError(MetricFunctionWrapper):
    def __init__(self):
        name = "MeanAbsoluteScaledError"
        func = mean_absolute_scaled_error
        greater_is_better = False
        super().__init__(func=func, name=name, greater_is_better=greater_is_better)


class MedianAbsoluteScaledError(MetricFunctionWrapper):
    def __init__(self):
        name = "MedianAbsoluteScaledError"
        func = median_absolute_scaled_error
        greater_is_better = False
        super().__init__(func=func, name=name, greater_is_better=greater_is_better)


class MeanSquaredScaledError(SquaredMetricFunctionWrapper):
    def __init__(self, square_root=False):
        name = "MeanSquaredScaledError"
        func = mean_squared_scaled_error
        greater_is_better = False
        super().__init__(
            func=func,
            name=name,
            greater_is_better=greater_is_better,
            square_root=square_root,
        )


class MedianSquaredScaledError(SquaredMetricFunctionWrapper):
    def __init__(self, square_root=False):
        name = "MedianSquaredScaledError"
        func = median_squared_scaled_error
        greater_is_better = False
        super().__init__(
            func=func,
            name=name,
            greater_is_better=greater_is_better,
            square_root=square_root,
        )


class MeanAbsoluteError(MetricFunctionWrapper):
    def __init__(self):
        name = "MeanAbsoluteError"
        func = mean_absolute_error
        greater_is_better = False
        super().__init__(func=func, name=name, greater_is_better=greater_is_better)


class MedianAbsoluteError(MetricFunctionWrapper):
    def __init__(self):
        name = "MedianAbsoluteError"
        func = median_absolute_error
        greater_is_better = False
        super().__init__(func=func, name=name, greater_is_better=greater_is_better)


class MeanSquaredError(SquaredMetricFunctionWrapper):
    def __init__(self, square_root=False):
        name = "MeanSquaredError"
        func = mean_squared_error
        greater_is_better = False
        super().__init__(
            func=func,
            name=name,
            greater_is_better=greater_is_better,
            square_root=square_root,
        )


class MedianSquaredError(SquaredMetricFunctionWrapper):
    def __init__(self, square_root=False):
        name = "MedianSquaredError"
        func = median_squared_error
        greater_is_better = False
        super().__init__(
            func=func,
            name=name,
            greater_is_better=greater_is_better,
            square_root=square_root,
        )


class MeanAbsolutePercentageError(PercentageMetricFunctionWrapper):
    def __init__(self, symmetric=True):
        name = "MeanAbsolutePercentageError"
        func = mean_absolute_percentage_error
        greater_is_better = False
        super().__init__(
            func=func,
            name=name,
            greater_is_better=greater_is_better,
            symmetric=symmetric,
        )


class MedianAbsolutePercentageError(PercentageMetricFunctionWrapper):
    def __init__(self, symmetric=True):
        name = "MedianAbsolutePercentageError"
        func = median_absolute_percentage_error
        greater_is_better = False
        super().__init__(
            func=func,
            name=name,
            greater_is_better=greater_is_better,
            symmetric=symmetric,
        )


class MeanSquaredPercentageError(SquaredPercentageMetricFunctionWrapper):
    def __init__(self, symmetric=True, square_root=False):
        name = "MeanSquaredPercentageError"
        func = mean_squared_percentage_error
        greater_is_better = False
        super().__init__(
            func=func,
            name=name,
            greater_is_better=greater_is_better,
            symmetric=symmetric,
            square_root=square_root,
        )


class MedianSquaredPercentageError(SquaredPercentageMetricFunctionWrapper):
    def __init__(self, symmetric=True, square_root=False):
        name = "MedianSquaredPercentageError"
        func = median_squared_percentage_error
        greater_is_better = False
        super().__init__(
            func=func,
            name=name,
            greater_is_better=greater_is_better,
            symmetric=symmetric,
            square_root=square_root,
        )


class MeanRelativeAbsoluteError(MetricFunctionWrapper):
    def __init__(self):
        name = "MeanRelativeAbsoluteError"
        func = mean_relative_absolute_error
        greater_is_better = False
        super().__init__(func=func, name=name, greater_is_better=greater_is_better)


class MedianRelativeAbsoluteError(MetricFunctionWrapper):
    def __init__(self):
        name = "MedianRelativeAbsoluteError"
        func = median_relative_absolute_error
        greater_is_better = False
        super().__init__(func=func, name=name, greater_is_better=greater_is_better)


class GeometricMeanRelativeAbsoluteError(MetricFunctionWrapper):
    def __init__(self):
        name = "GeometricMeanRelativeAbsoluteError"
        func = geometric_mean_relative_absolute_error
        greater_is_better = False
        super().__init__(func=func, name=name, greater_is_better=greater_is_better)


class GeometricMeanRelativeSquaredError(SquaredMetricFunctionWrapper):
    def __init__(self, square_root=False):
        name = "GeometricMeanRelativeSquaredError"
        func = geometric_mean_relative_squared_error
        greater_is_better = False
        super().__init__(
            func=func,
            name=name,
            greater_is_better=greater_is_better,
            square_root=square_root,
        )


class MeanAsymmetricError(AsymmetricMetricFunctionWrapper):
    def __init__(
        self,
        asymmetric_threshold=0,
        left_error_function="squared",
        right_error_function="absolute",
    ):
        name = "MeanAsymmetricError"
        func = mean_asymmetric_error
        greater_is_better = False
        super().__init__(
            func=func,
            name=name,
            greater_is_better=greater_is_better,
            asymmetric_threshold=asymmetric_threshold,
            left_error_function=left_error_function,
            right_error_function=right_error_function,
        )
