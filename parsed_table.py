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
  if len(services) != 0 and services[-1] == ',':
    services = services[:len(services)-1]
  # print(services)
  query += f"""(
    "{id}",
    "{claim['Patient']['Type']}",
    "{claim['Patient']['Name']}",
    "{claim['Patient']['FirstName']}",
    "{claim['Patient']['LastName']}",
    "{claim['Patient']['MiddleName']}",
    "{claim['Patient']['IDType']}",
    "{claim['Patient']['NPI']}",
    "{claim['Patient']['MemberID']}",
    "{claim['InsuredSubscriber']['Type']}",
    "{claim['InsuredSubscriber']['Name']}",
    "{claim['InsuredSubscriber']['FirstName']}",
    "{claim['InsuredSubscriber']['LastName']}",
    "{claim['InsuredSubscriber']['MiddleName']}",
    "{claim['InsuredSubscriber']['IDType']}",
    "{claim['InsuredSubscriber']['NPI']}",
    "{claim['InsuredSubscriber']['MemberID']}",
    "{claim['RenderingProvider']['Type']}",
    "{claim['RenderingProvider']['Name']}",
    "{claim['RenderingProvider']['FirstName']}",
    "{claim['RenderingProvider']['LastName']}",
    "{claim['RenderingProvider']['MiddleName']}",
    "{claim['RenderingProvider']['IDType']}",
    "{claim['RenderingProvider']['NPI']}",
    "{claim['RenderingProvider']['MemberID']}",
    "{claim['PayerClaimControlNumber']}",
    "{claim['PatientControlNumber']}",
    {claim['TotalClaimChargeAmount']},
    {claim['ClaimPaymentAmount']},
    {claim['PatientResponsibilityAmount']},
    "{claim['ProductionDate']}",
    "{claim['PaymentDate']}",
    "{claim['TrackNumber']}",
    "{claim['PayerIdentifier']}",
    "{claim['Payer']['Name']}",
    "{claim['Payer']['Address']}",
    "{claim['Payer']['City']}",
    "{claim['Payer']['State']}",
    "{claim['Payer']['ZipCode']}",
    "{claim['Payer']['ID']}",
    "{claim['Payer']['ContactName']}",
    "{claim['Payer']['ContactNumber']}",
    "{claim['Payee']['Name']}",
    "{claim['Payee']['IDType']}",
    "{claim['Payee']['NPI']}",
    "{claim['Payee']['MemberID']}",
    "{claim['Payee']['Address']}",
    "{claim['Payee']['City']}",
    "{claim['Payee']['State']}",
    "{claim['Payee']['ZipCode']}",
    "{claim['Payee']['TaxID']}",
    "{claim['ContractCode']}",
    "{claim['MedicalRecordNumber']}",
    "{claim['PolicyNumber']}",
    "{claim['PeriodStart']}",
    "{claim['PeriodEnd']}",
    "{claim['ReceiveDate']}",
    "{services}",
    "{filepath}",
    {cnt}
  ),"""
  total += 1

