# 📘 Publish–Subscribe Notification System (TCP + SSL)

## 🔹 Project Overview

This project implements a **secure publish–subscribe messaging system** using **TCP socket programming in Python**.

- Multiple clients can connect to a server  
- Clients can subscribe to topics  
- Messages are delivered in real-time  
- Communication is secured using SSL/TLS  

---

## ⚙️ Features

- Topic-based subscription system  
- Real-time message delivery  
- Multi-client support using threading  
- Secure communication using SSL  
- Custom application-layer protocol  

---

## 🧰 Requirements

- Python 3.x  
- OpenSSL installed  

---

## 📁 Project Structure

---

## 🔐 Step 1: Generate SSL Certificates

Run this command:
openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem
---

## ▶️ Step 2: Run Server
python3 server.py

Expected Output:
[LISTENING] on 0.0.0.0:5000

---

## 💻 Step 3: Run Client
---

## 💻 Step 3: Run Client


python3 client.py


---

## 🌐 Step 4: Run Multiple Clients

Open multiple terminals and run:


python3 client.py


---

## 🧠 Available Commands

### 📌 Subscribe

SUBSCRIBE <topic>
### 📌 Unsubscribe

UNSUBSCRIBE <topic>


### 📌 Publish

PUBLISH <topic> <message>


---

## 🔄 Example Workflow

Client 1:

SUBSCRIBE sports


Client 2:

PUBLISH sports Hello everyone


Output:

[sports] Hello everyone
---

## 🔐 Security Note

- SSL/TLS is used for encryption  
- Self-signed certificates are used for development  
- Certificate verification is disabled  

---

## ⚠️ Troubleshooting

### Connection Refused
Run server first:
python3 server.py
### SSL Error
Ensure:

cert.pem
key.pem


### Python Not Found
Use:

python3 client.py


---

## 📊 Performance

- Works efficiently for small number of clients  
- Latency increases with more clients  

---

## 🎯 Conclusion

This project demonstrates:

- TCP communication  
- Application-layer protocol design  
- Secure communication using SSL  
- Real-time messaging  

---

## 👨‍💻 Team:

Abhiraj Dhananjay - PESUG24CS016
Aarohi Jaiswal - PES1UG24CS009
Aaditya Vashisht - PES1UG24CS004