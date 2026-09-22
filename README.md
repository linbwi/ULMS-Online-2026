# ULMS_Online_Demo — Hệ thống Quản lý Thư viện Đại học (Sách số)


Demo Flask theo so do chuc nang **He thong Quan ly Thu vien Dai hoc (Sach so)**.

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
