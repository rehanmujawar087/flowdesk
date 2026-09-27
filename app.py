import csv
import io
import os
from flask import Flask, render_template, request, redirect, url_for, flash, Response

from services import supabase_service as fs
from services import task_utils

# Vercel serves static assets from public/** directly via its CDN, not
# through Flask. Pointing Flask's own static handler at the same public/
# folder (with an empty static_url_path) means url_for('static', ...)
# produces the same "/css/style.css"-style URL locally and in production,
# so templates don't need to change between environments.
app = Flask(__name__, static_folder="public", static_url_path="")

# Needed for flash messages. Uses an env var in production (set in Vercel
# project settings); falls back to a fixed dev-only value so local flash
# messages still work.
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-only-secret-key")


@app.route("/")
def index():
    """Dashboard page: stat cards + the overdue tasks list."""
    task_list = fs.get_tasks()

    for task in task_list:
        task["overdue"] = task_utils.is_overdue(task.get("deadline"), task.get("status"))

    stats = task_utils.get_dashboard_stats(task_list)
    overdue_tasks = [t for t in task_list if t["overdue"]]

    return render_template("index.html", stats=stats, overdue_tasks=overdue_tasks)


@app.route("/tasks")
def tasks():
    """Tasks page: shows the create-task form and the task table."""
    task_list = fs.get_tasks()
    for task in task_list:
        task["overdue"] = task_utils.is_overdue(task.get("deadline"), task.get("status"))
    employee_list = fs.get_employees()
    return render_template("tasks.html", tasks=task_list, employees=employee_list)


@app.route("/tasks/add", methods=["POST"])
def add_task_route():
    """Handle the create-task form submission."""
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    assigned_to = request.form.get("assigned_to", "").strip()
    priority = request.form.get("priority", "").strip()
    deadline = request.form.get("deadline", "").strip() or None

    if not title:
        flash("Task title cannot be empty.", "danger")
        return redirect(url_for("tasks"))

    if not assigned_to:
        flash("Please select an employee to assign this task to.", "danger")
        return redirect(url_for("tasks"))

    if priority not in ("High", "Medium", "Low"):
        flash("Please select a valid priority.", "danger")
        return redirect(url_for("tasks"))

    # Look up the employee's current name so the task can still display it
    # even if the employee is deleted later (assigned_to would become NULL,
    # but assigned_name is stored independently).
    employee_list = fs.get_employees()
    matching = [e for e in employee_list if e["id"] == assigned_to]

    if not matching:
        # Can happen if the employee was deleted after the form loaded but
        # before it was submitted. Without this check, inserting a task
        # with a non-existent assigned_to would violate the tasks table's
        # foreign key constraint and crash the request instead of failing
        # gracefully.
        flash("That employee no longer exists. Please choose another.", "danger")
        return redirect(url_for("tasks"))

    assigned_name = matching[0]["name"]

    fs.add_task(title, description, assigned_to, assigned_name, priority, deadline)
    flash(f"Task '{title}' created.", "success")
    return redirect(url_for("tasks"))


@app.route("/tasks/status/<task_id>", methods=["POST"])
def update_task_status_route(task_id):
    """Move a task to a new status (Pending -> In Progress -> Completed)."""
    new_status = request.form.get("new_status", "").strip()

    if new_status not in ("Pending", "In Progress", "Completed"):
        flash("Invalid status.", "danger")
        return redirect(url_for("tasks"))

    fs.update_task_status(task_id, new_status)
    flash("Task status updated.", "success")
    return redirect(url_for("tasks"))


@app.route("/tasks/delete/<task_id>", methods=["POST"])
def delete_task_route(task_id):
    """Delete a task by Supabase row id."""
    fs.delete_task(task_id)
    flash("Task deleted.", "success")
    return redirect(url_for("tasks"))


@app.route("/employees")
def employees():
    """Employees page: shows the add-employee form and the employee table."""
    employee_list = fs.get_employees()
    return render_template("employees.html", employees=employee_list)


@app.route("/employees/add", methods=["POST"])
def add_employee_route():
    """Handle the add-employee form submission."""
    name = request.form.get("name", "").strip()
    role = request.form.get("role", "").strip()

    if not name:
        flash("Employee name cannot be empty.", "danger")
    else:
        fs.add_employee(name, role)
        flash(f"Employee '{name}' added.", "success")

    return redirect(url_for("employees"))


@app.route("/employees/delete/<employee_id>", methods=["POST"])
def delete_employee_route(employee_id):
    """Delete an employee by Supabase row id."""
    fs.delete_employee(employee_id)
    flash("Employee deleted.", "success")
    return redirect(url_for("employees"))


@app.route("/export")
def export_tasks_csv():
    """Download all current tasks as a CSV file.

    Columns are named to match the EDA dataset's field names where the app
    actually tracks the equivalent data (see PROJECT_PLAN.md, section 15).
    Fields the app doesn't collect - department, estimated_hours,
    actual_hours, task_category - are not included here; those only exist
    in the separate synthetic EDA dataset.
    """
    task_list = fs.get_tasks()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "task_id", "task_title", "employee", "priority", "status",
        "created_date", "deadline", "completion_date",
    ])
    for task in task_list:
        writer.writerow([
            task.get("id"),
            task.get("title"),
            task.get("assigned_name") or "",
            task.get("priority"),
            task.get("status"),
            task.get("created_at"),
            task.get("deadline") or "",
            task.get("completed_at") or "",
        ])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=flowtask_tasks.csv"},
    )


@app.route("/analytics")
def analytics():
    """Analytics page (optional / nice-to-have)."""
    return render_template("analytics.html")


if __name__ == "__main__":
    # This block only runs for local development (`python app.py`).
    # On Vercel, the `app` object above is imported directly and this
    # block never executes.
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
