# FlowTask — Hackathon Project Specification

## 1. Project Overview

**Project Name:** FlowTask

**Tagline:**
Simple workflow management for small businesses.

**Project Type:**
Small Business Workflow & Task Management Platform

**Development Mode:**
Solo Hackathon MVP

**Target Development Time:**
Approximately 4 hours

---

# 2. Problem Statement

Small businesses often manage their daily operations using:

* WhatsApp messages
* Spreadsheets
* Phone calls
* Notebooks
* Verbal communication

This makes it difficult to track:

* Tasks
* Responsibilities
* Deadlines
* Priorities
* Pending work
* Completed work
* Employee workload
* Overdue tasks

There is a need for a simple centralized digital platform that helps small businesses organize their daily workflow.

---

# 3. Proposed Solution

FlowTask is a simple web-based workflow and task management platform.

It allows small businesses to:

* Create tasks
* Assign tasks to employees
* Set priorities
* Set deadlines
* Update task status
* Identify overdue tasks
* Manage employees
* Monitor productivity
* Analyze workflow data

The goal is not to build a complex enterprise system.

The goal is to build a practical MVP that solves the core workflow problem.

---

# 4. Core Workflow

The main workflow is:

```text
Create Task
     ↓
Assign Employee
     ↓
Set Priority
     ↓
Set Deadline
     ↓
Track Status
     ↓
Completed / Overdue
     ↓
Dashboard Statistics
     ↓
EDA / Business Insights
```

---

# 5. Technology Stack

## Frontend

* HTML
* CSS
* JavaScript
* Bootstrap

## Backend

* Python
* Flask

## Database

* Supabase (PostgreSQL), accessed from Flask using the official `supabase` Python client

## Data Analysis

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Jupyter Notebook / Google Colab

## Deployment

* Vercel (Flask served as a Python serverless function)

## Version Control

* Git
* GitHub

---

# 6. Architecture

The main architecture should be:

```text
                 USER
                   |
                   v
          +----------------+
          | Web Browser    |
          | HTML/CSS/JS    |
          +-------+--------+
                  |
                  v
          +----------------+
          | Flask Backend  |
          | Python         |
          +-------+--------+
                  |
                  v
          +----------------+
          | Supabase       |
          | (PostgreSQL)   |
          +----------------+
                  |
                  v
          +----------------+
          | Vercel         |
          | (Serverless)   |
          +----------------+
```

Analytics flow:

```text
Supabase (PostgreSQL)
    |
    v
Task Data
    |
    v
CSV / Dataset
    |
    v
Python + Pandas
    |
    v
EDA
    |
    v
Charts + Insights
```

---

# 7. Application Pages

The application should have these main sections:

```text
Dashboard
Tasks
Employees
Analytics
```

Optional pages should only be added if they do not affect the core MVP.

---

# 8. Dashboard

The dashboard is the main screen.

It should display:

* Total Tasks
* Pending Tasks
* In Progress Tasks
* Completed Tasks
* Overdue Tasks
* Completion Rate

Example:

```text
+----------------+----------------+----------------+
| Total Tasks    | Pending        | In Progress    |
|      25        |      10        |       7        |
+----------------+----------------+----------------+

+----------------+----------------+----------------+
| Completed      | Overdue        | Completion     |
|       8        |       3        | Rate: 32%     |
+----------------+----------------+----------------+
```

The values must come from actual database records.

Do not hardcode dashboard statistics.

---

# 9. Task Management

## 9.1 Create Task

The task creation form should contain:

* Task Title
* Description
* Assigned Employee
* Priority
* Deadline

Default status:

```text
Pending
```

---

## 9.2 Task Assignment

Tasks must be assigned to employees stored in Supabase (PostgreSQL).

The employee dropdown should dynamically load employees.

Do not hardcode employee names into the frontend.

---

## 9.3 Priority

Use:

```text
High
Medium
Low
```

---

## 9.4 Status

Use:

```text
Pending
In Progress
Completed
```

Basic workflow:

```text
Pending
   ↓
In Progress
   ↓
Completed
```

---

## 9.5 Deadline

Every task can have a deadline.

Use proper date handling.

Do not hardcode dates.

---

# 10. Overdue Task Detection

A task is considered overdue when:

