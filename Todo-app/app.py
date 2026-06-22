from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3


app = Flask(__name__)
# A secret key is required by Flask to use flash sessions safely
app.secret_key = "super_secret_todo_key"
DB_Name = "TODO.db"


def init_db():
    """ Create the table todos if it doesn't exist and run column migrations. """
    with sqlite3.connect(DB_Name) as conn:
        cursor = conn.cursor()
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS todos(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       task TEXT NOT NULL
                )
        ''')
        
        # Add columns dynamically if they do not exist
        columns_to_add = [
            ("due_date", "TEXT"),
            ("priority", "TEXT DEFAULT 'Medium'"),
            ("completed", "INTEGER DEFAULT 0"),
            ("created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        ]
        
        for col_name, col_type in columns_to_add:
            try:
                cursor.execute(f"ALTER TABLE todos ADD COLUMN {col_name} {col_type}")
            except sqlite3.OperationalError:
                # Column already exists, safe to ignore
                pass
                
        conn.commit()


init_db()


#------routes------


@app.route('/')
def index():
    """ READ: Fetch all tasks and display them. """
    try:
        with sqlite3.connect(DB_Name) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            # Order by: Pending first (completed=0), then by Priority (High -> Medium -> Low), then by Due Date
            cursor.execute("""
                SELECT * FROM todos 
                ORDER BY completed ASC, 
                CASE priority 
                    WHEN 'High' THEN 1 
                    WHEN 'Medium' THEN 2 
                    WHEN 'Low' THEN 3 
                    ELSE 4 
                END ASC, 
                due_date ASC
            """)
            tasks = [dict(row) for row in cursor.fetchall()]
            
            # Calculate task stats for the UI header
            total = len(tasks)
            completed_count = sum(1 for t in tasks if t['completed'] == 1)
            pending_count = total - completed_count
    except Exception as e:
        flash(f"Error loading tasks: {str(e)}", "danger")
        tasks = []
        total = completed_count = pending_count = 0
        
    return render_template('index.html', tasks=tasks, total=total, completed=completed_count, pending=pending_count)


@app.route('/add', methods=['POST'])
def add():
    """Create: Add a new task to DB with extra fields"""
    task_content = request.form.get('task')
    due_date = request.form.get('due_date') or None
    priority = request.form.get('priority') or 'Medium'
    
    if task_content:
        try:
            with sqlite3.connect(DB_Name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO todos (task, due_date, priority, completed) VALUES (?, ?, ?, 0)',
                    (task_content, due_date, priority)
                )
                conn.commit()
            flash("✨ Task added successfully!", "success")
        except Exception as e:
            flash(f"❌ Failed to add task: {str(e)}", "danger")
    else:
        flash("⚠️ Task cannot be empty!", "warning")
    return redirect(url_for('index'))


@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    """UPDATE: Modify an existing task's data."""
    new_content = request.form.get('new-task')
    due_date = request.form.get('due_date') or None
    priority = request.form.get('priority') or 'Medium'
    
    if new_content:
        try:
            with sqlite3.connect(DB_Name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE todos SET task=?, due_date=?, priority=? WHERE id=?",
                    (new_content, due_date, priority, id)
                )
                conn.commit()
            flash("🔄 Task updated successfully!", "info")
        except Exception as e:
            flash(f"❌ Failed to update task: {str(e)}", "danger")
    else:
        flash("⚠️ Task text cannot be empty!", "warning")
    return redirect(url_for('index'))


@app.route('/toggle/<int:id>')
def toggle(id):
    """TOGGLE: Mark a task as completed or pending."""
    try:
        with sqlite3.connect(DB_Name) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT completed FROM todos WHERE id=?", (id,))
            row = cursor.fetchone()
            if row:
                new_status = 1 if row['completed'] == 0 else 0
                cursor.execute("UPDATE todos SET completed=? WHERE id=?", (new_status, id))
                conn.commit()
                status_str = "completed" if new_status else "active"
                flash(f"Task marked as {status_str}!", "success")
            else:
                flash("⚠️ Task not found!", "warning")
    except Exception as e:
        flash(f"❌ Failed to toggle task status: {str(e)}", "danger")
    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete(id):
    """DELETE: Deleting an existing task's data."""
    try:
        with sqlite3.connect(DB_Name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM todos WHERE id=?", (id,))
            conn.commit()
        flash("🗑️ Task deleted successfully!", "danger")
    except Exception as e:
        flash(f"❌ Failed to delete task: {str(e)}", "danger")
    return redirect(url_for('index'))




if __name__ == '__main__':
    app.run(debug=True)
