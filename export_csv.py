import mysql.connector
import uuid
import csv

mysql_conn = mysql.connector.connect(
  host='localhost',
  user='root',
  password='',
  database='db_gabeo'
)

cursor = mysql_conn.cursor()

def export_diagnosis():
  csv_file = "claim_data.csv"

  query = f"SELECT * FROM rebound_claim"

  cursor.execute(query)

  results = cursor.fetchall()

# print(data)
  cnt = 0
  for result in results:

    claimId = result[3]
    diag = []
    servi = []
    carccarc = []
    
    query = f"SELECT * FROM rebound_diagnosis WHERE Claim='{result[0]}'"
    cursor.execute(query)
    rows = cursor.fetchall()
    # diagnosis = ""
    for diagnosis in rows:
      diag.append(diagnosis[2][:3]+"."+diagnosis[2][3:])
      # d[1] = (diagnosis[2][:3]+"."+diagnosis[2][3:])
    # d.append(diagnosis)
    
      query = f"SELECT * FROM rebound_service WHERE ClaimID='{result[0]}'"
      cursor.execute(query)
      services = cursor.fetchall()
    # services = ""
      for service in services:
        servi.append(service[6])
        # d[2] = service[6]
    # d.append(services)
    
        query = f"SELECT * FROM rebound_adjustment WHERE ServiceID='{service[0]}'"
        cursor.execute(query)
        adjustments = cursor.fetchall()
        rrr = ""
    # adjustments = ""
        for adjustment in adjustments:
          carccarc.append(adjustment[2]+adjustment[3])
          # rrr += adjustment[2]+adjustment[3] + " "
        # d[3] = rrr
        # writer.writerow(d)
        # print("write one")
    diag = sorted(set(diag))
    servi = sorted(set(servi))
    carccarc = sorted(set(carccarc))
    diag = ",".join(diag)
    servi = ",".join(servi)
    carccarc = ",".join(carccarc)
    cnt += 1
    if cnt == 1:
      query = f"INSERT INTO rebound_predict VALUES ('{str(uuid.uuid4())}', '{diag}', '{servi}', '{carccarc}')"
    else if cnt == 1000:
      cursor.execute(query)
      cnt = 0
    else:
      query += f", ('{str(uuid.uuid4())}', '{diag}', '{servi}', '{carccarc}')"
    print(cnt)
  if cnt != 0:
    cursor.execute(query)
  mysql_conn.commit()
  
  
def export_icd():
  data = [
    ['Code', 'Description']
  ]
  query = f"SELECT * FROM icd"
  cursor.execute(query)
  results = cursor.fetchall()
  for result in results:
    data.append([result[0], result[1]])
  with open('diagnosis.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

def export_cpt():
  data = [
    ['Code', 'Description']
  ]
  query = f"SELECT * FROM cpt"
  cursor.execute(query)
  results = cursor.fetchall()
  for result in results:
    data.append([result[0], result[1]])
  with open('services.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

def export_carc():
  data = [
    ['Code', 'Description', "Category"]
  ]
  query = f"SELECT * FROM carc"
  cursor.execute(query)
  results = cursor.fetchall()
  for result in results:
    data.append([result[0], result[1], result[2]])
  with open('carc.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

if __name__=="__main__":
  export_diagnosis()
  export_cpt()
  export_carc()
  export_icd()