```text
deadline < current date
```

AND:

```text
status != Completed
```

Example:

```text
Deadline: 25 September
Today: 27 September
Status: Pending
```

Result:

```text
OVERDUE
```

A completed task should not be displayed as overdue even if its deadline has passed.

**Note (Supabase/PostgreSQL):** unlike the earlier Firestore-based design, this
condition can be expressed as a single SQL `WHERE` clause
(`deadline < CURRENT_DATE AND status != 'Completed'`) — no need to fetch all
tasks and filter in Python.

---

# 11. Employee Management

Employee fields:

```text
name
role
created_at
```

Required operations:

* Add Employee
* View Employees
* Delete Employee

Example:

```text
Rahul     Sales
Amit      Inventory
Sneha     Accounts
Priya     Operations
Akash     Manager
```

The application must use actual Supabase (PostgreSQL) employee records.

---

# 12. Database (Supabase / PostgreSQL)

Use two tables.

## Table: employees

Example columns:

```text
employees
    |
    +-- id (primary key)
          |
          +-- name
          +-- role
          +-- created_at
```

---

## Table: tasks

Example columns:

```text
tasks
    |
    +-- id (primary key)
          |
          +-- title
          +-- description
          +-- assigned_to
          +-- priority
          +-- status
          +-- deadline
          +-- created_at
```

Do not create unnecessary tables.

---

# 13. Dashboard Calculations

The dashboard should calculate:

## Total Tasks

```text
Total Tasks = number of task records
```

## Pending

```text
status == Pending
```

## In Progress

```text
status == In Progress
```

## Completed

```text
status == Completed
```

## Overdue

```text
deadline < today
AND
status != Completed
```

## Completion Rate

```text
Completion Rate =
Completed Tasks / Total Tasks × 100
```

If total tasks is zero:

```text
Completion Rate = 0%
```

Avoid division-by-zero errors.

---

# 14. Search and Filtering

If time permits, implement:

* Task search
* Status filter
* Priority filter
* Employee filter

These are optional.

Do not sacrifice core functionality for filters.

---

# 15. Dataset Requirement

FlowTask must include a relevant dataset for EDA.

The dataset must represent task/workflow management.

Do not use an unrelated dataset.

Possible fields:

```text
task_id
task_title
employee
department
priority
status
created_date
deadline
completion_date
estimated_hours
actual_hours
task_category
```

---

# 16. Public Dataset vs Synthetic Dataset

First check whether a suitable public dataset can be verified.

If a suitable public dataset exists:

* Use the actual dataset.
* Record its source.
* Mention the source in README.
* Do not misrepresent the dataset.

If no suitable dataset can be verified:

Create a clearly labeled:

```text
Synthetic Demo Dataset
```

Do not claim synthetic data is real-world data.

---

# 17. Dataset Size

For the MVP, a synthetic dataset can contain approximately:

```text
100–500 records
```

The exact number is not important.

The dataset should contain enough variation to demonstrate EDA.

Include different:

* Employees
* Departments
* Priorities
* Statuses
* Categories
* Dates
* Completion times
* Estimated hours
* Actual hours

---

# 18. EDA Notebook

Create:

```text
analysis/
    flowtask_eda.ipynb
```

Optional:

```text
data/
    sample_tasks.csv
```

---

# 19. EDA Steps

The notebook should contain the following sections.

## 19.1 Import Libraries

