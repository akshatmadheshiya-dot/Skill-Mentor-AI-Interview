import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add send_otp_email function
otp_func = """
def send_otp_email(receiver_email, otp):
    import os, smtplib
    from email.mime.text import MIMEText
    sender_email = os.getenv('EMAIL_USERNAME')
    sender_password = os.getenv('EMAIL_PASSWORD')
    if not sender_email or not sender_password:
        print("Email credentials not configured")
        return False
    try:
        msg = MIMEText(f"Your OTP for Skill Mentor is: {otp}")
        msg['Subject'] = 'Skill Mentor - OTP Verification'
        msg['From'] = sender_email
        msg['To'] = receiver_email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

"""

if "def send_otp_email" not in content:
    content = content.replace("@app.route('/forgot-password'", otp_func + "@app.route('/forgot-password'")

# Update login function
old_login = """
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_email'] = user['email']
            flash('Login successful!')
            return redirect(url_for('dashboard'))
"""
new_login = """
        if user and check_password_hash(user['password'], password):
            if not user['is_verified']:
                # Resend OTP
                import random
                otp = f"{random.randint(100000, 999999)}"
                db.execute('UPDATE users SET verification_token = ? WHERE id = ?', (otp, user['id']))
                db.commit()
                send_otp_email(user['email'], otp)
                session['temp_email'] = user['email']
                flash('Please verify your email first. A new OTP has been sent.', 'warning')
                return redirect(url_for('verify_registration'))

            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_email'] = user['email']
            flash('Login successful!')
            return redirect(url_for('dashboard'))
"""
content = content.replace(old_login, new_login)


# Update forgot-password, captcha, new-password
old_forgot_flow_pattern = r"@app\.route\('/forgot-password'.*?return render_template\('new_password\.html'\)"
new_forgot_flow = r"""@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        if not user:
            flash('Email not registered')
            return redirect(url_for('forgot_password'))

        # Generate and send OTP
        import random
        otp = f"{random.randint(100000, 999999)}"
        db.execute('UPDATE users SET verification_token = ? WHERE email = ?', (otp, email))
        db.commit()
        
        if send_otp_email(email, otp):
            session['reset_email'] = email
            flash('OTP sent to your email.')
            return redirect(url_for('verify_forgot_password'))
        else:
            flash('Failed to send OTP email. Try again later.')
            return redirect(url_for('forgot_password'))

    return render_template('gmail.html')

@app.route('/verify-forgot-password', methods=['GET', 'POST'])
def verify_forgot_password():
    if 'reset_email' not in session:
        return redirect(url_for('forgot_password'))

    email = session['reset_email']
    if request.method == 'POST':
        user_otp = request.form.get('otp', '').strip()
        db = get_db()
        user = db.execute('SELECT verification_token FROM users WHERE email = ?', (email,)).fetchone()
        
        if user and user['verification_token'] == user_otp:
            # Clear token and redirect to new password
            db.execute('UPDATE users SET verification_token = NULL WHERE email = ?', (email,))
            db.commit()
            return redirect(url_for('new_password'))
        else:
            flash('Invalid OTP. Try again.')
            return redirect(url_for('verify_forgot_password'))

    return render_template('verify_registration_otp.html', email=email)

@app.route('/new-password', methods=['GET', 'POST'])
def new_password():
    if 'reset_email' not in session:
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$'  # define regex here

        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('new_password'))

        import re
        if not re.match(password_regex, password):
            flash('Password must be at least 8 characters long, include uppercase, lowercase, number, and special character')
            return redirect(url_for('new_password'))

        from werkzeug.security import generate_password_hash
        hashed_password = generate_password_hash(password)
        db = get_db()
        db.execute('UPDATE users SET password = ? WHERE email = ?', (hashed_password, session['reset_email']))
        db.commit()
        session.pop('reset_email', None)

        flash('Password updated successfully! Please login.')
        return redirect(url_for('login'))

    return render_template('new_password.html')"""

content = re.sub(old_forgot_flow_pattern, lambda m: new_forgot_flow, content, flags=re.DOTALL)


# Update register
old_register_pattern = r"@app\.route\('/register', methods=\['GET', 'POST'\]\)\ndef register\(\):.*?return render_template\('register\.html'\)"
new_register = r"""@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']

        db = get_db()
        existing_user = db.execute('SELECT id, is_verified FROM users WHERE email = ?', (email,)).fetchone()

        # Email validation
        if not (email.endswith('gmail.com') or email.endswith('apsit.edu.in')):
            flash('Please enter a valid email address')
            return redirect(url_for('register'))

        if existing_user:
            if existing_user['is_verified']:
                flash('Email already exists')
                return redirect(url_for('register'))
            else:
                pass
        
        # Password validation
        import re
        password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if not re.match(password_regex, password):
            flash('Password must be at least 8 characters, include uppercase, lowercase, number, and special character')
            return redirect(url_for('register'))

        from werkzeug.security import generate_password_hash
        hashed_password = generate_password_hash(password)
        
        import random
        otp = f"{random.randint(100000, 999999)}"
        
        if existing_user:
            db.execute('UPDATE users SET name = ?, password = ?, verification_token = ? WHERE email = ?',
                       (name, hashed_password, otp, email))
        else:
            db.execute('INSERT INTO users (email, name, password, is_verified, verification_token) VALUES (?, ?, ?, 0, ?)',
                       (email, name, hashed_password, otp))
        db.commit()
        
        if send_otp_email(email, otp):
            session['temp_email'] = email
            flash('OTP sent to your email. Please verify to complete registration.')
            return redirect(url_for('verify_registration'))
        else:
            flash('Failed to send OTP email. Please try again later.')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/verify-registration', methods=['GET', 'POST'])
def verify_registration():
    if 'temp_email' not in session:
        return redirect(url_for('register'))

    email = session['temp_email']
    if request.method == 'POST':
        user_otp = request.form.get('otp', '').strip()
        db = get_db()
        user = db.execute('SELECT id, name, verification_token FROM users WHERE email = ?', (email,)).fetchone()
        
        if user and user['verification_token'] == user_otp:
            # Mark as verified
            db.execute('UPDATE users SET is_verified = 1, verification_token = NULL WHERE email = ?', (email,))
            db.commit()
            
            # Log in
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_email'] = email
            session.pop('temp_email', None)
            
            flash('Registration successful! Welcome to SkillMentor!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid OTP. Try again.')
            return redirect(url_for('verify_registration'))

    return render_template('verify_registration_otp.html', email=email)"""

content = re.sub(old_register_pattern, lambda m: new_register, content, flags=re.DOTALL)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Auth logic patched successfully!")
