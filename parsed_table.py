import sys
import os
from edi_837 import parse_837
from edi_835 import parse_835
import mysql.connector
import uuid
from settings import *

mysql_conn = mysql.connector.connect(
  host=MYSQL_HOST,
  user=MYSQL_USER,
  password=MYSQL_PASSWORD,
  database=MYSQL_DB
)

cursor = mysql_conn.cursor()

query = ""
total = 0

def add_835(claim, filepath, cnt):
  print("835", filepath, cnt)
  global query
  global total
  # print(claim)
  id = str(uuid.uuid4())
  services = ""
  for service in claim['Service']:
    services += f"{service['Code']}:{service['Modifier']}:{service['ChargeAmount']}:{service['PayAmount']}:"
    for carc in service['CARC']:
      services += f"{carc['GroupCode']}{carc['Code']}@{carc['Amount']}#"
    if services[-1] == '#':
      services = services[:len(services)-1] + ":"
    else:
      services += ":"
    services += f"{service['Remark']},"
  if services[-1] == ',':
    services = services[:len(services)-1]
  # print(services)
  query += f"""(
    "{id}",
    "{claim["TaxID"]}",
    "{services}",
    "{claim["NPI"]}",
    "{claim["PatientControlNumber"]}",
    {claim["TotalClaimChargeAmount"]},
    {claim["ClaimPaymentAmount"]},
    "{claim["ServiceDate"]}",
    "{claim["Payee"]["Name"]}",
    "{claim["Payee"]["NPI"]}",
    "{claim["Payee"]["TaxID"]}",
    "{claim["Payer"]["Name"]}",
    "{claim["Payer"]["Address"]}",
    "{claim["Payer"]["City"]}",
    "{claim["Payer"]["State"]}",
    "{claim["Payer"]["ZipCode"]}",
    "{filepath}",
    {cnt}
  ),"""
  total += 1

def start_add_835():
  q = "INSERT INTO parsed_835_all SELECT * FROM parsed_835"
  cursor.execute(q)
  q = "DELETE FROM parsed_835"
  cursor.execute(q)
  mysql_conn.commit()
  global query
  global total
  total = 0
  query = "INSERT INTO parsed_835 VALUES "
  for file_name in os.listdir(base_dir_835):
    output = parse_835(base_dir_835+file_name)
    index = 0
    for claim in output['Claim']:
      index += 1
      add_835(claim, base_dir_835+file_name, index)
      if total == QUERY_SIZE:
        query = query[:len(query)-1]
        cursor.execute(query)
        mysql_conn.commit()
        total = 0
        query = "INSERT INTO parsed_835 VALUES "
  if query[-1] == ',':
    query = query[:len(query)-1]
    cursor.execute(query)
    mysql_conn.commit()
    total = 0
    query = "INSERT INTO parsed_835 VALUES "

def add_837(claim, filepath, cnt):
  print("837", filepath, cnt)
  global query
  global total
  id = str(uuid.uuid4())
  diagnosis = ":".join(claim['Diagnosis'])
  services = ""
  for service in claim['Services']:
    services += f"{service['ChargeAmount']}|{service['Units']}|{service['ServiceDate']}|{service['SourceID']}|{service['Code']}|{service['Modifier']}:"
  if services[-1] == ':':
    services = services[:len(services)-1]
  query += f"""(
    "{id}",
    "{claim["Patient"]["FirstName"]}",
    "{claim["Patient"]["LastName"]}",
    "{claim["Patient"]["MiddleName"]}",
    "{claim["Patient"]["Address"]}",
    "{claim["Patient"]["City"]}",
    "{claim["Patient"]["State"]}",
    "{claim["Patient"]["ZipCode"]}",
    "{claim["Patient"]["Birthday"]}",
    "{claim["Patient"]["Gender"]}",
    "{claim["Patient"]["SSN"]}",
    "{claim["Payer"]["Name"]}",
    "{claim["Payer"]["ID"]}",
    "{claim["Payer"]["Address"]}",
    "{claim["Payer"]["City"]}",
    "{claim["Payer"]["State"]}",
    "{claim["Payer"]["ZipCode"]}",
    "{diagnosis}",
    "{services}",
    "{claim["PatientAccountNumber"]}",
    {claim["TotalClaimChargeAmount"]},
    "{claim["AccidentDate"]}",
    "{claim["ServiceDate"]}",
    "{claim["MedicalRecordNumber"]}",
    "{claim["AuthNumber"]}",
    "{claim["RenderingProvider"]["Type"]}",
    "{claim["RenderingProvider"]["FirstName"]}",
    "{claim["RenderingProvider"]["LastName"]}",
    "{claim["RenderingProvider"]["Name"]}",
    "{claim["RenderingProvider"]["NPI"]}",
    "{claim["BillingProvider"]["Type"]}",
    "{claim["BillingProvider"]["FirstName"]}",
    "{claim["BillingProvider"]["LastName"]}",
    "{claim["BillingProvider"]["AddressLine1"]}",
    "{claim["BillingProvider"]["AddressLine2"]}",
    "{claim["BillingProvider"]["City"]}",
    "{claim["BillingProvider"]["State"]}",
    "{claim["BillingProvider"]["ZipCode"]}",
    "{claim["BillingProvider"]["NPI"]}",
    "{claim["BillingProvider"]["TaxID"]}",
    "{filepath}",
    {cnt}
  ),"""
  total += 1

def start_add_837():
  q = "INSERT INTO parsed_837_all SELECT * FROM parsed_837"
  cursor.execute(q)
  q = "DELETE FROM parsed_837"
  cursor.execute(q)
  mysql_conn.commit()
  global query
  global total
  total = 0
  query = "INSERT INTO parsed_837 VALUES "
  for file_name in os.listdir(base_dir_837):
    output = parse_837(base_dir_837+file_name)
    index = 0
    for claim in output['Claim']:
      index += 1
      add_837(claim, base_dir_837+file_name, index)
      if total == QUERY_SIZE:
        query = query[:len(query)-1]
        print(query)
        cursor.execute(query)
        mysql_conn.commit()
        total = 0
        query = "INSERT INTO parsed_837 VALUES "
  if query[-1] == ',':
    query = query[:len(query)-1]
    cursor.execute(query)
    mysql_conn.commit()
    total = 0
    query = "INSERT INTO parsed_837 VALUES "

if __name__ == '__main__':
  start_add_837()
  start_add_835()