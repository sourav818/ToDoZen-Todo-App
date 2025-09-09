from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory
from datetime import datetime
import os
import matplotlib.pyplot as plt
from twilio.rest import Client
import mysql.connector

app = Flask(__name__)

class TaskManager:
    def __init__(self):
        try:
            self.db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123@Sourav",
                database="todozen"
            )
            self.db_cursor = self.db_connection.cursor()
            print("Database connection successful!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.db_connection = None
            self.db_cursor = None

        # Twilio setup
        self.twilio_client = Client(
            "AC71f4632b631f5c5990277cbc87dae384",
            "8dd26447dc0ad53249dc8ecfd303a1e0"
        )
        self.twilio_phone_number = "+14173863760"
        self.user_phone_number = "+918822182793"

    def send_sms(self, message):
        """Send an SMS using Twilio."""
        try:
            self.twilio_client.messages.create(
                body=message,
                from_=self.twilio_phone_number,
                to=self.user_phone_number
            )
            print(f"📱 SMS sent: {message}")
        except Exception as e:
            print(f"⚠️ Failed to send SMS: {e}")

    def add_task(self, title, priority, deadline):
        """Add a task to the database."""
        try:
            deadline_dt = datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            return {"error": "Invalid deadline format. Use YYYY-MM-DD."}, 400

        query = """INSERT INTO tasks (Title, Priority, Completed, Deadline, RewardPoints) 
                   VALUES (%s, %s, %s, %s, %s)"""
        values = (title, priority.capitalize(), False, deadline_dt, 10)
        try:
            self.db_cursor.execute(query, values)
            self.db_connection.commit()

            self.send_sms(f'New Task Added: "{title}" with Priority: "{priority}" and Deadline: {deadline}')
            return {"message": "Task added successfully!"}, 200
        except Exception as e:
            print(f"Error adding task: {e}")
            return {"error": "Failed to add task."}, 500

    def get_tasks(self):
        """Retrieve tasks from the database."""
        try:
            self.db_cursor.execute("SELECT * FROM tasks")
            tasks = self.db_cursor.fetchall()
            return [
                {
                    "TaskID": task[0],
                    "Title": task[1],
                    "Priority": task[2],
                    "Completed": bool(task[3]),
                    "CreatedAt": task[4],
                    "Deadline": task[5],
                    "RewardPoints": task[6]
                }
                for task in tasks
            ]
        except Exception as e:
            print(f"Error retrieving tasks: {e}")
            return []

    def complete_task(self, task_id):
        """Mark a task as completed."""
        query = "UPDATE tasks SET Completed = %s WHERE TaskID = %s"
        values = (True, task_id)
        try:
            self.db_cursor.execute(query, values)
            self.db_connection.commit()
        except Exception as e:
            print(f"Error completing task: {e}")

    def generate_charts(self):
        """Generate and save visualization charts."""
        output_dir = os.path.join('static', 'images')
        os.makedirs(output_dir, exist_ok=True)

        self.save_task_completion_chart(os.path.join(output_dir, 'task-completion-chart.webp'))
        self.save_reward_points_chart(os.path.join(output_dir, 'reward-points-chart.webp'))
        print("Charts generated successfully!")

    def save_task_completion_chart(self, filepath):
        """Save a pie chart for task completion progress."""
        tasks = self.get_tasks()
        completed = sum(1 for task in tasks if task["Completed"])
        incomplete = len(tasks) - completed

        labels = ['Completed', 'Incomplete']
        sizes = [completed, incomplete]
        colors = ['#4CAF50', '#FF7043']

        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
        plt.title('Task Completion Progress')
        plt.savefig(filepath, format='webp')
        plt.close()

    def save_reward_points_chart(self, filepath):
        """Save a line chart for reward points progression."""
        tasks = self.get_tasks()
        if not tasks:
            plt.figure(figsize=(6, 6))
            plt.text(0.5, 0.5, "No Data Available", horizontalalignment='center', verticalalignment='center', fontsize=12)
            plt.savefig(filepath, format='webp')
            plt.close()
            return

        deadlines = [task["Deadline"] for task in tasks]
        reward_points = [task["RewardPoints"] for task in tasks]
        sorted_data = sorted(zip(deadlines, reward_points), key=lambda x: x[0])
        sorted_deadlines, sorted_rewards = zip(*sorted_data)

        plt.figure(figsize=(8, 4))
        plt.plot(sorted_deadlines, sorted_rewards, marker='o', color='#4CAF50', linestyle='-', linewidth=2)
        plt.title('Reward Points Progression Over Time')
        plt.xlabel('Deadline')
        plt.ylabel('Reward Points')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.savefig(filepath, format='webp')
        plt.close()

# Flask Routes

@app.route('/')
def home():
    return render_template('ToDoZen.html')

@app.route('/profile.html')
def redirect_profile_html():
    return redirect(url_for('profile_page'))

@app.route('/taskpage.html')
def redirect_taskpage_html():
    return redirect(url_for('task_page'))

@app.route('/profile')
def profile_page():
    user_id = 1  # Or fetch this from the logged-in user's session or data
    try:
        task_manager.db_cursor.execute("SELECT RewardPoints FROM users WHERE UserID = %s", (user_id,))
        updated_points = task_manager.db_cursor.fetchone()
        if updated_points:
            updated_points = updated_points[0]
        else:
            updated_points = 0  # If the user does not exist, set default points to 0.
    except Exception as e:
        print(f"Error fetching reward points: {e}")
        updated_points = 0  # Default to 0 if there's an error

    return render_template('profile.html', reward_points=updated_points)

@app.route('/taskpage')
def task_page():
    return render_template('taskpage.html')

@app.route('/add-task', methods=['POST'])
def add_task():
    data = request.json
    title = data.get('title')
    priority = data.get('priority')
    deadline = data.get('deadline')
    response, status = task_manager.add_task(title, priority, deadline)
    return jsonify(response), status

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = task_manager.get_tasks()
    return jsonify(tasks)

@app.route('/complete-task', methods=['POST'])
def complete_task():
    data = request.json
    task_id = data.get('task_id')

    if not task_id:
        return jsonify({"error": "Task ID is required"}), 400

    try:
        task_manager.db_cursor.execute("SELECT Title FROM tasks WHERE TaskID = %s", (task_id,))
        task = task_manager.db_cursor.fetchone()

        if task:
            task_title = task[0]
            task_manager.complete_task(task_id)
            task_manager.send_sms(f'Task "{task_title}" has been marked as completed! Well done!')
            task_manager.generate_charts()
            return jsonify({"message": "Task marked as completed and SMS sent"}), 200
        else:
            return jsonify({"error": "Task not found"}), 404
    except Exception as e:
        print(f"Error completing task: {e}")
        return jsonify({"error": "Failed to complete task"}), 500

@app.route('/claim-reward', methods=['POST'])
def claim_reward():
    print("Claim reward route accessed")  # Debugging line to check if the route is accessed
    data = request.json
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    try:
        # Reset the reward points to 0 after claiming the reward
        task_manager.db_cursor.execute(
            "UPDATE users SET RewardPoints = 0 WHERE UserID = %s", (user_id,)
        )
        task_manager.db_connection.commit()

        # Fetch the updated reward points (which should be 0 now)
        task_manager.db_cursor.execute("SELECT RewardPoints FROM users WHERE UserID = %s", (user_id,))
        updated_points = task_manager.db_cursor.fetchone()

        if updated_points:
            updated_points = updated_points[0]
        else:
            return jsonify({"error": "User not found"}), 404

        # Sending SMS after the reward is claimed and points are reset to 0
        task_manager.send_sms(f"Your reward has been successfully claimed! Your reward points have been reset to 0.")

        return jsonify({
            "message": "Reward claimed successfully, points reset to 0, and SMS sent!",
            "updated_reward_points": updated_points
        }), 200

    except Exception as e:
        print(f"Error claiming reward: {e}")
        return jsonify({"error": "Failed to claim reward"}), 500


@app.route('/generate-charts', methods=['GET'])
def generate_charts():
    task_manager.generate_charts()
    return jsonify({"message": "Charts generated and saved!"})

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    task_manager = TaskManager()
    task_manager.generate_charts()
    app.run(debug=True, port=8080, host='0.0.0.0', use_reloader=False)
