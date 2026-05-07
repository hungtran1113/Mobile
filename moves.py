import arcade

# Cấu hình hằng số
WIDTH = 640
TILE = WIDTH // 8

# Trong class kế thừa arcade.Window hoặc trong hàm draw:
# arcade.draw_text(
#     text="Nội dung",
#     start_x=tọa_độ_x,
#     start_y=tọa_độ_y,
#     color=màu_sắc,
#     font_size=kích_thước,
#     bold=True,
#     anchor_x="center" # Căn lề để dễ điều khiển vị trí
# )


arcade.draw_text(
    "CHECK!",
    300,             # Tọa độ x
    WIDTH - 50,      # Tọa độ y (Lấy chiều cao trừ đi khoảng cách từ đỉnh để giống Pygame)
    arcade.color.RED,
    font_size=45,    # Arcade dùng size pt, thường nhỏ hơn pixel của Pygame một chút
    bold=True
)