import sys
import os
from edi_835 import parse_835
from edi_837 import parse_837
import sqlite3
import uuid

con = sqlite3.connect("db.db")

# if __name__ == '__main__':
#   dir_835 = sys.argv[1]
#   dir_837 = sys.argv[2]
#   for file_name in os.listdir(dir_835):
#     parsed_835 = parse_835(dir_835 + '\\' + file_name)
#     for Claim_835 in parsed_835['Claim']:
#       for file_name1 in os.listdir(dir_837):
#         parsed_837 = parse_837(dir_837 + '\\' + file_name1)
#         for Claim_837 in parsed_837['Claim']:
#           if Claim_835['TotalClaimChargeAmount'] == Claim_837['TotalClaimChargeAmount'] \
#             and Claim_835['PatientControlNumber'] == Claim_837['PatientAccountNumber'] \
#             and Claim_835['TaxID'] == Claim_837['TaxID'] \
#             and Claim_835['NPI'] == Claim_837['NPI'] \
#             and Claim_835['ServiceDate'] == Claim_837['ServiceDate']:
#             print(Claim_835, Claim_837)

# if __name__ == '__main__':
#   dir_835 = sys.argv[1]
#   dir_837 = sys.argv[2]
#   cur = con.cursor()
#   for file_name in os.listdir(dir_835):
#     parsed_835 = parse_835(dir_835 + '\\' + file_name)
#     for Claim_835 in parsed_835['Claim']:
#       print(file_name)
#       print(Claim_835)
#       query = f"INSERT INTO edi_835(id, TotalClaimChargeAmount, PatientControlNumber, TaxID, NPI, ServiceDate) VALUES('{str(uuid.uuid4())}', {Claim_835['TotalClaimChargeAmount']}, '{Claim_835['PatientControlNumber']}', '{Claim_835['TaxID']}', '{Claim_835['NPI']}', '{Claim_835['ServiceDate']}')"
#       print(query)
#       cur.execute(query)
#     con.commit()
    
# if __name__ == '__main__':
#   dir_835 = sys.argv[1]
#   dir_837 = sys.argv[2]
#   cur = con.cursor()
#   for file_name in os.listdir(dir_837):
#     parsed_837 = parse_835(dir_837 + '\\' + file_name)
#     for Claim_837 in parsed_835['Claim']:
#       print(file_name)
#       print(Claim_837)
#       query = f"INSERT INTO edi_835(id, TotalClaimChargeAmount, PatientControlNumber, TaxID, NPI, ServiceDate) VALUES('{str(uuid.uuid4())}', {Claim_835['TotalClaimChargeAmount']}, '{Claim_835['PatientControlNumber']}', '{Claim_835['TaxID']}', '{Claim_835['NPI']}', '{Claim_835['ServiceDate']}')"
#       print(query)
#       cur.execute(query)
#     con.commit()

if __name__ == '__main__':
  dir_835 = sys.argv[1]
  dir_837 = sys.argv[2]
  cur = con.cursor()
  for file_name in os.listdir(dir_835):
    parsed_835 = parse_835(dir_835 + '\\' + file_name)
    for Claim_835 in parsed_835['Claim']:
      print(file_name)
      print(Claim_835)
      query = f"INSERT INTO edi_835(id, TotalClaimChargeAmount, PatientControlNumber, TaxID, NPI, ServiceDate) VALUES('{str(uuid.uuid4())}', {Claim_835['TotalClaimChargeAmount']}, '{Claim_835['PatientControlNumber']}', '{Claim_835['TaxID']}', '{Claim_835['NPI']}', '{Claim_835['ServiceDate']}')"
      print(query)
      cur.execute(query)
    con.commit()