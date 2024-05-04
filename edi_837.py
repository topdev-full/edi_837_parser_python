import sys
from datetime import datetime

def parse_837(file_name):
  output = {
    "Claim": []
  }
  first = True
  billingProvider = {
    "Type": "",
    "NPI": "",
    "TaxID": "",
    "Name": "",
    "FirstName": "",
    "LastName": "",
    "Address1": "",
    "Address2": "",
  }
  submitter = {
    'Type': '',
    'Name': '',
    'FirstName': '',
    'LastName': '',
    'ContactName': '',
    'ContactNumber': '',
    'ETIN': '',
  }
  receiver = {
    'Type': '',
    'Name': '',
    'FirstName': '',
    'LastName': '',
    'ETIN': '',
  }
  with open(file_name, "r") as file1:
    read_content = file1.read()
    segments = read_content.split('~')
    for i in range(len(segments)):
      segments[i] = segments[i].split('*')
      for j in range(len(segments[i])):
        if segments[i][j].find(':') != -1:
          segments[i][j] = segments[i][j].split(':')
    # print(segments)
    index = 0
    # loading header
    if segments[index][0] == 'ISA':
      index += 1
    if segments[index][0] == 'GS':
      index += 1
    
    # loading transaction set header
    if segments[index][0] == 'ST':
      index += 1
    if segments[index][0] == 'BHT':
      index += 1
      
    while segments[index][0] == 'NM1':
      if segments[index][1] == '41': # Submitter
        if segments[index][2] == '1':
          submitter['Type'] = 'INDIVIDUAL'
          submitter['FirstName'] = segments[index][4]
          submitter['LastName'] = segments[index][3]
        else:
          submitter['Type'] = 'BUSINESS'
          submitter['Name'] = segments[index][3]
        submitter['ETIN'] = segments[index][9]
        index += 1
        if segments[index][0] == 'PER':
          submitter['ContactName'] = segments[index][2]
          submitter['ContactNumber'] = segments[index][4]
          index += 1
      elif segments[index][1] == '40': # Receiver
        if segments[index][2] == '1':
          receiver['Type'] = 'INDIVIDUAL'
          receiver['FirstName'] = segments[index][4]
          receiver['LastName'] = segments[index][3]
        else:
          receiver['Type'] = 'BUSINESS'
          receiver['Name'] = segments[index][3]
        receiver['ETIN'] = segments[index][9]
        index += 1
      else:
        index += 1

    # loading billing provider hierarchical level
    while segments[index][0] == 'HL':
      # print(segments[index], index)
      if segments[index][2] == '':
        index += 1
        if segments[index][0] == 'PRV':
          index += 1
        while segments[index][0] == 'NM1':
          if segments[index][1] == '85': # Billing Provider
            if segments[index][2] == '2':
              billingProvider['Type'] = "BUSINESS"
              billingProvider['Name'] = segments[index][3]
            elif segments[index][2] == '1':
              billingProvider['Type'] = "INDIVIDUAL"
              billingProvider['FirstName'] = segments[index][4]
              billingProvider['LastName'] = segments[index][3]
            billingProvider['NPI'] = segments[index][9]
            index += 1
            if segments[index][0] == 'N3':
              billingProvider['Address1'] = segments[index][1]
              billingProvider['Address2'] = segments[index][2]
              index += 1
            if segments[index][0] == 'N4':
              billingProvider['City'] = segments[index][1]
              billingProvider['State'] = segments[index][2]
              billingProvider['ZipCode'] = segments[index][3]
              index += 1
            if segments[index][0] == 'REF':
              billingProvider['TaxID'] = segments[index][2]
              index += 1
          elif segments[index][1] == '87': # Pay To Address
            index += 1
            if segments[index][0] == 'N3':
              index += 1
            if segments[index][0] == 'N4':
              index += 1
      # loading subscriber hierarchical level
      if segments[index][0] == 'HL':
        output['Claim'].append({})
        output['Claim'][-1]['Patient'] = {
          "FirstName": '',
          "MiddleName": '',
          "LastName": '',
          "Address": '',
          "City": '',
          "State": '',
          "ZipCode": '',
          "Birthday": '',
          "Gender": '',
          "SSN": '',
          'RelationshipToSubscriber': '',
          'TaxID': '',
          'ID': '',
        }
        output['Claim'][-1]['PrimaryPayer'] = {
          'Name': '',
          'ID': '',
          'Address': '',
          'City': '',
          'State': '',
          'ZipCode': '',
          'Address': '',
        }
        output['Claim'][-1]['SecondaryPayer'] = {
          'Name': '',
          'ID': '',
          'Address': '',
          'City': '',
          'State': '',
          'ZipCode': '',
          'Address': '',
        }
        output['Claim'][-1]['PrimarySubscriber'] = {
          'Type': '',
          'FirstName': '',
          'LastName': '',
          'Name': '',
          'ID': '',
          'GroupName': '',
          'InsurancePlanType': '',
          'PayerSequence': '',
        }
        output['Claim'][-1]['SecondarySubscriber'] = {
          'Type': '',
          'FirstName': '',
          'LastName': '',
          'Name': '',
          'ID': '',
          'GroupName': '',
          'InsurancePlanType': '',
          'PayerSequence': '',
        }
        output['Claim'][-1]['ServiceFacility'] = {
          'Type': '',
          'FirstName': '',
          'LastName': '',
          'Name': '',
          'NPI': '',
          'Address1': '',
          'Address2': '',
          'City': '',
          'State': '',
          'ZipCode': '',
        }
        output['Claim'][-1]['SupervisingProvider'] = {
          'Type': '',
          'Name': '',
          'FirstName': '',
          'LastName': '',
          'NPI': '',
        }
        output['Claim'][-1]['RenderingProvider'] = {
          'Type': '',
          'FirstName': '',
          'LastName': '',
          'Name': '',
          'NPI': '',
          'Taxonomy': '',
          'Grouping': '',
        }
        output['Claim'][-1]['ReferringProvider'] = {
          'Type': '',
          'Name': '',
          'FirstName': '',
          'LastName': '',
          'NPI': '',
        }
        output['Claim'][-1]['Diagnosis'] = []
        output['Claim'][-1]['Services'] = []
        index += 1
      # loading PrimarySubscriber information
      if segments[index][0] == 'SBR':
        output['Claim'][-1]['PrimarySubscriber']['PayerSequence'] = segments[index][1]
        output['Claim'][-1]['PrimarySubscriber']['GroupName'] = segments[index][4]
        output['Claim'][-1]['PrimarySubscriber']['InsurancePlanType'] = segments[index][9]
        index += 1
      while segments[index][0] == 'NM1':
        if segments[index][1] == 'IL': # Insured Subscriber
          if segments[index][2] == '1':
            output['Claim'][-1]['PrimarySubscriber']['Type'] = 'INDIVIDUAL'
            output['Claim'][-1]['PrimarySubscriber']['FirstName'] = segments[index][4] if len(segments[index]) > 4 else ''
            output['Claim'][-1]['PrimarySubscriber']['MiddleName'] = segments[index][5] if len(segments[index]) > 5 else ''
            output['Claim'][-1]['PrimarySubscriber']['LastName'] = segments[index][3] if len(segments[index]) > 3 else ''
          else:
            output['Claim'][-1]['PrimarySubscriber']['Type'] = 'BUSINESS'
            output['Claim'][-1]['PrimarySubscriber']['Name'] = segments[index][3] if len(segments[index]) > 3 else ''
          index += 1
          if segments[index][0] == 'N3':
            output['Claim'][-1]['PrimarySubscriber']['Address'] = segments[index][1]
            index += 1
          if segments[index][0] == 'N4':
            output['Claim'][-1]['PrimarySubscriber']['City'] = segments[index][1]
            output['Claim'][-1]['PrimarySubscriber']['State'] = segments[index][2]
            output['Claim'][-1]['PrimarySubscriber']['ZipCode'] = segments[index][3]
            index += 1
          if segments[index][0] == 'DMG':
            output['Claim'][-1]['PrimarySubscriber']['Birthday'] = datetime.strptime(segments[index][2], "%Y%m%d")
            output['Claim'][-1]['PrimarySubscriber']['Gender'] = segments[index][3]
            index += 1
          if segments[index][0] == 'REF':
            index += 1
          if segments[index][0] == 'REF':
            index += 1
        elif segments[index][1] == 'PR': # Payer
          output['Claim'][-1]['PrimaryPayer']['Name'] = segments[index][3]
          output['Claim'][-1]['PrimaryPayer']['ID'] = segments[index][9]
          index += 1
          if segments[index][0] == 'N3':
            output['Claim'][-1]['PrimaryPayer']['Address'] = segments[index][1]
            index += 1
          if segments[index][0] == 'N4':
            output['Claim'][-1]['PrimaryPayer']['City'] = segments[index][1]
            output['Claim'][-1]['PrimaryPayer']['State'] = segments[index][2]
            output['Claim'][-1]['PrimaryPayer']['ZipCode'] = segments[index][3]
            index += 1
      # loading patient hierarchical level
      if segments[index][0] == 'HL':
        index += 1
      if segments[index][0] == 'PAT':
        index += 1
      
      # loading patient name
      if segments[index][0] == 'NM1':
        output['Claim'][-1]['Patient']['FirstName'] = segments[index][4]
        output['Claim'][-1]['Patient']['MiddleName'] = segments[index][5] if len(segments[index]) > 5 else ''
        output['Claim'][-1]['Patient']['LastName'] = segments[index][3]
        index += 1
      if segments[index][0] == 'N3':
        output['Claim'][-1]['Patient']['Address'] = segments[index][1]
        index += 1
      if segments[index][0] == 'N4':
        output['Claim'][-1]['Patient']['City'] = segments[index][1]
        output['Claim'][-1]['Patient']['State'] = segments[index][2]
        output['Claim'][-1]['Patient']['ZipCode'] = segments[index][3]
        index += 1
      if segments[index][0] == 'DMG':
        output['Claim'][-1]['Patient']['Birthday'] = datetime.strptime(segments[index][2], "%Y%m%d")
        output['Claim'][-1]['Patient']['Gender'] = segments[index][3]
        index += 1
      if segments[index][0] == 'REF':
        index += 1
      if segments[index][0] == 'REF':
        output['Claim'][-1]['Patient']['TaxID'] = segments[index][2]
        index += 1
      
      # loading claim information
      if segments[index][0] == 'CLM':
        output['Claim'][-1]['PatientAccountNumber'] = segments[index][1]
        output['Claim'][-1]['TotalClaimChargeAmount'] = float(segments[index][2])
        output['Claim'][-1]['AccidentDate'] = '1900-01-01'
        output['Claim'][-1]['ServiceDate'] = '1900-01-01'
        output['Claim'][-1]['MedicalRecordNumber'] = 'N/A'
        output['Claim'][-1]['AuthNumber'] = 'N/A'
        output['Claim'][-1]['ContractCode'] = 'N/A'
        output['Claim'][-1]['PolicyNumber'] = 'N/A'
        index += 1
        while segments[index][0] == 'DTP':
          if segments[index][1] == '439':
            output['Claim'][-1]['AccidentDate'] = datetime.strptime(segments[index][3], "%Y%m%d")
          elif segments[index][1] == '435':
            output['Claim'][-1]['AdmissionDate'] = datetime.strptime(segments[index][3], "%Y%m%d")
          index += 1
        while segments[index][0] == 'PWK':
          index += 1
        while segments[index][0] == 'REF':
          if segments[index][1] == 'G1':
            output['Claim'][-1]['AuthNumber'] = segments[index][2]
          elif segments[index][1] == 'EA':
            output['Claim'][-1]['MedicalRecordNumber'] = segments[index][2]
          elif segments[index][1] == 'CE':
            output['Claim'][-1]['ContractCode'] = segments[index][2]
          elif segments[index][1] == '1L':
            output['Claim'][-1]['PolicyNumber'] = segments[index][2]
          index += 1
        while segments[index][0] == 'NTE':
          index += 1
        while segments[index][0] == 'HI':
          ind = 1
          while len(segments[index]) > ind:
            output['Claim'][-1]['Diagnosis'].append({
              'Type': segments[index][ind][0],
              'Code': segments[index][ind][1],
            })
            ind += 1
          index += 1
        
        # loading rendering provider name
        # print('provider', segments[index], index)
        while segments[index][0] == 'NM1':
          if segments[index][1] == 'DN': # referring provider
            if segments[index][2] == '1':
              output['Claim'][-1]['ReferringProvider']['Type'] = 'INDIVIDUAL'
              output['Claim'][-1]['ReferringProvider']['FirstName'] = segments[index][4]
              output['Claim'][-1]['ReferringProvider']['LastName'] = segments[index][3]
            else:
              output['Claim'][-1]['ReferringProvider']['Type'] = 'BUSINESS'
              output['Claim'][-1]['ReferringProvider']['Name'] = segments[index][3]
            output['Claim'][-1]['ReferringProvider']['NPI'] = segments[index][9]
            index += 1
          elif segments[index][1] == '82': # rendering provider
            if segments[index][2] == '1':
              output['Claim'][-1]['RenderingProvider']['Type'] = 'INDIVIDUAL'
              output['Claim'][-1]['RenderingProvider']['FirstName'] = segments[index][4]
              output['Claim'][-1]['RenderingProvider']['LastName'] = segments[index][3]
            else:
              output['Claim'][-1]['RenderingProvider']['Type'] = 'BUSINESS'
              output['Claim'][-1]['RenderingProvider']['Name'] = segments[index][3]
            output['Claim'][-1]['RenderingProvider']['NPI'] = segments[index][9]
            index += 1
            if segments[index][0] == 'PRV':
              output['Claim'][-1]['RenderingProvider']['Taxonomy'] = segments[index][3]
              index += 1
          elif segments[index][1] == '77': # service facility location
            if segments[index][2] == '1':
              output['Claim'][-1]['ServiceFacility']['Type'] = 'INDIVIDUAL'
              output['Claim'][-1]['ServiceFacility']['FirstName'] = segments[index][4]
              output['Claim'][-1]['ServiceFacility']['LastName'] = segments[index][3]
            else:
              output['Claim'][-1]['ServiceFacility']['Type'] = 'BUSINESS'
              output['Claim'][-1]['ServiceFacility']['Name'] = segments[index][3]
            output['Claim'][-1]['ServiceFacility']['NPI'] = segments[index][9]
            index += 1
            if segments[index][0] == 'N3':
              output['Claim'][-1]['ServiceFacility']['Address1'] = segments[index][1]
              if len(segments[index]) > 2:
                output['Claim'][-1]['ServiceFacility']['Address2'] = segments[index][2]
              index += 1
            if segments[index][0] == 'N4':
              output['Claim'][-1]['ServiceFacility']['City'] = segments[index][1]
              output['Claim'][-1]['ServiceFacility']['State'] = segments[index][2]
              output['Claim'][-1]['ServiceFacility']['ZipCode'] = segments[index][3]
              index += 1
            if segments[index][0] == 'REF':
              index += 1
          elif segments[index][1] == 'DQ': # supervising provider name
            if segments[index][2] == '1':
              output['Claim'][-1]['SupervisingProvider']['Type'] = 'INDIVIDUAL'
              output['Claim'][-1]['SupervisingProvider']['FirstName'] = segments[index][4]
              output['Claim'][-1]['SupervisingProvider']['LastName'] = segments[index][3]
            else:
              output['Claim'][-1]['SupervisingProvider']['Type'] = 'BUSINESS'
              output['Claim'][-1]['SupervisingProvider']['Name'] = segments[index][3]
            output['Claim'][-1]['SupervisingProvider']['NPI'] = segments[index][9]
            index += 1
          else:
            index += 1
        while segments[index][0] == 'SBR':
          index += 1
          if segments[index][0] == 'AMT':
            index += 1
          if segments[index][0] == 'OI':
            index += 1
          while segments[index][0] == 'NM1':
            if segments[index][1] == 'PR':
              if segments[index][2] == '1':
                output['Claim'][-1]['SecondaryPayer']['Type'] = 'INDIVIDUAL'
                output['Claim'][-1]['SecondaryPayer']['FirstName'] = segments[index][4]
                output['Claim'][-1]['SecondaryPayer']['LastName'] = segments[index][3]
                output['Claim'][-1]['SecondaryPayer']['MiddleName'] = segments[index][5]
              else:
                output['Claim'][-1]['SecondaryPayer']['Type'] = 'BUSINESS'
                output['Claim'][-1]['SecondaryPayer']['Name'] = segments[index][3]
              output['Claim'][-1]['SecondaryPayer']['ID'] = segments[index][9]
              index += 1
              if segments[index][0] == 'REF':
                index += 1
            elif segments[index][1] == 'IL':
              if segments[index][2] == '1':
                output['Claim'][-1]['SecondarySubscriber']['Type'] = 'INDIVIDUAL'
                output['Claim'][-1]['SecondarySubscriber']['FirstName'] = segments[index][4]
                output['Claim'][-1]['SecondarySubscriber']['LastName'] = segments[index][3]
                output['Claim'][-1]['SecondarySubscriber']['MiddleName'] = segments[index][5]
              else:
                output['Claim'][-1]['SecondarySubscriber']['Type'] = 'BUSINESS'
                output['Claim'][-1]['SecondarySubscriber']['Type'] = segments[index][3]
              index += 1
              if segments[index][0] == 'N3':
                output['Claim'][-1]['SecondarySubscriber']['Address'] = segments[index][1]
                index += 1
              if segments[index][0] == 'N4':
                output['Claim'][-1]['SecondarySubscriber']['City'] = segments[index][1]
                output['Claim'][-1]['SecondarySubscriber']['State'] = segments[index][2]
                output['Claim'][-1]['SecondarySubscriber']['ZipCode'] = segments[index][3]
                index += 1
            else:
              index += 1
          
        # loading service line
        while segments[index][0] == 'LX':
          output['Claim'][-1]['Services'].append({
            'ChargeAmount': '',
            'Units': '',
            'ServiceDate': '',
            'SourceID': '',
            'Code': '',
            'Modifier': '',
          })
          # print(segments[index])
          index += 1
          if segments[index][0] == 'SV1':
            output['Claim'][-1]['Services'][-1]['ChargeAmount'] = float(segments[index][2])
            output['Claim'][-1]['Services'][-1]['Units'] = segments[index][4]
            output['Claim'][-1]['Services'][-1]['Code'] = segments[index][1][1]
            output['Claim'][-1]['Services'][-1]['Modifier'] = segments[index][1][2] if len(segments[index][1]) > 2 else ''
            output['Claim'][-1]['Services'][-1]['ProviderDescription'] = segments[index][1][6] if len(segments[index][1]) > 6 else ''
            index += 1
          if segments[index][0] == 'DTP':
            if segments[index][2] == 'D8':
              output['Claim'][-1]['Services'][-1]['ServiceDate'] = output['Claim'][-1]['ServiceDate'] = datetime.strptime(segments[index][3], "%Y%m%d")
            elif segments[index][2] == 'RD8':
              output['Claim'][-1]['Services'][-1]['ServiceDate'] = output['Claim'][-1]['ServiceDate'] = datetime.strptime(segments[index][3].split('-')[-1], "%Y%m%d")
            index += 1
          if segments[index][0] == 'REF':
            output['Claim'][-1]['Services'][-1]['SourceID'] = segments[index][2]
            index += 1
          if segments[index][0] == 'NM1':
            index += 1
          if segments[index][0] == 'N3':
            index += 1
          if segments[index][0] == 'N4':
            index += 1
          if segments[index][0] == 'NTE':
            index += 1
            if segments[index][0] == 'NM1':
              index += 1
            if segments[index][0] == 'N3':
              index += 1
            if segments[index][0] == 'N4':
              index += 1
          while segments[index][0] == 'LIN':
            index += 1
            if segments[index][0] == 'CTP':
              index += 1
              if segments[index][0] == 'NM1':
                index += 1
              if segments[index][0] == 'N3':
                index += 1
              if segments[index][0] == 'N4':
                index += 1
          while segments[index][0] == 'SVD':
            index += 1
            while segments[index][0] == 'CAS':
              index += 1
            if segments[index][0] == 'DTP':
              index += 1
      # print(output['Claim'][-1])
      if output['Claim'][-1]['AccidentDate'] == "":
        output['Claim'][-1]['AccidentDate'] = output['Claim'][-1]['ServiceDate']
      output['Claim'][-1]['BillingProvider'] = billingProvider
      output['Claim'][-1]['Submitter'] = submitter
      output['Claim'][-1]['Receiver'] = receiver
    
    if segments[index][0] == 'SE':
      # print(segments[index])
      index += 1
    if segments[index][0] == 'GE':
      index += 1
    if segments[index][0] == 'IEA':
      index += 1
  # print(output['Claim'], len(output['Claim']))
  # for claim in output['Claim']:
    # print(claim['PatientAccountNumber'])
  # return len(output['Claim'])
  return output

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print("Command Error")
    exit()
  file_name = sys.argv[1]
  print(parse_837(file_name)['Claim'][0])