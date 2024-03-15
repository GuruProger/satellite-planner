from .sat_pass_model import SatellitePassModel, SatelliteParamModel
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
	"""Класс, производящий расчёты полёта спутника"""

	def __init__(self, param: SatelliteParamModel):
		self.satellites_list = []
		self.intersecting_flights = []
		self.param = param

		for satellite_name in satellites:
			# Добавляем информацию каждого спутника в список
			self.satellite_info(satellite_name)
		self.sort_satellite()
		self.correction_flying()

	def satellite_info(self, satellite_name):
		"""Добавляет информацию про спутник в satellites_list"""

		satellite = Orbital(satellite_name, tle_file='utils/tle.txt')

		# Определяем время выхода объекта из-за горизонта
		passes = satellite.get_next_passes(
			self.param.start_time, self.param.flight_length,
			self.param.longitude, self.param.latitude, self.param.altitude, horizon=self.param.horizon)

		# Выводим время
		for pass_sat in passes:
			max_elevation_time = pass_sat[2]
			# Получаем кульминацию в градусах
			_, elevation = satellite.get_observer_look(
				max_elevation_time, self.param.longitude, self.param.latitude, self.param.altitude)
			if elevation >= self.param.minimum_culmination:
				# Если небыли найдены спутники с кульминацией > минимальной кульминации

				# Время выхода и захода из-за горизонта
				rise_time = pass_sat[0].replace(microsecond=0)
				fall_time = pass_sat[1].replace(microsecond=0)

				# Округляем кульминацию до сотых
				elevation = round(elevation, 2)
				self.satellites_list.append(SatellitePassModel(satellite_name, rise_time, fall_time, elevation))

	def sort_satellite(self):
		"""Сортирует dictionary по первому значению"""
		self.satellites_list = list(sorted(self.satellites_list, key=lambda i: i.rise))

	def correction_flying(self):
		"""Исправляем "пересекающиеся" полёты"""

		for i in range(1, len(self.satellites_list)):
			fall_satellite = self.satellites_list[i - 1].fall  # Время выхода из-за горизонта
			rise_satellite = self.satellites_list[i].rise  # Время захода за горизонт

			if fall_satellite >= rise_satellite:  # Если полёт пересекается
				new_fall_time = fall_satellite + datetime.timedelta(seconds=1)  # Новое время захода за горизонт
				self.satellites_list[i].fall = new_fall_time
				self.intersecting_flights.extend([i, i + 1])  # Добавляем индекс выхода и изменённого захода

		self.intersecting_flights = frozenset(self.intersecting_flights)  # Удаляем совпадения


def trajectory_satellite(satellite_name, start_time, end_time, latitude, longitude, altitude) -> str:
	"""Построение и запись в файл поминутной траектории спутника"""
	satellite = Orbital(satellite_name, tle_file='utils/tle.txt')
	text_to_write = (
		f"Satellite {satellite_name}\n"
		f"Start date & time {start_time.strftime('%Y-%m-%d %H:%M:%S')} UTC\n"
		f"Time (UTC) Azimuth Elevation\n"
	)

	# Определяем время выхода объекта из-за горизонта
	while start_time <= end_time:
		pass_sat = satellite.get_observer_look(start_time, longitude, latitude, altitude)
		pass_sat = [round(val, 2) for val in pass_sat]
		print(f"{start_time.strftime('%H:%M:%S')} {pass_sat[0]} {pass_sat[1]}")
		text_to_write += f"{start_time.strftime('%H:%M:%S')} {pass_sat[0]} {pass_sat[1]}\n"
		start_time = start_time + datetime.timedelta(seconds=1)
	# Убираем последний отступ
	text_to_write = text_to_write[:-1]
	return text_to_write
