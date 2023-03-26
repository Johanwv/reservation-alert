# Instructions

### Build image

docker build -t alert-reservation .

### Run container

docker run -e GMAIL_USER=gmailuser@gmail.com -e GMAIL_PASSWORD=password -e MAIL_RECIPIENT=recipient@gmail
alert-reservation