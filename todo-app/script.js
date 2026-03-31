/* Recursive helper functions */

// Count active (not completed) tasks recursively.
function calculateTotalPriority(tasks, index = 0) {
    if (index >= tasks.length) return 0;
    return (tasks[index].completed ? 0 : 1) + calculateTotalPriority(tasks, index + 1);
}

// Find a task by id recursively.
function findTaskRecursively(tasks, id, index = 0) {
    if (index >= tasks.length) return null;
    if (tasks[index].id === id) return tasks[index];
    return findTaskRecursively(tasks, id, index + 1);
}

/* Main app state and behavior */

function todoApp() {
    return {
        tasks: [],
        newTask: '',
        filter: 'active',
        showEditModal: false,
        editTaskId: null,
        editTaskText: '',
        nextId: 1,

        initApp() {
            const saved = localStorage.getItem('tasks');
            if (saved) {
                this.tasks = JSON.parse(saved);
                this.nextId = Math.max(...this.tasks.map(t => t.id), 0) + 1;
            } else {
                this.tasks = [];
                this.nextId = 1;
            }
        },

        addTask() {
            const text = this.newTask.trim();
            if (!text) return alert('Task cannot be empty');
            if (text.length > 200) return alert('Task cannot exceed 200 characters');
            
            this.tasks.push({
                id: this.nextId++,
                text,
                completed: false,
                createdAt: new Date().toISOString(),
            });
            this.newTask = '';
            this.saveTasks();
        },

        deleteTask(id) {
            this.tasks = this.tasks.filter(task => task.id !== id);
            this.saveTasks();
        },

        editTask(id) {
            const task = findTaskRecursively(this.tasks, id);
            this.editTaskId = id;
            this.editTaskText = task.text;
            this.showEditModal = true;
        },

        saveEdit() {
            const text = this.editTaskText.trim();
            if (!text) return alert('Task cannot be empty');
            if (text.length > 200) return alert('Task cannot exceed 200 characters');
            
            this.tasks = this.tasks.map(task => 
                task.id === this.editTaskId ? { ...task, text } : task
            );
            this.showEditModal = false;
            this.editTaskId = null;
            this.editTaskText = '';
            this.saveTasks();
        },

        getFilteredTasks() {
            switch (this.filter) {
                case 'active': return this.tasks.filter(t => !t.completed);
                case 'completed': return this.tasks.filter(t => t.completed);
                default: return this.tasks;
            }
        },

        getCompletedCount() {
            return this.tasks.reduce((count, task) => count + (task.completed ? 1 : 0), 0);
        },

        // Use recursion result directly in the UI stats.
        getActiveCount() {
            return calculateTotalPriority(this.tasks);
        },

        clearCompleted() {
            if (this.getCompletedCount() === 0) return;
            this.tasks = this.tasks.filter(task => !task.completed);
            this.saveTasks();
        },

        saveTasks() {
            localStorage.setItem('tasks', JSON.stringify(this.tasks));
        },
    };
}

window.todoApp = todoApp;
