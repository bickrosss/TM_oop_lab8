import pytest
import math

from tasks.pipeline_arctan_series import ArctanSeriesPipeline


def test_term_calculation() -> None:
    """Проверка вычисления членов ряда."""
    pipeline = ArctanSeriesPipeline(x=0.35)

    # n=0: x^1/1 = 0.35
    assert pipeline._term(0) == pytest.approx(0.35)

    # n=1: x^3/3 = 0.35^3/3
    assert pipeline._term(1) == pytest.approx(0.35**3 / 3)

    # n=2: x^5/5 = 0.35^5/5
    assert pipeline._term(2) == pytest.approx(0.35**5 / 5)


def test_second_function() -> None:
    """Проверка аналитического вычисления."""
    x = 0.35
    pipeline = ArctanSeriesPipeline(x=x)

    # Ожидаемое значение: 0.5 * ln((1+x)/(1-x))
    expected = 0.5 * math.log((1 + x) / (1 - x))
    assert pipeline._second_function() == pytest.approx(expected)


def test_series_convergence() -> None:
    """Проверка сходимости ряда к аналитическому значению."""
    pipeline = ArctanSeriesPipeline(x=0.35, eps=1e-7)

    pipeline.run()

    assert pipeline.series_result is not None
    assert pipeline.final_result is not None

    error = abs(pipeline.series_result - pipeline.final_result)
    assert error < 2e-7


def test_pipeline_final_result() -> None:
    """Проверка результатов конвейера."""
    pipeline = ArctanSeriesPipeline(x=0.35, eps=1e-7)

    pipeline.run()

    assert pipeline.series_result is not None
    assert pipeline.final_result is not None

    expected = 0.5 * math.log((1 + 0.35) / (1 - 0.35))
    assert pipeline.final_result == pytest.approx(expected)


def test_event_is_set() -> None:
    """Проверка, что событие установлено после вычислений."""
    pipeline = ArctanSeriesPipeline(x=0.35, eps=1e-7)

    pipeline.run()

    assert pipeline.ready_event.is_set()


@pytest.mark.parametrize("x", [0.1, 0.2, 0.3, 0.35])
def test_series_for_different_x(x: float) -> None:
    """Проверка для различных значений x."""
    pipeline = ArctanSeriesPipeline(x=x, eps=1e-7)

    pipeline.run()

    expected = 0.5 * math.log((1 + x) / (1 - x))

    assert pipeline.series_result == pytest.approx(expected, rel=1e-6)
    assert pipeline.final_result == pytest.approx(expected)


def test_edge_cases() -> None:
    """Проверка граничных случаев."""
    pipeline = ArctanSeriesPipeline(x=0.0, eps=1e-7)
    pipeline.run()

    assert pipeline.series_result == pytest.approx(0.0, abs=1e-7)
    assert pipeline.final_result == pytest.approx(0.0)


def test_error_calculation() -> None:
    """Проверка вычисления погрешностей."""
    pipeline = ArctanSeriesPipeline(x=0.35, eps=1e-7)
    pipeline.run()

    abs_error = pipeline.get_absolute_error()
    rel_error = pipeline.get_relative_error()

    assert abs_error is not None
    assert rel_error is not None
    assert abs_error < 2e-7


def test_series_result_not_none() -> None:
    """Проверка, что series_result не None после выполнения."""
    pipeline = ArctanSeriesPipeline(x=0.35, eps=1e-7)
    pipeline.run()
    assert pipeline.series_result is not None


def test_final_result_not_none() -> None:
    """Проверка, что final_result не None после выполнения."""
    pipeline = ArctanSeriesPipeline(x=0.35, eps=1e-7)
    pipeline.run()
    assert pipeline.final_result is not None
