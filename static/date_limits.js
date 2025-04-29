
    // Obtener la fecha actual
    const today = new Date();
    const twoMonthsLater = new Date();
    twoMonthsLater.setMonth(today.getMonth() + 2);

    // Formatear las fechas al formato "YYYY-MM-DD"
    const formatDate = (date) => date.toISOString().split('T')[0];

    // Establecer límites en el input
    document.getElementById("date-limited").min = formatDate(today);
    document.getElementById("date-limited").max = formatDate(twoMonthsLater);
