# coding=utf-8
"""
Michael duPont - michael@mdupont.com
Original source: https://github.com/flyinactor91/AVWX-Engine
Modified by etcher@daribouca.net
"""
# pylint: disable=all
# module
import typing

from . import core, translate
from .static import SPOKEN_UNITS
from .structs import MetarData, Number, TafData, TafLineData, Timestamp, Units


def ordinal(_number):
    """
    Dummy ordinal
    """
    return "%d%s" % (_number, "tsnrhtdd"[(_number / 10 % 10 != 1) * (_number % 10 < 4) * _number % 10::4])


def wind(direction: Number,
         speed: Number,
         gust: Number,
         vardir: typing.List[Number] = None,
         unit: str = 'kt') -> str:
    """
    Format wind details into a spoken word string
    """
    unit = SPOKEN_UNITS.get(unit, unit)
    val = translate.wind(direction, speed, gust, vardir, unit,
                         cardinals=False, spoken=True)
    return 'Winds ' + (val or 'unknown')


def temperature(header: str, temp: Number, unit: str = 'C') -> str:
    """
    Format temperature details into a spoken word string
    """
    if temp is None or temp.value is None:
        return header + ' unknown'
    if unit in SPOKEN_UNITS:
        unit = SPOKEN_UNITS[unit]
    use_s = '' if temp.spoken in ('one', 'minus one') else 's'
    result = (x for x in (header, temp.spoken, 'degree' + use_s, unit) if x)
    return ' '.join(result)


def visibility(vis: Number, unit: str = 'm') -> str:
    """
    Format visibility details into a spoken word string
    """
    if vis is None or vis.repr is None:
        return 'Visibility unknown'
    if vis.value is None or '/' in vis.repr:
        ret_vis = vis.spoken or ''
    else:
        ret_vis = translate.visibility(vis, unit=unit)
        if unit == 'm':
            unit = 'km'
        ret_vis = ret_vis[:ret_vis.find(' (')].lower().replace(unit, '').strip()
        ret_vis = core.spoken_number(core.remove_leading_zeros(ret_vis))
    ret = 'Visibility ' + ret_vis
    if unit in SPOKEN_UNITS:
        if '/' in vis.repr and 'half' not in ret:
            ret += ' of a'
        ret += ' ' + SPOKEN_UNITS[unit]
        if not (('one half' in ret and ' and ' not in ret) or 'of a' in ret):
            ret += 's'
    else:
        ret += unit
    return ret


def altimeter(alt: Number, unit: str = 'inHg') -> str:
    """
    Format altimeter details into a spoken word string
    """
    ret = 'Altimeter '
    if alt is None or alt.repr is None:
        ret += 'unknown'
    elif unit == 'inHg':
        ret += core.spoken_number(alt.repr[:2]) + ' point ' + core.spoken_number(alt.repr[2:])
    elif unit == 'hPa':
        ret += core.spoken_number(alt.repr)
    return ret


def other(wxcodes: typing.List[str]) -> str:
    """
    Format wx codes into a spoken word string
    """
    ret = []
    for code in wxcodes:
        item = translate.wxcode(code)
        if item.startswith('Vicinity'):
            item = item.lstrip('Vicinity ') + ' in the Vicinity'
        ret.append(item)
    return '. '.join(ret)


def type_and_times(type_: str, start: Timestamp, end: Timestamp, probability: Number = None) -> str:
    """
    Format line type and times into the beginning of a spoken line string
    """
    if not type_ or start.dt is None:
        return ''
    if type_ == 'BECMG':
        return f"At {start.dt.hour or 'midnight'} zulu becoming"
    if end.dt is None:
        return ''
    ret = f"From {start.dt.hour or 'midnight'} to {end.dt.hour or 'midnight'} zulu,"
    if probability and probability.value:
        ret += f" there's a {probability.value}% chance for"
    if type_ == 'INTER':
        ret += ' intermittent'
    elif type_ == 'TEMPO':
        ret += ' temporary'
    return ret


def wind_shear(shear: str, unit_alt: str = 'ft', unit_wind: str = 'kt') -> str:
    """
    Format wind shear string into a spoken word string
    """
    unit_alt = SPOKEN_UNITS.get(unit_alt, unit_alt)
    unit_wind = SPOKEN_UNITS.get(unit_wind, unit_wind)
    return translate.wind_shear(shear, unit_alt, unit_wind, spoken=True) or 'Wind shear unknown'


def metar(data: MetarData, units: Units) -> str:
    """
    Convert MetarData into a string for text-to-speech
    """
    speech = []
    if data.wind_direction and data.wind_speed:
        speech.append(wind(data.wind_direction, data.wind_speed,
                           data.wind_gust, data.wind_variable_direction,
                           units.wind_speed))
    if data.visibility:
        speech.append(visibility(data.visibility, units.visibility))
    if data.temperature:
        speech.append(temperature('Temperature', data.temperature, units.temperature))
    if data.dewpoint:
        speech.append(temperature('Dew point', data.dewpoint, units.temperature))
    if data.altimeter:
        speech.append(altimeter(data.altimeter, units.altimeter))
    if data.other:
        speech.append(other(data.other))
    speech.append(translate.clouds(data.clouds,
                                   units.altitude).replace(' - Reported AGL', ''))
    return ('. '.join([l for l in speech if l])).replace(',', '.')


def taf_line(line: TafLineData, units: Units) -> str:
    """
    Convert TafLineData into a string for text-to-speech
    """
    speech = []
    start = type_and_times(line.type, line.start_time, line.end_time, line.probability)
    if line.wind_direction and line.wind_speed:
        speech.append(wind(line.wind_direction, line.wind_speed,
                           line.wind_gust, unit=units.wind_speed))
    if line.wind_shear:
        speech.append(wind_shear(line.wind_shear, units.altimeter, units.wind_speed))
    if line.visibility:
        speech.append(visibility(line.visibility, units.visibility))
    if line.altimeter:
        speech.append(altimeter(line.altimeter, units.altimeter))
    if line.other:
        speech.append(other(line.other))
    speech.append(translate.clouds(line.clouds,
                                   units.altitude).replace(' - Reported AGL', ''))
    if line.turbulance:
        speech.append(translate.turb_ice(line.turbulance, units.altitude))
    if line.icing:
        speech.append(translate.turb_ice(line.icing, units.altitude))
    return start + ' ' + ('. '.join([l for l in speech if l])).replace(',', '.')


def taf(data: TafData, units: Units) -> str:
    """
    Convert TafData into a string for text-to-speech
    """
    if data.start_time.dt is None:
        return ''
    try:
        month = data.start_time.dt.strftime(r'%B')
        day = ordinal(data.start_time.dt.day)
        ret = f"Starting on {month} {day} - "
    except AttributeError:
        ret = ''
    return ret + '. '.join([taf_line(line, units) for line in data.forecast])
