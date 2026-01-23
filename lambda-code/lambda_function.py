import json
import boto3
import os
import time
from decimal import Decimal

# --- Clients ---
textract = boto3.client('textract')
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

# --- Environment Variables ---
TABLE_NAME = os.environ.get('TABLE_NAME')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')

def lambda_handler(event, context):
    print("🚀 Starting Receipt Processing with AnalyzeExpense...")
    
    try:
        # 1. Λήψη στοιχείων αρχείου από το S3 Event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        print(f"📂 Processing File: {bucket}/{key}")

        # 2. Κλήση στο Amazon Textract (Ειδική λειτουργία για Αποδείξεις)
        # Αντί για detect_document_text, χρησιμοποιούμε analyze_expense
        response = textract.analyze_expense(
            Document={'S3Object': {'Bucket': bucket, 'Name': key}}
        )
        
        # 3. Εξαγωγή του Total Amount (Ενισχυμένη Λίστα)
        total_amount = "0.00"
        vendor_name = "Unknown Vendor"
        
        # ΠΡΟΣΘΕΣΑΜΕ ΤΟ 'BALANCE' ΚΑΙ ΤΟ 'AMOUNT' ΣΤΗ ΛΙΣΤΑ!
        target_fields = [ 'TOTAL', 'AMOUNT_DUE', 'AMOUNT_PAID', 'GRAND_TOTAL', 'INVOICE_TOTAL', 'BALANCE', 'AMOUNT',  # English
                        'ΣΥΝΟΛΟ', 'ΠΛΗΡΩΤΕΟ', 'ΓΕΝΙΚΟ ΣΥΝΟΛΟ', 'ΤΕΛΙΚΟ ΠΟΣΟ', 'ΑΞΙΑ']  # Greek

        for doc in response['ExpenseDocuments']:
            
            print("🔍 Analyzing Summary Fields found in receipt:")
            for field in doc['SummaryFields']:
                key_type = field['Type']['Text']
                value = field['ValueDetection']['Text'] if 'ValueDetection' in field else ""
                
                print(f"   🔹 Found Field: {key_type} = '{value}'")

                # Έλεγχος: Αν το κλειδί είναι στη λίστα ΜΑΣ ΚΑΙ η τιμή ΔΕΝ είναι κενή
                if key_type in target_fields and value.strip() != "":
                    total_amount = value
                    print(f"   ✅ MATCHED TOTAL (via {key_type}): {total_amount}")
                
                if key_type == 'VENDOR_NAME':
                    vendor_name = value
                    print(f"   🏢 MATCHED VENDOR: {vendor_name}")

        # Καθαρισμός του ποσού από σύμβολα (π.χ. $46.30 -> 46.30)
        clean_amount = total_amount.replace('$', '').replace('€', '').replace(',', '.').strip()

        # 4. Αποθήκευση στη DynamoDB
        table = dynamodb.Table(TABLE_NAME)
        receipt_id = key.split('.')[0] 
        
        item = {
            'receipt_id': receipt_id,
            'created_at': str(time.time()),
            'file_name': key,
            'vendor': vendor_name,        # Πλέον έχουμε και όνομα καταστήματος!
            'total_amount': clean_amount,
            'raw_amount': total_amount    # Κρατάμε και το αρχικό για έλεγχο
        }
        
        table.put_item(Item=item)
        print("💾 Saved to DynamoDB")

        # 5. Αποστολή Email μέσω SNS
        message = (
            f"🧾 New Receipt Processed!\n\n"
            f"🏢 Store: {vendor_name}\n"
            f"📂 File: {key}\n"
            f"💰 Total Amount: {clean_amount}\n"
            f"✅ Status: Saved to Database"
        )
        
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject="AWS Receipt Processed"
        )
        print("📧 Notification Sent")

        return {
            'statusCode': 200,
            'body': json.dumps('Receipt processed successfully with AnalyzeExpense!')
        }

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise e