import argparse


def main(argv=None):
    parser = argparse.ArgumentParser(
            description='Forward wake-on-lan packets to the '
            'broadcast IP address.'
    )
    parser.add_argument('-L',
            metavar='listen port',
            default=DEFAULT_LISTEN_PORT,
            dest='L',
            nargs=1,
            type=int,
            help='The UDP port number you want to listen to '
            '(default 1729).'
    )
    parser.add_argument('-F',
            metavar='forward port',
            default=DEFAULT_TARGET_PORT,
            dest='F',
            nargs=1,
            type=int,
            help='The UDP port number you want to forward WOL '
            'packets to (default 9).'
    )
    parser.add_argument('-I',
            metavar='forward IP',
            default=DEFAULT_TARGET_IP,
            dest='I',
            nargs=1,
            help='The IP address you want to forward WOL packets '
            'to (default 255.255.255.255).'
    )
    args = parser.parse_args(argv)
    listen(listen_port=args.L,
            target_port=args.F,
            target_ip=args.I)


if __name__ == '__main__':
    main()

