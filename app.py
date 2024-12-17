from flask import Flask, render_template, request, redirect, url_for
import calendar
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

# データベースに接続する関数
def get_db_connection():
    conn = sqlite3.connect('calendar_app.db')
    conn.row_factory = sqlite3.Row  # レコードを辞書形式で取得
    return conn

@app.route('/', methods=['GET'])
def index():
    # GET パラメータから年と月を取得
    year = int(request.args.get('year', datetime.now().year))
    month = int(request.args.get('month', datetime.now().month))

    # 前月・次月のボタンが押された場合
    if 'prev_month' in request.args:
        if month == 1:
            year -= 1
            month = 12
        else:
            month -= 1
    elif 'next_month' in request.args:
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1

    # 前月・次月の年と月を計算
    if month == 1:
        prev_year = year - 1
        prev_month = 12
    else:
        prev_year = year
        prev_month = month - 1

    if month == 12:
        next_year = year + 1
        next_month = 1
    else:
        next_year = year
        next_month = month + 1

    # カレンダーを作成
    cal = calendar.Calendar(firstweekday=6)  # 日曜始まり
    month_days = cal.monthdayscalendar(year, month)

    # データベースからその月の予定を取得
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM events WHERE strftime("%Y-%m", date) = ?', (f'{year}-{month:02d}',))
    events = c.fetchall()  # その月の予定を取得
    conn.close()

    # 日別のイベントを辞書形式で整理
    event_dict = {}
    for event in events:
        day = int(event['date'].split('-')[2])  # 日付部分を抽出
        if day not in event_dict:
            event_dict[day] = []
        event_dict[day].append(event['description'])

    return render_template('calendar.html', year=year, month=month, 
                           prev_year=prev_year, prev_month=prev_month, 
                           next_year=next_year, next_month=next_month,
                           month_days=month_days, events=event_dict)

@app.route('/add_event', methods=['POST'])
def add_event():
    # フォームからデータを受け取る
    date = request.form['date']
    event_description = request.form['event']

    # データベースに予定を追加
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO events (date, description) VALUES (?, ?)', (date, event_description))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))  # カレンダー画面にリダイレクト

@app.route('/delete_event/<date>', methods=['POST'])
def delete_event(date):
    print(f"Deleting event for date: {date}")  # デバッグ用
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM events WHERE date = ?', (date,))
    conn.commit()
    conn.close()
    return '', 204  # 成功時に204 No Contentを返す

@app.route('/edit_event', methods=['POST'])
def edit_event():
    # フォームからデータを受け取る
    date = request.form['date']
    event_description = request.form['event']

    # データベースで予定を更新
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('UPDATE events SET description = ? WHERE date = ?', (event_description, date))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))  # 編集後にカレンダー画面にリダイレクト



if __name__ == '__main__':
    app.run(debug=True)
