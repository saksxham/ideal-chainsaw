import os
import sys
import subprocess
import threading
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext


class EditorApp:
    def __init__(self, root):
        self.root = root
        root.title('Simple Python Editor — Run & Commit')

        toolbar = tk.Frame(root)
        toolbar.pack(side='top', fill='x')

        open_btn = tk.Button(toolbar, text='Open', command=self.open_file)
        open_btn.pack(side='left')
        save_btn = tk.Button(toolbar, text='Save', command=self.save_file)
        save_btn.pack(side='left')
        run_btn = tk.Button(toolbar, text='Run + Commit', command=self.on_run_commit)
        run_btn.pack(side='left')

        self.filename = None

        self.editor = scrolledtext.ScrolledText(root, wrap='none', height=25)
        self.editor.pack(fill='both', expand=True)

        self.output = scrolledtext.ScrolledText(root, wrap='word', height=10, bg='#111', fg='#eee')
        self.output.pack(fill='both')

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[('Python', '*.py'), ('All', '*.*')])
        if not path:
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            messagebox.showerror('Open file', str(e))
            return
        self.filename = path
        self.editor.delete('1.0', tk.END)
        self.editor.insert('1.0', text)
        self.root.title(f'Simple Python Editor — {os.path.basename(path)}')

    def save_file(self):
        if not self.filename:
            path = filedialog.asksaveasfilename(defaultextension='.py', filetypes=[('Python', '*.py')])
            if not path:
                return
            self.filename = path
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                f.write(self.editor.get('1.0', tk.END))
        except Exception as e:
            messagebox.showerror('Save file', str(e))
            return

    def on_run_commit(self):
        if not self.filename:
            messagebox.showinfo('Save first', 'Please save the file before running.')
            return
        # run in background to keep UI responsive
        threading.Thread(target=self.run_commit_flow, daemon=True).start()

    def append_output(self, text):
        self.output.configure(state='normal')
        self.output.insert(tk.END, text + '\n')
        self.output.see(tk.END)
        self.output.configure(state='disabled')

    def run_commit_flow(self):
        self.append_output('Saving file...')
        self.save_file()

        self.append_output('Running: ' + self.filename)
        try:
            proc = subprocess.Popen([sys.executable, self.filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            out, err = proc.communicate()
            if out:
                self.append_output('--- STDOUT ---')
                self.append_output(out)
            if err:
                self.append_output('--- STDERR ---')
                self.append_output(err)
        except Exception as e:
            self.append_output('Execution error: ' + str(e))

        # Git commit + push
        repo_dir = os.path.dirname(self.filename)
        # walk up to find .git
        cur = repo_dir
        found = False
        while True:
            if os.path.isdir(os.path.join(cur, '.git')):
                found = True
                break
            parent = os.path.dirname(cur)
            if parent == cur:
                break
            cur = parent

        if not found:
            self.append_output('No git repository found for this file. Skipping commit/push.')
            return

        git_cwd = cur
        relpath = os.path.relpath(self.filename, git_cwd)

        self.append_output('Staging file: ' + relpath)
        try:
            subprocess.check_call(['git', 'add', relpath], cwd=git_cwd)
            msg = f'Edit from simple editor: {os.path.basename(self.filename)} ({datetime.datetime.now().isoformat()})'
            subprocess.check_call(['git', 'commit', '-m', msg], cwd=git_cwd)
            self.append_output('Committed: ' + msg)
            # push
            self.append_output('Pushing to remote...')
            push = subprocess.run(['git', 'push'], cwd=git_cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if push.returncode == 0:
                self.append_output('Push succeeded.')
                self.append_output(push.stdout)
            else:
                self.append_output('Push failed:')
                self.append_output(push.stderr)
        except subprocess.CalledProcessError as e:
            self.append_output('Git command failed: ' + str(e))
        except Exception as e:
            self.append_output('Error during git operations: ' + str(e))


def main():
    root = tk.Tk()
    app = EditorApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
