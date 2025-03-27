# FastAPI Notion API CRUD

Bài tập này giúp làm quen với FastAPI bằng cách xây dựng một API để thao tác với Notion Database. API sẽ hỗ trợ các thao tác CRUD (Create, Read, Update, Delete) với các subpage trong Notion.

## 1. Cài đặt thư viện:
   ```bash
         python apps.py
   ```

## 2. Lấy NOTION_KEY và NOTION_DATABASE_ID

2.1. Tạo một Notion Integration

Truy cập Notion Developers và đăng nhập.

Nhấn New integration → Đặt tên bất kỳ → Chọn quyền Read, Update, Insert, Delete.

Sao chép Internal Integration Token (đây chính là NOTION_KEY).

2.2. Lấy Notion Database ID

Mở Notion, chọn database cần thao tác.

Nhấn vào Share (góc trên bên phải) → Invite → Dán Integration Token vừa tạo.

Sao chép URL của database,vd :
   ```bash
      https://www.notion.so/workspace-name/1234567890abcdef1234567890abcdef
   ```
Thì 1234567890abcdef1234567890abcdef chính là NOTION_DATABASE_ID.

Tạo env  :
```bash
NOTION_KEY=your_notion_api_key
NOTION_DATABASE_ID=your_database_id
```
# 🚀 Chạy ứng dụng FastAPI
```bash
uvicorn main:app --reload
```
Sau khi chạy, API docs có thể xem tại:

-  Swagger UI: http://127.0.0.1:8000/docs

-  Redoc: http://127.0.0.1:8000/redoc

# 📌 API Endpoints
| Method | Endpoint            | Mô tả |
|--------|--------------------|-------|
| GET    | `/product`         | Lấy danh sách sản phẩm |
| POST   | `/product`         | Thêm sản phẩm mới |
| PATCH  | `/product/update`  | Cập nhật sản phẩm theo `title` |
| DELETE | `/product/delete`  | Xóa sản phẩm theo `title` |


# 🔥 Ghi chú
- Notion API yêu cầu Bearer Token, hãy đảm bảo bạn đã tạo một integration token và có quyền truy cập database.

#  Nguồn tham khảo
### Notion API
-  Để hiểu rõ hơn cách hoạt động của Notion Database, bạn có thể đọc tài liệu chính thức tại: 👉 https://developers.notion.com/

- Video về Notion API mình tham khảo : https://www.youtube.com/watch?si=JPa9tLTEFVED2_g3&v=ec5m6t77eYM&feature=youtu.be


### FastAPI 
- Nếu bạn chưa biết API thì có thể tham khảo video này 👉 https://www.youtube.com/watch?si=KLGVhaq4YOn3Nkiw&v=JUvsdFWL7WM&feature=youtu.be

- Sau đó bạn cần hiểu hơn về kiến trúc REST,RESTFul API: https://www.youtube.com/watch?v=fFGAm1phR3E

- Cuối cùng là hiểu về FastAPI : https://www.youtube.com/watch?si=EsUJ5dufpdktNjL1&v=-yEbzQSbZCo&feature=youtu.be

# Database
- Đây là một database của một anh soạn bài tập cho các bạn intern vào công ty, như một bài test nhỏ để  chứng minh các bạn hiểu được về fastAPI :https://quartz-dollar-727.notion.site/C-y-1-15bb74c8fed180c4ab12f178c04cfbfc (cần duplicate cái template này về )
