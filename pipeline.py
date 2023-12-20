import time

from sample_extract import #<something>
from transform_readings import #<something>
from load import #<something>


def main():

    # main pipeline script goes here
    pass


if __name__ == "__main__":

    while True:
        start_time = time.time()
        main()
        end_time = time.time()

        elapsed_time = end_time - start_time
        if elapsed_time > 60:
            continue
        else:
            time.sleep(60 - elapsed_time)
