def fix():
    with open('Backend/app.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    start_idx = -1
    for i, l in enumerate(lines):
        if "def manage_users():" in l:
            start_idx = i
            break
            
    end_idx = -1
    for i, l in enumerate(lines):
        if "def handle_attendance():" in l:
            # go backwards to find the route decorator
            end_idx = i - 1
            break
            
    print(f"Replacing lines {start_idx} to {end_idx-1}")
    
    correct_block = """def manage_users():
    \"\"\"Create a new user (admin only)\"\"\"
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    # Validation
    required_fields = ['username', 'password', 'role', 'full_name']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
        
    if data['role'] not in ['admin', 'teacher', 'parent']:
        return jsonify({'error': 'Invalid role'}), 400
        
    try:
        query = \"\"\"
            INSERT INTO users (username, password_hash, email, role, full_name, phone_number)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        \"\"\"
        
        result = execute_query(
            query,
            (
                data['username'],
                hash_password(data['password']),
                data.get('email'),
                data['role'],
                data['full_name'],
                data.get('phone_number')
            ),
            fetch_one=True,
            commit=True
        )
        
        if result and 'id' in result:
            new_user_id = result['id']
            # If the new user is a parent and 'children' array is provided, insert them into students table
            if data['role'] == 'parent' and 'children' in data and isinstance(data['children'], list):
                import random
                import string
                for child in data['children']:
                    # Generate student ID (S + 4 random digits)
                    student_id = 'S' + ''.join(random.choices(string.digits, k=4))
                    execute_query(
                        \"\"\"
                        INSERT INTO students (student_id, full_name, grade_level, class_name, parent_id)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (student_id) DO NOTHING
                        \"\"\",
                        (
                            student_id,
                            child.get('full_name'),
                            child.get('grade_level'),
                            child.get('class_name'),
                            new_user_id
                        ),
                        commit=True
                    )
            
            elif data['role'] == 'teacher' and data.get('teacher_grade'):
                grade_taught = data['teacher_grade'] 
                from datetime import datetime
                curr_year = datetime.now().year
                subjects = ['English', 'Maths', 'Sesotho', 'Geography', 'Physical Science', 'Religion', 'Computer']
                for subj in subjects:
                    execute_query(
                        \"\"\"
                        INSERT INTO teacher_classes (teacher_id, grade_level, class_name, subject, academic_year, term)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING
                        \"\"\",
                        (new_user_id, grade_taught, 'A', subj, curr_year, 1),
                        commit=True
                    )

            return jsonify({'success': True, 'message': 'User created successfully', 'id': new_user_id})
        else:
            return jsonify({'error': 'Failed to create user'}), 500

    except Exception as e:
        print(f"Error creating user: {e}")
        return jsonify({'error': 'An error occurred'}), 500

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    \"\"\"Delete a user (admin only)\"\"\"
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Don't allow deleting yourself
    if user_id == session['user_id']:
        return jsonify({'error': 'Cannot delete your own account'}), 400
    
    result = execute_query(
        "UPDATE users SET is_active = false WHERE id = %s",
        (user_id,),
        commit=True
    )
    
    if result and result.get('rowcount', 0) > 0:
        return jsonify({'success': True, 'message': 'User deleted successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/api/students', methods=['GET'])
def get_students():
    \"\"\"Get students, optionally filtered by class or grade\"\"\"
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    class_name = request.args.get('class')
    grade_level = request.args.get('grade')
    
    query = "SELECT * FROM students WHERE is_active = true"
    params = []
    
    if class_name:
        query += " AND class_name = %s"
        params.append(class_name)
    elif grade_level:
        query += " AND grade_level = %s"
        params.append(grade_level)
    
    query += " ORDER BY full_name"
    
    students = execute_query(query, params, fetch_all=True)
    return jsonify(students if students else [])
"""

    if start_idx != -1 and end_idx != -1:
        new_lines = lines[:start_idx] + [correct_block + "\n"] + lines[end_idx:]
        with open('Backend/app.py', 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print("Fixed successfully!")

fix()
