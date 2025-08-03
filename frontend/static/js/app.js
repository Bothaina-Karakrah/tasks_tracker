const API_BASE = 'http://localhost:8000';
let tasks = [];
let categories = [];

document.addEventListener('DOMContentLoaded', () => {
    loadTasks();
    loadCategories();
    loadAnalytics();

    document.getElementById('createTaskForm')?.addEventListener('submit', createTask);
    document.getElementById('editTaskForm')?.addEventListener('submit', updateTask);
});

function showTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.nav-tab').forEach(tab => tab.classList.remove('active'));

    document.getElementById(tabId)?.classList.add('active');
    event.target.classList.add('active');

    if (tabId === 'analytics') loadAnalytics();
}

async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

async function loadTasks() {
    try {
        const params = new URLSearchParams();
        ['status', 'priority', 'category'].forEach(key => {
            const val = document.getElementById(`${key}Filter`)?.value;
            if (val) params.append(key, val);
        });

        const query = params.toString();
        const endpoint = query ? `/tasks/?${query}` : '/tasks/';
        tasks = await apiCall(endpoint);
        renderTasks();
    } catch {
        showError('taskError', 'Failed to load tasks');
    }
}

function renderTasks() {
    const container = document.getElementById('tasksContainer');
    if (!tasks.length) {
        container.innerHTML = '<div class="loading">No tasks found. Create your first task!</div>';
        return;
    }

    container.innerHTML = tasks.map(task => `
        <div class="task-card ${task.status} ${task.priority}">
            <div class="task-header">
                <div class="task-title">${task.title}</div>
                <div class="task-actions">
                    <button class="btn" onclick="editTask(${task.id})"><i class="fas fa-edit"></i></button>
                    <button class="btn btn-danger" onclick="deleteTask(${task.id})"><i class="fas fa-trash"></i></button>
                </div>
            </div>
            <div class="task-meta">
                <span class="status-${task.status}">${formatStatus(task.status)}</span>
                <span class="priority-${task.priority}">${formatPriority(task.priority)}</span>
                <span>${task.category || 'General'}</span>
                ${task.estimated_days ? `<span>${task.estimated_days}h estimated</span>` : ''}
                ${task.actual_days ? `<span>${task.actual_days}h actual</span>` : ''}
            </div>
            ${task.description ? `<p class="task-description">${task.description}</p>` : ''}
            <div class="task-dates">
                ${task.due_date ? `<span class="due-date">Due: ${formatDateTime(task.due_date)}</span>` : ''}
                ${task.started_at ? `<span class="started-date">Started: ${formatDateTime(task.started_at)}</span>` : ''}
            </div>
            <div class="timestamp">
                Created: ${formatDateTime(task.created_at)}
                ${task.completed_at ? ` | Completed: ${formatDateTime(task.completed_at)}` : ''}
            </div>
        </div>
    `).join('');
}

async function loadCategories() {
    try {
        categories = await apiCall('/categories/');
        const categorySelects = ['categoryFilter', 'createCategory', 'editCategory'];

        categorySelects.forEach(selectId => {
            const select = document.getElementById(selectId);
            if (!select) return;

            const currentValue = select.value;

            if (selectId === 'categoryFilter') {
                select.innerHTML = '<option value="">All Categories</option>';
            } else {
                select.innerHTML = '<option value="">Select Category</option>';
            }

            categories.forEach(cat => {
                const option = document.createElement('option');
                option.value = cat;
                option.textContent = cat;
                select.appendChild(option);
            });

            // Add "General" option if not present
            if (!categories.includes('General')) {
                const option = document.createElement('option');
                option.value = 'General';
                option.textContent = 'General';
                select.appendChild(option);
            }

            select.value = currentValue;
        });
    } catch {
        console.error('Failed to load categories.');
    }
}

function filterTasks() {
    loadTasks();
}

async function createTask(e) {
    e.preventDefault();
    const data = new FormData(e.target);

    const payload = {
        title: data.get('title'),
        description: data.get('description') || null,
        priority: data.get('priority') || 'medium',
        category: data.get('category') || 'General',
        estimated_days: parseInt(data.get('estimated_days')) || 1,
        actual_days: parseInt(data.get('actual_days')) || 0,
        due_date: data.get('due_date') ? new Date(data.get('due_date')).toISOString() : null,
        started_at: data.get('started_at') ? new Date(data.get('started_at')).toISOString() : null,
        completed_at: data.get('completed_at') ? new Date(data.get('completed_at')).toISOString() : null  // Added here
    };

    try {
        await apiCall('/tasks/', {
            method: 'POST',
            body: JSON.stringify(payload)
        });
        showSuccess('createSuccess', 'Task created!');
        e.target.reset();
        loadTasks();
        loadCategories();
    } catch (error) {
        console.error('Create task error:', error);
        showError('createError', 'Failed to create task');
    }
}

