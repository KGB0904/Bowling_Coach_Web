document.addEventListener('DOMContentLoaded', (event) => {
  const socket = io();
  const progressBar = document.getElementById('progressBar');
  let progress = 0;

  socket.on('terminalData', (data) => {
    const terminalOutput = document.getElementById('terminalOutput');
    terminalOutput.innerHTML += data + '<br>';

    // Increase progress by 25% for each terminalData event
    progress += 20;
    progressBar.style.width = progress + '%';
    progressBar.innerText = progress + '%';
  });

  socket.on('redirect', (url) => {
    window.location.href = url;
  });
});
