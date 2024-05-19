//h5모델 로드안되는 이슈로 인한 샘플 실행 파일 ㅅㅂ ㅠㅠ 

//__dirname : 현재 파일의 디렉토리

const express = require('express');
const { exec } = require('child_process');
const path = require('path');
const fs= require('fs');

const app = express();
const sample_py_path = path.resolve(__dirname, '..','..', '..', 'model', 'ETC','sample.py');
app.get('/', (req, res) => {
    exec(`python "${sample_py_path}"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return res.status(500).send('Something went wrong');
        }
    const regex = /This is .*?%/;
    const match = stdout.match(regex);
    const pythonOutput = match ? match[0] : 'No matching output found';

    //let html = fs.readFileSync(path.join(__dirname, '..','FBHtml', 'Donut_Chart_FeedBack.html'), 'utf8');
    let html = fs.readFileSync(path.join(__dirname, '..','..','FBHtml', 'index.html'), 'utf8');

    const numberRegex = /(\d+)%/;
    const numberMatch = pythonOutput.match(numberRegex);
    const numberOutput = numberMatch ? numberMatch[1] : 'No number found';
    console.log(pythonOutput);

    html = html.replace('{{pythonOutput}}', pythonOutput);
    html = html.replace('{{numberOutput}}', numberOutput);
    res.send(html);

    });
});
app.listen(8000, () => {
    console.log('http://localhost:8000');
});