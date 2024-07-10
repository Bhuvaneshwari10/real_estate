import uvicorn
from fastapi import FastAPI,HTTPException
import mysql.connector
app = FastAPI()

def connect():
    return mysql.connector.connect(
        host="3.7.198.191",
	    user="bu-trausr",
	    password="r9*rwr$!usFw0MCPj#fJ",
	    database="bu-training",
	    port=8993,
	    auth_plugin='mysql_native_password'
    )

@app.get('/total_sales')
async def total_sales_amount():
    try:
        conn = connect()
        cursor = conn.cursor()
        query = "select sum(price) from real_estate_bhuvana where status='sold' group by status;"
        cursor.execute(query)
        conn.close()
        values = cursor.fetchall()
        return values
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get('/total_broker')
async def total_broker():
    try:
        conn = connect()
        cursor = conn.cursor()
        query = "select count(distinct brokered_by) from real_estate_bhuvana;"
        cursor.execute(query)
        conn.close()
        values = cursor.fetchall()
        return values
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get('/house_sold')
async def house_sold():
    try:
        conn = connect()
        cursor = conn.cursor()
        query = "select count(status) from real_estate_bhuvana where status='sold' group by status;"
        cursor.execute(query)
        conn.close()
        values = cursor.fetchall()
        return values
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get('/total_city')
async def total_city():
    try:
        conn = connect()
        cursor = conn.cursor()
        query = "select count(distinct city) from real_estate_bhuvana;"
        cursor.execute(query)
        conn.close()
        values = cursor.fetchall()
        return values
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get('/Top_states')
def get_top_states():
    try:
        conn = connect()
        cursor = conn.cursor()
        query = """
        select state, sum(price) as sum_of_price from real_estate_bhuvana where status = 'sold'
        group by state order by sum_of_price desc limit 5;
        """
        cursor.execute(query)
        values = cursor.fetchall()
        conn.close()
        return values
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/Top_broker')
def get_users5():
    try:
        conn=connect()
        cursor=conn.cursor()
        query="""select brokered_by, count(status) as num_sold from real_estate_bhuvana where status = 'sold' 
        group by brokered_by order by num_sold desc limit 5"""
        cursor.execute(query)
        values=cursor.fetchall()
        conn.close()
        return values
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/status_data')
def get_users4():
    try:
        conn=connect()
        cursor=conn.cursor()
        query="select status,count(*) as statuswise_count from real_estate_bhuvana group by status"
        cursor.execute(query)
        values=cursor.fetchall()
        conn.close()
        return values
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/Top_city_sale')
def get_user7():
    try:
        conn = connect()
        cursor = conn.cursor()
        query = """select city, count(*) as for_sale_count from real_estate_bhuvana where status = 'for_sale' 
        group by city order by for_sale_count desc limit 3;"""
        cursor.execute(query)
        values = cursor.fetchall()
        conn.close()
        return values
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/avg_house_size_bedrooms')
def get_avg_house_size_bedrooms():
    try:
        conn = connect()
        cursor = conn.cursor()
        query = """
        select bed, avg(house_size) as avg_house_size from real_estate_bhuvana
        group by bed order by bed;
        """
        cursor.execute(query)
        values = cursor.fetchall()
        conn.close()
        return values
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/avg_bathrooms')
def get_size_bathrooms():
    try:
        conn = connect()
        cursor = conn.cursor()
        query = """
        select bath as number_of_bathrooms, count(*) as count_of_bathrooms from real_estate_bhuvana group by bath 
        order by count_of_bathrooms desc limit 10;
        """
        cursor.execute(query)
        values = cursor.fetchall()
        conn.close()
        return values
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get('/search_city/{city}')
async def search_city(city:str):
    con=connect()
    cur=con.cursor()
    query1="select * from real_estate_bhuvana where city = %s;"
    cur.execute(query1,(city,))
    result=cur.fetchall()
    cur.close()
    return result

@app.get('/search_house_size/{house_size}')
async def search_house_size(house_size:str):
    con=connect()
    cur=con.cursor()
    query2="select * from real_estate_bhuvana where house_size = %s;"
    cur.execute(query2,(house_size,))
    result=cur.fetchall()
    cur.close()
    return result

@app.get('/search_status/{status}')
async def search_status(status:str):
    con=connect()
    cur=con.cursor()
    query2="select * from real_estate_bhuvana where status = %s;"
    cur.execute(query2,(status,))
    result=cur.fetchall()
    cur.close()
    return result

@app.get('/city_list')
async def city_list1():
    con = connect()
    cur = con.cursor()
    query = "select distinct city from real_estate_bhuvana"
    cur.execute(query)
    values = cur.fetchall()
    con.close()
    return values

@app.get('/house_size')
async def house_size():
    con = connect()
    cur = con.cursor()
    query = "select distinct house_size from real_estate_bhuvana"
    cur.execute(query)
    values = cur.fetchall()
    con.close()
    return values

@app.get('/status')
async def status():
    con=connect()
    cur=con.cursor()
    query="select distinct status from real_estate_bhuvana"
    cur.execute(query)
    values=cur.fetchall()
    con.close()
    return values