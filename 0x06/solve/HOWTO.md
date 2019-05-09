#Bài 1:
Sau khi đọc code từ file encrypt.cpp thì ta có thể xác định được cách thức mã hóa file như sau:
* Một file đầu vào được đọc theo các khối 4byte
* Sử dụng thuật toán tạo random 1 số và ghi vào 1 file .key với 4byte 1 lần tạo số ngẫu nhiên
* Ghi vào 1 file .enc 4 byte đầu là độ dài của file cần enc.
* Lần lượt lấy 4byte từ file cần mã hóa và 4 byte sinh ra từ hàm tạo random ta sẽ có thể thu được 4 byte sau khi mã hóa bằng cách XOR chúng với nhau. Ghi các byte này vào file .enc
* Sau quá trình mã hóa ta thu được 1 file .key và 1 file .enc. Để có thể giải mã ta chỉ cần XOR ngược lại 2 file này với nhau là được.

Ta có đoạn code các bước mã hóa của đề bài:
```c
int main()
{
    initialize("seed");

    encrypt("encrypt.cpp", "encrypt.enc", "encrypt.key");
    encrypt("flag.jpg", "flag.enc", "flag.key");

    //  decrypt("encrypt_dec.cpp", "encrypt.enc", "encrypt.key");
    //  decrypt("flag_dec.jpg", "flag.enc", "flag.key");
}
```
Ta thấy rằng file người ta đã mã hóa 2 file encrpt.cpp và flag.jpg. Và chỉ để lại cho ta file encrypt.cpp, encrypt.key và flag.enc

Từ đó ta xác định được cách thức giải bài này để lấy được flag trong file flag.jpg như sau:

- Ta sẽ từ XOR file encrypt.cpp với file encrypt.enc để lấy được file .key
- Sau đó lấy được tất cả các số đã được random ra để ghi vào file encrypt.key
- Sau đó ta tìm cách để đảo ngược quá trình sinh ra số ngẫu nhiên này để tìm được seed hoặc bộ số để tạo số random.
- Sau đó ta thực hiện random và ghi vào file flag.key với kích cỡ bằng kích cỡ file flag.enc trừ đi 4 byte lưu kích thước file và xor 2 file này với nhau ta sẽ thu được file flag.jpg

Ta phân tích code phần sinh số ngẫu nhiên ta có thể thấy rằng việc sinh code này được tạo bằng cách tạo ra 1 mảng gồm 624 phần tử từ file seed. Với mỗi lần gọi hàm tạo số ngẫu nhiên sẽ lấy lần lượt các phần tử trong mảng này và dùng phép biến đổi :
```c
y = mt[mti++];

    /* Tempering */
    y ^= (y >> 11);
    y ^= (y << 7) & 0x9d2c5680UL;
    y ^= (y << 15) & 0xefc60000UL;
    y ^= (y >> 18);
```
để sinh ra được số cần tìm. Và khi hết 624 số này thì mảng sẽ được tạo lại dựa vào mảng cũ.
Ta sẽ lấy 624 số này từ file encypt.enc và dùng code sau để đảo ngược lại lấy số trong mảng seed:

```python
def unshiftRight(x, shift):
    res = x
    for i in range(32):
        res = x ^ res >> shift
    return res


def unshiftLeft(x, shift, mask):
    res = x
    for i in range(32):
        res = x ^ (res << shift & mask)
    return res


def untemper(v):
    v = unshiftRight(v, 18)
    v = unshiftLeft(v, 15, 0xefc60000)
    v = unshiftLeft(v, 7, 0x9d2c5680)
    v = unshiftRight(v, 11)
    return v
```

