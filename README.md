# 🧾 Serverless Receipt Scanner & Analyzer

A cloud-native system designed to automate receipt processing and expense tracking using **AWS Serverless** architecture and **AI-powered OCR**.

## 🚀 Project Overview
This project solves the problem of manual expense entry. By simply uploading a photo of a receipt, the system automatically:
1.  **Scans** the entire document using **Amazon Textract** (AI/ML).
2.  **Identifies** and extracts the **Total Amount** via custom logic within an AWS Lambda function.
3.  **Stores** the transaction details (Date, ID, Amount) in a **DynamoDB** NoSQL database.
4.  **Notifies** the user instantly via **Email** through **Amazon SNS**.

## 🏗️ Architecture
![AWS Architecture Diagram](diagram.png)

## 🛠️ Tech Stack
* **Compute:** Python 3.12+ on **AWS Lambda** (Serverless)
* **Storage:** **Amazon S3** (Image hosting)
* **Database:** **Amazon DynamoDB** (NoSQL Persistence)
* **AI/ML:** **Amazon Textract** (Optical Character Recognition - OCR)
* **Messaging:** **Amazon SNS** (Simple Notification Service)

## ⚙️ How it Works (Data Flow)
1.  **Upload:** The user uploads an image (`.jpg` or `.png`) to a specific S3 bucket.
2.  **Trigger (Event-Driven):** S3 generates an event that automatically triggers the Lambda function.
3.  **AI Analysis:** The Lambda function sends the image to Amazon Textract for analysis.
4.  **Extraction Logic:** Textract returns the raw text (JSON). The Python code parses this data to locate and extract the specific "Total" payment value.
5.  **Persistence:** The extracted data is saved as a new item in the DynamoDB table.
6.  **Notification:** Finally, a message is published to an SNS Topic, which sends an automated email notification to the user.

---
*Developed as a Cloud Engineering hands-on project to demonstrate expertise in Event-Driven architectures.*
