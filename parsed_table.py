import sys
import os
from edi_837 import parse_837
from edi_835 import parse_835
import mysql.connector
import uuid

mysql_conn = mysql.connector.connect(
  host='localhost',
  user='root',
  password='',
  database='db_gabeo'
)

cursor = mysql_conn.cursor()

def check_patient(patient):
  query = f"""SELECT * FROM rebound_patient WHERE FirstName='{patient['FirstName']}' AND LastName="{patient['LastName']}" AND MiddleName='{patient['MiddleName']}' AND Address='{patient['Address']}' AND City="{patient['City']}" AND State='{patient['State']}' AND ZipCode='{patient['ZipCode']}' AND Birthday='{patient['Birthday']}' AND Gender='{patient['Gender']}' AND SSN='{patient['SSN']}'"""
  print(query)
  cursor.execute(query)
  result = cursor.fetchall()
  if len(result) == 0:
    id = str(uuid.uuid4())
    query = f"INSERT INTO rebound_patient(id, FirstName, LastName, MiddleName, Address, City, State, ZipCode, Birthday, Gender, SSN) VALUES('{id}', '{patient['FirstName']}', '{patient['LastName']}', '{patient['MiddleName']}', '{patient['Address']}', '{patient['City']}', '{patient['State']}', '{patient['ZipCode']}', '{patient['Birthday']}', '{patient['Gender']}', '{patient['SSN']}')"
    cursor.execute(query)
    return id
  else:
    return result[0][0]

def check_payer(payer):
  query = f"SELECT * FROM rebound_payer WHERE Name='{payer['Name']}' AND Payer_ID='{payer['ID']}' AND Address='{payer['Address']}' AND City='{payer['City']}' AND State='{payer['State']}' AND ZipCode='{payer['ZipCode']}'"
  cursor.execute(query)
  result = cursor.fetchall()
  if len(result) == 0:
    id = str(uuid.uuid4())
    query = f"INSERT INTO rebound_payer(id, Name, Payer_ID, Address, City, State, ZipCode) VALUES('{id}', '{payer['Name']}', '{payer['ID']}', '{payer['Address']}', '{payer['City']}', '{payer['State']}', '{payer['ZipCode']}')"
    cursor.execute(query)
    return id
  else:
    return result[0][0]

def check_billingprovider(billingprovider):
  query = f"SELECT * FROM rebound_billingprovider WHERE Type='{billingprovider['Type']}' AND Name='{billingprovider['Name']}' AND FirstName='{billingprovider['FirstName']}' AND LastName='{billingprovider['LastName']}' AND AddressLine1='{billingprovider['AddressLine1']}' AND AddressLine2='{billingprovider['AddressLine2']}' AND City='{billingprovider['City']}' AND State='{billingprovider['State']}' AND ZipCode='{billingprovider['ZipCode']}' AND NPI='{billingprovider['NPI']}' AND TaxID='{billingprovider['TaxID']}'"
  cursor.execute(query)
  result = cursor.fetchall()
  if len(result) == 0:
    billingprovider_uuid = str(uuid.uuid4())
    query = f"INSERT INTO rebound_billingprovider(id, Type, Name, FirstName, LastName, AddressLine1, AddressLine2, City, State, ZipCode, NPI, TaxID) VALUES('{billingprovider_uuid}', '{billingprovider['Type']}', '{billingprovider['Name']}', '{billingprovider['FirstName']}', '{billingprovider['LastName']}', '{billingprovider['AddressLine1']}', '{billingprovider['AddressLine2']}', '{billingprovider['City']}', '{billingprovider['State']}', '{billingprovider['ZipCode']}', '{billingprovider['NPI']}', '{billingprovider['TaxID']}')"
    cursor.execute(query)
    return billingprovider_uuid
  else:
    return result[0][0]

