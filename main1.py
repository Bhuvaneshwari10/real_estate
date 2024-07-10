from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import logging
import seaborn as sns
import pandas as pd

apps = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@apps.route("/")
def sales():
    try:
        response1 = requests.get("http://127.0.0.1:8000/total_sales")
        total_sales = response1.json()
        total_sales_conversion = format_price(total_sales[0][0])

        response2 = requests.get("http://127.0.0.1:8000/total_city")
        total_city = response2.json()

        response3 = requests.get("http://127.0.0.1:8000/total_broker")
        total_broker = response3.json()

        response4 = requests.get("http://127.0.0.1:8000/house_sold")
        total_house_sold = response4.json()

        response5 = requests.get("http://127.0.0.1:8000/status_data")
        status_data = response5.json()
        status_chart_img = status_pie_chart(status_data, "Sales by Status")

        response6 = requests.get("http://127.0.0.1:8000/Top_broker")
        broker_data = response6.json()
        broker_chart_img = broker_donut_chart(broker_data, "Top 5 Brokers by Properties Sold")

        response7 = requests.get("http://127.0.0.1:8000/Top_states")
        top_states_data = response7.json()
        top_states_chart_img = states_bar_chart(top_states_data, "Top 5 States with Highest Total Sales (Sold Properties)")

        response8 = requests.get("http://127.0.0.1:8000/Top_city_sale")
        top_city_sale_data = response8.json()
        top_city_sale_chart_img = city_pie_chart(top_city_sale_data, "Top 3 Cities with Highest For Sale Count")

        response9 = requests.get("http://127.0.0.1:8000/avg_house_size_bedrooms")
        avg_house_size_bedrooms_data = response9.json()
        avg_house_size_bedrooms_chart_img = bedroom_scatter_chart(avg_house_size_bedrooms_data, "Average House Size by Number of Bedrooms")

        response10 = requests.get("http://127.0.0.1:8000/avg_bathrooms")
        avg_bathrooms_data = response10.json()
        avg_bathrooms_chart_img = bathrooms_bar_plot(avg_bathrooms_data, "Count of Bathrooms")

        return render_template(
            "dashboard.html",
            total_sales=total_sales_conversion,
            dup_city=total_city[0][0],
            dup_broker=total_broker[0][0],
            dup_house=total_house_sold[0][0],
            status_chart=status_chart_img,
            broker_chart=broker_chart_img,
            top_states_chart=top_states_chart_img,
            top_city_sale_chart=top_city_sale_chart_img,
            avg_house_size_bedrooms_chart=avg_house_size_bedrooms_chart_img,
            avg_bathrooms_chart=avg_bathrooms_chart_img
        )

    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return render_template("dashboard.html", error=f"Error fetching data: {e}")

@apps.template_filter('format_price')
def format_price(n):
    return f"{n / 1e9:.0f}B+"

def states_bar_chart(data, title):
    states = [item[0] for item in data]
    total_sales = [item[1] for item in data]
    fig, ax = plt.subplots()
    ax.bar(states, total_sales, color='skyblue')
    ax.set_xlabel('State')
    ax.set_ylabel('Total Sales')
    ax.set_title(title)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return img_base64

def broker_donut_chart(data, title):
    labels = [item[0] for item in data]
    sizes = [item[1] for item in data]
    colors=['#575195','#7ab874','#ffce74','#ff9bbb','#f44f4f']
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=60,wedgeprops=dict(width=0.5),colors=colors)
    ax.axis('equal') #circle
    ax.set_title(title)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return img_base64

def status_pie_chart(data, title):
    labels = [item[0] for item in data]
    sizes = [item[1] for item in data]
    colors=['#6ea6f2','#fc6a8b','#7ab874']
    fig, ax = plt.subplots()
    wedges,text,auto_text=ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90,colors=colors)
    legend_label=['for_sale','ready_to_build','sold']
    ax.legend(wedges,legend_label,loc='lower left',bbox_to_anchor=(-0.15,-0.1),prop={'size':10})
    ax.axis('equal')
    ax.set_title(title)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return img_base64

def city_pie_chart(data, title):
    labels = [item[0] for item in data]
    sizes = [item[1] for item in data]
    colors = ['#575195', '#ffce74', '#f44f4f']
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=60,
        wedgeprops=dict(width=0.4),
        colors=colors
    )
    ax.axis('equal')  
    ax.set_title(title) 
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return img_base64

def bedroom_scatter_chart(data, title):
    df = pd.DataFrame(data, columns=['bed', 'avg_house_size'])
    fig, ax = plt.subplots(figsize=(10, 6)) #width,height
    sns.scatterplot(data=df, x='bed', y='avg_house_size', size='avg_house_size', sizes=(20, 200), legend=None, ax=ax)
    ax.set_xlabel('Number of Bedrooms',fontsize=17)
    ax.set_ylabel('Average House Size (sqft)',fontsize=17)
    ax.set_title(title,fontsize=19)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return img_base64

def bathrooms_bar_plot(data, title):
    df = pd.DataFrame(data, columns=['number_of_bathrooms', 'count_of_bathrooms'])
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=df, x='number_of_bathrooms', y='count_of_bathrooms', palette='viridis', ax=ax)
    ax.set_xlabel('Number of Bathrooms',fontsize=17)
    ax.set_ylabel('Count of Bathrooms',fontsize=17)
    ax.set_title(title,fontsize=19)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return img_base64

response_1 = requests.get("http://127.0.0.1:8000/city_list")
response_2=requests.get("http://127.0.0.1:8000/house_size")
response_3=requests.get("http://127.0.0.1:8000/status")
city = response_1.json()
house_size=response_2.json()
house_status=response_3.json()
cities = [usa_city[0] for usa_city in city]
house_sizes=[str(usa_house[0]) for usa_house in house_size]
status=[usa_status[0] for usa_status in house_status]

search_categories ={"house_size":house_sizes,"city": cities,"status":status}

@apps.route('/get_suggestions', methods=['POST'])
def get_suggestions():
    category = request.form.get('category')
    query = request.form.get('query', '').lower()
    suggestions = []
    if category in search_categories:
        suggestions = [item for item in search_categories[category] if query in item.lower()]
    return jsonify({"suggestions": suggestions})

@apps.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('query')
        category = request.form.get('category')
    else:
        query = request.args.get('query')
        category = request.args.get('category')
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    if category == 'city':
        response = requests.get(f"http://127.0.0.1:8000/search_city/{query}")
    elif category == 'status':
        response = requests.get(f"http://127.0.0.1:8000/search_status/{query}")
    elif category == 'house_size':
        response = requests.get(f"http://127.0.0.1:8000/search_house_size/{query}")
    else:
        return render_template('search.html', error="Invalid category selected!")
    
    if response.status_code == 200:
        search_data = response.json()
    else:
        return render_template('search.html', error="Error fetching data from FastAPI!")
    
    datas = 'valid' if search_data else 'invalid'
    
    total_properties = len(search_data)
    total_pages = (total_properties + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    paginated_properties = search_data[start:end]
    p_start = max(1, page - 1)
    p_end = min(total_pages, page + 3)
    
    return render_template(
        'search.html',
        search_data=paginated_properties,
        category=category,
        datas=datas,
        page=page,
        total_pages=total_pages,
        p_start=p_start,
        p_end=p_end,
        query=query
    )

if __name__ == '__main__':
    apps.run(debug=True)