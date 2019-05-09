import subprocess
import os
import cv2
import numpy

path = '/home/lkintheend/Desktop/Cyber/FLEGGO/'
number_map = {0: [1, 3, 4, 5, 6, 7],
              1: [6, 7],
              2: [1, 2, 3, 5, 6],
              3: [1, 2, 3, 6, 7],
              4: [2, 4, 6, 7],
              5: [1, 2, 3, 4, 7],
              6: [1, 2, 3, 4, 5, 7],
              7: [1, 6, 7],
              8: [1, 2, 3, 4, 5, 6, 7],
              9: [1, 2, 3, 4, 6, 7]}

img_digit_map = {1: [10, 3], 2: [10, 20], 3: [10, 40], 4: [3, 10], 5: [3, 30], 6: [15, 10], 7: [15, 30]}
black = [29, 19, 5]
white = [255, 255, 255]


def getNumber(img, start_x=0, start_y=0):
    fist_number = []
    for x in range(1, 8):
        temp = img_digit_map.get(x)
        px1 = img[temp[1] + start_x, temp[0] + start_y]
        if numpy.array_equal(px1, black):
            fist_number.append(x)
    for key, value in number_map.iteritems():
        if numpy.array_equal(value, fist_number):
            return str(key)
    return None


def read_image(filename):
    global img_digit_map
    img = cv2.imread(path + filename)
    result = getNumber(img)
    sec = getNumber(img, start_y=25)
    if sec is not None:
        result += sec
    return result


def get_list_file():
    os.chdir(path)
    files = subprocess.Popen(["ls" " *.exe"], shell=True, stdout=subprocess.PIPE).communicate()[0]
    return str(files).splitlines()


def getPassOfFile(file_name):
    return subprocess.Popen(["strings -e l " + path + file_name], shell=True, stdout=subprocess.PIPE).communicate()[
        0].splitlines()[12]


result = {}
for f in get_list_file():
    password = getPassOfFile(f)
    process = subprocess.Popen(["wine", path + f],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    process.stdin.write(password)
    a = process.communicate()[0].splitlines()[2]
    temp = a.split(" ")

    result[read_image(temp[0])] = temp[2]
    process.stdin.close()
print result
print len(result)

final_result = ''
for x in range(1, 49):
    final_result += result[str(x)]
print final_result
