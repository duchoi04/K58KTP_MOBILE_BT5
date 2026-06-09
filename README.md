# App Monitor + Alert Data Realtime (Multi-Services Architecture)

Hệ thống giám sát biến động dữ liệu động theo thời gian thực (Realtime Data Pipeline) sử dụng cấu trúc đa dịch vụ (Multi-services) triển khai trên nền tảng Docker Compose, Node-RED, Backend Flask, Frontend Nginx và hệ thống cảnh báo tự động qua Telegram Bot API.

---

## 📌 PHẦN I: LÝ THUYẾT NỀN TẢNG DOCKER & DOCKER COMPOSE

### 1.1 Docker là gì?
**Docker** là một nền tảng mã nguồn mở cho phép người phát triển đóng gói, triển khai và chạy các ứng dụng bên trong các môi trường cô lập được gọi là **Container**. 

Khác với ảo hóa truyền thống (Virtual Machines) phải mang theo cả một hệ điều hành khách (Guest OS) nặng nề, Container của Docker chia sẻ chung nhân kernel của hệ điều hành máy chủ (Host OS). Nhờ đó, Container cực kỳ nhẹ, khởi động trong vài mili giây và tiêu tốn rất ít tài nguyên phần cứng.

### 1.2 Các keyword sử dụng trong file `docker-compose.yml`

#### A. Từ khóa cấp cao (Top-level Keywords)
* `version`: Định nghĩa phiên bản cấu trúc của Docker Compose được sử dụng (Ví dụ: `'3.8'`).
* `services`: Khai báo danh sách các container/ứng dụng cấu thành nên hệ thống.
* `networks`: Khai báo các mạng ảo cô lập để các container kết nối và truyền thông nội bộ với nhau.
* `volumes`: Khai báo các phân vùng lưu trữ dữ liệu bền vững, giúp giữ lại dữ liệu kể cả khi container bị xóa bỏ.

#### B. Từ khóa chi tiết để mô tả một Service (Container)

| Từ khóa | Ý nghĩa kỹ thuật | Ví dụ minh họa trong bài |
| :--- | :--- | :--- |
| **`image`** | Khai báo tên và phiên bản của Image gốc cần tải về từ Docker Hub. | `image: mariadb:10.11` |
| **`container_name`** | Đặt tên cố định cho container thay vì để Docker tự sinh ngẫu nhiên. | `container_name: monitor_nodered` |
| **`ports`** | Ánh xạ cổng mạng từ máy chủ vào trong container (`Host_Port:Container_Port`). | `ports: - "1880:1880"` |
| **`volumes`** | Gắn phân vùng dữ liệu (Volume hoặc Thư mục) từ máy chủ vào trong container để lưu data. | `volumes: - nodered_data:/data` |
| **`environment`** | Thiết lập các biến môi trường cấu hình cho ứng dụng bên trong (Mật khẩu, múi giờ...). | `environment: TZ: "Asia/Ho_Chi_Minh"` |
| **`networks`** | Chỉ định container này sẽ tham gia vào mạng ảo nào để giao tiếp nội bộ. | `networks: - monitor_net` |
| **`depends_on`** | Thiết lập thứ tự khởi chạy (Container này phải đợi container khác khởi động xong mới chạy). | `depends_on: - mariadb` |
| **`build`** | Chỉ định đường dẫn tới thư mục chứa Dockerfile để tự động build Image từ mã nguồn sạch. | `build: ./myapi` |
| **`dns`** | Cấu hình máy chủ phân giải tên miền thủ công cho container để kết nối mạng ngoài ổn định. | `dns: - 8.8.8.8` |
| **`restart`** | Chính sách tự động khởi động lại container nếu gặp sự cố crash hoặc khi máy chủ reboot. | `restart: always` |

### 1.3 Ưu điểm khi triển khai ứng dụng sử dụng Docker
* **Tính nhất quán (Consistency):** Đảm bảo môi trường chạy ứng dụng ở máy lập trình viên, máy kiểm thử và máy chủ thật giống nhau 100%.
* **Triển khai siêu tốc (Rapid Deployment):** Việc khởi tạo, tắt, đập đi xây lại một container diễn ra trong vài giây chỉ bằng 1 dòng lệnh.
* **Tiết kiệm tài nguyên (Resource Efficiency):** Chạy được mật độ ứng dụng cao trên cùng một máy chủ do dùng chung nhân OS, không tốn tài nguyên duy trì OS ảo.
* **Cô lập an toàn (Isolation):** Mỗi container độc lập hoàn toàn. Nếu một container bị lỗi, các container còn lại trong hệ thống vẫn an toàn.

### 1.4 Quy trình triển khai ứng dụng lên Máy chủ thật không có Internet (Offline Deployment)
Khi máy chủ Production hoàn toàn bị cô lập mạng mạng ngoại vi, ta áp dụng quy trình gồm 4 bước:
1. **Tại máy cá nhân (Có Internet):** Khởi chạy, cấu hình và kiểm thử toàn bộ ứng dụng thành công.
2. **Đóng gói Image:** Sử dụng lệnh `docker save` để nén các Docker Image cần thiết thành file vật lý `.tar`.
   ```bash
   docker save -o monitor_images.tar nodered/node-red:latest mariadb:10.11 influxdb:2.7 grafana/grafana:latest nginx:alpine
