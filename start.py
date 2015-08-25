__author__ = 'fgh'

import argparse
import locale
import os

from beans.data import Data

# call sampre
# python start.py -f "/home/fgh/Dropbox/Astronomia/zona WASP-48 b/WASP-48 b/20150824_informe_test_brut.txt" -p 2457259.51356 -n 15

global file_name
global first_flip_point
global number_of_points

global original_file_lines

def getArguments():
    global first_flip_point
    global number_of_points
    global file_name

    parser = argparse.ArgumentParser(description='Deploy eureka discovery services')
    parser.add_argument('-f', '--file_name', required=True, help='Name of the file that contains light curve data')
    parser.add_argument('-p', '--first_flip_point', required=True, type=float, help='date of the first point after step')
    parser.add_argument('-n', '--number_of_points', required=True, type=int, help='Number of points to calculate the step size')
    args = parser.parse_args()

    file_name = args.file_name
    first_flip_point = args.first_flip_point
    number_of_points = args.number_of_points

def getData(file_name):
    global original_file_lines

    result = dict()
    before_step = []
    after_step = []

    if not os.path.isfile(file_name) :
        raise Exception('FILE NOT EXIST', 'The file ' + file_name + ' doesn\'t exist.')

    start = False
    with open(file_name) as f:
        lines = f.readlines()

    original_file_lines = lines

    for line in lines:
        if start:
            if line == "\r\n":
                start = False
            else:
                values = line.strip().split()

                data = Data(values[0], values[1], values[2])
                if data.date < first_flip_point:
                    before_step.append(data)
                else:
                    after_step.append(data)
        else:
            if "----------------------------------" in line:
                start = True

    result["before_step"] = before_step
    result["after_step"] = after_step
    return result


def main():
    getArguments()

    point_list = getData(file_name)

    before_step = point_list["before_step"]
    after_step = point_list["after_step"]

    dif = 0

    for x in range(0, number_of_points-1):
         dif += after_step[x].magnitude - before_step[len(before_step) - (number_of_points-x)].magnitude

    dif = dif / number_of_points
    dif = float("%.2f" % dif)

    for data in after_step:
        data.magnitude = data.magnitude - dif


    f = open(file_name + "_corrected",'w')

    start = False
    for line in original_file_lines:
        if start:
            if line == "\r\n":
                f.write(line)
                start = False
            else:
                values = line.strip().split()

                data = Data(values[0], values[1], values[2])
                if data.date < first_flip_point:
                    f.write(line)
                else:
                    for data in after_step:
                        if str(data.date) in line:
                            new_date = str(data.date)
                            zeros = 5 - len(str(data.date).split(".")[1])
                            for x in range(0, zeros):
                                new_date += "0"

                            new_magnitude = str(data.magnitude)
                            zeros = 4 - len(str(data.magnitude).split(".")[1])
                            for x in range(0, zeros):
                                new_magnitude += "0"
                            
                            new_line = new_date

                            blancks = 12 - len(new_magnitude)
                            for x in range(0, blancks):
                                new_line += " "

                            new_line += new_magnitude
                            new_line += "   " + str(data.error)

                            f.write(new_line + "\r\n")
        else:
            f.write(line)
            if "----------------------------------" in line:
                start = True

    f.close()




if __name__ == '__main__':
    main()

