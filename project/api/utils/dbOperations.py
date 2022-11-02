import json
import decimal, datetime
from sqlalchemy import null

def alchemy_encoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)

def execute_raw_object_query(cursor,spName, params):
    cursor.callproc(spName,params)
    row_headers=[x[0] for x in cursor.description]
    results = cursor.fetchall()
    json_data=[]
    for result in results:
        json_data.append(dict(zip(row_headers,result)))
        jsonResults = json.dumps(json_data[0],default=alchemy_encoder)
    return jsonResults

def execute_raw_query_next(cursor):
    results = cursor.fetchall()
    if str(results) != "()":
        json_data=[]
        row_headers=[x[0] for x in cursor.description]
        print(len(results))
        for result in results:
            json_data.append(dict(zip(row_headers,result)))
            if len(results) > 1:
                jsonResults = json.dumps(json_data,default=alchemy_encoder)
            else:
                jsonResults = json.dumps(json_data[0],default=alchemy_encoder)

        return jsonResults
    else:
        return None

def decode_query_result(query_result):
    json_data = json.loads(json.dumps([dict(r) for r in query_result], default= alchemy_encoder))
    return json_data

def insert_query_builder(obj, tableName, db):
        string1 = ""
        values1 = ""
        m = ""
        for i, (x) in enumerate(obj):
            if(obj[x] != None):
                m = '"{}"'.format(obj[x])
            else:
                m = str(null())

            if (i != len(obj)-1):
                string1 = string1+x+","
                
                values1 = values1+m+","
            if (i == len(obj)-1):
                string1 = string1+x
                values1 = values1+m

        query_build = "insert into "+tableName+"("+string1+")"+"values"+"("+values1+")"
        query_result = db.session.execute(query_build)
        return query_result.lastrowid