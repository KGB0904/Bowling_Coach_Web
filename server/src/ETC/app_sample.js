const express = require('express');
const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');
const app = express();

// 파이썬 파일 경로 설정
const samplePyPath = path.resolve(__dirname, '..', '..', '..','model', 'ETC', 'sample.py');

app.get('/load', (req, res) => {
    exec(`python "${samplePyPath}"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return res.status(500).send('Something went wrong');
        }
    const regex = /This is .*?%/;
    const match = stdout.match(regex);
    const pythonOutput = match ? match[0] : 'No matching output found';

    //let html = fs.readFileSync(path.join(__dirname, '..','FBHtml', 'Donut_Chart_FeedBack.html'), 'utf8');

    const numberRegex = /(\d+)%/;
    const numberMatch = pythonOutput.match(numberRegex);
    const numberOutput = numberMatch ? numberMatch[1] : 'No number found';


        // 파이썬 출력 내용을 /페이지로 전달합니다.
    res.redirect(`/feedback?output=${encodeURIComponent(pythonOutput)}&number=${encodeURIComponent(numberOutput)}`);
    });
});

app.get('/feedback', (req, res) => {
    const pythonOutput = req.query.output || 'No output found';
    const numberOutput = req.query.number || 'No number found';

    // Use pythonOutput and numberOutput as needed
    console.log(`Python Output: ${pythonOutput}`);
    console.log(`Number Output: ${numberOutput}`);

    let html = fs.readFileSync(path.join(__dirname, '..','..','FBHtml', 'index.html'), 'utf8');

    // HTML 파일에 파이썬 출력을 삽입합니다.
    html = html.replace('{{pythonOutput}}', pythonOutput);
    html = html.replace('{{numberOutput}}', numberOutput);
    res.send(html);

});

app.listen(8000, () => {
    console.log('Server is running on http://localhost:8000');
});
