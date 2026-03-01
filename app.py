from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["productivity_db"]
tasks_collection = db["tasks"]


# Home Page
@app.route("/")
def index():
    tasks = list(tasks_collection.find().sort("created_at", -1))
    return render_template("index.html", tasks=tasks)

# Add Task
@app.route("/add", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        task = {
            "title": request.form.get("title"),
            "priority": request.form.get("priority"),
            "status": "Pending",
            "created_at": datetime.now()
        }
        tasks_collection.insert_one(task)
        return redirect(url_for("index"))
    return render_template("add.html")

# Delete Task
@app.route("/delete/<task_id>")
def delete_task(task_id):
    tasks_collection.delete_one({"_id": ObjectId(task_id)})
    return redirect(url_for("index"))

# Toggle Status
@app.route("/toggle/<task_id>")
def toggle_status(task_id):
    task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    new_status = "Completed" if task["status"] == "Pending" else "Pending"
    tasks_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": {"status": new_status}}
    )
    return redirect(url_for("index"))

# Update Priority
@app.route("/update_priority/<task_id>", methods=["POST"])
def update_priority(task_id):
    new_priority = request.form.get("priority")
    tasks_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": {"priority": new_priority}}
    )
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)