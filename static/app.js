/* =====================================
   VAAYUM SPACE - FRONTEND
===================================== */


// =====================================
// SHOW / HIDE PASSWORD
// =====================================

document.querySelectorAll(
    "[data-toggle-password]"
).forEach(function (button) {

    button.addEventListener("click", function () {

        var input = document.getElementById(
            button.dataset.togglePassword
        );

        if (!input) {
            return;
        }

        if (input.type === "password") {

            input.type = "text";

            button.textContent = "Hide";

        } else {

            input.type = "password";

            button.textContent = "Show";

        }

    });

});


// =====================================
// MOBILE SIDEBAR
// =====================================

var menuButton = document.getElementById(
    "menu-button"
);

var sidebar = document.getElementById(
    "sidebar"
);

if (menuButton && sidebar) {

    menuButton.addEventListener("click", function () {

        sidebar.classList.toggle("open");

    });


    document.addEventListener("click", function (event) {

        if (
            !sidebar.contains(event.target)
            && !menuButton.contains(event.target)
        ) {

            sidebar.classList.remove("open");

        }

    });

}


// =====================================
// CIRCULAR PROGRESS CHARTS
// =====================================

document.querySelectorAll(
    "[data-progress]"
).forEach(function (chart) {

    var value = Number(
        chart.dataset.progress
    ) || 0;

    value = Math.max(
        0,
        Math.min(100, value)
    );

    chart.style.setProperty(
        "--progress",
        value + "%"
    );

});


// =====================================
// PROGRESS BARS
// =====================================

document.querySelectorAll(
    "[data-width]"
).forEach(function (bar) {

    var value = Number(
        bar.dataset.width
    ) || 0;

    value = Math.max(
        0,
        Math.min(100, value)
    );

    bar.style.width = value + "%";

});


// =====================================
// BLOCKER REASON FIELD
// =====================================

document.querySelectorAll(
    ".status-form"
).forEach(function (form) {

    var select = form.querySelector(
        ".status-select"
    );

    var field = form.querySelector(
        ".blocker-field"
    );

    if (!select || !field) {
        return;
    }

    function update() {

        field.hidden = select.value !== "Blocker";

    }

    select.addEventListener(
        "change",
        update
    );

    update();

});


// =====================================
// SEARCH TASKS
// =====================================

document.querySelectorAll(
    "[data-task-search]"
).forEach(function (search) {

    search.addEventListener("input", function () {

        var query = search.value.trim().toLowerCase();

        document.querySelectorAll(
            "[data-search-item]"
        ).forEach(function (item) {

            item.hidden = !item.dataset.searchItem.includes(
                query
            );

        });

    });

});


// =====================================
// EMPLOYEE TASK DRAG AND DROP
// =====================================

var movingCard = null;


// -------------------------------------
// START DRAGGING A CARD
// -------------------------------------

document.querySelectorAll(
    "[data-drag-task]"
).forEach(function (card) {

    card.addEventListener("dragstart", function (event) {

        // Prevent dragging while using form controls.
        if (
            event.target.closest(
                "input, select, textarea, button"
            )
        ) {

            event.preventDefault();

            return;
        }

        movingCard = card;

        event.dataTransfer.setData(
            "text/plain",
            card.dataset.dragTask
        );

        event.dataTransfer.effectAllowed = "move";

        card.classList.add("dragging");

    });


    card.addEventListener("dragend", function () {

        card.classList.remove("dragging");

        movingCard = null;

        document.querySelectorAll(
            ".drop-target"
        ).forEach(function (column) {

            column.classList.remove("drop-target");

        });

    });

});


// -------------------------------------
// SAVE TASK STATUS
// -------------------------------------

function updateDraggedTask(card, newStatus) {

    var oldStatus = card.dataset.currentStatus;

    // No update needed.
    if (newStatus === oldStatus) {
        return;
    }


    // Only Owner can complete tasks.
    if (newStatus === "Completed") {

        alert(
            "Only the owner can approve tasks as Completed."
        );

        return;
    }


    // Review is allowed only from In Progress.
    if (
        newStatus === "Review"
        && oldStatus !== "In Progress"
    ) {

        alert(
            "Move the task to In Progress before submitting for Review."
        );

        return;
    }


    // Find the card's status form.
    var form = card.querySelector(
        ".status-form"
    );

    if (!form) {
        return;
    }


    var select = form.querySelector(
        ".status-select"
    );

    var blocker = form.querySelector(
        "[name='blocker']"
    );


    // Ask for a reason if blocked.
    if (newStatus === "Blocker") {

        var answer = prompt(
            "What is blocking this task?",
            blocker.value || ""
        );

        if (
            answer === null
            || !answer.trim()
        ) {

            return;
        }

        blocker.value = answer.trim();

    } else {

        blocker.value = "";

    }


    // Set the new status.
    select.value = newStatus;


    // Submit to Flask.
    form.submit();

}


// -------------------------------------
// DROP CARD IN ANOTHER COLUMN
// -------------------------------------

document.querySelectorAll(
    "[data-drop-status]"
).forEach(function (column) {

    column.addEventListener("dragover", function (event) {

        if (!movingCard) {
            return;
        }

        event.preventDefault();

        event.dataTransfer.dropEffect = "move";

        column.classList.add("drop-target");

    });


    column.addEventListener("dragleave", function (event) {

        if (
            !column.contains(event.relatedTarget)
        ) {

            column.classList.remove("drop-target");

        }

    });


    column.addEventListener("drop", function (event) {

        event.preventDefault();

        column.classList.remove("drop-target");

        if (movingCard) {

            updateDraggedTask(
                movingCard,
                column.dataset.dropStatus
            );

        }

    });

});