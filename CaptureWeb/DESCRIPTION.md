# 
Project from https://www.fiverr.com/inbox/ngviendong

### Description
```
1. File txt có nội dung thay đổi mỗi 15 phút 1 lần.

2. File txt có nhiều dòng, mỗi dòng là một mã chứng khoáng, có nội dung ví dụ như sau:
Nội dung file "FilterStock.txt"
ACB
DXG
HAG
HNG
VCB

3. Đọc nội dung file "FilterStock.txt" lần lượt theo từng dòng, ví dụ như:
- Đọc dòng 1 có nội dung là "ACB"
- Sau đó thêm ký tự ACB vào 3 ký tự cuối cùng của trang web:
https://robotchungkhoan.nududo.com/#/phantichcophieu?stockcode=
Thành:
https://robotchungkhoan.nududo.com/#/phantichcophieu?stockcode=ACB
- Sau đó chụp hình nội dung trang web đó lưu thành file có tên theo định dạng là:
[3 ký tự của file text]_SUM_FA.jpg
ACB_SUM_FA.jpg
- Vòng lặp lần lượt như vậy cho tất cả các dòng có trong file FilterStock.txt đến khi làm hết tất cả các dòng có trong đó.

4. Mỗi 15 phút check file FilterStock.txt 1 lần và chụp hình tất cả các dòng có trong đó.

5. Kiểm tra giờ máy tính, chỉ hoạt động từ thời gian quy định từ hh:mm đến hh:mm
Ví dụ như time_from từ 09 giờ 00 đến 14 giờ 00
Qua thời gian quy định sẽ không chụp hình và check file FilterStock.txt nữa, đến giờ bắt đầu sẽ tự động thực hiện vòng lặp check file txt và chụp hình đến giờ kết thúc sẽ ngưng.

6. Đóng trang web xuống taskbar vẫn chụp hình bình thường (mình không thể mở web lớn lên liên tục)
```