Use:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
```

---

## 19.2 Load Dataset

Display:

* First 5 rows
* Last 5 rows
* Shape
* Column names

---

## 19.3 Data Information

Check:

* Data types
* Missing values
* Duplicate records

---

## 19.4 Data Cleaning

Handle:

* Missing values
* Duplicate records
* Incorrect data types
* Date conversion

Explain each cleaning step.

---

# 20. Descriptive Statistics

Calculate appropriate:

* Mean
* Median
* Minimum
* Maximum
* Standard deviation

for numerical fields.

For example:

```text
estimated_hours
actual_hours
```

---

# 21. Univariate Analysis

Analyze:

### Task Status

```text
Pending
In Progress
Completed
```

### Priority

```text
High
Medium
Low
```

### Employee Distribution

Number of assigned tasks per employee.

### Task Category

Number of tasks per category.

---

# 22. Bivariate Analysis

Analyze relationships such as:

```text
Employee vs Status
Priority vs Status
Department vs Workload
Estimated Hours vs Actual Hours
Priority vs Overdue
```

---

# 23. Time Analysis

Analyze:

* Tasks created over time
* Tasks completed over time
* Deadline patterns

Create appropriate line/bar charts.

---

# 24. Overdue Analysis

Calculate:

```text
Overdue Rate =
Overdue Tasks / Total Tasks × 100
```

Analyze overdue tasks by:

* Priority
* Employee
* Category

Use neutral descriptions.

Example:

> High-priority tasks represent 40% of overdue tasks in this dataset.

Do not make unsupported conclusions.

---

# 25. Productivity Analysis

Calculate:

```text
Completion Rate =
Completed Tasks / Total Tasks × 100
```

Also analyze:

* Assigned workload
* Completed tasks
* Pending tasks
* In-progress tasks

Do not describe an employee as "best" or "worst".

Use factual wording:

> Employee A has 15 assigned tasks in this dataset.

---

# 26. Required EDA Charts

Create useful charts such as:

1. Task Status Distribution
2. Priority Distribution
3. Employee Workload
4. Employee Workload vs Completed Tasks
5. Overdue Tasks by Priority
6. Task Category Distribution
7. Tasks Created Over Time
8. Estimated Hours vs Actual Hours

Do not create unnecessary charts.

---

# 27. Optional Analytics Page

If time permits, create an Analytics page in the web application.

Show:

* Total Tasks
* Completion Rate
* Overdue Rate
* Average Completion Time

And charts:

* Status Distribution
* Priority Distribution
* Employee Workload

The main application and deployment have higher priority than the analytics page.

---

# 28. CSV Export

If practical, add:

```text
Export Tasks as CSV
```

The exported data should contain the current task records.

Preferred flow:

```text
FlowTask
   ↓
Supabase (PostgreSQL)
   ↓
Task Records
   ↓
CSV
   ↓
EDA
```

If this takes too much time, keep EDA based on the prepared dataset.

---

# 29. Project Structure

Recommended structure:

```text
flowtask/
│
├── app.py
├── requirements.txt
├── vercel.json
├── .env                 (local only, git-ignored)
├── .env.example         (committed, no real values)
├── README.md
├── PROJECT_PLAN.md
├── .gitignore
│
├── templates/
│   ├── index.html
│   ├── tasks.html
│   ├── employees.html
│   └── analytics.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── app.js
│
├── services/
│   └── supabase_service.py
│
├── data/
│   └── sample_tasks.csv
│
└── analysis/
    └── flowtask_eda.ipynb
```

The structure can be simplified if necessary. The exact Vercel entry-point
convention (e.g. a `vercel.json` rewrite to `app.py`, or an `api/` directory,
depending on the Vercel Python runtime being used) will be confirmed against
current Vercel documentation when the deployment step is implemented, rather
than assumed here.

---

# 30. Security Requirements

Never commit:

```text
.env
SUPABASE_URL
SUPABASE_KEY
API keys
passwords
tokens
private credentials
```

Credentials:

* `SUPABASE_URL` and `SUPABASE_KEY` (the server-side secret/service role key)
  are read from environment variables only.
* Locally: stored in `.env` (git-ignored), loaded by the Flask app.
* In production: set in Vercel project settings (Environment Variables),
  never committed to the repository.
* `SUPABASE_KEY` is a server-side secret. It must never be sent to the
  browser, embedded in frontend JavaScript, or exposed via any API response.
  All Supabase reads/writes happen inside Flask (server-side) only.

Do not hardcode credentials.

---

# 31. Docker (Optional / Future Improvement Only)

Docker is **not** required for this deployment approach. The application
deploys to Vercel directly from source (Python serverless function), so
there is no Dockerfile, no manual `PORT` binding, and no container build
step in the MVP path.

Docker/Cloud Run containerization may be listed under README "Future
Improvements" as a possible alternative deployment path, but it is not part
of the MVP build or the submission requirements.

---

# 32. Vercel Deployment

The final application MUST be deployed to:

```text
Vercel
```

Deployment flow:

```text
Source Code (GitHub repo)
    ↓
Vercel Project (imports the repo)
    ↓
