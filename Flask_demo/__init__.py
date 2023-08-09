import platform

# Lấy thông tin kiến trúc của hệ thống
arch = platform.architecture()[0]

# Kiểm tra kiến trúc
if arch == "32bit":
    print("Đang chạy trong môi trường 32-bit")
elif arch == "64bit":
    print("Đang chạy trong môi trường 64-bit")
else:
    print("Kiến trúc không xác định")