function editTask(id) {
    const task = tasks.find(t => t.id === id);
    if (!task) return;

    document.getElementById('editTaskId').value = task.id;
    document.getElementById('editTitle').value = task.title;
    document.getElementById('editDescription').value = task.description || '';
    document.getElementById('editStatus').value = task.status;
    document.getElementById('editPriority').value = task.priority;
    document.getElementById('editCategory').value = task.category || 'General';
    document.getElementById('editActualDays').value = task.actual_days || '';
    document.getElementById('editDueDate').value = task.due_date ? formatDateTimeInput(task.due_date) : '';
    document.getElementById('editStartedAt').value = task.started_at ? formatDateTimeInput(task.started_at) : '';
    document.getElementById('editCompletedAt').value = task.completed_at ? formatDateTimeInput(task.completed_at) : '';
    document.getElementById('editModal').style.display = 'block';
}

async function updateTask(e) {
    e.preventDefault();
    const id = document.getElementById('editTaskId').value;
    const data = new FormData(e.target);

    const payload = {
        title: data.get('title'),
        description: data.get('description') || null,
        status: data.get('status'),
        priority: data.get('priority'),
        category: data.get('category'),
        actual_days: data.get('actual_days') ? parseInt(data.get('actual_days')) : null,
        due_date: data.get('due_date') ? new Date(data.get('due_date')).toISOString() : null
    };

    const startedAtValue = data.get('started_at');
    if (startedAtValue) {
        payload.started_at = new Date(startedAtValue).toISOString();
    }
    const completedAtValue = data.get('completed_at');  // fixed name here
    if (completedAtValue) {
        payload.completed_at = new Date(completedAtValue).toISOString();
    }

    try {
        await apiCall(`/tasks/${id}`, {
            method: 'PUT',
            body: JSON.stringify(payload)
        });
        closeEditModal();
        showSuccess('taskSuccess', 'Task updated!');
        loadTasks();
        loadCategories();
    } catch (error) {
        console.error('Update task error:', error);
        showError('taskError', 'Failed to update task');
    }
}

async function deleteTask(id) {
    if (!confirm('Delete this task?')) return;
    try {
        await apiCall(`/tasks/${id}`, { method: 'DELETE' });
        showSuccess('taskSuccess', 'Task deleted!');
        loadTasks();
        loadCategories();
    } catch {
        showError('taskError', 'Failed to delete task');
    }
}

async function loadAnalytics() {
    try {
        const data = await apiCall('/analytics/');
        renderAnalytics(data);
    } catch {
        document.getElementById('analyticsContainer').innerHTML =
            '<div class="error-message">Failed to load analytics</div>';
    }
}

function renderAnalytics(data) {
    const container = document.getElementById('analyticsContainer');
    container.innerHTML = `
        <div class="analytics-grid">
            ${renderStat('Total Tasks', data.total_tasks)}
            ${renderStat('Completed', data.completed_tasks)}
            ${renderStat('In Progress', data.in_progress_tasks)}
            ${renderStat('Completion Rate', data.completion_rate + '%')}
            ${renderStat('Avg Completion Time', data.avg_completion_time + 'h')}
        </div>
        ${renderChart('Tasks by Category', data.tasks_by_category)}
        ${renderChart('Tasks by Priority', data.tasks_by_priority, true)}
    `;
}

function renderStat(label, value) {
    return `
        <div class="stat-card">
            <div class="stat-value">${value}</div>
            <div class="stat-label">${label}</div>
        </div>`;
}

function renderChart(title, data, isPriority = false, isDaily = false) {
    return `
        <div class="chart-container">
            <h3>${title}</h3>
            <div class="chart-data">
                ${Object.entries(data).map(([k, v]) => `
                    <div class="chart-row">
                        <span>${isDaily ? formatDate(k) : isPriority ? formatPriority(k) : k}</span>
                        <span><strong>${isDaily ? v.completed : v}</strong></span>
                    </div>
                `).join('')}
            </div>
        </div>`;
}

// Utility functions
function formatStatus(s) {
    return { 'todo': 'To Do', 'in_progress': 'In Progress', 'completed': 'Completed' }[s] || s;
}

function formatPriority(p) {
    return p.charAt(0).toUpperCase() + p.slice(1);
}

function formatDate(str) {
    const d = new Date(str);
    return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
}

function formatDateTime(str) {
    const d = new Date(str);
    return d.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatDateTimeInput(str) {
    const d = new Date(str);
    return d.toISOString().slice(0, 16); // Format for datetime-local input
}

function showSuccess(id, msg) {
    const el = document.getElementById(id);
    if (el) {
        el.textContent = msg;
        el.style.display = 'block';
        setTimeout(() => (el.style.display = 'none'), 3000);
    }
}

function showError(id, msg) {
    const el = document.getElementById(id);
    if (el) {
        el.textContent = msg;
        el.style.display = 'block';
        setTimeout(() => (el.style.display = 'none'), 4000);
    }
}

function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
}