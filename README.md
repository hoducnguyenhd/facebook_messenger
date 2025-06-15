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
 * [Hot to obtain your user's PSID](#how-to-obtain-your-user-psid)
 * [Installation and Configuration Summary](#installation-and-configuration-summary)
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

Để sử dụng tích hợp này, bạn phải đăng ký làm nhà phát triển Facebook và tạo ứng dụng sẽ thay mặt bạn gửi thông báo. Đầu tiên đăng nhập vào tài khoản Facebook của bạn và click [here](https://developers.facebook.com/async/registration) để bắt đầu quá trình đăng ký. làm theo hướng dẫn cảu Facebook (use developer :wink:).\
When you've done with registration process, add [new application](https://developers.facebook.com/apps/create/).

1. Choose app type Business
2. Choose Display name, enter your email and click Create App. You'll have to enter password again.
3. On the next page **Add products to your app** find Messenger tile and click Set up.
4. Find **Access Tokens** section and click **Create new Page**, new tab will open, keep this one open, you return here in steps 7 and 10
5. Provide Name and Category, you may choose whatever you like, but Name must be unique.
6. Click next until you reach Ready page, you don't have to provide any additional information
7. Return to **Access Tokens** tab, and this time click **Add or remove Page**, new window opens
8. Confirm that it's really you, check Page you've just created, and click Next
9. Ignore warning and click Ready!, your page is connected with Facebook
10. Return to **Access Tokens** tab again, now click **Generate token**, check I understand,
11. Success :muscle: finally you have your token, copy and save it

----

### How to obtain your user PSID

This part is quite tricky, hope you can get through this. As using phone numbers is not an option nowdays, this is the only way to get things working. To find your (or your testers) PSID you have to assign webhook
to your page, that webhook will reply with your PSID. Let's start.

1. For creating webhook we'll use [glitch.com](https://glitch.com), you don't need to register there
2. Open my project [get-messenger-page-sid](https://glitch.com/edit/#!/get-messenger-page-sid) and click `Remix`
3. New project is created, on the left you have file manager, click `.env`
4. Paste your **Facebook Access Token** as **PAGE_ACCESS_TOKEN** variable value
5. Put value of your choice into **VERIFY_TOKEN** value, exactly the same value you enter at Facebook, step 10
6. At the bottom of the screen click `PREVIEW` then `Open preview pane`
7. Preview opens on the right side, you'll see url ex. `observant-foregoing-scent.glitch.me/`, open menu and click `Copy Link`
8. Now go to your facebook developer dashboard [https://developers.facebook.com/apps/](https://developers.facebook.com/apps/), and click your app
9. On the left menu click `Messenger`, `Settings`, find `Webhooks` section, click `Add Callback URL`
10. Paste your glitch url here, append `/webhook` at the end so full url looks something like `https://observant-foregoing-scent.glitch.me/webhook`, enter your verify token, click `Verify and save`
11. You should see your webhook added, click `Add subscriptions` and select `messages`
12. Your webhook is ready, now use Messenger to send any message to your page, it replies with your PSID


----

### Installation and Configuration Summary

Quick summary to get things working:

- Install **facebook_messenger** integration
- Reboot Home Assistant
- Create a `notify` entity, use your facebook page token
- Reboot Home Assistant
- Start adding the new entity to your automations & scripts :)

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
#### Automation_Webhook JSON event

```yaml
alias: Webhook Event Messenger
description: ""
triggers:
  - webhook_id: messenger_inbox
    trigger: webhook
    allowed_methods:
      - POST
      - PUT
      - GET
    local_only: false
actions:
  - variables:
      data: "{{ trigger.json }}"
      messaging: "{{ data.entry[0].messaging[0] }}"
      sender_id: "{{ messaging.sender.id }}"
      text: |-
        {% if 'message' in messaging and 'text' in messaging.message %}
          {{ messaging.message.text }}
        {% elif 'postback' in messaging and 'title' in messaging.postback %}
          {{ messaging.postback.title }}
        {% else %}
          ""
        {% endif %}
      payload: |-
        {% if 'postback' in messaging %}
          {{ messaging.postback.payload }}
        {% elif 'message' in messaging and 'quick_reply' in messaging.message %}
          {{ messaging.message.quick_reply.payload }}
        {% else %}
          "null"
        {% endif %}
      action_type: |-
        {% if 'postback' in messaging %}
          button
        {% elif 'message' in messaging and 'quick_reply' in messaging.message %}
          quick_reply
        {% else %}
          null
        {% endif %}
  - event: messenger_webhook
    event_data:
      sender_id: "{{ sender_id }}"
      text: "{{ text }}"
      payload: "{{ payload }}"
      action_type: "{{ action_type }}"

```

It is important to specify correct `media_type`. It is validated by Facebook and message will be rejected when `media_type` doesn't match actual media file type. `image/jpeg` is default value.

You can also test it in Developer Tools, under Services tab.

----

### License

This software is released under the <a href="https://opensource.org/licenses/MIT" target="_blank">MIT license</a>.
