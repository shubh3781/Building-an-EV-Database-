from google.cloud import datastore
import os
import google.oauth2.id_token
from flask import Flask, render_template, request,redirect
from google.auth.transport import requests
import random
from datetime import datetime



app = Flask(__name__)
datastore_client = datastore.Client()
firebase_request_adapter = requests.Request()

#--------------------------------------------------------------------------------------------
def retrieveUserInfo(claims):
    entity_key = datastore_client.key('UserInfo', claims['email'])
    entity = datastore_client.get(entity_key)
    return entity

#--------------------------------------------------------------------------------------------
def createUserInfo(claims):
    entity_key = datastore_client.key('UserInfo', claims['email'])
    entity = datastore.Entity(key = entity_key)
    entity.update({
        'email': claims['email'],
        'name': claims['name']
    })
    datastore_client.put(entity)

#--------------------------------------------------------------------------------------------
def check_ev(name,manufacturer, year):
    query = datastore_client.query(kind='EVDATA')
    query.add_filter("name","=",name)
    query.add_filter("manufacturer","=",manufacturer)
    query.add_filter("year","=",year)
    result = list(query.fetch())
    print(len(result))
    print(name)
    print(manufacturer)
    print(year)
    if len(result)>0:
        return True
    return False

#--------------------------------------------------------------------------------------------
def ev_model(name, manufacturer, year, battery_size, WLTP_range, cost, power):
    if not check_ev(name,manufacturer,year):
        id = random.getrandbits(63)
        entity_key = datastore_client.key('EVDATA', id)
        entity = datastore.Entity(key = entity_key)
        entity.update({
            'name':name,
            'manufacturer':manufacturer,
            'year':year,
            'battery_size':battery_size,
            'WLTP_range':WLTP_range,
            'cost':cost,
            'power':power
        })
        datastore_client.put(entity)
        return True
    else:
        return False

#--------------------------------------------------------------------------------------------
@app.route('/add_evs',methods=['post'])
def add_evs():
    id_token = request.cookies.get("token")
    claims = None
    if id_token:
        claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
        return render_template('add.html', user_data=claims)
    else:
        "Please Signin or login"
#--------------------------------------------------------------------------------------------
@app.route("/add_ev",methods=['POST'])
def add_ev():
    name = request.form['name']
    manufacturer = request.form['manufacturer']
    year = request.form['year']
    battery_size = request.form['battery_size']
    wltp_range = request.form['wltp_range']
    cost = request.form['cost']
    power = request.form['power']
    if ev_model(name,manufacturer,int(year),int(battery_size),int(wltp_range),int(cost),int(power)):
        return "EV added in store"
    else:
        return "EV Already in store"
#--------------------------------------------------------------------------------------------
def get_all_evs():
    return list(datastore_client.query(kind='EVDATA').fetch())
#--------------------------------------------------------------------------------------------
@app.route('/search',methods=['post'])
def search():
    name = request.form['name']
    manufacturer = request.form['manufacturer']
    year_low = request.form['year_low']
    year_high = request.form['year_high']
    battery_size_low = request.form['battery_size_low']
    battery_size_high = request.form['battery_size_high']
    wltp_range_low = request.form['wltp_range_low']
    wltp_range_high = request.form['wltp_range_high']
    cost_low = request.form['cost_low']
    cost_high = request.form['cost_high']
    power_low = request.form['power_low']
    power_high = request.form['power_high']
    query = datastore_client.query(kind='EVDATA')
    if name!='':
        query.add_filter('name','=',name)
    if manufacturer!='':
        query.add_filter('manufacturer','=',manufacturer)
    res = list(query.fetch())
    result = []
    for r in res:
        if year_low!='' and r['year']<int(year_low):
            continue
        if year_high!='' and r['year']>int(year_high):
            continue
        if battery_size_low!='' and r['battery_size']<int(battery_size_low):
            continue
        if battery_size_high!='' and r['battery_size']>int(battery_size_high):
            continue
        if wltp_range_low!='' and r['wltp_range']<int(wltp_range_low):
            continue
        if wltp_range_high!='' and r['wltp_range']>int(wltp_range_high):
            continue
        if cost_low!='' and r['cost']<int(cost_low):
            continue
        if cost_high!='' and r['cost']>int(cost_high):
            continue
        if power_low!='' and r['power']<int(power_low):
            continue
        if power_high!='' and r['power']>int(power_high):
            continue
        result.append(r)
    id_token = request.cookies.get("token")
    claims = None
    if id_token:
        claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
        return render_template('index.html', user_data=claims,evs=result)
    else:
        return render_template('index.html', evs=result)

#--------------------------------------------------------------------------------------------
@app.route('/show_ev',methods=['post'])
def show_ev():
    id = (request.form['id'])
    entity_key = datastore_client.key('EVDATA', int(id))
    entity = datastore_client.get(entity_key)
    id_token = request.cookies.get("token")
    reviews = get_reviews(int(id))
    average_score = get_average_score(reviews)
    claims = None
    if id_token:
        claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
    return render_template('EV_info.html', user_data=claims,ev = entity,reviews=reviews,average_score=average_score)
