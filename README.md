# ULMS_Online_Demo — Hệ thống Quản lý Thư viện Đại học (Sách số)


Demo Flask theo so do chuc nang **He thong Quan ly Thu vien Dai hoc (Sach so)**.

## Da bo sung theo 7 diem thieu + so do

1. **Staff theo doi yeu cau muon**: tab Cho duyet (Pending Approval), Duyet / Tu choi, thu hoi quyen doc.
2. **Giam sat tai khoan**: trang chi tiet user (ngay tao, lich su muon, lich su vi pham, phat, audit, trang thai Ban/Ngat quyen/Binh thuong).
3. **Ngat quyen muon**: `can_borrow` — user van dang nhap duoc nhung khong muon/doc; Admin/Staff xu ly vi pham co the ngat.
4. **Gioi han so sach/user**: cau hinh tai Admin > Cau hinh (mac dinh 5, co the 5–8).
5. **Quan ly ban quyen (DRM)**: doc online + chan copy/paste/chuot phai/PrintScreen/F12; watermark; sau 3 lan vi pham tu dong xu ly theo chinh sach (canh bao → ngat 5 ngay → ban).
6. **Ban tai khoan vi pham**: ban tam / ban vinh vien, ly do, ban_until; trang Vi pham cho Staff/Admin xu ly.
7. **Quan ly kho sach**: them/sua/xoa, trang thai Available | Hidden | NoCopyright | Archived, thoi han muon theo sach, so ban quyen so.

## Tai khoan demo
- Admin: admin@lib.university.edu.vn / admin123
- Staff: lan@lib.university.edu.vn / staff123
- Member: an.nguyen@student.university.edu.vn / student123

## Chay
```bash
pip install -r requirements.txt
# Xoa DB cu neu can seed lai:
rm -f instance/ulms.db
python app.py
```
Mo http://127.0.0.1:5000/

## Luu y
- DRM la bao ve phia client (JS) — demo, khong thay the DRM server-side that.
- Email/SMS that va SSO la enhancement production.