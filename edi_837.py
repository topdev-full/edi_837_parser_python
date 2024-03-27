import sys
from datetime import datetime

def parse_837(file_name):
  output = {
    "Claim": []
  }
  first = True
  billingProvider = {}
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
      
    # loading submitter
    if segments[index][0] == 'NM1':
      index += 1
    if segments[index][0] == 'PER':
      index += 1
    
    # loading receiver
    if segments[index][0] == 'NM1':
      index += 1
    
    # loading billing provider hierarchical level
    while segments[index][0] == 'HL':
      # print(segments[index], index)
      if segments[index][2] == '':
        index += 1
        if segments[index][0] == 'PRV':
          index += 1
        # loading billing provider name
        if segments[index][0] == 'NM1':
          billingProvider['NPI'] = segments[index][9]
          index += 1
        if segments[index][0] == 'N3':
          index += 1
        if segments[index][0] == 'N4':
          index += 1
        if segments[index][0] == 'REF':
          billingProvider['TaxID'] = segments[index][2]
          index += 1
        
        # loading pay to address name
        if segments[index][0] == 'NM1':
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
        }
        output['Claim'][-1]['Payer'] = {
          'Name': '',
          'ID': '',
          'Address': '',
          'City': '',
          'State': '',
          'ZipCode': '',
          'Address': '',
        }
        output['Claim'][-1]['Diagnosis'] = []
        output['Claim'][-1]['Services'] = []
        index += 1
      # loading subscriber information
      if segments[index][0] == 'SBR':
        index += 1
      if segments[index][0] == 'NM1':
        if segments[index][2] == '1':
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
        index += 1
      if segments[index][0] == 'NM1':
        output['Claim'][-1]['Payer']['Name'] = segments[index][3]
        output['Claim'][-1]['Payer']['ID'] = segments[index][9]
        index += 1
      if segments[index][0] == 'N3':
        output['Claim'][-1]['Payer']['Address'] = segments[index][1]
        index += 1
      if segments[index][0] == 'N4':
        output['Claim'][-1]['Payer']['City'] = segments[index][1]
        output['Claim'][-1]['Payer']['State'] = segments[index][2]
        output['Claim'][-1]['Payer']['ZipCode'] = segments[index][3]
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
        index += 1
      
      # loading claim information
      if segments[index][0] == 'CLM':
        output['Claim'][-1]['NPI'] = billingProvider['NPI']
        output['Claim'][-1]['TaxID'] = billingProvider['TaxID']
        output['Claim'][-1]['PatientAccountNumber'] = segments[index][1]
        output['Claim'][-1]['TotalClaimChargeAmount'] = float(segments[index][2])
        output['Claim'][-1]['AccidentDate'] = '1900-01-01'
        output['Claim'][-1]['ServiceDate'] = '1900-01-01'
        output['Claim'][-1]['MedicalRecordNumber'] = ''
        index += 1
        first = True
        while segments[index][0] == 'DTP':
          if first:
            output['Claim'][-1]['AccidentDate'] = datetime.strptime(segments[index][3], "%Y%m%d")
            first = False
          index += 1
        while segments[index][0] == 'PWK':
          index += 1
        while segments[index][0] == 'REF':
          output['Claim'][-1]['MedicalRecordNumber'] = segments[index][2]
          index += 1
        while segments[index][0] == 'NTE':
          index += 1
        while segments[index][0] == 'HI':
          ind = 1
          while len(segments[index]) > ind:
            output['Claim'][-1]['Diagnosis'].append(segments[index][ind][1])
            ind += 1
          index += 1
        
        # loading rendering provider name
        # print('provider', segments[index], index)
        while segments[index][0] == 'NM1':
          if segments[index][1] == 'DN': # referring provider
            index += 1
          elif segments[index][1] == '82': # rendering provider
            index += 1
            if segments[index][0] == 'PRV':
              index += 1
          elif segments[index][1] == '77': # service facility location
            index += 1
            if segments[index][0] == 'N3':
              index += 1
            if segments[index][0] == 'N4':
              index += 1
            if segments[index][0] == 'REF':
              index += 1
          elif segments[index][1] == 'DQ': # supervising provider name
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
            # print(segments[index], 'NM1')
            if segments[index][1] == 'PR':
              index += 1
              if segments[index][0] == 'REF':
                index += 1
            elif segments[index][1] == 'IL':
              index += 1
              if segments[index][0] == 'N3':
                index += 1
              if segments[index][0] == 'N4':
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
  print(parse_837(file_name))