def start_add_835():
  # q = "INSERT INTO parsed_835_all SELECT * FROM parsed_835"
  # cursor.execute(q)
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
  diagnosis = ""
  for diagnos in claim['Diagnosis']:
    diagnosis += diagnos['Type'] + '*' + diagnos['Code'] + ':'
  if len(diagnosis) and diagnosis[-1] == ':':
    diagnosis = diagnosis[:len(diagnosis)-1]
  services = ""
  for service in claim['Services']:
    services += f"{service['ChargeAmount']}|{service['Units']}|{service['ServiceDate']}|{service['SourceID']}|{service['Code']}|{service['Modifier']},"
  if len(services) != 0 and services[-1] == ',':
    services = services[:len(services)-1]
  query += f"""(
    "{id}",
    "{claim['Patient']['FirstName']}",
    "{claim['Patient']['LastName']}",
    "{claim['Patient']['MiddleName']}",
    "{claim['Patient']['Address']}",
    "{claim['Patient']['City']}",
    "{claim['Patient']['State']}",
    "{claim['Patient']['ZipCode']}",
    "{claim['Patient']['Birthday']}",
    "{claim['Patient']['Gender']}",
    "{claim['Patient']['SSN']}",
    "{claim['Patient']['RelationshipToSubscriber']}",
    "{claim['Patient']['TaxID']}",
    "{claim['Patient']['ID']}",
    "{claim['PrimaryPayer']['Name']}",
    "{claim['PrimaryPayer']['ID']}",
    "{claim['PrimaryPayer']['Address']}",
    "{claim['PrimaryPayer']['City']}",
    "{claim['PrimaryPayer']['State']}",
    "{claim['PrimaryPayer']['ZipCode']}",
    "{claim['SecondaryPayer']['Name']}",
    "{claim['SecondaryPayer']['ID']}",
    "{claim['SecondaryPayer']['Address']}",
    "{claim['SecondaryPayer']['City']}",
    "{claim['SecondaryPayer']['State']}",
    "{claim['SecondaryPayer']['ZipCode']}",
    "{claim['PrimarySubscriber']['Type']}",
    "{claim['PrimarySubscriber']['FirstName']}",
    "{claim['PrimarySubscriber']['LastName']}",
    "{claim['PrimarySubscriber']['Name']}",
    "{claim['PrimarySubscriber']['ID']}",
    "{claim['PrimarySubscriber']['GroupName']}",
    "{claim['PrimarySubscriber']['InsurancePlanType']}",
    "{claim['PrimarySubscriber']['PayerSequence']}",
    "{claim['SecondarySubscriber']['Type']}",
    "{claim['SecondarySubscriber']['FirstName']}",
    "{claim['SecondarySubscriber']['LastName']}",
    "{claim['SecondarySubscriber']['Name']}",
    "{claim['SecondarySubscriber']['ID']}",
    "{claim['SecondarySubscriber']['GroupName']}",
    "{claim['SecondarySubscriber']['InsurancePlanType']}",
    "{claim['SecondarySubscriber']['PayerSequence']}",
    "{claim['ServiceFacility']['Type']}",
    "{claim['ServiceFacility']['FirstName']}",
    "{claim['ServiceFacility']['LastName']}",
    "{claim['ServiceFacility']['Name']}",
    "{claim['ServiceFacility']['NPI']}",
    "{claim['ServiceFacility']['Address1']}",
    "{claim['ServiceFacility']['Address2']}",
    "{claim['ServiceFacility']['City']}",
    "{claim['ServiceFacility']['State']}",
    "{claim['ServiceFacility']['ZipCode']}",
    "{claim['SupervisingProvider']['Type']}",
    "{claim['SupervisingProvider']['Name']}",
    "{claim['SupervisingProvider']['FirstName']}",
    "{claim['SupervisingProvider']['LastName']}",
    "{claim['SupervisingProvider']['NPI']}",
    "{claim['RenderingProvider']['Type']}",
    "{claim['RenderingProvider']['FirstName']}",
    "{claim['RenderingProvider']['LastName']}",
    "{claim['RenderingProvider']['Name']}",
    "{claim['RenderingProvider']['NPI']}",
    "{claim['RenderingProvider']['Taxonomy']}",
    "{claim['RenderingProvider']['Grouping']}",
    "{claim['ReferringProvider']['Type']}",
    "{claim['ReferringProvider']['Name']}",
    "{claim['ReferringProvider']['FirstName']}",
    "{claim['ReferringProvider']['LastName']}",
    "{claim['ReferringProvider']['NPI']}",
    "{claim['PatientAccoutnNumber']}",
    {claim['TotalClaimChargeAmount']},
    "{claim['AccidentDate']}",
    "{claim['ServiceDate']}",
    "{claim['MedicalRecordNumber']}",
    "{claim['AuthNumber']}",
    "{claim['ContractCode']}",
    "{claim['PolicyNumber']}",
    "{claim['BillingProvider']['Type']}",
    "{claim['BillingProvider']['NPI']}",
    "{claim['BillingProvider']['TaxID']}",
    "{claim['BillingProvider']['Name']}",
    "{claim['BillingProvider']['FirstName']}",
    "{claim['BillingProvider']['LastName']}",
    "{claim['BillingProvider']['Address1']}",
    "{claim['BillingProvider']['Address2']}",
    "{claim['BillingProvider']['City']}",
    "{claim['BillingProvider']['State']}",
    "{claim['BillingProvider']['ZipCode']}",
    "{claim['Submitter']['Type']}",
    "{claim['Submitter']['Name']}",
    "{claim['Submitter']['FirstName']}",
    "{claim['Submitter']['LastName']}",
    "{claim['Submitter']['ContactName']}",
    "{claim['Submitter']['ContactNumber']}",
    "{claim['Submitter']['ETIN']}",
    "{claim['Receiver']['Type']}",
    "{claim['Receiver']['Name']}",
    "{claim['Receiver']['FirstName']}",
    "{claim['Receiver']['LastName']}",
    "{claim['Receiver']['ETIN']}",
    "{diagnosis}",
    "{services}",
    "{filepath}",
    {cnt}
  ),"""
  total += 1

def start_add_837():
  # q = "INSERT INTO parsed_837_all SELECT * FROM parsed_837"
  # cursor.execute(q)
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
        # print(query)
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
  # start_add_835()