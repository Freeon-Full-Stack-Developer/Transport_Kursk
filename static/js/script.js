// Функция для переключения боковой панели
function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");

    if (sidebar) {
        if (sidebar.style.width === "250px") {
            sidebar.style.width = "0";
        } else {
            sidebar.style.width = "250px";
        }
    } else {
        console.warn("Sidebar not found!");
    }
}

// Функция для переключения отображения подробной информации о поездке
function toggleDetails(tripId) {
    var details = document.getElementById(tripId);

    if (details) {
        details.classList.toggle('show');
    } else {
        console.warn(`Details for trip ID "${tripId}" not found!`);
    }
}
