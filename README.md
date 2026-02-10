# UPI_FRAUD_DETECTION_SYSTEM
🔐 UPI Fraud Detection System

The UPI Fraud Detection System is a Python-based web application designed to identify and prevent fraudulent Unified Payments Interface (UPI) transactions in real time. With the rapid growth of digital payments in India, UPI fraud cases such as fake payment requests, blacklisted mobile numbers, and high-value scam transactions have increased significantly. This project aims to provide a simple, effective, and user-friendly solution to verify transactions before payment completion.

The application is developed using Python and Streamlit, allowing users to interact with the system through a web-based interface. Users can enter transaction details such as UPI ID, receiver mobile number, and transaction amount. Once the details are submitted, the system immediately verifies the transaction using rule-based fraud detection logic and blacklist verification. Based on the verification process, the transaction is classified as Safe (Low Risk) or Fraud (High Risk) and the result is displayed instantly.

To ensure transparency and traceability, every transaction is recorded in a CSV-based transaction log, which can later be used for analysis and monitoring. An Admin module is also included, allowing authorized users to view transaction logs and manage blacklisted UPI IDs and mobile numbers. This helps in maintaining system security and monitoring suspicious activities.

The project follows standard software engineering design principles, including ER Diagram, Use Case Diagram, Sequence Diagram, Activity Diagram, Data Flow Diagram (DFD), and a layered System Architecture. The architecture is divided into three layers: Presentation Layer (Streamlit UI), Application Layer (fraud detection logic), and Data Layer (CSV files for storage).

Although the current system uses rule-based detection, it is designed to be easily extensible. In the future, the project can be enhanced by integrating machine learning models, real-time bank/UPI APIs, behavioral analysis, and cloud deployment to improve accuracy and scalability.

Yeh system sirf random guess nahi karta, balki "Multi-Factor Risk Scoring" model par kaam karta hai. Niche diye gaye 5 points ke basis par fraud detect hota hai:
Global Blacklist Check (100% Risk):
System sabse pehle check karta hai ki kya woh UPI ID Admin dwara pehle se block ki gayi hai. Agar milti hai, toh turant 100% Fraud declare kar deta hai.
Temporal Risk (Time Analysis - 20% Score):
Raat ke 11 PM se subah 4 AM ke beech hone wale transactions ko risky maana jata hai, kyunki zyadatar fraud isi time window mein hote hain.
Threshold & Value Risk (Amount Analysis - Up to 50% Score):
Agar transaction ₹90,000 se upar hai, toh high alert trigger hota hai. ₹45,000 se upar hone par medium risk score add hota hai.
Phishing Pattern Recognition (55% Score):
System UPI handle (naam) ko scan karta hai. Agar handle mein lottery, win, prize, gift, ya hacker jaise keywords milte hain, toh score badh jata hai.
Mule Account Detection: Agar handle bahut lamba hai ya usme ajeeb numbers (random generation) hain, toh system use "Mule Account" (fake account) ki category mein daalta hai.
Geographic Anomaly (Location Shift - 35% Score):
Aapne code mein Mumbai ko home city set kiya hai. Agar koi transaction kisi door ki city se hota hai, toh system use "IP/Location shift" maankar risk score badha deta hai.

⭐ Key Features

Real-time transaction verification

Blacklist-based fraud detection

Admin monitoring and control

CSV-based logging system

Simple and interactive Streamlit UI
