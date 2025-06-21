[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=emes30&repository=facebook_messenger&category=integration)
\
[![License](https://img.shields.io/badge/License-MIT-blue)](#license)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)

# Facebook Messenger for Home Assistant

Đây là bản nâng cấp cho <a href="https://www.home-assistant.io/integrations/facebook/" target="_blank">Home Assistant</a> Facebook integration. Nó cho phép bạn gửi thông báo đến Messenger với hình ảnh, text, button, quicky_reply.

----

### Contents

 * [Chức năng](#functionality)
 * [Cài đặt](#installation)
 * [Cấu hình](#configuration)
 * [Cách lấy mã thông báo Facebook của bạn](#how-to-obtain-your-facebook-token)
 * [Cách lấy user PSID](#how-to-obtain-your-user-psid)
 * [Usage](#usage)
 * [License](#license)

----

### Chức năng

Tích hợp này dựa trên tích hợp Facebook hiện có trong Trợ lý gia đình.
Có thể gửi thông báo dựa trên văn bản, button, quick_reply và hình ảnh. 
Bạn cũng có thể gán tên cho SID của mình và sử dụng nó làm mục tiêu thông báo.

----

### Cài đặt

Cài đặt thông HACS. [here](https://my.home-assistant.io/redirect/hacs_repository/?owner=hoducnguyenhd&repository=facebook_messenger&category=integration)

----

### Cấu hình

Tích hợp này tự hiển thị như một <a href="https://www.home-assistant.io/integrations/notify/" target="_blank">notifications integration</a>, và có thể được định cấu hình bằng cách thêm đoạn mã này vào file `configuration.yaml`:

```yaml
notify:
  name: messenger
  platform: facebook_messenger
  page_access_token: <YOUR FACEBOOK TOKEN>
  targets:
    - sid: <YOUR PSID>
      name: abc
```

Thay thế `<YOUR FACEBOOK TOKEN>` bằng Facebook token của bạn, nên đặt ở secrets.yaml để bảo mật hơn.

`targets` là thuộc tính là tùy chọn. Nếu bạn khai báo nó, bạn có thể sử dụng tên người có thể đọc được thay vì các chữ số làm mục tiêu thông báo của bạn.

Khởi động lại Home Assistant để tải cấu hình. 

---

### Làm thế nào để lấy Facebook token

Để sử dụng tích hợp này, bạn phải đăng ký làm nhà phát triển Facebook và tạo ứng dụng sẽ thay mặt bạn gửi thông báo. Đầu tiên đăng nhập vào tài khoản Facebook của bạn và click [here](https://developers.facebook.com/async/registration) để bắt đầu quá trình đăng ký. làm theo hướng dẫn của Facebook (use developer :wink:).\
----

### Cách lấy user PSID

----

### Usage

#### Text notification

```yaml
  action:
    - service: notify.messenger
      data:
        target: nguyen
        message: "Test Home Assistant."
```

#### Image notification

```yaml
  action:
    - service: notify.messenger
      data:
        target: nguyen
        data:
          media: "<path to image file on server>"
          media_type: "image/jpeg"
```
#### Button notification

```yaml
  action:
    - service: notify.messenger
      data:
        target: nguyen
        message: "Chọn thao tác:"
        data:
          buttons:
            - type: postback
              title: "BẬT đèn"
              payload: "BAT_DEN"
            - type: postback
              title: "Tắt đèn"
              payload: "TAT_DEN"  
```
#### Quick replies notification

```yaml
  action:
    - service: notify.messenger
      data:
        target: nguyen
        message: "Bạn muốn làm gì?"
        data:
          quick_replies:
            - content_type: text
              title: "Bật đèn"
              payload: "BAT_DEN"
            - content_type: text
              title: "Tắt đèn"
              payload: "TAT_DEN"    
```

----

### License

This software is released under the <a href="https://opensource.org/licenses/MIT" target="_blank">MIT license</a>.