#--------------------------------------------------------------------------------------------
@app.route('/edit',methods=['post'])
def edit():
    id = request.form['id']
    entity_key = datastore_client.key('EVDATA', int(id))
    entity = datastore_client.get(entity_key)
    id_token = request.cookies.get("token")
    claims = None
    if id_token:
        claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
    return render_template('edit_Page.html',user_data=claims,ev=entity)
#--------------------------------------------------------------------------------------------
@app.route('/edit_ev',methods=['post'])
def edit_ev():
    id = request.form['id']
    name = request.form['name']
    manufacturer = request.form['manufacturer']
    year = request.form['year']
    battery_size = request.form['battery_size']
    wltp_range = request.form['wltp_range']
    cost = request.form['cost']
    power = request.form['power']
    if not check_ev(name,manufacturer,int(year)):
        #update
        entity_key = datastore_client.key('EVDATA', int(id))
        entity = datastore_client.get(entity_key)
        entity.update({
            'name':name,
            'manufacturer':manufacturer,
            'year':int(year),
            'battery_size':int(battery_size),
            'WLTP_range':int(wltp_range),
            'cost':int(cost),
            'power':int(power)
        })
        datastore_client.put(entity)
        return redirect('/')
    else:
        return "EV With Same Info Found"
#--------------------------------------------------------------------------------------------
@app.route('/delete',methods=['post'])
def delete():
    id = request.form['id']
    entity_key = datastore_client.key('EVDATA', int(id))
    datastore_client.delete(entity_key)
    return redirect('/')
#--------------------------------------------------------------------------------------------
@app.route('/compare_evs_page',methods=['post'])
def compare_evs_page():
    id_token = request.cookies.get("token")
    claims = None
    if id_token:
        claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
    all_evs = get_all_evs()
    return render_template('compare.html',user_data=claims,all_evs=all_evs,selected_evs_list="")
#--------------------------------------------------------------------------------------------
@app.route('/compare_evs',methods=['post'])
def compare_evs():
    ids = request.form['selected_evs_id']
    ids=ids.split(';')
    ids.pop()
    selected_evs_list = request.form['selected_evs_list']
    evs = []
    reviews_list = []
    avg_scores = []
    for id in ids:
        entity_key = datastore_client.key('EVDATA', int(id))
        evs.append(datastore_client.get(entity_key))
    for id in ids:
        reviews_list.append(get_reviews(int(id)))
    for review in reviews_list:
        avg_scores.append(get_average_score(review))
    all_evs = get_all_evs()
    property_list = ['name','manufacturer','year','battery_size','WLTP_range','cost','power']
    result = []
    for i in range(7):
        result.append([])
        for j in range(len(evs)):
            result[i].append(evs[j][property_list[i]])
    min_ = []
    max_ = []
    for i in range (2,len(result)):
        min_.append(min(result[i]))
        max_.append(max(result[i]))
    min_.append(min(avg_scores))
    max_.append(max(avg_scores))
    id_token = request.cookies.get("token")
    claims = None
    if id_token:
        claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
    return render_template('compare.html',user_data=claims,all_evs=all_evs,evs=result,avg_scores=avg_scores,\
        selected_evs_list=selected_evs_list,property_list = property_list,min_=min_,max_=max_)
#--------------------------------------------------------------------------------------------
@app.route('/add_rating',methods=['post'])
def add_rating():
    review = request.form['review']
    id = request.form['id']
    rating = request.form['rating']
    entity_key = datastore_client.key('RatingsInfo', random.getrandbits(50))
    entity = datastore.Entity(key = entity_key)
    entity.update({
        'ev_id':int(id),
        'review':review,
        'rating':int(rating),
        'time': datetime.now()
    })
    datastore_client.put(entity)
    return redirect('/')
#--------------------------------------------------------------------------------------------
def get_reviews(id):
    query = datastore_client.query(kind='RatingsInfo')
    query.order = ['-time']
    query.add_filter('ev_id','=',id)
    return list(query.fetch())
#--------------------------------------------------------------------------------------------
def get_average_score(reviews):
    sum= 0
    for r in reviews:
        sum+=r['rating']
    average_score = 0
    if len(reviews)>0:
        average_score = sum/len(reviews)
    else:
        average_score = 0
    return float("{:.2f}".format(average_score))
#--------------------------------------------------------------------------------------------
@app.route('/')
def root():
    id_token = request.cookies.get("token")
    error_message = None
    claims = None
    user_info = None
    evs = get_all_evs()
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
            user_info = retrieveUserInfo(claims)
            if not user_info:
                createUserInfo(claims)
        except ValueError as exc:
            error_message = str(exc)
    return render_template('index.html', user_data=claims, error_message=error_message,evs=evs)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
