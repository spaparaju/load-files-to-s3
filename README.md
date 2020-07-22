# Purpose
Loads files from a source directory to a S3 bucket

# Usage
1.  AWS credetials are present at ~/.aws/credentials
2.  pip3 install -r requirements.txt
3.  python3 xero.py <xero_client_id> <xero_token> <xero_scope>  <source_folder_name>  <s3_bucket_name>

You will get to see the invoice (a sample) from Xero

{'Id': 'cdfe863a-d4c5-441a-b1ba-f9db7170b39e', 'Status': 'OK', 'ProviderName': 'some-app', 'DateTimeUTC': '/Date(1595391240370)/', 'Invoices': [{'Type': 'ACCREC', 'InvoiceID': '2709172e-c896-499d-9157-504d65236a08', 'InvoiceNumber': 'INV-0001', 'Reference': '', 'Payments': [], 'CreditNotes': [], 'Prepayments': [], 'Overpayments': [], 'AmountDue': 1000.0, 'AmountPaid': 0.0, 'AmountCredited': 0.0, 'CurrencyRate': 1.0, 'IsDiscounted': False, 'HasAttachments': False, 'HasErrors': False, 'Contact': {'ContactID': '7dfa7add-991c-42d0-88af-9bf3bd3c8868', 'Name': 'partner', 'Addresses': [], 'Phones': [], 'ContactGroups': [], 'ContactPersons': [], 'HasValidationErrors': False}, 'DateString': '2020-07-22T00:00:00', 'Date': '/Date(1595376000000+0000)/', 'DueDateString': '2020-07-23T00:00:00', 'DueDate': '/Date(1595462400000+0000)/', 'Status': 'DRAFT', 'LineAmountTypes': 'Exclusive', 'LineItems': [], 'SubTotal': 1000.0, 'TotalTax': 0.0, 'Total': 1000.0, 'UpdatedDateUTC': '/Date(1595387811403+0000)/', 'CurrencyCode': 'AUD'}]}

