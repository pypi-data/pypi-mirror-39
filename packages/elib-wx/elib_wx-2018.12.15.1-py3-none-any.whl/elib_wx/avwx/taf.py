# coding=utf-8
"""
Michael duPont - michael@mdupont.com
Original source: https://github.com/flyinactor91/AVWX-Engine
Modified by etcher@daribouca.net
"""
import typing

# stdlib
# module
from . import core, service
from .static import IN_UNITS, NA_UNITS
from .structs import TafData, TafLineData, Units


def fetch(station: str) -> str:
    """
    Returns TAF report string or raises an error

    Maintains backwards compatability but uses the new Service object.
    It is recommended to use the Service class directly instead of this function
    """
    return service.get_service(station)('taf').fetch(station)


def parse(station: str, txt: str) -> typing.Tuple[TafData, Units]:
    """
    Returns TafData and Units dataclasses with parsed data and their associated units
    """
    core.valid_station(station)
    while len(txt) > 3 and txt[:4] in ('TAF ', 'AMD ', 'COR '):
        txt = txt[4:]
    _, station, time = core.get_station_and_time(txt[:20].split(' '))
    retwx: typing.Dict[str, typing.Any] = {
        'end_time': None,
        'raw': txt,
        'remarks': None,
        'start_time': None,
        'station': station,
        'time': core.make_timestamp(time)
    }
    txt = txt.replace(station, '')
    txt = txt.replace(time, '').strip()
    if core.uses_na_format(station):
        use_na = True
        units = Units(**NA_UNITS)
    else:
        use_na = False
        units = Units(**IN_UNITS)
    # Find and remove remarks
    txt, retwx['remarks'] = core.get_taf_remarks(txt)
    # Split and parse each line
    lines = core.split_taf(txt)
    parsed_lines = parse_lines(lines, units, use_na)
    # Perform additional info extract and corrections
    if parsed_lines:
        parsed_lines[-1]['other'], retwx['max_temp'], retwx['min_temp'] \
            = core.get_temp_min_and_max(parsed_lines[-1]['other'])
        if not (retwx['max_temp'] or retwx['min_temp']):
            parsed_lines[0]['other'], retwx['max_temp'], retwx['min_temp'] \
                = core.get_temp_min_and_max(parsed_lines[0]['other'])
        # Set start and end times based on the first line
        start, end = parsed_lines[0]['start_time'], parsed_lines[0]['end_time']
        parsed_lines[0]['end_time'] = None
        retwx['start_time'], retwx['end_time'] = start, end
        parsed_lines = core.find_missing_taf_times(parsed_lines, start, end)
        parsed_lines = core.get_taf_flight_rules(parsed_lines)
    # Extract Oceania-specific data
    if retwx['station'][0] == 'A':
        parsed_lines[-1]['other'], retwx['alts'], retwx['temps'] \
            = core.get_oceania_temp_and_alt(parsed_lines[-1]['other'])
    # Convert to dataclass
    retwx['forecast'] = [TafLineData(**line) for line in parsed_lines]
    return TafData(**retwx), units


def parse_lines(lines: typing.List[str],
                units: Units,
                use_na: bool = True) -> typing.List[typing.Dict[str, typing.Any]]:
    """
    Returns a list of parsed line dictionaries
    """
    parsed_lines = []
    prob = ''
    while lines:
        raw_line = lines[0].strip()
        line = core.sanitize_line(raw_line)
        # Remove prob from the beginning of a line
        if line.startswith('PROB'):
            # Add standalone prob to next line
            if len(line) == 6:
                prob = line
                line = ''
            # Add to current line
            elif len(line) > 6:
                prob = line[:6]
                line = line[6:].strip()
        if line:
            parsed_line = (parse_na_line if use_na else parse_in_line)(line, units)
            for key in ('start_time', 'end_time'):
                parsed_line[key] = core.make_timestamp(parsed_line[key])
            parsed_line['probability'] = core.make_number(prob[4:])
            parsed_line['raw'] = raw_line
            parsed_line['sanitized'] = prob + ' ' + line if prob else line
            prob = ''
            parsed_lines.append(parsed_line)
        lines.pop(0)
    return parsed_lines


def parse_na_line(txt: str, units: Units) -> typing.Dict[str, typing.Any]:
    """
    Parser for the North American TAF forcast varient
    """
    retwx: typing.Dict[str, typing.Any] = {}
    wxdata = txt.split(' ')
    wxdata, _, retwx['wind_shear'] = core.sanitize_report_list(wxdata)
    wxdata, retwx['type'], retwx['start_time'], retwx['end_time'] = core.get_type_and_times(wxdata)
    wxdata, wind_dir, wind_speed, wind_gust, _ = core.get_wind(wxdata, units)
    retwx['wind_direction'] = wind_dir
    retwx['wind_speed'] = wind_speed
    retwx['wind_gust'] = wind_gust
    wxdata, retwx['visibility'] = core.get_visibility(wxdata, units)
    wxdata, retwx['clouds'] = core.get_clouds(wxdata)
    other, altimeter, icing, turbulense = core.get_taf_alt_ice_turb(wxdata)
    retwx['other'] = other
    retwx['altimeter'] = altimeter
    retwx['icing'] = icing
    retwx['turbulance'] = turbulense
    return retwx


def parse_in_line(txt: str, units: Units) -> typing.Dict[str, typing.Any]:
    """
    Parser for the International TAF forcast varient
    """
    retwx: typing.Dict[str, typing.Any] = {}
    wxdata = txt.split(' ')
    wxdata, _, retwx['wind_shear'] = core.sanitize_report_list(wxdata)
    wxdata, retwx['type'], retwx['start_time'], retwx['end_time'] = core.get_type_and_times(wxdata)
    wxdata, wind_dir, wind_speed, wind_gust, _ = core.get_wind(wxdata, units)
    retwx['wind_direction'] = wind_dir
    retwx['wind_speed'] = wind_speed
    retwx['wind_gust'] = wind_gust
    if 'CAVOK' in wxdata:
        retwx['visibility'] = core.make_number('CAVOK')
        retwx['clouds'] = []
        wxdata.pop(wxdata.index('CAVOK'))
    else:
        wxdata, retwx['visibility'] = core.get_visibility(wxdata, units)
        wxdata, retwx['clouds'] = core.get_clouds(wxdata)
    retwx['other'], retwx['altimeter'], retwx['icing'], retwx['turbulance'] = core.get_taf_alt_ice_turb(wxdata)
    return retwx
