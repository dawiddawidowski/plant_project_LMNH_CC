import time

# from <extract_script> import <something>
# from <transform_script> import <something>
# from <load_script> import <something>


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
            # Start the next task immediately if the current iteration
            # took longer than 1 minute
            continue

        else:
            # If the current iteration took less than 1 minute, wait
            # until 1 minute has passed before starting the next task
            time.sleep(60 - elapsed_time)
