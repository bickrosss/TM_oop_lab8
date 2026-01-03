#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pipeline_arctan_series import ArctanSeriesPipeline

if __name__ == "__main__":
    # Создаем конвейер с параметрами из задания
    pipeline = ArctanSeriesPipeline(x=0.35, eps=1e-7)
    
    # Выводим описание задачи
    print(pipeline)
    
    # Запускаем конвейер
    pipeline.run()

    print("\n--- РЕЗУЛЬТАТЫ ВЫЧИСЛЕНИЙ ---")
    
    if pipeline.series_result is not None and pipeline.final_result is not None:
        # Выводим результаты с высокой точностью
        print(f"Сумма ряда (приближенно): {pipeline.series_result:.12f}")
        print(f"Аналитическое значение:   {pipeline.final_result:.12f}")
        
        # Вычисляем и выводим погрешности
        error = pipeline.series_result - pipeline.final_result
        abs_error = abs(error)
        
        print(f"\nРазность (S - y):          {error:.2e}")
        print(f"Абсолютная погрешность:   {abs_error:.2e}")
        
        # Вычисляем относительную погрешность
        if pipeline.final_result != 0:
            rel_error = abs_error / abs(pipeline.final_result)
            print(f"Относительная погрешность: {rel_error:.2e}")
        
        # Проверяем достижение заданной точности
        print(f"\nЗаданная точность: ε = {pipeline.eps}")
        if abs_error < pipeline.eps:
            print("✓ Требуемая точность достигнута!")
        else:
            print("✗ Требуемая точность не достигнута")
    
    # Выводим информацию о событии
    print(f"\nСобытие ready_event установлено: {pipeline.ready_event.is_set()}")
    
    print("\n" + "=" * 60)
