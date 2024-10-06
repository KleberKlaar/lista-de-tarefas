import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import json
from datetime import datetime

class Task:
    def __init__(self, name, deadline, description, completed=False):
        self.name = name
        self.deadline = deadline
        self.description = description
        self.completed = completed

    def to_dict(self):
        return {
            "name": self.name,
            "deadline": self.deadline,
            "description": self.description,
            "completed": self.completed
        }

class TaskOrganizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Organizador de Tarefas - Kleber Klaar")
        self.tasks = []

        # Carregar tarefas salvas
        self.load_tasks()

        # Interface gráfica
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        # Campo para adicionar tarefa
        self.task_name_entry = tk.Entry(self.frame, width=30)
        self.task_name_entry.grid(row=0, column=0, padx=5)
        self.task_name_entry.insert(0, "Nome da tarefa")

        # Campo para adicionar prazo
        self.task_deadline_entry = tk.Entry(self.frame, width=15)
        self.task_deadline_entry.grid(row=0, column=1, padx=5)
        self.task_deadline_entry.insert(0, "Prazo (dd/mm/aaaa)")

        # Botão para adicionar nova tarefa
        self.add_button = tk.Button(self.frame, text="Adicionar Tarefa", command=self.add_task)
        self.add_button.grid(row=0, column=2, padx=5)

        # Tabela de tarefas
        columns = ("name", "deadline", "status")
        self.tree = ttk.Treeview(root, columns=columns, show="headings")
        self.tree.heading("name", text="Nome")
        self.tree.heading("deadline", text="Prazo")
        self.tree.heading("status", text="Status")
        self.tree.pack(pady=10)
        self.tree.bind("<Double-Button-1>", self.show_task_description)

        # Botão para remover tarefa
        self.remove_button = tk.Button(root, text="Remover Tarefa", command=self.remove_task)
        self.remove_button.pack()

        # Rodapé com o crédito
        self.footer_label = tk.Label(root, text="Criado por Kleber Klaar", font=("Arial", 10), fg="gray")
        self.footer_label.pack(side="bottom", pady=10)

        # Atualizar tabela de tarefas
        self.update_task_table()

    def add_task(self):
        # Captura os dados da tarefa
        name = self.task_name_entry.get()
        deadline = self.task_deadline_entry.get()

        # Abre um diálogo para obter a descrição da tarefa
        description = simpledialog.askstring("Descrição", "Digite a descrição da tarefa:")

        # Validar o formato da data
        try:
            deadline_date = datetime.strptime(deadline, "%d/%m/%Y")  # Formato de data atualizado para incluir ano
        except ValueError:
            messagebox.showwarning("Data inválida", "Digite o prazo no formato dd/mm/aaaa.")
            return

        if name and description:
            # Cria e adiciona a tarefa na lista
            task = Task(name, deadline, description)
            self.tasks.append(task)
            self.sort_tasks()  # Ordena as tarefas após adicionar
            self.update_task_table()
            self.save_tasks()
        else:
            messagebox.showwarning("Dados incompletos", "Preencha todos os campos.")

        # Limpa os campos de entrada
        self.task_name_entry.delete(0, tk.END)
        self.task_deadline_entry.delete(0, tk.END)

    def update_task_table(self):
        # Limpar a tabela atual
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Adicionar as tarefas na tabela
        for task in self.tasks:
            status = "Concluída" if task.completed else "Pendente"
            self.tree.insert("", tk.END, values=(task.name, task.deadline, status))

    def show_task_description(self, event):
        # Exibe a descrição da tarefa ao clicar duas vezes
        selected_item = self.tree.selection()
        if selected_item:
            selected_task = self.tree.item(selected_item)["values"]
            task_name = selected_task[0]
            task = next((t for t in self.tasks if t.name == task_name), None)
            if task:
                messagebox.showinfo(f"Tarefa: {task.name}", f"Descrição: {task.description}")

    def remove_task(self):
        # Remove a tarefa selecionada
        selected_item = self.tree.selection()
        if selected_item:
            selected_task = self.tree.item(selected_item)["values"]
            task_name = selected_task[0]
            self.tasks = [task for task in self.tasks if task.name != task_name]
            self.update_task_table()
            self.save_tasks()
        else:
            messagebox.showwarning("Nenhuma tarefa selecionada", "Selecione uma tarefa para remover.")

    def sort_tasks(self):
        # Ordena as tarefas pelo prazo (convertendo para datetime)
        def convert_to_date(task):
            try:
                return datetime.strptime(task.deadline, "%d/%m/%Y")
            except ValueError:
                return datetime.max

        self.tasks.sort(key=convert_to_date)

    def save_tasks(self):
        # Salva as tarefas em um arquivo JSON
        with open("tasks.json", "w") as f:
            json.dump([task.to_dict() for task in self.tasks], f)

    def load_tasks(self):
        # Carrega as tarefas de um arquivo JSON
        try:
            with open("tasks.json", "r") as f:
                task_dicts = json.load(f)
                self.tasks = [Task(**task_dict) for task_dict in task_dicts]
        except FileNotFoundError:
            self.tasks = []

# Inicializa o programa
root = tk.Tk()
app = TaskOrganizer(root)
root.mainloop()
