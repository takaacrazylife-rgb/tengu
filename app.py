from flask import Flask, render_template, request, session, redirect, url_for, jsonify, Response
from flask_compress import Compress
import json, threading
from datetime import datetime, timedelta
from database import init_db, get_or_create_user, get_profile, save_profile
from database import get_active_session, create_session, get_session_messages, append_message, end_session, all_users
from llm import chat, extract_profile_update, is_ollama_ready, build_opening_message, generate_daily_question, generate_portrait

app = Flask(__name__)
app.secret_key = 'nexus-local-secret-2026'

# gzip — критично для пользователей через VPN, экономит ~75% трафика
Compress(app)

# Кеш статики на 1 день в браузере
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 86400

# Сколько сообщений показывать при загрузке страницы (остальные подгружаются скроллом)
INITIAL_MESSAGES_LIMIT = 30

init_db()

# ── AUTH ─────────────────────────────────────────────────────────────────────

@app.route('/', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('chat_page'))
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip().lower()
        if not username:
            error = 'Введи имя'
        elif len(username) < 2:
            error = 'Имя слишком короткое'
        else:
            user = get_or_create_user(username)
            session['user_id'] = user['id']
            session['username'] = username
            return redirect(url_for('chat_page'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    _save_session_profile()
    session.clear()
    return redirect(url_for('login'))

# ── CHAT ─────────────────────────────────────────────────────────────────────

@app.route('/chat')
def chat_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    username = session['username']
    profile = get_profile(user_id)

    # New user without onboarding → redirect
    if profile.get('session_count', 0) == 0 and not profile.get('onboarding_done'):
        return redirect(url_for('onboarding'))

    # restore or create session
    active = get_active_session(user_id)
    if not active:
        session_id = create_session(user_id)
    else:
        session_id = active['id']
    session['session_id'] = session_id

    all_messages = get_session_messages(session_id)

    # Первое сообщение от TENGU — снимает барьер страха
    if not all_messages:
        opening = build_opening_message(username, profile)
        append_message(session_id, 'assistant', opening)
        all_messages = get_session_messages(session_id)

    # Рендерим только последние N сообщений — старые подгружаются по запросу
    total_messages = len(all_messages)
    messages = all_messages[-INITIAL_MESSAGES_LIMIT:]
    has_older = total_messages > INITIAL_MESSAGES_LIMIT

    # Ежедневный вопрос — если прошло 20+ часов с последнего визита
    daily_q = None
    last_seen = profile.get('last_seen')
    if last_seen and profile.get('session_count', 0) > 0:
        try:
            last_dt = datetime.fromisoformat(last_seen)
            if datetime.now() - last_dt > timedelta(hours=20):
                daily_q = generate_daily_question(profile)
        except Exception:
            pass

    # Обновляем last_seen
    profile['last_seen'] = datetime.now().isoformat()
    save_profile(user_id, profile)

    model_ready = is_ollama_ready()

    return render_template('chat.html',
        username=username,
        messages=messages,
        profile=profile,
        model_ready=model_ready,
        session_count=profile.get('session_count', 0),
        daily_q=daily_q,
        has_older=has_older,
        total_messages=total_messages
    )

@app.route('/messages/older')
def older_messages():
    if 'user_id' not in session:
        return jsonify({'error': 'not logged in'}), 401
    session_id = session.get('session_id')
    if not session_id:
        return jsonify({'messages': []})
    before = int(request.args.get('before', INITIAL_MESSAGES_LIMIT))
    limit = 30
    all_messages = get_session_messages(session_id)
    end = max(0, len(all_messages) - before)
    start = max(0, end - limit)
    return jsonify({
        'messages': all_messages[start:end],
        'has_older': start > 0
    })

@app.route('/send', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return jsonify({'error': 'not logged in'}), 401

    data = request.get_json()
    user_text = (data.get('message') or '').strip()
    if not user_text:
        return jsonify({'error': 'empty'}), 400

    user_id = session['user_id']
    session_id = session.get('session_id')
    username = session['username']

    if not session_id:
        session_id = create_session(user_id)
        session['session_id'] = session_id

    profile = get_profile(user_id)
    append_message(session_id, 'user', user_text)
    messages = get_session_messages(session_id)

    reply = chat(messages, profile, username)
    append_message(session_id, 'assistant', reply)

    # auto-update profile every 6 user messages silently in background
    total = profile.get('total_messages', 0) + 1
    if total % 6 == 0:
        threading.Thread(target=_bg_profile_update, args=(user_id, session_id, profile), daemon=True).start()

    return jsonify({'reply': reply})

def _bg_profile_update(user_id, session_id, current_profile):
    messages = get_session_messages(session_id)
    updated = extract_profile_update(messages, current_profile)
    save_profile(user_id, updated)

def _save_session_profile():
    user_id = session.get('user_id')
    session_id = session.get('session_id')
    if user_id and session_id:
        profile = get_profile(user_id)
        messages = get_session_messages(session_id)
        if messages:
            updated = extract_profile_update(messages, profile)
            save_profile(user_id, updated)
            end_session(session_id)

@app.route('/new_session', methods=['POST'])
def new_session():
    if 'user_id' not in session:
        return jsonify({'error': 'not logged in'}), 401
    _save_session_profile()
    session_id = create_session(session['user_id'])
    session['session_id'] = session_id
    return jsonify({'ok': True})

# ── PROFILE ──────────────────────────────────────────────────────────────────

@app.route('/profile')
def profile_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    profile = get_profile(session['user_id'])
    return render_template('profile.html', profile=profile, username=session['username'])

@app.route('/profile/save', methods=['POST'])
def save_profile_route():
    if 'user_id' not in session:
        return jsonify({'error': 'not logged in'}), 401
    data = request.get_json()
    profile = get_profile(session['user_id'])
    allowed = ['notes', 'style', 'pace', 'depth', 'analogies', 'fears', 'strengths']
    for key in allowed:
        if key in data:
            profile[key] = data[key]
    save_profile(session['user_id'], profile)
    return jsonify({'ok': True})

# ── ADMIN ────────────────────────────────────────────────────────────────────

@app.route('/admin')
def admin():
    if session.get('username') != 'lem':
        return redirect(url_for('login'))
    users = all_users()
    for u in users:
        try:
            u['profile'] = json.loads(u.get('profile_data') or '{}')
        except Exception:
            u['profile'] = {}
    return render_template('admin.html', users=users)

# ── PORTRAIT ─────────────────────────────────────────────────────────────────

@app.route('/portrait')
def portrait_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    profile = get_profile(session['user_id'])
    portrait = profile.get('portrait')
    return render_template('portrait.html',
        username=session['username'],
        portrait=portrait
    )

@app.route('/portrait/generate', methods=['POST'])
def portrait_generate():
    if 'user_id' not in session:
        return jsonify({'error': 'not logged in'}), 401
    user_id = session['user_id']
    session_id = session.get('session_id')
    if not session_id:
        active = get_active_session(user_id)
        if active:
            session_id = active['id']
    if not session_id:
        return jsonify({'error': 'no session'}), 400
    messages = get_session_messages(session_id)
    profile = get_profile(user_id)
    portrait = generate_portrait(messages, profile, session['username'])
    if not portrait or portrait.get('error'):
        return jsonify({'error': (portrait or {}).get('error') or 'Нужно минимум 3 сообщения для портрета'}), 400
    profile['portrait'] = portrait
    save_profile(user_id, profile)
    return jsonify(portrait)

# ── PITCH ────────────────────────────────────────────────

@app.route('/pitch')
def pitch():
    return render_template('pitch.html')

@app.route('/plan')
def plan():
    return render_template('plan.html')

@app.route('/demo')
def demo():
    return render_template('demo.html')

# ── ONBOARDING ───────────────────────────────────────────────────────────────

@app.route('/onboarding', methods=['GET', 'POST'])
def onboarding():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        data = request.get_json()
        topics = data.get('topics', [])
        profile = get_profile(session['user_id'])
        profile['topics'] = topics
        profile['onboarding_done'] = True
        save_profile(session['user_id'], profile)
        return jsonify({'ok': True})
    return render_template('onboarding.html', username=session['username'])

# ── STATUS ───────────────────────────────────────────────────────────────────

@app.route('/status')
def status():
    return jsonify({'ollama': is_ollama_ready(), 'ok': True})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=7070, threaded=True)
