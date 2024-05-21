const express = require('express');
const http = require('http');
const socketIO = require('socket.io');
const { exec } = require('child_process');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = socketIO(server);

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '..','..','FBHtml','ETC','socket.html'));
    
});

io.on('connection', (socket) => {
    console.log('New client connected');

    const samplePyPath = 'C:\\Users\\dongj\\Desktop\\Happy\\University\\Senior_1st\\Graduation_Design\\BFP\\model\\ETC\\sample.py';
    const process = exec(`python "${samplePyPath}"`);

    process.stdout.on('data', (data) => {
        const regex = /This is .*?%/;
        const match = data.match(regex);
        const pythonOutput = match ? match[0] : 'No matching output found';

        const numberRegex = /(\d+)%/;
        const numberMatch = pythonOutput.match(numberRegex);
        const numberOutput = numberMatch ? numberMatch[1] : 'No number found';

        // 클라이언트로 데이터를 보냅니다.
        socket.emit('python_output', { output: pythonOutput, number: numberOutput });
    });

    process.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });

    process.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
        socket.emit('python_output', { output: 'Process finished', number: '' });
    });

    socket.on('disconnect', () => {
        console.log('Client disconnected');
    });
});

const PORT = process.env.PORT || 8000;
server.listen(PORT, () => console.log(`http://localhost:${PORT}`));
