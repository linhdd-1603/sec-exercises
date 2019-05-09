# Bài 2:
```php
	<!DOCTYPE html>
	<html>
	<head>
		<title>Simple Auth</title>
	</head>
	<body>
		<div>
	<?php
	$password = 'FLAG_????????????????';
	if (isset($_POST['password']))
		if (strcasecmp($_POST['password'], $password) == 0)
			echo "Congratulations! The flag is $password";
		else
			echo "incorrect...";
	?>
		</div>
		<form method="POST">
		<input type="password" name="password">
		<input type="submit">
		</form>
	</body>
</html>
```
	- Ta thấy mã nguồn của php của sử dụng hàm strcasecmp() để so sánh. Hàm này có 1 lỗ hổng là sẽ trả về 0 nếu 1 chuỗi được sánh với một mảng.

	- Ta sẽ truyền param password lên theo dạng mảng để website trả về flag.
	- Dùng postman với phương thức POST trên url : http://ctfq.sweetduet.info:10080/~q32/auth.php
	với body là form-data : password[] = 'something'
	- Ta nhận được flag là : FLAG_VQcTWEK7zZYzvLhX
