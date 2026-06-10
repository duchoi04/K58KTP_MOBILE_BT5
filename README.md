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


PHẦN II: KHỞI TẠO HẠ TẦNG DOCKER COMPOSE

Bước 1: Trên Terminal Ubuntu, tạo thư mục dự án:


<img width="1920" height="1080" alt="Screenshot 2026-06-08 164318" src="https://github.com/user-attachments/assets/adc4a242-25e9-46d7-bf36-a029fc34db33" />



Bước 2: 

Tạo file docker-compose.yml:

<img width="1920" height="1080" alt="Screenshot 2026-06-08 164327" src="https://github.com/user-attachments/assets/d3ebb890-1da8-459b-bd40-9a190c8ec0fa" />

Tạo file requirements.txt:


<img width="1110" height="637" alt="Screenshot 2026-06-08 164508" src="https://github.com/user-attachments/assets/8b769f59-d0d6-4e5a-a9dc-5f7fe656e548" />

Tạo file app.py:


<img width="1920" height="1080" alt="Screenshot 2026-06-08 164655" src="https://github.com/user-attachments/assets/95566718-5fe9-4cd8-b889-7944fe9ebf57" />


Tạo file Docker file:


<img width="1108" height="643" alt="Screenshot 2026-06-08 164805" src="https://github.com/user-attachments/assets/809cc249-d9fb-412c-90a8-efe23af2688d" />


Tạo file index.html:


<img width="1920" height="1080" alt="Screenshot 2026-06-08 164910" src="https://github.com/user-attachments/assets/0f4ec32e-5077-407d-be8d-739af92d1a41" />



<img width="1655" height="686" alt="Screenshot 2026-06-08 173709" src="https://github.com/user-attachments/assets/3c9d05ce-529d-43f3-84fe-36f05e508cdf" />


Bước 3: Khởi chạy hệ thống: docker compose up -d


<img width="1655" height="686" alt="Screenshot 2026-06-08 173709" src="https://github.com/user-attachments/assets/ad09b286-2e43-4e3a-96fe-6712a8608c0b" />

 
PHẦN III: THIẾT LẬP TELEGRAM BOT API , Grana & Web Hệ thống giám sát biến động dữ liệu động theo thời gian thực

1. THIẾT LẬP TELEGRAM BOT API

  Truy cập @BotFather gửi lệnh /newbot tạo Bot Duchoi Bot rồi Lấy mã Token: 


<img width="1179" height="2556" alt="image" src="https://github.com/user-attachments/assets/34937b2b-91d9-487d-82d5-7d42c561f084" />

  Tạo nhóm chat "Hệ Thống Cảnh Báo Realtime BTL", thêm Bot vào nhóm và cấp quyền Admin:

<img width="1179" height="2556" alt="image" src="https://github.com/user-attachments/assets/238dc2be-00f4-41cb-8251-b89542cf0cb0" />


<img width="1179" height="2556" alt="image" src="https://github.com/user-attachments/assets/c8099307-8722-4b8f-a790-a23f90abcc96" />

   Lấy mã Chat ID của nhóm qua Telegram Web: 

     Mã nhóm của em sau dấu #

<img width="1072" height="241" alt="Screenshot 2026-06-10 012940" src="https://github.com/user-attachments/assets/527eb043-cf93-4625-9df4-c945d6cdd489" />

2. Grafana

Đăng nhập theo đường link 192.168.1.125:3000 sẽ hiện ra trang Grafana:

<img width="1920" height="1080" alt="Screenshot 2026-06-10 015039" src="https://github.com/user-attachments/assets/652f2b46-f3df-455f-abab-9dc5fecc293a" />


Bấm vaaof thanh menu trên cùng bên trái và bấm vào Connections sau đó bấm View configured data sources rồi chọn lnfluxDB rồi cấu hình như trong ảnh cuối cùng bấm Save & test:

<img width="1291" height="956" alt="Screenshot 2026-06-10 015131" src="https://github.com/user-attachments/assets/c78a935a-38ec-4502-849d-29672c63b9cd" />


<img width="1293" height="970" alt="Screenshot 2026-06-10 015312" src="https://github.com/user-attachments/assets/3e204461-2d77-4b38-8672-9ef0b092a7ea" />


