$(document).ready(function () {
    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay',
        },
        events: [],
    });

    let tasks = [];

    async function fetchTasks() {
        try {
            const response = await fetch("/tasks");
            if (!response.ok) throw new Error("Failed to fetch tasks.");
            tasks = await response.json();
            updateTaskList();
            updateCalendarEvents();
        } catch (error) {
            console.error("Error fetching tasks:", error);
        }
    }

    async function addTask(title, priority, deadline) {
        try {
            const response = await fetch("/add-task", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ title, priority, deadline }),
            });
            if (!response.ok) throw new Error("Failed to add task.");
            await fetchTasks();
        } catch (error) {
            console.error("Error adding task:", error);
        }
    }

    async function completeTask(taskId) {
        try {
            const response = await fetch("/complete-task", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ task_id: taskId }),
            });
            if (!response.ok) throw new Error("Failed to mark task as completed.");
            await fetchTasks();
        } catch (error) {
            console.error("Error completing task:", error);
        }
    }

    function updateTaskList() {
        const taskListElement = document.getElementById("task-list");
        taskListElement.innerHTML = "";

        const activeTasks = tasks.filter(task => !task.Completed);

        activeTasks.forEach((task) => {
            const li = document.createElement("li");
            li.innerHTML = `
                <span>${task.Title} - <strong>${task.Priority}</strong> (Deadline: ${task.Deadline})</span>
                <button class="complete-btn" data-id="${task.TaskID}">✔️ Complete</button>
            `;

            const completeBtn = li.querySelector(".complete-btn");
            completeBtn.addEventListener("click", function () {
                completeTask(task.TaskID);
            });

            taskListElement.appendChild(li);
        });
    }

    function updateCalendarEvents() {
        const calendarEvents = tasks.map(task => ({
            title: task.Title,
            start: task.Deadline,
            color: task.Priority === "High" ? "red" : task.Priority === "Medium" ? "yellow" : "green",
        }));

        $('#calendar').fullCalendar("removeEvents");
        $('#calendar').fullCalendar("addEventSource", calendarEvents);
    }

    document.getElementById("task-form")?.addEventListener("submit", function (e) {
        e.preventDefault();
        const title = document.getElementById("task-title").value;
        const priority = document.getElementById("task-priority").value;
        const deadline = document.getElementById("task-deadline").value;
        addTask(title, priority, deadline);
        document.getElementById("task-form").reset();
    });

    fetchTasks();
});
