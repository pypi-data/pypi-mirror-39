import argparse

# from pyultrasonic import UltrasonicSensor
from pyultrasonic.output import output_influx

VERSION = "0.1"

def main():
    """Entrypoint function."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--trigger',
                        help='Your GPIO Trigger pin')
    parser.add_argument('-e', '--echo',
                        help='Your GPIO Echo pin')
    parser.add_argument('-d', '--depth',
                        help='Pit depth')
    parser.add_argument('-c', '--compensation',
                        help='Compensation')
    parser.add_argument('-j', '--json', action='store_true',
                        default=False, help='Json output')
    parser.add_argument('-i', '--influxdb', action='store_true',
                        default=False, help='InfluxDb output')

    args = parser.parse_args()

    if args.version:
        print(VERSION)
        return 0

    if not args.trigger or not args.echo:
        parser.print_usage()
        print("pyultrasonic: error: the following arguments are required: "
              "-t/--trigger, -p/--echo, -d/--depth")
        return 3

    sensor = UltrasonicSensor(args.trigger, args.echo, args.depth, args.compensation)
    loop = asyncio.get_event_loop()

    sensor.retrieveDistance()

    if args.influxdb:
        output_influx(sensor.get_data())
    elif args.json:
        output_json(client.get_data())
    return 0


if __name__ == '__main__':
    sys.exit(main())