<img width="1285" height="967" alt="Screenshot 2026-06-10 015527" src="https://github.com/user-attachments/assets/92af35cf-7c92-4b0c-a133-fdd1c2d790c3" />


<img width="1920" height="1080" alt="Screenshot 2026-06-10 015602" src="https://github.com/user-attachments/assets/4e53e536-1085-4650-9b31-d489090c4124" />


Tiếp theo bấm quay trở lại thanh menu chọn Dashboards tạo new Dashboards :

<img width="1297" height="821" alt="Screenshot 2026-06-10 015853" src="https://github.com/user-attachments/assets/a8057ef1-e4a8-4406-aec2-9a756092c914" />


<img width="1287" height="784" alt="Screenshot 2026-06-10 015949" src="https://github.com/user-attachments/assets/1609d73b-27d3-4cc0-83e7-f94e1002f253" />


Sau khi tạo xong dán code vào và chạy biểu đồ sẽ hiện ra:

<img width="1449" height="919" alt="Screenshot 2026-06-10 020031" src="https://github.com/user-attachments/assets/ff9a070d-efb5-49f5-8cdd-b4f9dfd7e202" />



3. Web Hệ thống giám sát biến động dữ liệu động theo thời gian thực
   
Sau khi tạo xong Grafana truy cập trang web với đường link : 192.168.1.125 sẽ thấy biểu đồ của Grafana hiện ra


<img width="1920" height="1080" alt="Screenshot 2026-06-09 161134" src="https://github.com/user-attachments/assets/e641523f-37df-4bfb-8233-1c59089e5c4f" />



PHẦN IV: XÂY DỰNG LUỒNG DỮ LIỆU TRÊN NODE-RED

1. Truy cập http://192.168.1.125:1880 vào phần menu bên góc phải màn hình chọn phần important dán đoạn code vào sẽ hiện ra giao diện Node Red như bên dưới.Vào Manage palette cài đặt gói thư viện mở rộng: node-red-contrib-telegrambot.


<img width="1920" height="1080" alt="Screenshot 2026-06-10 000021" src="https://github.com/user-attachments/assets/c0e3d3fa-296f-46db-a131-552352894a3e" />


<img width="1415" height="901" alt="Screenshot 2026-06-10 013201" src="https://github.com/user-attachments/assets/c10aa070-04e1-4d3c-a8aa-8abe5ef55ae4" />


2.  Cấu hình của các Node Red trong hình:

Lấy giá Bitcoin: 

<img width="493" height="758" alt="Screenshot 2026-06-10 014225" src="https://github.com/user-attachments/assets/abcabe4a-8da4-41dc-8d9a-1097db962d8d" />

Phân tích và Kiểm tra ngưỡng:


<img width="582" height="761" alt="Screenshot 2026-06-10 014310" src="https://github.com/user-attachments/assets/e0d1aada-4eed-4888-99e6-fecb135e1131" />


MariaDB:

<img width="522" height="688" alt="Screenshot 2026-06-10 014131" src="https://github.com/user-attachments/assets/d5494091-1342-4693-a60c-824d73e85487" />



Fomat lnfluxDB:


<img width="634" height="804" alt="Screenshot 2026-06-10 014401" src="https://github.com/user-attachments/assets/ab34995f-f1c5-4041-9834-3cb7e5041271" />


Tạo tin nhắn Alert:


<img width="627" height="896" alt="Screenshot 2026-06-10 013421" src="https://github.com/user-attachments/assets/1009dcde-7e8c-4c25-be6d-7c7354d02aad" />


Telegram sender:


<img width="689" height="837" alt="Screenshot 2026-06-10 013538" src="https://github.com/user-attachments/assets/8fe0f271-11ec-402a-8ed1-d398ffa60d84" />


PHẦN V: KẾT QUẢ

Hệ thống giám sát thông số và cảnh báo thời gian thực:


<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/0f104535-5cff-4abb-b2d1-3ea07a686f8f" />


Telegram Bot cứ mỗi 5 giây lại gửi tin nhắn về:


<img width="1179" height="2556" alt="image" src="https://github.com/user-attachments/assets/053b2f21-e159-4280-87e4-d81e7a92944d" />


<img width="1179" height="2556" alt="image" src="https://github.com/user-attachments/assets/a38b0bbf-7bb9-46aa-8068-116f7af77b6b" />

























































 




































































