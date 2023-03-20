from ping import Ping
import asyncio
import sys
import signal

if __name__ == '__main__':
    if len(sys.orig_argv) <= 2:
        filename = input("Input filename: ")
    else:
        filename = sys.orig_argv[-1]
    loop = asyncio.new_event_loop()
    p = Ping(filename, loop)
    asyncio.set_event_loop(loop)
    signal.signal(signal.SIGINT, p.sigint_handler)
    loop.run_forever()
