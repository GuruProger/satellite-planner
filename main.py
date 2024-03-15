import io
from datetime import datetime
from utils.forms import ParamsForm
from utils import flight_calculation
from flask import Flask, request, render_template, send_file
from utils.flight_calculation import trajectory_satellite
from utils.sat_pass_model import SatelliteParamModel

app = Flask(__name__)
app.secret_key = '#$%^&*'


@app.route("/", methods=["POST", "GET"])
@app.route("/home", methods=["POST", "GET"])
def home():
	form = ParamsForm(request.form)
	if request.method == 'POST':  # При отправке формы
		if not form.validate():
			return (render_template(
				'parameter_input.html',
				form=form) + '<script>alert("Заполните данные правильно")</script>')

		# try:
			# Отображение всех полётов
		flight_data, intersecting_flights = processing_values(form)
		return render_template(
			'flight_table.html',
			form=form, table_data=flight_data, intersection_data=intersecting_flights)

		# except:
		# 	# Неверно заполнены данные
		# 	return (
		# 			render_template('parameter_input.html', form=form)
		# 			+ '<script>alert("Заполните данные правильно")</script>')
	# Если получаем GET запрос, то выводим форму
	return render_template('parameter_input.html', form=form)


@app.route(
	'/download/'
	'<string:satellite_name>/<string:start_time>/<string:end_time>/<float:latitude>/<float:longitude>/<float:altitude>')
def download(satellite_name, start_time, end_time, latitude: float, longitude: float, altitude: float):
	"""Загрузка траектории спутника"""
	start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
	end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
	satellite_params = [satellite_name, start_time, end_time, latitude, longitude, altitude]

	trajectory_satellite_text = trajectory_satellite(*satellite_params)
	trajectory_satellite_text = io.BytesIO(trajectory_satellite_text.encode('utf-8'))
	return send_file(
		trajectory_satellite_text,
		mimetype='text/plain',
		as_attachment=True,
		download_name=f"trajectory_{satellite_name}.txt")


def processing_values(form: ParamsForm) -> tuple[str, str]:
	"""Проверка введённых значений"""

	# Получаем введённые значения из формы
	satellite_param = SatelliteParamModel(
		form.latitude.data, form.longitude.data, form.altitude.data,
		form.horizon.data, form.minimum_culmination.data,
		datetime.combine(form.start_data.data, form.start_time.data), form.flight_length.data)

	# Получаем данные полётов
	flight_data = flight_calculation.CalculationsSatellite(satellite_param)
	# Получаем номера пересекающихся полётов
	intersecting_flights = flight_data.intersecting_flights
	return flight_data.satellites_list, intersecting_flights


if __name__ == '__main__':
	app.run(debug=True)
