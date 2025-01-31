import requests
from pathlib import Path


def update_tle():
	url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=weather&FORMAT=tle'
	try:
		response = requests.get(url)

		if response.status_code == 200:  # Если получилось открыть страницу
			with open(Path(__file__).resolve().parent / 'tle.txt', 'wb') as file:
				for chunk in response.iter_content(chunk_size=1024):
					if chunk:  # Фильтруем пустые куски
						file.write(chunk)
		print("tle успешно обновлено")

	except Exception as e:
		print("Ошибка загрузки tle:", e)
