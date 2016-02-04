import threading
import sys, time

class progressbar(threading.Thread):

    position = old_position = -1

    def __init__(self, sign="#", length=100, infinite=False):
        threading.Thread.__init__(self)
        self.daemon = True
        self.signal = None
        self.sign = sign
        self.length = length
        self.infinite = infinite

    def pos(self, position):
        self.position = position

    def run(self):

        while True:
            if self.infinite:
                self.position += 1

                if self.position > self.length:
                    self.position = 1
            else:
                if self.position > self.length:
                    self.position = self.length


            # do not update if position hasn't been changed
            if self.old_position != self.position:
                self.old_position = self.position
                bar_str = "[{0}{1}]".format(self.sign * self.position,
                                            " " * (self.length - self.position))
                sys.stdout.write('\r{}'.format(bar_str))
                sys.stdout.flush()

            # check signal, if stop requested, break the loop
            if self.signal == "stop":
                self.signal = "success"
                break

            # infinite loop causes load on cpu, so we need a short wait here
            # decrease it if there is a lag.
            time.sleep(0.05)

    def stop(self):
        self.signal = "stop"
        # wait until the thread ends
        while self.signal != "success":
            time.sleep(0.1)


if __name__ == "__main__":
    pbar = progressbar(sign="#", length=50, infinite=False)

    try:
        pbar.start()
        while True:
            pbar.pos(0)
            time.sleep(0.5)
            pbar.pos(50)
            time.sleep(0.5)

    except KeyboardInterrupt:
        pbar.stop()
        print ('interrupted!')

