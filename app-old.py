import threading
from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
from pandas.core.api import (
    DataFrame,
)
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from sqlalchemy import create_engine, text
import os, sys
import requests
import json
import numpy as np

app = Flask(__name__)

# 设置文件上传路径
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

#app.config['/O2O_web_app/uploads/ccf_train.csv'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = 'uploads'

# 创建MySQL数据库连接
DB_CONNECTION = 'mysql+pymysql://root:q89kfj82@mytwitter.lz-0315.com:3306/O2O'
engine = create_engine(DB_CONNECTION)

df_cache: DataFrame = None

def process_csv(file_path):
    df = pd.read_csv(file_path)

    # 将原始数据保存到数据库
    # df.to_sql('ccf_train', con=engine, if_exists='replace', index=False)

    # 处理日期格式
    df['Date_received'] = pd.to_datetime(df['Date_received'], format='%Y%m%d', errors='coerce')
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d', errors='coerce')

    # 将处理后的数据保存到数据库
    df.to_sql('ccf_train_processed', con=engine, if_exists='replace', index=False)
    global df_cache
    df_cache = df

    return df

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            df = process_csv(file_path)
            #df.to_sql('ccf_train_features', con=engine, if_exists='replace', index=False)
            return redirect(url_for('result'))
    return render_template('index.html')

@app.route('/result', methods=['GET'])
def result():
    df = pd.read_sql('SELECT * FROM ccf_train_processed', con=engine)

    font = FontProperties(fname='C:/Windows/Fonts/simsun.ttc', size=12)

    # 缺失值数量条形图
    missing_values = df.isnull().sum()
    plt.figure(figsize=(12, 6))
    missing_values.plot(kind='bar')
    plt.title('缺失值数量统计', fontproperties=font)
    plt.xlabel('列', fontproperties=font)
    plt.ylabel('数量', fontproperties=font)
    plt.savefig('static/missing_values.png')

    # 标签分布直方图/柱状图
    plt.figure(figsize=(8, 6))
    label_distribution = df['label'].value_counts()
    label_distribution.plot(kind='bar')
    plt.title('标签分布', fontproperties=font)
    plt.xlabel('标签', fontproperties=font)
    plt.ylabel('数量', fontproperties=font)
    plt.savefig('static/label_distribution.png')

    # 优惠券类型占比饼状图
    if 'Discount_rate' in df.columns and not df['Discount_rate'].isnull().all():
        coupon_type_distribution = df['Discount_rate'].value_counts()
        plt.figure(figsize=(8, 8))
        coupon_type_distribution.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title('优惠券类型占比', fontproperties=font)
        plt.ylabel('', fontproperties=font)
        plt.savefig('static/coupon_type_distribution.png')

    return render_template('result.html', label_counts=label_counts)

@app.route('/upload_db', methods=['POST'])
def upload_db():
    df = pd.read_sql('SELECT * FROM ccf_train_features', con=engine)
    df.to_sql('ccf_train_features', con=engine, if_exists='replace', index=False)
    return "数据已上传到数据库。"

def get_bing_wallpaper():
    url = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=8"
    response = requests.get(url)
    data = response.json()
    images = data['images']
    return ["https://www.bing.com" + image['url'] for image in images]

@app.context_processor
def inject_bing_wallpapers():
    return dict(bing_wallpapers=get_bing_wallpaper())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
