# Bài 1:

Decompile file .jar ta được đoạn code trong class:

```java
    import javax.swing.JOptionPane;

    public class InviteValidator {
        public InviteValidator() {}
        public static void main(String[] args) { 
            String response = JOptionPane.showInputDialog(null, "Enter your invitation code:", "Minesweeper Championship 2018", 3);
            if (response.equals"GoldenTicket2018@flare-on.com")){
            JOptionPane.showMessageDialog(null, "Welcome to the Minesweeper Championship 2018!\nPlease enter the following code to the ctfd.flare-on.com website to compete:\n\n" + response, "Success!", -1);
            } else {
            JOptionPane.showMessageDialog(null, "Incorrect invitation code. Please try again next year.", "Failure", 0);
            }
        }
    }
```

    -> flag là: GoldenTicket2018@flare-on.com

# Bài 5:

Sau khi extract file .zip ra ta được 48 file .exe
Chạy thử file exe này với lệnh wine trên ubuntu ta thu được thông báo hỏi password.

Ta sẽ thử dùng lệnh strings để  lấy tất cả các kí tự có thể chứa trong file này ta thu được:
```
HOT7h5vvZsV4vISSb60Xj3pX5G.exe 
@BRICK
%s\%s
IronManSucks
Oh, hello Batman...
I super hate you right now.
What is the password?
%15ls
Go step on a brick!
Oh look a rainbow.
Everything is awesome!
%s => %s
BRICK
ZImIT7DyCMOeF6
```
Ta thử lấy dòng cuối điền vào password thì chương trình chạy và trả về cho ta 1 file ảnh kèm theo 1 kí tự.
Trong mỗi file ảnh có kèm theo 1 số nên ta sẽ viết tool để làm việc này với tất cả các file .exe này và ghép các kí tự theo số trên ảnh để thu được 1 string:

Đầu tiên là đoạn chương trình để lấy danh sách các file cần xử lý và pass của chúng:
```python
def get_list_file():
    os.chdir(path)
    files = subprocess.Popen(["ls" " *.exe"], shell=True, stdout=subprocess.PIPE).communicate()[0]
    return str(files).splitlines()


def getPassOfFile(file_name):
    return subprocess.Popen(["strings -e l " + path + file_name], shell=True, stdout=subprocess.PIPE).communicate()[
        0].splitlines()[12]
```
Đây là đoạn code sử để trích xuất số ở trên mỗi ảnh ra:
```python
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
```

Đoạn code sau để  chạy với toàn bộ các file và ghép chuỗi lại thành flag:
```python
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

```
Sau khi run chương trình ta tìm được flag: 
mor3_awes0m3_th4n_an_awes0me_p0ssum@flare-on.com