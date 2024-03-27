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

def add_to_database_1(claim_837):
  query = f"SELECT * FROM rebound_claim WHERE PatientAccountNumber='{claim_837['PatientAccountNumber']}'"
  cursor.execute(query)
  result = cursor.fetchall()
  if len(result) == 1:
    return
  print(claim_837)
  patient_uuid = str(uuid.uuid4())
  query = f"""INSERT INTO rebound_patient(id, FirstName, LastName, MiddleName, Address, City, State, ZipCode, Birthday, Gender, SSN) VALUES("{patient_uuid}", "{claim_837['Patient']['FirstName']}", "{claim_837['Patient']['LastName']}", "{claim_837['Patient']['MiddleName']}", "{claim_837['Patient']['Address']}", "{claim_837['Patient']['City']}", "{claim_837['Patient']['State']}", "{claim_837['Patient']['ZipCode']}", "{claim_837['Patient']['Birthday']}", "{claim_837['Patient']['Gender']}", "{claim_837['Patient']['SSN']}")"""
  cursor.execute(query)
  payer_uuid = str(uuid.uuid4())
  query = f"INSERT INTO rebound_payer(id, Name, Payer_ID, Address, City, State, ZipCode) VALUES('{payer_uuid}', '{claim_837['Payer']['Name']}', '{claim_837['Payer']['ID']}', '{claim_837['Payer']['Address']}', '{claim_837['Payer']['City']}', '{claim_837['Payer']['State']}', '{claim_837['Payer']['ZipCode']}')"
  cursor.execute(query)
  claim_uuid = str(uuid.uuid4())
  query = f"INSERT INTO rebound_claim(id, Patient, Payer, PatientAccountNumber, TotalClaimChargeAmount, AccidentDate, ServiceDate, MedicalRecordNumber, TaxID, NPI, Type) VALUES('{claim_uuid}', '{patient_uuid}', '{payer_uuid}', '{claim_837['PatientAccountNumber']}', '{claim_837['TotalClaimChargeAmount']}', '{claim_837['AccidentDate']}', '{claim_837['ServiceDate']}', '{claim_837['MedicalRecordNumber']}', '{claim_837['TaxID']}', '{claim_837['NPI']}', 'ACTIVE')"
  cursor.execute(query)
  for diagnosis in claim_837['Diagnosis']:
    query = f"INSERT INTO rebound_diagnosis(id, Claim, Code) VALUES('{str(uuid.uuid4())}', '{claim_uuid}', '{diagnosis}')"
    cursor.execute(query)
  for i in range(len(claim_837['Services'])):
    service = claim_837['Services'][i]
    service_id = str(uuid.uuid4())
    query = f"INSERT INTO rebound_service(id, ClaimID, ChargeAmount, PaymentAmount, Units, ServiceDate, SourceID, Code, Modifier, Remark) VALUES('{service_id}', '{claim_uuid}', '{service['ChargeAmount']}', '{service['ChargeAmount']}', '{service['Units']}', '{service['ServiceDate']}', '{service['SourceID']}', '{service['Code']}', '{service['Modifier']}', '')"
    cursor.execute(query)
  mysql_conn.commit()


