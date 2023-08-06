"""PyUltrasonic Output Module."""

def output_influx(data):
    """Print data using influxDB format."""

    # Pop yesterdays data
    retrievetime_data = data['retrievetime']
    del data['retrievetime']

    # Print general data
    # out = "pyultrasonic,contract=" + contract + " "
    out = "pyultrasonic,source=\"HC-SR04sensor\" "

    for index, key in enumerate(data):
        if index != 0:
            out = out + ","
        out += key + "=" + str(data[contract][key])

    out += " " + self.ts_utc_from_datestr(last_ts_str) + '000000000'
    print(out)

@staticmethod
def ts_utc_from_datestr(utc_date_str):
    utc = datetime.strptime(utc_date_str, '%Y-%m-%d %H:%M:%S')

    pst = pytz.timezone('Etc/UTC')
    utc = pst.localize(utc)

    # return calendar.timegm(dt.utctimetuple())
    return utc.timestamp()
