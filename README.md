# 🧾 AI Serverless Receipt Scanner (AWS)

A production-ready, event-driven serverless application that automates receipt data extraction using Artificial Intelligence. This project leverages **Amazon Textract** to process receipts uploaded to **Amazon S3**, stores the metadata in **Amazon DynamoDB**, and sends real-time notifications via **Amazon SNS**.

---

## 🏗️ Architecture Diagram
![Architecture Diagram](./architecture-diagram/diagram_receiptScanner.png)

### 🔄 The Workflow:
1. **Upload:** A receipt image (PNG/JPG) is uploaded to an **S3 Bucket**.
2. **Trigger:** The upload event triggers an **AWS Lambda** function.
3. **AI Processing:** Lambda calls **Amazon Textract (AnalyzeExpense)** to extract vendor name and total amount.
4. **Data Storage:** The extracted data is stored in a **DynamoDB Table**.
5. **Notification:** An email notification is sent via **Amazon SNS** with the processing results.

---

## 🚀 Key Features
- **Event-Driven:** Fully automated process triggered by S3 uploads.
- **AI-Powered OCR:** Uses specialized expense analysis to handle complex receipt layouts.
- **Multi-language Support:** Successfully tested with both **English** and **Greek** receipts.
- **Smart Parsing:** Advanced logic to filter out empty "Total" fields and handle various currency formats.
- **Cost-Efficient:** Built entirely on a Serverless stack (Pay-as-you-go).

---

## 🛠️ Tech Stack
- **Compute:** AWS Lambda (Python 3.x)
- **AI/ML:** Amazon Textract
- **Storage:** Amazon S3, Amazon DynamoDB
- **Messaging:** Amazon SNS
- **SDK:** Boto3

---

## 📂 Project Structure
- `lambda-code/`: The Python source code for the processing engine.
- `iam-policies/`: JSON templates for the IAM roles and permissions.
- `architecture-diagram/`: Visual representation of the cloud infrastructure.
- `sample-receipts/`: Example receipts used for testing (blurred for privacy).

---

## 🔧 Deployment Steps
1. Create an **S3 Bucket** for receipt uploads.
2. Create a **DynamoDB Table** (Partition Key: `receipt_id`).
3. Create an **SNS Topic** and subscribe your email.
4. Deploy the **Lambda Function** with the provided code.
5. Attach the **IAM Policies** to the Lambda role (S3, Textract, DynamoDB, SNS access).
6. Set Environment Variables in Lambda: `TABLE_NAME` and `SNS_TOPIC_ARN`.

---

## 📈 Future Improvements
- [ ] Integration with a frontend dashboard to visualize expenses.
- [ ] Support for multi-page PDF document analysis.
- [ ] Adding AWS Step Functions for more complex error handling.

---

## 👨‍💻 About the Author
This project is part of my Serverless Cloud Portfolio, where I document my journey into AWS Cloud Architecture. 
👉 Explore the Live Portfolio here: (https://d1fx4silgg9iud.cloudfront.net/)
