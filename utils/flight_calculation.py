from pyorbital.orbital import Orbital
import datetime

satellites = [
    "METEOR-M2 2",
    "METEOR-M2 3",
    "NOAA 18",
    "NOAA 19",
    "METOP-B",
    "METOP-C"
]  # Названия спутников, для которых стоится расписание


class CalculationsSatellite:
    """Класс, производящий расчеты полёта спутника"""

    def __init__(self, coordinates, horizon_and_culmination, schedule_length):
        self.satellites_list = []
        self.intersecting_flights = []

        for satellite_name in satellites:
            # Добавляем информацию каждого спутника в список
            self.satellite_info(satellite_name, coordinates, horizon_and_culmination, schedule_length)
        self.sort_satellite()
        self.correction_flying()

    def satellite_info(self, satellite_name, coordinates, horizon_and_culmination, schedule_length):
        """Добавляет информацию про спутник в satellites_list"""
        latitude, longitude, altitude = coordinates
        horizon, minimum_culmination = horizon_and_culmination
        start_time, flight_length = schedule_length

        satellite = Orbital(satellite_name, tle_file='utils/tle.txt')

        # Определяем время выхода объекта из-за горизонта

        passes = satellite.get_next_passes(start_time, flight_length, longitude, latitude, altitude, horizon=horizon)

        # Выводим время
        for p in passes:
            max_elevation_time = p[2]
            # Получаем кульминацию в градусах
            _, elevation = satellite.get_observer_look(max_elevation_time, longitude, latitude, altitude)
            if elevation >= minimum_culmination:
                # Если небыли найдены спутники с кульминацией > минимальной кульминации

                # Время выхода и захода из-за горизонта
                rise_time = p[0].replace(microsecond=0)
                fall_time = p[1].replace(microsecond=0)

                # Округляем кульминацию до сотых
                elevation = round(elevation, 2)
                self.satellites_list.append([satellite_name, rise_time, fall_time, elevation])
        else:
            # Если не найдены полеты с кульминацией > минимальной кульминации
            return

    def sort_satellite(self):
        """Сортирует dictionary по первому значению"""
        self.satellites_list = list(sorted(self.satellites_list, key=lambda i: i[1]))

    def correction_flying(self):
        """Исправляем “пересекающиеся” полёты"""
        for i in range(len(self.satellites_list)):
            if i == 0:  # Пропускаем первый элемент
                continue

            flight_satellite1 = self.satellites_list[i - 1][2]  # Время выхода из-за горизонта
            flight_satellite2 = self.satellites_list[i][1]  # Время захода за горизонт

            if flight_satellite1 >= flight_satellite2:  # Если полёт пересекается
                new_time = flight_satellite1 + datetime.timedelta(seconds=1)  # Новое время
                self.satellites_list[i][1] = new_time

                self.intersecting_flights.extend([i, i + 1])  # Добавляем индекс выхода и индекс изменённого захода

        self.intersecting_flights = frozenset(self.intersecting_flights)


def trajectory_satellite(satellite_name, start_time, end_time, latitude, longitude, altitude) -> str:
    """Построение и запись в файл поминутной траектории спутника"""
    satellite = Orbital(satellite_name, tle_file='utils/tle.txt')
    # Определяем время выхода объекта из-за горизонта
    text_to_write = (f"Satellite {satellite_name}\n"
                     f"Start date & time {start_time.strftime('%Y-%m-%d %H:%M:%S')} UTC\n"
                     f"Time (UTC) Azimuth Elevation\n")
    while start_time <= end_time:
        p = satellite.get_observer_look(start_time, longitude, latitude, altitude)
        p = [round(val, 2) for val in p]
        print(f"{start_time.strftime('%H:%M:%S')} {p[0]} {p[1]}")
        text_to_write += f"{start_time.strftime('%H:%M:%S')} {p[0]} {p[1]}\n"
        start_time = start_time + datetime.timedelta(seconds=1)
    # Убираем последний отступ
    text_to_write = text_to_write[:-1]
    return text_to_write
