$(document).ready(function () {
    var currentMonth = new Date().getMonth();
    var currentYear = new Date().getFullYear();

    function daysInMonth(month, year) {
        return new Date(year, month, 0).getDate();
    }

    function firstDayOfMonth(month, year) {
        return new Date(year, month, 1).getDay();
    }

    function updateCalendar(month, year) {
        var days = daysInMonth(month + 1, year);
        var firstDay = firstDayOfMonth(month, year);

        var calendar = $('#calendar');
        calendar.empty();

        // Calendar header
        var header = $('<div class="calendar-header"></div>');
        header.append('<div>' + new Date(year, month).toLocaleString('default', { month: 'long' }) + ' ' + year + '</div>');
        calendar.append(header);

        // Days of the week
        var daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
        var weekRow = $('<div class="calendar-row"></div>');
        for (var i = 0; i < 7; i++) {
            weekRow.append('<div class="calendar-day-header">' + daysOfWeek[i] + '</div>');
        }
        calendar.append(weekRow);

        // Dates in the month
        var date = 1;
        for (var i = 0; i < 6; i++) {
            var weekRow = $('<div class="calendar-row"></div>');
            for (var j = 0; j < 7; j++) {
                if (i === 0 && j < firstDay) {
                    weekRow.append('<div class="calendar-day empty"></div>');
                } else if (date > days) {
                    weekRow.append('<div class="calendar-day empty"></div>'); // Fill empty cells
                } else {
                    var cellDate = year + '-' + (month + 1).toString().padStart(2, '0') + '-' + date.toString().padStart(2, '0');
                    var cell = $('<div class="calendar-day clickable">' + date + '</div>').data('date', cellDate);
                    weekRow.append(cell);
                    date++;
                }
            }
            calendar.append(weekRow);
            if (date > days) {
                break;
            }
        }

        // Attach click event to clickable cells
        $('.clickable').click(function () {
            var selectedDate = $(this).data('date');
            // Redirect to the "day/cell_date" URL
            window.location.href = '/day/' + selectedDate;
        });
    }

    function changeMonth(step) {
        currentMonth += step;
        if (currentMonth < 0) {
            currentMonth = 11;
            currentYear--;
        } else if (currentMonth > 11) {
            currentMonth = 0;
            currentYear++;
        }
        updateCalendar(currentMonth, currentYear);
    }

    $('#prevMonth').click(function () {
        changeMonth(-1);
    });

    $('#nextMonth').click(function () {
        changeMonth(1);
    });

    updateCalendar(currentMonth, currentYear);
});
