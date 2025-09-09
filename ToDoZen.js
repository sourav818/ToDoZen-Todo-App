document.addEventListener("DOMContentLoaded", () => {
    const taskForm = document.getElementById("task-form");
    const taskTitle = document.getElementById("task-title");
    const taskDeadline = document.getElementById("task-deadline");
    const taskPriority = document.getElementById("task-priority");

    // Listen for form submission
    taskForm.addEventListener("submit", async function (event) {
        event.preventDefault(); // Prevent default form submission

        const title = taskTitle.value.trim();
        const deadline = taskDeadline.value;
        const priority = taskPriority.value;

        // Ensure all fields are filled
        if (!title || !deadline || !priority) {
            alert("Please fill out all fields.");
            return;
        }

        // Validate the deadline format (should be 'YYYY-MM-DD')
        const deadlineRegex = /^\d{4}-\d{2}-\d{2}$/;
        if (!deadlineRegex.test(deadline)) {
            alert("Invalid deadline format. Please use 'YYYY-MM-DD'.");
            return;
        }

        // Prepare the task object
        const newTask = {
            title: title,
            deadline: deadline,
            priority: priority,
        };

        try {
            // Send task data to Flask backend via POST request
            const response = await fetch("/add-task", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(newTask),
            });

            // Handle the response
            if (response.ok) {
                const result = await response.json();
                alert(result.message); // Show success message from backend

                // Clear form inputs after submission
                taskTitle.value = "";
                taskDeadline.value = "";
                taskPriority.value = "";
            } else {
                const error = await response.json();
                alert(error.error || "Failed to add task. Please try again.");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred while adding the task. Please try again.");
        }
    });
});
