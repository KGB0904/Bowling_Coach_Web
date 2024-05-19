function setChartColor(percentage) {
    const chart = document.querySelector('.chart');
    if (percentage < 60) {
        chart.style.background = `conic-gradient(#ff0000 0, #ff0000 ${percentage}%, #ccc ${percentage}%, #ccc 100%)`;
    } else if (percentage < 80) {
        chart.style.background = `conic-gradient(#ffeb3b 0, #ffeb3b ${percentage}%, #ccc ${percentage}%, #ccc 100%)`;
    } else if (percentage < 95) {
        chart.style.background = `conic-gradient(#4caf50 0, #4caf50 ${percentage}%, #ccc ${percentage}%, #ccc 100%)`;
    } else {
        chart.style.background = `conic-gradient(red, orange, yellow, green, blue, indigo, violet)`;
    }
}

function animateProgress(targetPercentage, duration) {
    const percentageElem = document.querySelector('.percentage');
    let start = null;

    function step(timestamp) {
        if (!start) start = timestamp;
        const progress = timestamp - start;
        const percentage = Math.min((progress / duration) * targetPercentage, targetPercentage);
        setChartColor(percentage);
        percentageElem.textContent = `${Math.round(percentage)}%`;

        if (percentage < targetPercentage) {
            window.requestAnimationFrame(step);
        }
    }

    window.requestAnimationFrame(step);
}

const initialPercentage = parseInt('{{numberOutput}}', 10);
animateProgress(initialPercentage, 3000);