import sys
from datetime import datetime
from utils import eat_space

def parse_835(file_name):
  output = {
    "Claim": []
  }
  payee = {
    'Name': '',
    'IDType': '',
    'NPI': '',
    'MemberID': '',
    'Address': '',
    'City': '',
    'State': '',
    'ZipCode': '',
    'TaxID': '',
  }
  payer = {
    'Name': '',
    'Address': '',
    'City': '',
    'State': '',
    'ZipCode': '',
    'ID': '',
    'ContactName': '',
    'ContactNumber': '',
  }
  productionDate = ''
  paymentDate = ''
  trackNumber = ''
  payerIdentifier = ''
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
      paymentDate = datetime.strptime(segments[index][16], "%Y%m%d")
      index += 1
    if segments[index][0] == 'TRN':
      trackNumber = segments[index][2]
      payerIdentifier = segments[index][3]
      index += 1
    while segments[index][0] == 'REF':
      index += 1
    if segments[index][0] == 'DTM':
      if segments[index][1] == '405':
        productionDate = datetime.strptime(segments[index][2], "%Y%m%d")
      index += 1
    
    # payer identification
    while segments[index][0] == 'N1':
      if segments[index][1] == 'PR':
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
          if segments[index][1] == '2U':
            payer['ID'] = segments[index][2]
          index += 1
        while segments[index][0] == 'PER':
          if segments[index][1] == 'CX':
            payer['ContactName'] = segments[index][2]
            pass
          elif segments[index][1] == 'BL':
            pass
          if segments[index][3] == 'TE':
            payer['ContactNumber'] = segments[index][4]
          elif segments[index][3] == 'UR':
            pass
          index += 1
      elif segments[index][1] == 'PE':
        payee['Name'] = segments[index][2]
        if segments[index][3] == 'XX':
          payee['IDType'] = 'NPI'
          payee['NPI'] = segments[index][4]
        elif segments[index][3] == 'MI':
          payee['IDType'] = 'MemberID'
          payee['MemberID'] = segments[index][4]
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
        output['Claim'][-1]['Patient'] = {
          'Type': '',
          'Name': '',
          'FirstName': '',
          'LastName': '',
          'MiddleName': '',
          'IDType': '',
          'MemberID': '',
          'NPI': '',
        }
        output['Claim'][-1]['InsuredSubscriber'] = {
          'Type': '',
          'Name': '',
          'FirstName': '',
          'LastName': '',
          'MiddleName': '',
          'IDType': '',
          'MemberID': '',
          'NPI': '',
        }
        output['Claim'][-1]['RenderingProvider'] = {
          'Type': '',
          'Name': '',
          'FirstName': '',
          'LastName': '',
          'MiddleName': '',
          'IDType': '',
          'MemberID': '',
          'NPI': '',
        }
        output['Claim'][-1]['PayerClaimControlNumber'] = segments[index][7]
        output['Claim'][-1]['Service'] = []
        output['Claim'][-1]['PatientControlNumber'] = segments[index][1]
        output['Claim'][-1]['TotalClaimChargeAmount'] = float(segments[index][3])
        output['Claim'][-1]['ClaimPaymentAmount'] = float(segments[index][4])
        output['Claim'][-1]['PatientResponsibilityAmount'] = float(segments[index][5]) if segments[index][5] != '' else 0
        output['Claim'][-1]['ProductionDate'] = productionDate
        output['Claim'][-1]['PaymentDate'] = paymentDate
        output['Claim'][-1]['TrackNumber'] = trackNumber
        output['Claim'][-1]['PayerIdentifier'] = payerIdentifier
        output['Claim'][-1]['Payer'] = payer
        output['Claim'][-1]['Payee'] = payee
        output['Claim'][-1]['ContractCode'] = ''
        output['Claim'][-1]['MedicalRecordNumber'] = ''
        output['Claim'][-1]['PolicyNumber'] = ''
        output['Claim'][-1]['PeriodStart'] = ''
        output['Claim'][-1]['PeriodEnd'] = ''
        output['Claim'][-1]['ReceiveDate'] = ''
        index += 1
        while segments[index][0] == 'CAS':
          index += 1
        while segments[index][0] == 'NM1':
          if segments[index][1] == 'QC':
            if segments[index][2] == '1':
              output['Claim'][-1]['Patient']['Type'] = 'INDIVIDUAL'
              output['Claim'][-1]['Patient']['FirstName'] = segments[index][4] if len(segments[index]) > 4 else ''
              output['Claim'][-1]['Patient']['LastName'] = segments[index][3] if len(segments[index]) > 3 else ''
              output['Claim'][-1]['Patient']['MiddleName'] = segments[index][5] if len(segments[index]) > 5 else ''
            else:
              output['Claim'][-1]['Patient']['Type'] = 'BUSINESS'
              output['Claim'][-1]['Patient']['Name'] = segments[index][3] if len(segments[index]) > 3 else ''
            if len(segments[index]) > 8:
              if segments[index][8] == 'XX':
                output['Claim'][-1]['Patient']['IDType'] = 'NPI'
                output['Claim'][-1]['Patient']['NPI'] = segments[index][9]
              elif segments[index][8] == 'MI':
                output['Claim'][-1]['Patient']['IDType'] = 'MemberID'
                output['Claim'][-1]['Patient']['MemberID'] = segments[index][9]
          elif segments[index][1] == 'IL':
            if segments[index][2] == '1':
              output['Claim'][-1]['InsuredSubscriber']['Type'] = 'INDIVIDUAL'
              output['Claim'][-1]['InsuredSubscriber']['FirstName'] = segments[index][4] if len(segments[index]) > 4 else ''
              output['Claim'][-1]['InsuredSubscriber']['LastName'] = segments[index][3] if len(segments[index]) > 3 else ''
              output['Claim'][-1]['InsuredSubscriber']['MiddleName'] = segments[index][5] if len(segments[index]) > 5 else ''
            else:
              output['Claim'][-1]['InsuredSubscriber']['Type'] = 'BUSINESS'
              output['Claim'][-1]['InsuredSubscriber']['Name'] = segments[index][3] if len(segments[index]) > 3 else ''
            if len(segments[index]) > 8:
              if segments[index][8] == 'XX':
                output['Claim'][-1]['InsuredSubscriber']['IDType'] = 'NPI'
                output['Claim'][-1]['InsuredSubscriber']['NPI'] = segments[index][9]
              elif segments[index][8] == 'MI':
                output['Claim'][-1]['InsuredSubscriber']['IDType'] = 'MemberID'
                output['Claim'][-1]['InsuredSubscriber']['MemberID'] = segments[index][9]
          elif segments[index][1] == '82':
            if segments[index][2] == '1':
              output['Claim'][-1]['RenderingProvider']['Type'] = 'INDIVIDUAL'
              output['Claim'][-1]['RenderingProvider']['FirstName'] = segments[index][4] if len(segments[index]) > 4 else ''
              output['Claim'][-1]['RenderingProvider']['LastName'] = segments[index][3] if len(segments[index]) > 3 else ''
              output['Claim'][-1]['RenderingProvider']['MiddleName'] = segments[index][5] if len(segments[index]) > 5 else ''
            else:
              output['Claim'][-1]['RenderingProvider']['Type'] = 'BUSINESS'
              output['Claim'][-1]['RenderingProvider']['Name'] = segments[index][3] if len(segments[index]) > 3 else ''
            if len(segments[index]) > 8:
              if segments[index][8] == 'XX':
                output['Claim'][-1]['RenderingProvider']['IDType'] = 'NPI'
                output['Claim'][-1]['RenderingProvider']['NPI'] = segments[index][9]
              elif segments[index][8] == 'MI':
                output['Claim'][-1]['RenderingProvider']['IDType'] = 'MemberID'
                output['Claim'][-1]['RenderingProvider']['MemberID'] = segments[index][9]
          index += 1
        while segments[index][0] == 'MOA':
          index += 1
        while segments[index][0] == 'MIA':
          index += 1
        while segments[index][0] == 'REF':
          if segments[index][1] == 'CE':
            output['Claim'][-1]['ContractCode'] = segments[index][2]
          elif segments[index][1] == 'EA':
            output['Claim'][-1]['MedicalRecordNumber'] = segments[index][2]
          elif segments[index][1] == '1L':
            output['Claim'][-1]['PolicyNumber'] = segments[index][2]
          index += 1
        while segments[index][0] == 'DTM':
          if segments[index][1] == '232':
            output['Claim'][-1]['PeriodStart'] = datetime.strptime(segments[index][2], "%Y%m%d")
          elif segments[index][1] == '233':
            output['Claim'][-1]['PeriodEnd'] = datetime.strptime(segments[index][2], "%Y%m%d")
          elif segments[index][1] == '050':
            output['Claim'][-1]['ReceiveDate'] = datetime.strptime(segments[index][2], "%Y%m%d")
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
            "Remark": "",
            "Date": "",
          })
          index += 1
          while segments[index][0] == 'DTM':
            if segments[index][1] == '472':
              output['Claim'][-1]['Service'][-1]['Date'] = datetime.strptime(segments[index][2], "%Y%m%d")
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
  print(parse_835(file_name)['Claim'][0])