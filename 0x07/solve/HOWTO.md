# Bài 1:
  Ta viewsource js lên và thấy rằng flag nhập vào sẽ được mã hóa bởi hàm ;
  ```javascript
  flag.replace(/[a-zA-Z]/g, function(c) {
            return String.fromCharCode(
              (c <= "Z" ? 90 : 122) >= (c = c.charCodeAt(0) + 13) ? c : c - 26
            );
          });
  ```
  Và ta thấy rằng đây là mã hóa rot13 nên ta sẽ chạy lệnh sau trong console:
  ```javascript

  'PyvragFvqrYbtvafNerRnfl@syner-ba.pbz'.replace(/[a-zA-Z]/g, function(c) {
            return String.fromCharCode(
              (c <= "Z" ? 90 : 122) >= (c = c.charCodeAt(0) + 13) ? c : c - 26
            );
          });
  ```
  và ra được flag:ClientSideLoginsAreEasy@flare-on.com