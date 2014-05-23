#!/usr/bin/env python3

from ut61e import es51922
import logging
import sys

DIGITMAP = {
    "0": "ABCDEF", "1": "BC", "2": "ABGED", "3": "ABCDG",
    "4": "BCFG", "5": "AFGCD", "6": "AFEDCG", "7": "ABC",
    "8": "ABCDEFG", "9": "ABCDFG", "":"",
    "U": "BCDEF", "O": "ABCDEF", "L": "DEF", "": "",
}

def set_ol():
    segments = ['OL']
    segments += set_digit(4,'')
    segments += set_digit(3,'O')
    segments += set_digit(2,'L')
    segments += set_digit(1,'')
    segments += set_digit(0,'')
    segments.append("DIGIT2DP")
    segments += show_bargraph(220, ol=True)
    return segments

def set_ul():
    segments += set_digit(4,'')
    segments += set_digit(3,'U')
    segments += set_digit(2,'L')
    segments += set_digit(1,'')
    segments += set_digit(0,'')
    segments.append("DIGIT1DP")
    segments += show_bargraph(0, ul=True)
    return segments

def set_digit(n, value):
    if n < 0 or n > 4:
        logging.error('Invalid: Trying to set the value for digit #{}.'.format(n))
    try:
        segments = DIGITMAP[str(value)]
    except:
        logging.error('Invalid: Trying to set a digit to {}.'.format(n,value))
    return ["DIGIT" + str(n) + segment for segment in segments]

UNITMAP = {
    "V"   : ["VOLT"],
    "mV"  : ["MILLI", "VOLT"],
    "A"   : ["AMPERE"],
    "mA"  : ["MILLI", "AMPERE"],
    "µA"  : ["MICRO", "AMPERE"],
    "F"   : ["FARAD"],
    "mF"  : ["MILLIF", "FARAD"],
    "µF"  : ["MICROF", "FARAD"],
    "nF"  : ["NANOF", "FARAD"],
    "Ω"   : ["OHM"],
    "kΩ"  : ["KILO", "OHM"],
    "MΩ"  : ["MEGA", "OHM"],
    "Hz"  : ["HERTZ"],
    "kHz" : ["KILO", "HERTZ"],
    "MHz" : ["MEGA", "HERTZ"],
    "%"   : ["PERCENT"],
}

def show_bargraph(value, ol=False, ul=False):
    value = int(value)
    if value > 220: value = 220
    segments = ["LABEL{:03d}".format(n) for n in [0, 50, 100, 150, 200]]
    segments += ["BAR{:03d}".format(n) for n in range(0, value + 1, 5)]
    if ol: segments.append("OL")
    return segments

def active_segments(results):
    pd = results['packet_details']
    segs = []
    segs.append("TRANSMISSION")
    if results['current']: segs.append(results['current']) # AC DC
    segs.append("AUTO") if pd['options']['AUTO'] else segs.append("MANU")
    if pd['options']['HOLD']: segs.append("HOLD")
    if pd['options']['PMIN']: segs.append("PMIN")
    if pd['options']['PMAX']: segs.append("PMAX")
    if pd['options']['MIN']: segs.append("MIN")
    if pd['options']['MAX']: segs.append("MAX")
    if pd['options']['OL']:
        segs += set_ol()
    else:
        digit4 = pd['data_bytes']['d_digit4'] - 48
        digit3 = pd['data_bytes']['d_digit3'] - 48
        digit2 = pd['data_bytes']['d_digit2'] - 48
        digit1 = pd['data_bytes']['d_digit1'] - 48
        digit0 = pd['data_bytes']['d_digit0'] - 48
        digits = [digit0, digit1, digit2, digit3, digit4]
        dp = pd['range']['dp_digit_position']
        significant_digits = len(str(int("".join([str(d) for d in digits[::-1]]))))
        for i in range(5):
            if i <= dp or i < significant_digits:
                segs += set_digit(i, digits[i])
        segs.append("DIGIT" + str(dp) + "DP")
        segs += show_bargraph(str(digit4) + str(digit3) + str(digit2))
    du = results['display_unit']
    if du in UNITMAP: segs += UNITMAP[du]
    return segs

while True:
    line = sys.stdin.readline()
    if not line: break
    try:
        line = line.encode('ascii')
    except:
        logging.warning('Not an ASCII input line, ignoring: "{}"'.format(line))
        continue
    line = line.strip()
    if len(line)==12:
        try:
            results = es51922.parse(line, True)
        except Exception as e:
            logging.warning('Error "{}" packet from multimeter: "{}"'.format(e, line))
            continue
        del results['packet_details']['raw_data_binary']
        sys.stdout.write(" ".join(active_segments(results)) + "\n")
        sys.stdout.flush()
    elif line:
        logging.warning('Unknown packet from multimeter: "{}"'.format(line))
