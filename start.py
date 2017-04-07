import argparse
import fcntl
import struct
import sys
import logging
import traceback
from Node import *
from common import *


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


def parse_args():
    # args parsing
    parser = argparse.ArgumentParser(description='DHT-Torrent Client.')

    parser.add_argument('--static', action='store_true', default=False, dest='static', help='Create static node')
    parser.add_argument('--id', action='store', dest='id', type=int, help='This node id')
    parser.add_argument('--ip', action='store', dest='ip', help='This node ip')

    parser.add_argument('--nextpeerid', action='store', dest='nextid', type=int, default=None, help='Next node ID')
    parser.add_argument('--nextpeerip', action='store', dest='nextip', default=None, help='Next node IP address')

    parser.add_argument('--dynamic', action='store_true', default=False, dest='dynamic',
                        help='Create dynamic node')
    parser.add_argument('--file', action='store', dest='filePath', help='Path of torrent system info file')

    return parser.parse_args()


def cli_get_help():
    help = "commands [case-insensitive]:\n"
    help += "\tINSERT KEY :: VALUE\t\t[inserts a key-value into DHT]\n"
    help += "\tLOOKUP KEY\t\t[lookup a value in DHT]\n"
    help += "\tINFO\t\t[prints current node information]\n"

    return help


def cli_parse_command(line):
    cmd = line.split(" ")[0]

    return cmd.upper().strip('\n'), ' '.join(line.split(" ")[1:]).strip('\n')


def setup_logging():
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    ch.setLevel(logging.DEBUG)
    log.addHandler(ch)


def start():
    setup_logging()
    args = parse_args()

    my_node = None
    if args.static:
        if args.nextid:
            my_node = create_static_node(args.id, args.ip, args.nextid, args.nextip)
        else:
            my_node = create_static_node(args.id, args.ip)

    print cli_get_help()
    try:
        while True:
            try:
                my_node.socket.run()
                if sys.stdin in select.select([sys.stdin], [], [], 2)[0]:
                    line = sys.stdin.readline()
                    if not line:
                        break
                    cmd, arg = cli_parse_command(line)
                    if cmd.startswith("HELP"):
                        print cli_get_help()
                    elif cmd.startswith("INSERT"):
                        key, value = arg.split("::")
                        my_node.insert_value(key.strip(), value.strip())
                    elif cmd.startswith("LOOKUP"):
                        my_node.lookup_key(arg.strip())
                    elif cmd.startswith("INFO"):
                        log.info("\n" + my_node.to_str())
                    elif cmd.startswith("PYTHON"):
                        exec arg
                    else:
                        log.info("unknown command")
            except Exception as e:
                log.error(str(e))
                log.error(traceback.format_exc())
                continue
    except KeyboardInterrupt:
        print "KeyboardInterrupt"
    finally:
        log.info(my_node.myInfo.to_str() + " disconnected.")
        print "terminated"

if __name__ == '__main__':
    start()
