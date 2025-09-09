document.addEventListener("DOMContentLoaded", () => {
    const completedTasksElement = document.getElementById("completed-tasks");
    const rewardPointsElement = document.getElementById("reward-points");
    const progressBar = document.getElementById("progress-bar");
    const rewardPercentageText = document.getElementById("reward-percentage");
    const claimRewardBtn = document.getElementById("claim-reward-btn");
    const loadingSpinnerTaskCompletion = document.querySelectorAll(".loading-spinner")[0];
    const loadingSpinnerRewardPoints = document.querySelectorAll(".loading-spinner")[1];

    // Handle the "Back to Home" button click event
    const backHomeBtn = document.getElementById("back-home-btn");
    if (backHomeBtn) {
        backHomeBtn.addEventListener("click", () => {
            window.location.href = "/"; // Change this to the appropriate URL for your home page
        });
    }

    // Check if reward has been claimed previously and reset state accordingly
    function loadStateFromStorage() {
        const rewardClaimed = localStorage.getItem('rewardClaimed');

        if (rewardClaimed === 'true') {
            // Reset to 0 if the reward was already claimed
            resetTaskProgressInStorage();
        } else {
            // If reward is not claimed, load previous state or default to 0
            const completedTasks = localStorage.getItem('completedTasks') || 0;
            const rewardPoints = localStorage.getItem('rewardPoints') || 0;
            const progress = localStorage.getItem('progress') || 0;

            updateProgressUI(completedTasks, progress, rewardPoints);
        }
    }

    // Update the UI with the progress values
    function updateProgressUI(completedTasks, totalTasks, rewardPoints) {
        completedTasksElement.textContent = completedTasks;
        rewardPointsElement.textContent = rewardPoints;

        const progress = totalTasks > 0 ? (completedTasks / totalTasks) * 100 : 0;
        const offset = 283 - (283 * progress) / 100;

        progressBar.style.strokeDashoffset = offset;
        rewardPercentageText.textContent = `${Math.round(progress)}%`;
    }

    // Reset task progress, reward points, and the progress bar to zero
    function resetTaskProgressInStorage() {
        // Set the state in localStorage to 0
        localStorage.setItem('completedTasks', 0);
        localStorage.setItem('rewardPoints', 0);
        localStorage.setItem('progress', 0);
        localStorage.setItem('rewardClaimed', 'true'); // Mark reward as claimed

        // Update the UI to reflect the state
        updateProgressUI(0, 0, 0); // Set all values to 0

        // Trigger visualization reset
        refreshCharts();
    }

    // Fetch tasks from server and update the progress bar, completed tasks count, and reward points dynamically
    async function fetchTasksAndUpdateUI() {
        try {
            const response = await fetch('/tasks');
            if (!response.ok) {
                throw new Error(`Failed to fetch tasks: ${response.statusText}`);
            }

            const tasks = await response.json();

            // Calculate completed tasks, total tasks, and reward points
            const completedTasks = tasks.filter(task => task.Completed).length;
            const totalTasks = tasks.length;
            const rewardPoints = tasks.reduce((acc, task) => acc + (task.Completed ? task.RewardPoints : 0), 0);

            // Update the UI elements
            updateProgressUI(completedTasks, totalTasks, rewardPoints);

            // Store values in localStorage
            localStorage.setItem('completedTasks', completedTasks);
            localStorage.setItem('rewardPoints', rewardPoints);
            localStorage.setItem('progress', completedTasks); // Set progress as the number of completed tasks
        } catch (error) {
            console.error("Error fetching tasks:", error);
        }
    }

    // Handles the "Claim Reward" button click event and resets the task progress, score, and reward bar
    claimRewardBtn.addEventListener("click", async () => {
        if (loadingSpinnerTaskCompletion && loadingSpinnerRewardPoints) {
            loadingSpinnerTaskCompletion.style.display = 'block';
            loadingSpinnerRewardPoints.style.display = 'block';
        }

        try {
            // Example user ID, replace with dynamic data
            const userId = 1;

            const response = await fetch('/claim-reward', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user_id: userId })
            });

            if (!response.ok) {
                throw new Error(`Failed to claim reward: ${response.statusText}`);
            }

            // Mark reward as claimed in localStorage
            localStorage.setItem('rewardClaimed', 'true');

            // Reset task progress, reward points, and the progress bar
            resetTaskProgressInStorage();

            console.log("Reward claimed successfully.");
        } catch (error) {
            console.error("Error claiming reward:", error);
            alert("Failed to claim the reward. Please try again.");
        } finally {
            if (loadingSpinnerTaskCompletion && loadingSpinnerRewardPoints) {
                loadingSpinnerTaskCompletion.style.display = 'none';
                loadingSpinnerRewardPoints.style.display = 'none';
            }
        }
    });

    // Function to refresh charts dynamically
    function refreshCharts() {
        console.log("Refreshing charts...");
        
        // Example for Chart.js
        if (window.myChart) {
            window.myChart.destroy(); // Destroy the existing chart instance
        }

        const ctx = document.getElementById("chartCanvas").getContext("2d");
        window.myChart = new Chart(ctx, {
            type: 'bar', // Chart type
            data: {
                labels: ['Task 1', 'Task 2', 'Task 3'], // Example labels
                datasets: [{
                    label: 'Rewards Progress',
                    data: [0, 0, 0], // Reset data to zero
                    backgroundColor: ['red', 'blue', 'green']
                }]
            }
        });
    }

    // Thumbnail image controls
    let slideIndex = 1;

    // Initial setup
    showSlides(slideIndex);

    // Next/previous controls
    const prevButton = document.querySelector('.prev');
    const nextButton = document.querySelector('.next');

    // Add event listeners to the buttons
    if (prevButton) {
        prevButton.addEventListener('click', function() {
            plusSlides(-1);
        });
    }

    if (nextButton) {
        nextButton.addEventListener('click', function() {
            plusSlides(1);
        });
    }

    // Function to navigate slides
    function plusSlides(n) {
        showSlides(slideIndex += n);
    }

    // Show specific slide
    function showSlides(n) {
        let i;
        let slides = document.getElementsByClassName("mySlides");
        let dots = document.getElementsByClassName("dot");

        if (n > slides.length) { slideIndex = 1 }
        if (n < 1) { slideIndex = slides.length }

        for (i = 0; i < slides.length; i++) {
            slides[i].style.display = "none";
        }

        for (i = 0; i < dots.length; i++) {
            dots[i].className = dots[i].className.replace(" active", "");
        }

        slides[slideIndex - 1].style.display = "block";
        if (dots[slideIndex - 1]) {
            dots[slideIndex - 1].className += " active";
        }
    }

    // Initial fetch and UI update
    fetchTasksAndUpdateUI();

    // Load state from localStorage on page load
    loadStateFromStorage();

    // Expose refreshCharts to global scope
    window.refreshCharts = refreshCharts;
});
