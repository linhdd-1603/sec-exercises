# Bài 1:
Ở đây dùng phương thức xác thực là basic authention nghĩa là mã hóa uername và password bằng base64
Ta encode Authorization: Basic cTg6RkxBR181dXg3eksyTktTSDhmU0dB được username:password la:q8:FLAG_5ux7zK2NKSH8fSGA
flag ta tìm được là: FLAG_5ux7zK2NKSH8fSGA
	
# Bài 2:
Ở đây phương thức xác thực là digest authention. Phân tích gói tin ta tìm được HA1 là mã MD5 của username:realm:password là:

    q9:secret:c627e19450db746b739f41b64097d449

Mặt khác ta tìm được 

    <p>The flag is <a href="flag.html">here</a>.</p> 

nên ta sẽ tìm cách truy cập vào url /~q9/flag.html để  tìm flag

Ở đây ta sẽ tính ra reponse dựa vào công thức : 

    HA1 = MD5(username:realm:password) = c627e19450db746b739f41b64097d449
    HA2 = MD5(GET:/~q9/flag.html)
    reponse = MD5(HA1:nonce:nonceCount:clientNonce:qop:HA2)
	
Gửi ngược lại reponse và ta truy cập vào được /~q9/flag.html và ta lấy được flag FLAG_YBLyivV4WEvC4pp3

