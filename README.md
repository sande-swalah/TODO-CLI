# ✅ TODO CLI — Project Management Tool

A fully interactive Python CLI application for managing tasks, built with OOP principles, JSON persistence, and role-based authentication.

---

## 📁 Project Structure

```
todo_cli/
├── main.py              ← CLI entry point & interactive menu loop
├── requirements.txt     ← External dependencies
├── README.md
│
├── models/
│   ├── __init__.py
│   ├── user.py          ← Person base class + User (inheritance, encapsulation)
│   └── task.py          ← Task class (@property, validation, serialisation)
│
├── utils/
│   ├── __init__.py
│   └── auth.py          ← JSON I/O, decorators, input helpers
│
└── data/
    ├── users.json        ← Persisted user accounts
    └── tasks.json        ← Persisted tasks
```

---

## 🚀 Setup & Run

```bash
# 1. Clone / download the project
cd todo_cli

# 2. (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python main.py
```

> The app works without `tabulate` installed — tables just look plainer.

---

## 🖥️ Menu Options

### When NOT logged in
| Option | Action |
|--------|--------|
| 1 | Register a new account |
| 2 | Login |
| 0 | Exit |

### When logged in (User)
| Option | Action |
|--------|--------|
| 3 | View my tasks |
| 4 | Add a new task |
| 5 | Update task status |
| 6 | Edit task details (title, priority, due date) |
| 7 | Delete a task |
| 8 | Filter tasks by status or priority |
| L | Logout |

### Admin extras
| Option | Action |
|--------|--------|
| 9 | List all registered users |
| 10 | Promote a user to Admin |
| 11 | Delete a user and their tasks |

---

## Authentication & Roles

- Passwords are hashed with **SHA-256** before storage — never stored in plain text.
- The **first user to register** automatically becomes **Admin**.
- All subsequent registrations create standard **User** accounts.
- Access control is enforced via Python **decorators** (`@require_login`, `@require_admin`).

---

## OOP Concepts Demonstrated

| Concept | Where |
|---------|-------|
| **Inheritance** | `Person → User` in `models/user.py` |
| **Encapsulation** | `_private` attributes + `@property` in `User` and `Task` |
| **Class attributes** | `User._id_counter`, `Task._id_counter` |
| **Decorators** | `@require_login`, `@require_admin`, `@log_action` in `utils/auth.py` |
| **CRUD** | Create, Read, Update, Delete for both Users and Tasks |
| **JSON persistence** | `load_json()` / `save_json()` with try-except error handling |

---

## Known Issues / Limitations

- Password hashing uses SHA-256 without a salt. For production use, replace with `bcrypt`.
- No password reset / recovery feature.
- Single user session per run (no concurrent multi-user support).
- Task assignment is to the currently logged-in user only (no assigning to others).

---

## Git Workflow (Recommended)

```bash
# Feature branch workflow
git checkout -b feature/add-task-model
# ... make changes ...
git add .
git commit -m "feat: add Task model with status validation"
git push origin feature/add-task-model
# Open pull request → review → merge to main
```


# TODO-CLI
BY: ALVIN SWALAH, BERRYL KHALAI, CEWA MAHAN.

