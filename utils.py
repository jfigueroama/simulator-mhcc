def write_result(fname, consuption, power, dt):
    with open(fname, "a") as f:
        line = (dt.strftime("%Y-%m-%dT%H:%M:%S:%z") + "\t"
                + str(consuption) + "\t"
                + str(power) + "\t"
                + str(consuption + (power*1000)) + "\t"
                + str(consuption - (power*1000)) + "\n")
        f.write(line)


def print_headers():
    print("Captured at" + "\t"
          "consumption(W)" + "\t"
          "pvpower(kW)" + "\t"
          "consumption+pvpower(W)" + "\t"
          "consumption-pvpower(W)")

def print_result(consuption, power, dt):
    line = (dt.strftime("%Y-%m-%dT%H:%M:%S:%z") + "\t"
            + str(consuption) + "\t"
            + str(power) + "\t"
            + str(consuption + (power*1000)) + "\t"
            + str(consuption - (power*1000)))
    print(line)

