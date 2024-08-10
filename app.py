import time

from flask import Flask, request, jsonify, render_template, session, redirect, url_for,send_file
from static.getChart import getchart,export_to_excel
from static.util.db_tools import DBTools
from static.login import AuthService
from static.huawei_iotda_greenhouse import HuaweiIoTDAEnvironment

app = Flask(__name__)
app.secret_key = '09hxb2PXq31UstkTWtWK3qt136hBoDdbKwOj3Too'
db_tools = DBTools()
auth_service = AuthService(db_tools)
db_tools.connect()
huawei = HuaweiIoTDAEnvironment()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/api/login', methods=['POST'])
def api_login():
    username = request.form['username']
    password = request.form['password']

    # 调用 auth_service 的 login 方法
    login_result = auth_service.login(username, password)

    if login_result['success']:
        # 登录成功，设置 session 来保存用户状态
        session['logged_in'] = True
        session['user_id'] = auth_service.get_user_id(username)  # 这里可以是实际的用户 ID 或其他标识
        return redirect(url_for('index'))
    else:
        # 登录失败，重定向到登录页面或其他错误处理
        return redirect(url_for('login'))


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/api/register', methods=['POST'])
def api_register():
    username = request.form.get('username')
    password = request.form.get('password')

    result = auth_service.register(username, password)
    return redirect(url_for('index'))


@app.route('/api/logout')
def logout():
    # 清除 session 中的登录状态
    session.pop('logged_in', None)
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/api/is_logged_in')
def is_logged_in():
    if 'logged_in' in session and session['logged_in']:
        # 用户已登录
        return 'Welcome to the dashboard!'
    else:
        # 用户未登录
        return redirect(url_for('login'))


@app.route('/account_management')
def account_management():
    return render_template('account_management.html')


@app.route('/greenhouse_management')
def greenhouse_management():
    return render_template('greenhouse_management.html')


@app.route('/modules_management')
def modules_management():
    return render_template('modules_management.html')


@app.route('/api/environment_data')
def environment_data():
    data = huawei.get_environment_data()
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to retrieve data from IoTDA"}), 500


# 灯光API
@app.route('/api/set_led_state', methods=['POST'])
def set_led_state():
    state = request.form.get('state')
    print(state)
    if state in ['on', 'auto', 'off']:
        status_code = huawei.post_command('deng', state)
        if status_code == 200:
            return jsonify({"status": "success", "message": f"led 状态设置为： {state}"}), 200
        else:
            return jsonify({"status": "error", "message": f"命令下发失败，错误码:{status_code}"}), status_code
    else:
        return jsonify({"status": "error", "message": "Invalid state"}), 400


# 风扇API
@app.route('/api/set_fan_state', methods=['POST'])
def set_fan_state():
    state = request.form.get('state')
    print(state)
    if state in ['on', 'auto', 'off']:
        status_code = huawei.post_command('feng', state)
        if status_code == 200:
            return jsonify({"status": "success", "message": f"风扇状态设置为： {state}"}), 200
        else:
            return jsonify({"status": "error", "message": f"命令下发失败，错误码:{status_code}"}), status_code
    else:
        return jsonify({"status": "error", "message": "Invalid state"}), 400

# 水泵API
@app.route('/api/set_pump_state', methods=['POST'])
def set_pump_state():
    state = request.form.get('state')
    print(state)
    if state in ['on', 'auto', 'off']:
        status_code = huawei.post_command('shui', state)
        if status_code == 200:
            return jsonify({"status": "success", "message": f"水泵状态设置为：{state}"}), 200
        else:
            return jsonify({"status": "error", "message": f"命令下发失败，错误码:{status_code}"}), status_code
    else:
        return jsonify({"status": "error", "message": "Invalid state"}), 400


# 棚顶API
@app.route('/api/set_roof_state', methods=['POST'])
def set_roof_state():
    state = request.form.get('state')
    print(state)
    if state in ['on', 'auto', 'off']:
        status_code = huawei.post_command('peng', state)
        if status_code == 200:
            return jsonify({"status": "success", "message": f"棚顶状态设置为{state}"}), 200
        else:
            return jsonify({"status": "error", "message": f"命令下发失败，错误码:{status_code}"}), status_code
    else:
        return jsonify({"status": "error", "message": "Invalid s    tate"}), 400


@app.route('/chart')
def chart():
    startdata = request.args.get('startdata')
    enddata = request.args.get('enddata')
    print(startdata, enddata)
    chart = getchart(startdata,enddata)
    return render_template('chart.html', chart=chart)


@app.route('/api/change_password', methods=['POST'])
def change_password():
    username = request.form.get('username')
    password = request.form.get('password')
    result = auth_service.change_password(username, password)
    print(result)


@app.route('/api/get_name', methods=['GET'])
def get_name():
    g_id = session.get('user_id')[0]['g_id']
    print(g_id)
    username = auth_service.get_user_name(g_id)[0]['name']
    print(username)
    return jsonify({'username': username})


@app.route('/api/export-excel', methods=['GET'])
def export_excel():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    print(start_date, end_date)
    excel_path = export_to_excel(start_date, end_date)
    print(excel_path)
    return send_file(excel_path, as_attachment=True, download_name=f'{start_date}-{end_date}.xlsx')


if __name__ == '__main__':
    app.run(port=5000, debug=True)

