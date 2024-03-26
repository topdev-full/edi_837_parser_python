import sys
from datetime import datetime
from utils import eat_space

def parse_835(file_name):
  output = {
    "Claim": []
  }
  first = True
  payee = {}
  payer = {}
  with open(file_name, "r") as file1:
    read_content = file1.read()
    segments = read_content.split('~')
    for i in range(len(segments)):
      segments[i] = segments[i].split('*')
      for j in range(len(segments[i])):
        if segments[i][j].find(':') != -1:
          segments[i][j] = segments[i][j].split(':')
          for k in range(len(segments[i][j])):
            segments[i][j][k] = eat_space(segments[i][j][k], " \n")
        else:
          segments[i][j] = eat_space(segments[i][j], " \n")
    index = 0
    # print(segments)
    if segments[index][0] == 'ISA':
      index += 1
    if segments[index][0] == 'GS':
      index += 1
    # transaction set header
    if segments[index][0] == 'ST':
      index += 1
    if segments[index][0] == 'BPR':
      index += 1
    if segments[index][0] == 'TRN':
      index += 1
    while segments[index][0] == 'REF':
      index += 1
    if segments[index][0] == 'DTM':
      index += 1
    
    # payer identification
    if segments[index][0] == 'N1':
      payer['Name'] = segments[index][2]
      index += 1
    if segments[index][0] == 'N3':
      payer['Address'] = segments[index][1]
      index += 1
    if segments[index][0] == 'N4':
      payer['City'] = segments[index][1]
      payer['State'] = segments[index][2]
      payer['ZipCode'] = segments[index][3]
      index += 1
    while segments[index][0] == 'REF':
      index += 1
    while segments[index][0] == 'PER':
      index += 1
      
    # payee identification
    if segments[index][0] == 'N1':
      payee['Name'] = segments[index][2]
      payee['NPI'] = segments[index][4]
      index += 1
    if segments[index][0] == 'N3':
      payee['Address'] = segments[index][1]
      index += 1
    if segments[index][0] == 'N4':
      payee['City'] = segments[index][1]
      payee['State'] = segments[index][2]
      payee['ZipCode'] = segments[index][3]
      index += 1
    while segments[index][0] == 'REF':
      if segments[index][1] == 'TJ':
        payee['TaxID'] = segments[index][2]
      index += 1
    
    while segments[index][0] == 'LX':
      index += 1
      if segments[index][0] == 'TS3':
        index += 1
      while segments[index][0] == 'CLP':  
        # print(segments[index])
        output['Claim'].append({})
        output['Claim'][-1]['TaxID'] = payee['TaxID'] if "TaxID" in payee else None
        output['Claim'][-1]['Service'] = []
        output['Claim'][-1]['NPI'] = payee['NPI'] if "NPI" in payee else None
        output['Claim'][-1]['PatientControlNumber'] = segments[index][1]
        output['Claim'][-1]['TotalClaimChargeAmount'] = float(segments[index][3])
        output['Claim'][-1]['ClaimPaymentAmount'] = float(segments[index][4])
        output['Claim'][-1]['ServiceDate'] = None
        output['Claim'][-1]['Payer'] = payer
        output['Claim'][-1]['Payee'] = payee
        index += 1
        while segments[index][0] == 'CAS':
          index += 1
        while segments[index][0] == 'NM1':
          index += 1
        while segments[index][0] == 'MOA':
          index += 1
        while segments[index][0] == 'MIA':
          index += 1
        while segments[index][0] == 'REF':
          index += 1
        first = True
        while segments[index][0] == 'DTM':
          if first:
            output['Claim'][-1]['ServiceDate'] = datetime.strptime(segments[index][2], "%Y%m%d")
            first = False
          index += 1
        while segments[index][0] == 'PER':
          index += 1
        while segments[index][0] == 'AMT':
          index += 1
        while segments[index][0] == 'SVC':
          output['Claim'][-1]['Service'].append({
            "Code": segments[index][1][1],
            "Modifier": segments[index][1][2] if len(segments[index][1]) > 2 else "",
            "ChargeAmount": float(segments[index][2]),
            "PayAmount": float(segments[index][3]),
            "CARC": [],
            "Remark": ""
          })
          index += 1
          while segments[index][0] == 'DTM':
            output['Claim'][-1]['ServiceDate'] = datetime.strptime(segments[index][2], "%Y%m%d")
            index += 1
          while segments[index][0] == 'CAS':
            # print(segments[index])
            ind = 1
            groupCode = ""
            while ind + 2 < len(segments[index]):
              if segments[index][ind] != "":
                groupCode = segments[index][ind]
              output['Claim'][-1]['Service'][-1]['CARC'].append({
                "GroupCode": groupCode,
                "Code": segments[index][ind+1],
                "Amount": float(segments[index][ind+2])
              })
              ind += 3
            index += 1
          while segments[index][0] == 'REF':
            index += 1
          while segments[index][0] == 'AMT':
            # print(segments[index])
            index += 1
          while segments[index][0] == 'LQ':
            output['Claim'][-1]['Service'][-1]['Remark'] = segments[index][2]
            index += 1
    if segments[index][0] == 'SE':
      index += 1
    # print(output['Claim'], len(output['Claim']))
    # return len(output['Claim'])
    return output

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print("Command Error")
    exit()
  file_name = sys.argv[1]
  print(parse_835(file_name))