Vercel Build (installs requirements.txt, runs Flask as a Python
              serverless function per vercel.json / project settings)
    ↓
Public URL
```

Environment variables (`SUPABASE_URL`, `SUPABASE_KEY`) are configured in the
Vercel project settings, not in source code.

The final URL must be accessible to the hackathon jury.

Do not claim deployment is successful until the URL is actually tested.

Exact Vercel CLI/config details (e.g. `vercel.json` structure, Python runtime
version pinning) will be verified against current Vercel documentation at
the deployment step rather than assumed now.

---

# 33. GitHub

The final repository must be public.

It must contain:

* Complete source code
* README
* PROJECT_PLAN.md
* requirements.txt
* `vercel.json` (Vercel deployment configuration)
* `.env.example` (documents required variable names, no real values)
* EDA notebook
* Dataset or dataset instructions
* Templates
* Static files

Do not upload credentials. `.env` must never be committed.

---

# 34. README Requirements

README.md must contain:

## Project Name

FlowTask

## Problem Statement

Explain the problem.

## Solution

Explain FlowTask.

## Features

List implemented features only.

## Technology Stack

List actual technologies.

## Architecture

Include the system architecture.

## Dataset

Explain whether the dataset is:

* Public
* Synthetic
* Application-generated

## EDA

Explain:

* Cleaning
* Statistics
* Charts
* Insights

## Local Setup

Provide actual working commands.

## Supabase Setup

Explain the required configuration (project creation, table creation,
obtaining `SUPABASE_URL` / `SUPABASE_KEY`, setting them locally in `.env`).

## Vercel Deployment

Explain the actual deployment method used, and how environment variables
were configured in the Vercel project.

## Screenshots

Add screenshots.

## Demo URL

Add the verified Vercel deployment URL.

## GitHub

Add the verified repository URL.

## Future Improvements

Clearly distinguish future features from implemented features. May mention
Docker/Cloud Run as an alternative deployment path not used in this MVP.

---

# 35. Development Rules for Claude Code

Claude Code must:

1. Inspect the current code before modifying it.
2. Keep existing working functionality.
3. Avoid unnecessary technologies.
4. Avoid unnecessary files.
5. Use beginner-friendly code.
6. Run tests/checks after major changes.
7. Fix actual errors.
8. Never fabricate commands.
9. Never fabricate dataset sources.
10. Never fabricate EDA results.
11. Never expose secrets.
12. Never claim something works unless it has been tested.

---

# 36. Development Order

Follow this order.

```text
STEP 1
Project Setup
        ↓
STEP 2
Flask Application
        ↓
STEP 3
Supabase (PostgreSQL)
        ↓
STEP 4
Dashboard
        ↓
STEP 5
Task Management
        ↓
STEP 6
Employee Management
        ↓
STEP 7
Overdue Detection
        ↓
STEP 8
Productivity Statistics
        ↓
STEP 9
Dataset
        ↓
STEP 10
EDA
        ↓
STEP 11
Testing
        ↓
STEP 12
Vercel Deployment
        ↓
STEP 13
GitHub
        ↓
STEP 14
README
        ↓
STEP 15
Poster
        ↓
STEP 16
Social Media
```

---

# 37. 4-Hour Priority Plan

## 0:00–0:20

Project setup.

## 0:20–0:50

Flask backend.

## 0:50–1:20

Supabase (PostgreSQL) setup and connection.

## 1:20–2:10

Task management.

## 2:10–2:40

Status, priority and deadlines.

## 2:40–3:10

Dashboard.

## 3:10–3:30

Overdue detection and statistics.

## 3:30–3:45

UI polish.

## 3:45–4:00

Deployment/testing.

EDA should be completed only after the core application is functional.

---

# 38. Feature Priority

## MUST HAVE

* Task creation
* Task assignment
* Priority
* Deadline
* Status
* Dashboard
* Supabase (PostgreSQL) persistence
* Vercel deployment

## SHOULD HAVE

* Employee management
* Overdue detection
* Productivity statistics

## NICE TO HAVE

* Search
* Filters
* CSV export
* Analytics page
* Charts
* Dark mode
* Animations

If time becomes limited, skip NICE TO HAVE features.

---

# 39. Demo Flow

The live demonstration should take approximately 2–3 minutes.

### Step 1

Open the Vercel deployment URL.

### Step 2

Show:

```text
Total Tasks
Pending
In Progress
Completed
Overdue
Completion Rate
```

### Step 3

Create an employee.

### Step 4

Create a task.

Example:

```text
Task:
Prepare customer quotation