def check_renderingprovider(renderingprovider):
  query = f"SELECT * FROM rebound_renderingprovider WHERE Type='{renderingprovider['Type']}' AND FirstName='{renderingprovider['FirstName']}' AND LastName='{renderingprovider['LastName']}' AND Name='{renderingprovider['Name']}' AND NPI='{renderingprovider['NPI']}'"
  cursor.execute(query)
  result = cursor.fetchall()
  if len(result) == 0:
    renderingprovider_uuid = str(uuid.uuid4())
    query = f"INSERT INTO rebound_renderingprovider(id, Type, FirstName, LastName, Name, NPI) VALUES('{renderingprovider_uuid}', '{renderingprovider['Type']}', '{renderingprovider['FirstName']}', '{renderingprovider['LastName']}', '{renderingprovider['Name']}', '{renderingprovider['NPI']}')"
    cursor.execute(query)
    return renderingprovider_uuid
  else:
    return result[0][0]


def add_837(claim):
  print(claim)
  patient_id = check_patient(claim['Patient'])
  payer_id = check_payer(claim['Payer'])
  billingprovider_id = check_billingprovider(claim['BillingProvider'])
  renderingprovider_id = check_renderingprovider(claim['RenderingProvider'])
  id = str(uuid.uuid4())
  diagnosis = ",".join(claim['Diagnosis'])
  services = ""
  for service in claim['Services']:
    if services != "":
      services += ","
    services += service['Code']
  query = f"INSERT INTO parsed_837(id, Patient, Payer, Diagnosis, Services, PatientAccountNumber, TotalClaimChargeAmount, AccidentDate, ServiceDate, MedicalRecordNumber, AuthNumber, BillingProvider, RenderingProvider) VALUES('{id}', '{patient_id}', '{payer_id}', '{diagnosis}', '{services}', '{claim['PatientAccountNumber']}', '{claim['TotalClaimChargeAmount']}', '{claim['AccidentDate']}', '{claim['ServiceDate']}', '{claim['MedicalRecordNumber']}', '{claim['AuthNumber']}', '{billingprovider_id}', '{renderingprovider_id}')"
  cursor.execute(query)
  mysql_conn.commit()

def check_payee(payee):
  query = f"SELECT * FROM rebound_payee WHERE Name='{payee['Name']}' AND NPI='{payee['NPI']}'"
  cursor.execute(query)
  result = cursor.fetchall()
  if len(result) == 0:
    payee_id = str(uuid.uuid4())
    query = f"INSERT INTO rebound_payee(id, Name, NPI) VALUES('{payee_id}', '{payee['Name']}', '{payee['NPI']}')"
    cursor.execute(query)
    return payee_id
  else:
    return result[0][0]

def add_835(claim):
  print(claim)
  services = ""
  for service in claim['Service']:
    services += service['Code'] + ":["
    for carc in service['CARC']:
      if services[-1] != '[':
        services += ","
      services += carc['GroupCode']+carc['Code']
    services += "],"
  services = services[:len(services)-1]
  payee_id = check_payee(claim['Payee'])
  id = str(uuid.uuid4())
  query = f"INSERT INTO parsed_835(id, TaxID, Service, NPI, PatientControlNumber, TotalClaimChargeNumber, ClaimPaymentAmount, ServiceDate, Payee) VALUES('{id}', '{claim['TaxID']}', '{services}', '{claim['NPI']}', '{claim['PatientControlNumber']}', '{claim['TotalClaimChargeAmount']}', '{claim['ClaimPaymentAmount']}', '{claim['ServiceDate']}', '{payee_id}')"
  cursor.execute(query)
  mysql_conn.commit()

if __name__ == '__main__':
  query = "DELETE FROM parsed_837"
  cursor.execute(query)
  query = "DELETE FROM parsed_835"
  cursor.execute(query)
  mysql_conn.commit()
  base_dir_837 = "C:/Users/DevOps/Documents/837/"
  base_dir_835 = "C:/Users/DevOps/Documents/835/"
  claims_837 = []
  claims_835 = []
  index_set_835 = {}
  index_set_837 = {}
  for file_name in os.listdir(base_dir_837):
    print(file_name)
    output = parse_837(base_dir_837+file_name)
    for claim in output['Claim']:
      add_837(claim)
  for file_name in os.listdir(base_dir_835):
    print(file_name)
    output = parse_835(base_dir_835+file_name)
    for claim in output['Claim']:
      add_835(claim)
  