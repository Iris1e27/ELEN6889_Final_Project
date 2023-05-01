from flask import Flask, render_template, request
from datetime import datetime, timedelta
from plotBigQuery import plot_bigquery

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot', methods=['GET', 'POST'])
def plot():
    if request.method == 'POST':
        # retrieve form data
        start_time = request.form['starttime']
        duration = request.form['duration']

        # generate images using plot_bigquery function
        start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
        end_time = start_time + timedelta(hours=int(duration))

        # 调用plot_bigquery函数，返回path1，path2，path3
        path1, path2, path3 = plot_bigquery(start_time, end_time)

        # 将 path1、path2、path3 作为参数传递给模板文件
        return render_template('plot.html', start_time=start_time, end_time=end_time, duration=duration,
                               image1=path1, image2=path2, image3=path3)
    # 如果是 GET 请求，返回空表单
    return render_template('plot.html')

if __name__ == '__main__':
    app.secret_key = "super secret key"
    app.run(host='0.0.0.0', port=8111, debug=True)