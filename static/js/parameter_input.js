// Получите ссылки на кнопки "Next" и "Previous"
var nextButtons = document.getElementsByClassName("next");
var prevButtons = document.getElementsByClassName("previous");

// Получите все fieldset
var fieldsets = document.getElementsByTagName("fieldset");
var currentFieldset = 0; // Текущий fieldset, начиная с 0

// Скрыть все fieldset, кроме первого
for (var i = 1; i < fieldsets.length; i++) {
    fieldsets[i].style.display = "none";
}

// Обработчик нажатия кнопки "Далее"
function next() {
    // Проверка, что мы не достигли последнего fieldset
    if (currentFieldset < fieldsets.length - 1) {
        // Скрыть текущий fieldset
        fieldsets[currentFieldset].style.display = "none";
        // Показать следующий fieldset
        fieldsets[currentFieldset + 1].style.display = "block";
        // Обновить текущий fieldset
        currentFieldset++;
        if (animating) return;
        animating = true;

        current_fs = $(this).parent();
        next_fs = $(this).parent().next();

// активируем следующий шаг на прогресс-баре, используя индекс next_fs
        $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");

    }
}

// Обработчик нажатия кнопки "Назад"
function previous() {
    // Проверка, что мы не находимся на первом fieldset
    if (currentFieldset > 0) {
        // Скрыть текущий fieldset
        fieldsets[currentFieldset].style.display = "none";
        // Показать предыдущий fieldset
        fieldsets[currentFieldset - 1].style.display = "block";
        // Обновить текущий fieldset
        currentFieldset--;
    }
}

// Назначить обработчики событий кнопкам "Далее" и "Назад"
for (var i = 0; i < nextButtons.length; i++) {
    nextButtons[i].addEventListener("click", next);
}

for (var i = 0; i < prevButtons.length; i++) {
    prevButtons[i].addEventListener("click", previous);
}