Employee:
Rahul

Priority:
High

Deadline:
Tomorrow
```

### Step 5

Show the task in the task list.

### Step 6

Change:

```text
Pending
   ↓
In Progress
```

### Step 7

Change:

```text
In Progress
   ↓
Completed
```

### Step 8

Show dashboard statistics changing.

### Step 9

Show an overdue task.

### Step 10

Show the EDA/analytics.

---

# 40. Project Pitch

Use this basic explanation:

> Small businesses often manage daily work through WhatsApp, spreadsheets, calls and notebooks. This makes it difficult to know what needs to be done, who is responsible, and which tasks are overdue.
>
> FlowTask provides a centralized workflow platform where businesses can create tasks, assign employees, set priorities and deadlines, track status, identify overdue work and view productivity statistics.
>
> The task data can also be analyzed using EDA to provide basic operational insights.

Do not claim capabilities that are not implemented.

---

# 41. Poster Content

Poster should contain:

## FLOWTASK

### Simple workflow management for small businesses.

### Problem

Scattered task management through:

WhatsApp + Excel + Calls + Notebooks

### Solution

One centralized workflow platform.

### Features

* Task Creation
* Task Assignment
* Priority
* Deadlines
* Status Tracking
* Overdue Detection
* Employee Management
* Dashboard
* Productivity Analytics
* EDA

### Technology

HTML
CSS
JavaScript
Bootstrap
Python
Flask
Supabase (PostgreSQL)
Pandas
NumPy
Matplotlib
Seaborn
Vercel

---

# 42. Social Media Requirements

The project post should mention:

Flora Institute of Technology

@gdg.fit.pune

@the_flora_institutes

Required hashtags:

#FITFEST2026
#FITFESTHACKATHON
#GDGFITPUNE
#GDGPUNE
#FLORAINSTITUTES
#FLORAINSTITUTEOFTECHNOLOGY
#HACKATHON2026
#PUNEHACKATHON
#STUDENTHACKATHON
#SOLOHACKATHON
#TECHHACKATHON

Do not invent URLs.

Use the actual verified GitHub and deployment URLs.

---

# 43. Final Submission Checklist

Before submission:

## Application

* [ ] Dashboard works
* [ ] Task creation works
* [ ] Task assignment works
* [ ] Priority works
* [ ] Deadline works
* [ ] Status works
* [ ] Overdue detection works
* [ ] Employee management works
* [ ] Statistics work
* [ ] Supabase (PostgreSQL) persistence works

## EDA

* [ ] Dataset available
* [ ] Dataset source documented
* [ ] EDA notebook works
* [ ] Data cleaning completed
* [ ] Charts generated
* [ ] Statistics calculated from actual data
* [ ] No fabricated insights

## Deployment

* [ ] Vercel deployment works
* [ ] Public URL works
* [ ] Supabase works in production (Vercel)
* [ ] Environment variables configured in Vercel project settings (not committed)

## GitHub

* [ ] Repository is public
* [ ] Source code uploaded
* [ ] README complete
* [ ] No credentials committed
* [ ] Screenshots added

## Submission

* [ ] GitHub URL
* [ ] Vercel deployment URL
* [ ] Social media post URL
* [ ] Project poster
* [ ] Documentation

---

# 44. Important Instruction to Claude Code

This file is the project specification.

When working on FlowTask:

* Read this file before major implementation decisions.
* Follow the development order.
* Prioritize the MVP.
* Do not implement unnecessary features.
* Do not fabricate information.
* Do not fabricate dataset sources.
* Do not fabricate statistics.
* Do not expose credentials.
* Test before declaring a feature complete.

Build the project incrementally.

The final objective is:

```text
WORKING WEB APPLICATION
        +
SUPABASE (POSTGRESQL)
        +
EDA
        +
VERCEL DEPLOYMENT
        +
PUBLIC GITHUB
        +
DOCUMENTATION
```

The application must be functional and demonstrable, not just a prototype mockup.
