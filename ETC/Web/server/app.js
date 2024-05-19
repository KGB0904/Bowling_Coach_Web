const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

const app = express();
const port = 8080; // 포트 번호를 8080으로 고정

// 동영상을 저장할 디렉토리 설정
const uploadDir = path.join(__dirname, 'videos');

// 디렉토리가 없으면 생성
if (!fs.existsSync(uploadDir)){
    fs.mkdirSync(uploadDir);
}

// Multer 설정
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, uploadDir);
    },
    filename: (req, file, cb) => {
        cb(null, file.originalname);
    }
});
const upload = multer({ storage: storage });

// 루트 경로에 파일 업로드 폼 제공
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// 동영상 업로드 및 자르기 처리
app.post('/upload', upload.single('video'), (req, res) => {
    const startTime = req.body.startTime;
    const endTime = req.body.endTime;
    const inputFilePath = req.file.path;
    const outputFilePath = path.join(uploadDir, 'cut_video.mp4');
    
    const ffmpegProcess = spawn('ffmpeg', [
        '-i', inputFilePath,
        '-ss', startTime,
        '-to', endTime,
        '-c', 'copy',
        outputFilePath
    ]);

    ffmpegProcess.on('close', (code) => {
        if (code === 0) {
            res.send('동영상이 자르고 저장되었습니다.');
            // 업로드한 원본 동영상 파일을 삭제
            fs.unlinkSync(inputFilePath);
        } else {
            res.status(500).send('동영상 자르기 실패');
        }
    });
});

// 서버 시작
app.listen(port, () => {
    console.log(`서버가 http://localhost:${port} 에서 실행 중입니다.`);
});