Đoạn code sau để lấy ra file encypt.key:
```python
path = '/home/lkintheend/Desktop/CyberSercurity/encrypt/'
enc_bytes = bytearray(open(path + "encrypt.enc", "rb").read())
cipher_bytes = bytearray(open(path + "encrypt.cpp", "rb").read())
size = 2600
xord_byte_array = bytearray(size)
for i in range(size):
    xord_byte_array[i] = enc_bytes[i + 4] ^ cipher_bytes[i]
open(path + "test.key", 'wb').write(xord_byte_array)
enc_bytes = bytearray(open(path + "encrypt.enc", "rb").read())
cipher_bytes = bytearray(open(path + "encrypt.cpp", "rb").read())
size = 2600
xord_byte_array = bytearray(size)
for i in range(size):
    xord_byte_array[i] = enc_bytes[i + 4] ^ cipher_bytes[i]

open(path + "encypt.key", 'wb').write(xord_byte_array)
```
Sau đó ta sẽ sinh ngược lại được file flag.key và XOR ngược lại để lấy được flag. Ta đọc file flag và thu được flag là:
FLAG_G9A77N4nBW8gorxC

#Bài 2:
Sau khi phân tích source code thì ta có thể thấy rằng mỗi lần client request thì chương trình sẽ tạo ra 1 số ngẫu nhiên thông qua hàm getrandbits(32) để tạo 1 số từ 32 bit ngẫu nhiên.
View source code của hàm này nên ta có thể thấy rằng nó dùng thuật toán mt để sinh số ngẫu nhiên.
Từ đó ta có cách giải quyết bài toán là sẽ request 624 lần lên server để lấy được 1 list các số từ đó lật ngược lại để tạo hàm sinh random riêng theo thuật toán mt.
Ta có code sau:
```python
from socket import socket

N = 624
M = 397
MATRIX_A = 0x9908b0df
UPPER_MASK = 0x80000000
LOWER_MASK = 0x7fffffff

mt = [0 for i in xrange(624)]
mti = N + 1


def genrand_int32():
    global mti
    y = 0
    mag01 = [0x0, 0x9908b0df]

    if mti >= N:
        kk = 0

        for kk in range(kk, N - M):
            y = (mt[kk] & UPPER_MASK) | (mt[kk + 1] & LOWER_MASK)
            mt[kk] = mt[kk + M] ^ (y >> 1) ^ mag01[y & 0x1]
        kk += 1

        for kk in range(kk, N - 1, 1):
            y = (mt[kk] & UPPER_MASK) | (mt[kk + 1] & LOWER_MASK)
            mt[kk] = mt[kk + (M - N)] ^ (y >> 1) ^ mag01[y & 0x1]
        y = (mt[N - 1] & UPPER_MASK) | (mt[0] & LOWER_MASK)
        mt[N - 1] = mt[M - 1] ^ (y >> 1) ^ mag01[y & 0x1]
        mti = 0
    y = mt[mti]
    mti += 1
    y ^= (y >> 11)
    y ^= (y << 7) & 0x9d2c5680
    y ^= (y << 15) & 0xefc60000
    y ^= (y >> 18)

    return y


def unshiftRight(x, shift):
    res = x
    for i in range(32):
        res = x ^ res >> shift
    return res


def unshiftLeft(x, shift, mask):
    res = x
    for i in range(32):
        res = x ^ (res << shift & mask)
    return res


def untemper(v):
    v = unshiftRight(v, 18)
    v = unshiftLeft(v, 15, 0xefc60000)
    v = unshiftLeft(v, 7, 0x9d2c5680)
    v = unshiftRight(v, 11)
    return v


def getNumber(data):
    return int(data.split(" ")[5][0:-1])


sock = socket()
sock.connect(('188.166.218.1', 2017))
# sock.connect(('0.0.0.0', 2017))
data = sock.recv(10240)
print data
data = sock.recv(10240)
print data
for x in range(624):
    sock.send('123\n'.encode())
    data = sock.recv(10240)
    number = getNumber(data)
    data = sock.recv(10240)
    mt[x] = untemper(number)
    print str(x)
mti = 0
for x in range(624):
    genrand_int32()
for x in range(501):
    temp = str(genrand_int32()) + '\n'
    print temp
    sock.send(temp.encode())
    data = sock.recv(10240)
    print data
    data = sock.recv(10240)
    print data

```
Sau khi chạy ta có thể lấy được flag là: 
Flag{Am4zing_g0_Buy_v1etlot_n0w_$$$}