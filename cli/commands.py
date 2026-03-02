import sys
from models import User, Project, Task

def handle_command(args):
    cmd = args.command

    if cmd == 'add-user':
        user = User(args.name, args.email)
        User.add(user)
        print(f"User added: {user}")

    elif cmd == 'add-project':
        user = User.find_by_name(args.user)
        if not user:
            print(f"Error: User '{args.user}' not found.")
            sys.exit(1)
        project = Project(args.title, user.user_id, args.description, args.due)
        Project.add(project)
        user.add_project(project.project_id)
        User.save_all()
        print(f"Project added: {project}")

    elif cmd == 'add-task':
        project = Project.find_by_title(args.project)
        if not project:
            print(f"Error: Project '{args.project}' not found.")
            sys.exit(1)
        assigned_id = None
        if args.assigned_to:
            assigned = User.find_by_name(args.assigned_to)
            if not assigned:
                print(f"Error: Assigned user '{args.assigned_to}' not found.")
                sys.exit(1)
            assigned_id = assigned.user_id
        task = Task(args.title, project.project_id, args.status, assigned_id)
        Task.add(task)
        project.add_task(task.task_id)
        Project.save_all()
        print(f"Task added: {task}")

    elif cmd == 'list-users':
        users = User.get_all()
        if not users:
            print("No users found.")
        else:
            for u in users:
                print(f"ID: {u.user_id}, Name: {u.name}, Email: {u.email}")

    elif cmd == 'list-projects':
        if args.user:
            user = User.find_by_name(args.user)
            if not user:
                print(f"Error: User '{args.user}' not found.")
                sys.exit(1)
            projects = Project.get_for_user(user.user_id)
        else:
            projects = Project.get_all()
        if not projects:
            print("No projects found.")
        else:
            for p in projects:
                user = User._all_users.get(str(p.user_id))
                uname = user.name if user else 'Unknown'
                print(f"ID: {p.project_id}, Title: {p.title}, User: {uname}, Due: {p.due_date}")

    elif cmd == 'list-tasks':
        tasks = Task.get_all()
        if args.project:
            proj = Project.find_by_title(args.project)
            if not proj:
                print(f"Error: Project '{args.project}' not found.")
                sys.exit(1)
            tasks = [t for t in tasks if t.project_id == proj.project_id]
        if args.user:
            user = User.find_by_name(args.user)
            if not user:
                print(f"Error: User '{args.user}' not found.")
                sys.exit(1)
            tasks = [t for t in tasks if t.assigned_to == user.user_id]
        if not tasks:
            print("No tasks found.")
        else:
            for t in tasks:
                proj = Project._all_projects.get(str(t.project_id))
                ptitle = proj.title if proj else 'Unknown'
                assigned = User._all_users.get(str(t.assigned_to))
                aname = assigned.name if assigned else 'Unassigned'
                print(f"ID: {t.task_id}, Title: {t.title}, Project: {ptitle}, Status: {t.status}, Assigned: {aname}")

    elif cmd == 'update-task':
        task = Task.find_by_id(args.id)
        if not task:
            print(f"Error: Task with ID {args.id} not found.")
            sys.exit(1)
        task.status = args.status
        Task.save_all()
        print(f"Task {args.id} status updated to '{args.status}'.")

    elif cmd == 'complete-task':
        task = Task.find_by_id(args.id)
        if not task:
            print(f"Error: Task with ID {args.id} not found.")
            sys.exit(1)
        task.status = 'completed'
        Task.save_all()
        print(f"Task {args.id} marked as completed.")