def add_to_database(claim_837, claim_835):
  query = f"SELECT * FROM rebound_claim WHERE PatientAccountNumber='{claim_837['PatientAccountNumber']}'"
  cursor.execute(query)
  result = cursor.fetchall()
  if len(result) == 1:
    return
  print(claim_837)
  # print(claim_837, claim_835)
  patient_uuid = str(uuid.uuid4())
  query = f"""INSERT INTO rebound_patient(id, FirstName, LastName, MiddleName, Address, City, State, ZipCode, Birthday, Gender, SSN) VALUES("{patient_uuid}", "{claim_837['Patient']['FirstName']}", "{claim_837['Patient']['LastName']}", "{claim_837['Patient']['MiddleName']}", "{claim_837['Patient']['Address']}", "{claim_837['Patient']['City']}", "{claim_837['Patient']['State']}", "{claim_837['Patient']['ZipCode']}", "{claim_837['Patient']['Birthday']}", "{claim_837['Patient']['Gender']}", "{claim_837['Patient']['SSN']}")"""
  cursor.execute(query)
  payer_uuid = str(uuid.uuid4())
  query = f"INSERT INTO rebound_payer(id, Name, Payer_ID, Address, City, State, ZipCode) VALUES('{payer_uuid}', '{claim_837['Payer']['Name']}', '{claim_837['Payer']['ID']}', '{claim_837['Payer']['Address']}', '{claim_837['Payer']['City']}', '{claim_837['Payer']['State']}', '{claim_837['Payer']['ZipCode']}')"
  cursor.execute(query)
  claim_uuid = str(uuid.uuid4())
  query = f"INSERT INTO rebound_claim(id, Patient, Payer, PatientAccountNumber, TotalClaimChargeAmount, AccidentDate, ServiceDate, MedicalRecordNumber, TaxID, NPI, Type) VALUES('{claim_uuid}', '{patient_uuid}', '{payer_uuid}', '{claim_837['PatientAccountNumber']}', '{claim_837['TotalClaimChargeAmount']}', '{claim_837['AccidentDate']}', '{claim_837['ServiceDate']}', '{claim_837['MedicalRecordNumber']}', '{claim_837['TaxID']}', '{claim_837['NPI']}', 'DENIED')"
  cursor.execute(query)
  for diagnosis in claim_837['Diagnosis']:
    query = f"INSERT INTO rebound_diagnosis(id, Claim, Code) VALUES('{str(uuid.uuid4())}', '{claim_uuid}', '{diagnosis}')"
    cursor.execute(query)
  for i in range(len(claim_837['Services'])):
    service = claim_837['Services'][i]
    service_id = str(uuid.uuid4())
    query = f"INSERT INTO rebound_service(id, ClaimID, ChargeAmount, PaymentAmount, Units, ServiceDate, SourceID, Code, Modifier, Remark) VALUES('{service_id}', '{claim_uuid}', '{service['ChargeAmount']}', '{claim_835['Service'][i]['PayAmount']}', '{service['Units']}', '{service['ServiceDate']}', '{service['SourceID']}', '{service['Code']}', '{service['Modifier']}', '{claim_835['Service'][i]['Remark']}')"
    cursor.execute(query)
    for carc in claim_835['Service'][i]['CARC']:
      query = f"INSERT INTO rebound_adjustment(id, ServiceID, GroupCode, Code, Amount) VALUES('{str(uuid.uuid4())}', '{service_id}', '{carc['GroupCode']}', '{carc['Code']}', '{carc['Amount']}')"
      cursor.execute(query)
  mysql_conn.commit()

if __name__ == '__main__':
  query = f"DELETE FROM rebound_adjustment;"
  cursor.execute(query)
  query = f"DELETE FROM rebound_claim;"
  cursor.execute(query)
  query = f"DELETE FROM rebound_diagnosis;"
  cursor.execute(query)
  query = f"DELETE FROM rebound_patient;"
  cursor.execute(query)
  query = f"DELETE FROM rebound_payer;"
  cursor.execute(query)
  query = f"DELETE FROM rebound_service;"
  cursor.execute(query)

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
      if claim['PatientAccountNumber'] in index_set_837:
        index_set_837[claim['PatientAccountNumber']].append(len(claims_837))
      else:
        index_set_837[claim['PatientAccountNumber']] = [len(claims_837)]
      claims_837.append(claim)
  for file_name in os.listdir(base_dir_835):
    print(file_name)
    output = parse_835(base_dir_835+file_name)
    for claim in output['Claim']:
      if claim['PatientControlNumber'] in index_set_835:
        index_set_835[claim['PatientControlNumber']].append(len(claims_835))
      else:
        index_set_835[claim['PatientControlNumber']] = [len(claims_835)]
      claims_835.append(claim)
  cnt = 0
  print('running...')
  print(len(claims_837), len(claims_835))
  # sys.exit()
  for i in range(len(claims_837)):
    if claims_837[i]['PatientAccountNumber'] in index_set_835:
      for ind in range(len(index_set_835[claims_837[i]['PatientAccountNumber']])):
        j = index_set_835[claims_837[i]['PatientAccountNumber']][ind]
        if claims_837[i]['PatientAccountNumber'] == claims_835[j]['PatientControlNumber']\
          and claims_837[i]['TotalClaimChargeAmount'] == claims_835[j]['TotalClaimChargeAmount']\
          and claims_837[i]['TaxID'] == claims_835[j]['TaxID']\
          and claims_837[i]['NPI'] == claims_835[j]['NPI']\
          and claims_837[i]['ServiceDate'] == claims_835[j]['ServiceDate']:
          k = 0
          if len(claims_837[i]['Services']) == len(claims_835[j]['Service']):
            while k < len(claims_837[i]['Services']):
              if claims_837[i]['Services'][k]['ChargeAmount'] != claims_835[j]['Service'][k]['ChargeAmount']\
                or claims_837[i]['Services'][k]['Code'] != claims_835[j]['Service'][k]['Code']\
                or claims_837[i]['Services'][k]['Modifier'] != claims_835[j]['Service'][k]['Modifier']:
                break
              k += 1
            if k == len(claims_837[i]['Services']):
              cnt += 1
              add_to_database(claims_837[i], claims_835[j])
              # print(claims_837[i], claims_835[j])
              print(cnt)
              break
      if ind == len(index_set_835[claims_837[i]['PatientAccountNumber']]):
        add_to_database_1(claims_837[i])
        cnt += 1
        print(cnt)
    else:
      add_to_database_1(claims_837[i])
      cnt += 1
      print(cnt)