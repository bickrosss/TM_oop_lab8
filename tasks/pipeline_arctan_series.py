#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from threading import Event, Thread


class ArctanSeriesPipeline:
    """
    Конвейер для вычисления:
    1. Суммы ряда: S = Σ x^(2n+1)/(2n+1) для n от 0 до ∞
    2. Функции: y = ln(sqrt((1+x)/(1-x))) = 0.5 * ln((1+x)/(1-x))
    
    Ряд представляет собой разложение в ряд Тейлора для 0.5*ln((1+x)/(1-x))
    """

    def __init__(self, x: float = 0.35, eps: float = 1e-7) -> None:
        """
        Инициализация конвейера.
        
        Args:
            x: Значение аргумента (по умолчанию 0.35 из задания)
            eps: Точность вычисления (по умолчанию 1e-7 из задания)
        """
        self.x: float = x
        self.eps: float = eps

        self.series_result: float | None = None
        self.final_result: float | None = None

        # Событие для синхронизации потоков
        self.ready_event: Event = Event()

    def _term(self, n: int) -> float:
        """
        Вычисление n-го члена ряда: x^(2n+1)/(2n+1)
        
        Args:
            n: Номер члена ряда (начиная с 0)
            
        Returns:
            Значение n-го члена ряда
        """
        return (self.x ** (2 * n + 1)) / (2 * n + 1)

    def _first_worker(self, index: int) -> None:
        """
        Первый поток: вычисление суммы ряда S = Σ x^(2n+1)/(2n+1)
        
        Args:
            index: Идентификатор потока для отладки
        """
        print(f"[Thread {index}] Начало вычисления суммы ряда для x = {self.x}")

        s: float = 0.0
        n: int = 0
        prev_s: float = 0.0
        
        # Основной цикл суммирования
        while True:
            # Вычисляем текущий член ряда
            a_n = self._term(n)
            s += a_n
            n += 1
            
            if abs(s - prev_s) < self.eps:
                print(f"[Thread {index}] Достигнута точность ε={self.eps} на n={n}")
                break
                
            prev_s = s
            
            if n > 10000: 
                print(f"[Thread {index}] Достигнут предел итераций: {n}")
                break

        self.series_result = s
        print(f"[Thread {index}] Сумма ряда S = {s:.10f} (вычислено {n} членов)")
        
        self.ready_event.set()

    def _second_function(self) -> float:
        """
        Аналитическое вычисление функции:
        y = ln(sqrt((1+x)/(1-x))) = 0.5 * ln((1+x)/(1-x))
        
        Returns:
            Точное значение функции
        """
        return 0.5 * math.log((1 + self.x) / (1 - self.x))

    def _second_worker(self, index: int) -> None:
        """
        Второй поток: вычисление аналитического значения.
        
        Args:
            index: Идентификатор потока для отладки
        """
        print(f"[Thread {index}] Ожидание результата первой функции...")
    
        self.ready_event.wait()

        assert self.series_result is not None
        self.final_result = self._second_function()

        print(f"[Thread {index}] Результат второй функции = {self.final_result:.10f}")

    def run(self) -> None:
        """
        Запуск конвейера вычислений.
        """
        print("=" * 50)
        print("ЗАПУСК КОНВЕЙЕРА ВЫЧИСЛЕНИЙ")
        print("=" * 50)
        
        t1: Thread = Thread(target=self._first_worker, args=(1,))
        t2: Thread = Thread(target=self._second_worker, args=(2,))

        t1.start()
        t2.start()

        t1.join()
        t2.join()
        
        print("\n" + "=" * 50)
        print("КОНВЕЙЕР ВЫПОЛНЕН")
        print("=" * 50)

    def get_absolute_error(self) -> float | None:
        """
        Вычисление абсолютной погрешности.
        
        Returns:
            Абсолютная погрешность или None, если результаты не вычислены
        """
        if self.series_result is not None and self.final_result is not None:
            return abs(self.series_result - self.final_result)
        return None

    def get_relative_error(self) -> float | None:
        """
        Вычисление относительной погрешности.
        
        Returns:
            Относительная погрешность или None, если результаты не вычислены
        """
        if self.series_result is not None and self.final_result is not None:
            if self.final_result != 0:
                return abs((self.series_result - self.final_result) / self.final_result)
        return None

    def __str__(self) -> str:
        """
        Строковое представление задачи.
        
        Returns:
            Описание задачи с формулами
        """
        return (
            "\n" + "=" * 60 + "\n"
            "ИНДИВИДУАЛЬНОЕ ЗАДАНИЕ: ВЫЧИСЛЕНИЕ С ИСПОЛЬЗОВАНИЕМ МНОГОПОТОЧНОСТИ\n"
            "=" * 60 + "\n\n"
            "Ряд для вычисления:\n"
            "S = Σ [x^(2n+1) / (2n+1)], n = 0 .. ∞\n"
            f"  при x = {self.x}\n\n"
            "Аналитическое выражение:\n"
            "y = ln(√((1+x)/(1-x))) = 0.5 * ln((1+x)/(1-x))\n\n"
            f"Точность вычислений: ε = {self.eps}\n"
            "=" * 60 + "\n"
        )
