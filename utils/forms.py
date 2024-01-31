from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, DateField, TimeField
from wtforms.validators import InputRequired, NumberRange


class ParamsForm(FlaskForm):
    """Форма ввода параметров станции"""
    latitude = FloatField('', validators=[InputRequired()], render_kw={"placeholder": "Широта"})
    longitude = FloatField('', validators=[InputRequired()], render_kw={"placeholder": "Долгота"})
    altitude = FloatField('', validators=[InputRequired()], render_kw={"placeholder": "Высота в км"})
    horizon = FloatField('', validators=[InputRequired()], render_kw={"placeholder": "Горизонт"})
    minimum_culmination = FloatField(
        "", validators=[InputRequired()], render_kw={"placeholder": "Минимальная кульминация"})

    start_data = DateField("Начальная дата", None, "%Y-%m-%d")  # год-месяц-день
    start_time = TimeField(
        "Начальное время", None, render_kw={"placeholder": ""})  # год-месяц-день
    flight_length = IntegerField('', validators=[InputRequired(), NumberRange(min=0)],
                                 render_kw={"placeholder": "Длинна расписания в часах"})
