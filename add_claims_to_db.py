import mysql.connector
import uuid
from settings import *

mysql_conn = mysql.connector.connect(
  host=MYSQL_HOST,
  user=MYSQL_USER,
  password=MYSQL_PASSWORD,
  database=MYSQL_DB
)

cursor = mysql_conn.cursor(dictionary=True)

matching_query = "INSERT INTO matching_837_835 VALUES "
claim_query = "INSERT INTO rebound_claim VALUES "
service_query = "INSERT INTO rebound_service VALUES "
diagnosis_query = "INSERT INTO rebound_diagnosis VALUES "
adjustment_query = "INSERT INTO rebound_adjustment VALUES "
ids = []
total_cnt = 0

if __name__ == '__main__':
  query = "SELECT COUNT(id) AS CNT FROM parsed_835"
  cursor.execute(query)
  result = cursor.fetchone()
  count = result['CNT']
  period = int((count - 1) / PERIOD_SIZE) + 1
  offset = 0
  for i in range(period):
    query = f"CREATE OR REPLACE VIEW temp_835 AS SELECT * FROM parsed_835 LIMIT {PERIOD_SIZE} OFFSET {offset}"
    cursor.execute(query)

    query = """
      SELECT temp_835.id AS id_835,
      parsed_837.id AS id_837,
      parsed_837.PatientFirstName,
      parsed_837.PatientLastName,
      parsed_837.PatientMiddleName,
      parsed_837.PatientAddress,
      parsed_837.PatientCity,
      parsed_837.PatientState,
      parsed_837.PatientZipCode,
      parsed_837.PatientBirthday,
      parsed_837.PatientGender,
      parsed_837.PatientSSN,
      parsed_837.PayerName,
      parsed_837.PayerID,
      parsed_837.PayerAddress,
      parsed_837.PayerCity,
      parsed_837.PayerState,
      parsed_837.PayerZipCode,
      parsed_837.PatientAccountNumber,
      parsed_837.TotalClaimChargeAmount,
      parsed_837.AccidentDate,
      parsed_837.ServiceDate,
      parsed_837.MedicalRecordNumber,
      parsed_837.AuthNumber,
      parsed_837.RenderingProviderType,
      parsed_837.RenderingProviderFirstName,
      parsed_837.RenderingProviderLastName,
      parsed_837.RenderingProviderName,
      parsed_837.RenderingProviderNPI,
      parsed_837.BillingProviderType,
      parsed_837.BillingProviderFirstName,
      parsed_837.BillingProviderLastName,
      parsed_837.BillingProviderAddressLine1,
      parsed_837.BillingProviderAddressLine2,
      parsed_837.BillingProviderCity,
      parsed_837.BillingProviderState,
      parsed_837.BillingProviderZipCode,
      parsed_837.BillingProviderNPI,
      parsed_837.BillingProviderTaxID,
      temp_835.Service,
      parsed_837.Diagnosis,
      parsed_837.Services
      FROM temp_835 INNER JOIN parsed_837
      ON temp_835.PatientControlNumber=parsed_837.PatientAccountNumber
      AND temp_835.NPI = parsed_837.BillingProviderNPI
      AND temp_835.ServiceDate=parsed_837.ServiceDate
      AND temp_835.TaxID=parsed_837.BillingProviderTaxID
      AND temp_835.TotalClaimChargeNumber=parsed_837.TotalClaimChargeAmount
      ORDER BY parsed_837.id
    """

    cursor.execute(query)
    results = cursor.fetchall()

    for result in results:
      ids.append(result["id_837"])
      matching_query += f"""("{str(uuid.uuid4())}", "{result["id_835"]}", "{result["id_837"]}"),"""
      id = str(uuid.uuid4())
      diagnosis = result['Diagnosis'].split(':')
      for diag in diagnosis:
        diagnosis_query += f"""(
          "{str(uuid.uuid4())}",
          "{id}",
          "{diag}"
        ),"""
      services_837 = result['Services'].split(',')
      services_835 = result['Service'].split(',')
      maxCode = "Not Set"
      maxAmount = 0
      category = ""
      for i in range(len(services_837)):
        service_id = str(uuid.uuid4())
        services = services_837[i].split('|')

        adjustments = services_835[i].split(':')
        paymentamount = float(adjustments[3])
        remark = adjustments[-1]
        for adj in adjustments[-2].split('#'):
          codes = adj.split('@')
          if len(codes) == 2:
            code = ''
            groupcode = ''
            if codes[0][0].isalpha() == True and codes[0][1].isalpha() == True:
              code = codes[0][2:]
              groupcode = codes[0][:2]
            else:
              code = codes[0]
              groupcode = ''
            if maxCode == "Not Set":
              maxCode = code
            elif maxAmount < float(codes[1]):
              qq = f"SELECT * FROM carc WHERE Code='{code}'"
              cursor.execute(qq)
              res = cursor.fetchone()
              maxAmount = float(codes[1])
              maxCode = res['Code']
              category = res['DenialCategory']
            adjustment_query += f"""(
              "{str(uuid.uuid4())}",
              "{service_id}",
              "{groupcode}",
              "{code}",
              {float(codes[1])}
            ),"""

        paymentamount = 0
        remark = ""

        service_query += f"""(
          "{service_id}",
          "{id}",
          {float(services[0])},
          {int(services[1])},
          "{services[2]}",
          "{services[3]}",
          "{services[4]}",
          "{services[5]}",
          {paymentamount},
          "{remark}"
        ),"""

      if category == "":
        category = "Not set yet"

      claim_query += f"""(
        "{id}",
        "{result["PatientFirstName"]}",
        "{result["PatientLastName"]}",
        "{result["PatientMiddleName"]}",
        "{result["PatientAddress"]}",
        "{result["PatientCity"]}",
        "{result["PatientState"]}",
        "{result["PatientZipCode"]}",
        "{result["PatientBirthday"]}",
        "{result["PatientGender"]}",
        "{result["PatientSSN"]}",
        "{result["PayerName"]}",
        "{result["PayerID"]}",
        "{result["PayerAddress"]}",
        "{result["PayerCity"]}",
        "{result["PayerState"]}",
        "{result["PayerZipCode"]}",
        "{result["PatientAccountNumber"]}",
        "{result["TotalClaimChargeAmount"]}",
        "{result["AccidentDate"]}",
        "{result["ServiceDate"]}",
        "{result["MedicalRecordNumber"]}",
        "DENIED",
        "{category}",
        "{maxCode}",
        "{result["AuthNumber"]}",
        "Review",
        "{result["RenderingProviderType"]}",
        "{result["RenderingProviderFirstName"]}",
        "{result["RenderingProviderLastName"]}",
        "{result["RenderingProviderName"]}",
        "{result["RenderingProviderNPI"]}",
        "{result["BillingProviderType"]}",
        "{result["BillingProviderFirstName"]}",
        "{result["BillingProviderLastName"]}",
        "{result["BillingProviderAddressLine1"]}",
        "{result["BillingProviderAddressLine1"]}",
        "{result["BillingProviderCity"]}",
        "{result["BillingProviderState"]}",
        "{result["BillingProviderZipCode"]}",
        "{result["BillingProviderNPI"]}",
        "{result["BillingProviderTaxID"]}",
        "{result["Service"]}",
        "{result['Diagnosis']}"
      ),"""
    if matching_query[-1] == ',':
      matching_query = matching_query[:len(matching_query)-1]
    if claim_query[-1] == ',':
      claim_query = claim_query[:len(claim_query)-1]
    if service_query[-1] == ',':
      service_query = service_query[:len(service_query)-1]
    if diagnosis_query[-1] == ',':
      diagnosis_query = diagnosis_query[:len(diagnosis_query)-1]
    if adjustment_query[-1] == ',':
      adjustment_query = adjustment_query[:len(adjustment_query)-1]
    cursor.execute(matching_query)
    cursor.execute(claim_query)
    cursor.execute(service_query)
    cursor.execute(diagnosis_query)
    cursor.execute(adjustment_query)
    mysql_conn.commit()
    matching_query = "INSERT INTO matching_837_835 VALUES "
    claim_query = "INSERT INTO rebound_claim VALUES "
    service_query = "INSERT INTO rebound_service VALUES "
    diagnosis_query = "INSERT INTO rebound_diagnosis VALUES "
    adjustment_query = "INSERT INTO rebound_adjustment VALUES "
    offset += PERIOD_SIZE
    print(offset)
    break

  query = f"""SELECT * FROM parsed_837 WHERE id NOT IN ({"'" + "','".join(ids) + "'"})"""
  cnt = 0
  cursor.execute(query)
  results = cursor.fetchall()
  for result in results:
    id = str(uuid.uuid4())
    service_value = ""
    for service in result['Services'].split(','):
      service_item = service.split('|')
      service_value += f"{service_item[4]}:{service_item[5]}:{service_item[0]}:{service_item[0]}::"
    claim_query += f"""(
      "{id}",
      "{result["PatientFirstName"]}",
      "{result["PatientLastName"]}",
      "{result["PatientMiddleName"]}",
      "{result["PatientAddress"]}",
      "{result["PatientCity"]}",
      "{result["PatientState"]}",
      "{result["PatientZipCode"]}",
      "{result["PatientBirthday"]}",
      "{result["PatientGender"]}",
      "{result["PatientSSN"]}",
      "{result["PayerName"]}",
      "{result["PayerID"]}",
      "{result["PayerAddress"]}",
      "{result["PayerCity"]}",
      "{result["PayerState"]}",
      "{result["PayerZipCode"]}",
      "{result["PatientAccountNumber"]}",
      "{result["TotalClaimChargeAmount"]}",
      "{result["AccidentDate"]}",
      "{result["ServiceDate"]}",
      "{result["MedicalRecordNumber"]}",
      "ACTIVE",
      "NONE",
      "",
      "{result["AuthNumber"]}",
      "Review",
      "{result["RenderingProviderType"]}",
      "{result["RenderingProviderFirstName"]}",
      "{result["RenderingProviderLastName"]}",
      "{result["RenderingProviderName"]}",
      "{result["RenderingProviderNPI"]}",
      "{result["BillingProviderType"]}",
      "{result["BillingProviderFirstName"]}",
      "{result["BillingProviderLastName"]}",
      "{result["BillingProviderAddressLine1"]}",
      "{result["BillingProviderAddressLine1"]}",
      "{result["BillingProviderCity"]}",
      "{result["BillingProviderState"]}",
      "{result["BillingProviderZipCode"]}",
      "{result["BillingProviderNPI"]}",
      "{result["BillingProviderTaxID"]}",
      "{service_value}",
      "{result['Diagnosis']}"
    ),"""
    cnt += 1
    if cnt == QUERY_SIZE:
      total_cnt += cnt
      print(total_cnt)
      cnt = 0
      if claim_query[-1] == ',':
        claim_query = claim_query[:len(claim_query)-1]
      cursor.execute(claim_query)
      mysql_conn.commit()
      claim_query = "INSERT INTO rebound_claim VALUES "
  if cnt != 0:
    if claim_query[-1] == ',':
      claim_query = claim_query[:len(claim_query)-1]
    cursor.execute(claim_query)
    mysql_conn.commit()