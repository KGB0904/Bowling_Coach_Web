//모듈
const fs = require('fs');
const path = require('path');
const socketIo = require('socket.io');
const {spawn} = require('child_process');
const http = require('http');

//서버실행
const express = require('express');
const app = express();
const server = http.createServer(app);
const io = socketIo(server);



//미들웨어
const multer = require("./middlewares/multer");
const { cutVideoController } = require("./useCases/CutVideo");
const { getVideoController } = require("./useCases/GetVideo");

//전역경로
const processor_path = path.resolve(__dirname, '..', '..', 'model', 'processor.py');
const sample_path = path.resolve(__dirname, '..', '..', 'model', 'ETC','sample.py');

let video_filePath='' //양동이

//미들웨어 사용
//app.use(express.urlencoded({ extended: true, limit: '10mb' }))
app.use(express.urlencoded({ extended: false }));                       //클라이언트가 html form을 사용해서 보낸 데이터를 처리하는데 도와주는 미들웨어
app.use(express.static(path.resolve(__dirname, '..', 'IndexHtml')));              
app.use(express.static(path.resolve(__dirname, '..', 'CutHtml')));            
app.use(express.static(path.resolve(__dirname, '..', 'temp', 'edited')));    //temp, edited 폴더 사용
app.use(express.static(path.resolve(__dirname, '..', 'temp', 'raw')));       //raw
app.use(express.static(path.resolve(__dirname, '..', 'FBHtml')));
app.use(express.static(path.resolve(__dirname, '..', 'LoadHtml')));  



///////////////////////////////////////////////////////////////////////////////////////////////
//라우터
///////////////////////////////////////////////////////////////////////////////////////////////


//초기화면
app.get('/main', (_, response) => {
  return response.sendFile(path.resolve(__dirname,'..', 'IndexHtml', '1.html'));
});

//영상편집 초기화면
app.get('/start', (_, response) => {
  return response.sendFile(path.resolve(__dirname,'..', 'CutHtml', 'index.html'));
});

//영상편집 진행 화면
app.post('/cut', multer.single('raw'), (request, response) => { // request와 response 인자 두개를 쓴다는 의미
  return cutVideoController.handle(request, response);
});

//영상편집 진행화면 2
app.get('/cut/:name', (request, response) => {
    
  return getVideoController.handle(request, response);
});


//로딩
app.post('/load', multer.single('raw'), (req, res) => {
  console.log("-----------------------------------")
  // 업로드된 파일의 경로
  
  //[1]리얼
  video_filePath = req.file.path;
  let file_path=video_filePath
  console.log(`데이터 전송 완료: ${file_path}`);
  res.sendFile(path.resolve(__dirname , '..','LoadHtml/load.html'));
});

//피드백
app.get('/feedback', (req, res) => {
  const pythonOutput = req.query.output;
  const numberOutput = req.query.number;

  let html = fs.readFileSync(path.resolve(__dirname, '..','FBHtml/feedback.html'), 'utf8');
  html = html.replace('{{pythonOutput}}', pythonOutput);
  html = html.replace('{{numberOutput}}', numberOutput);
  res.send(html);

});


//피드백 클라이언트 대기
io.on('connection', (socket) => {
  console.log('유저의 연결이 성공하였습니다.');

  // 수정
  //98 line 딥러닝_모델.py 실행
  //99 line 단순한 print.py 실행
  //const pythonProcess = spawn('python', [processor_path, video_filePath]);
  const pythonProcess = spawn('python', [sample_path]);


  pythonProcess.stdout.on('data', (data) => {
    const dataString = data.toString();
    const regex = /This is .*?%/;
    const match = dataString.match(regex);
    console.log("-----------------------------------")

    console.log(`모델 출력 로그: ${dataString}`);

    
    
    // "CheckPoint"로 시작하는 데이터만 클라이언트로 전송
    if (dataString.startsWith("Check") || dataString.startsWith("Error!")) {
      socket.emit('terminalData', dataString);
      console.log(`웹페이지 출력 로그: ${dataString}`);

    }
    
    else if(match != null){
        let pythonOutput = match[0]
        console.log(`Output Text : ${pythonOutput}`);
        const numberRegex = /(\d+)%/;
        let numberMatch = pythonOutput.match(numberRegex);
        let numberOutput = numberMatch ? numberMatch[1] : 'No number found';
        console.log(`Output Percent : ${numberOutput}`);

        const redirectUrl = `/feedback?output=${encodeURIComponent(pythonOutput)}&number=${encodeURIComponent(numberOutput)}`;
        socket.emit('redirect', redirectUrl);
    }
  })

  pythonProcess.stderr.on('data', (data) => {
    console.error(`모델 경고 및 에러: ${data}`);
    //socket.emit('terminalData', data.toString()); // 클라이언트로 에러 데이터 전송
  });

  pythonProcess.on('close', (code) => {
    console.log('--------------------------------------------------------');
    console.log(`피드백 무사히 성공 with code ${code}`);
  });

  socket.on('disconnect', () => {
    console.log('--------------------------------------------------------');
    console.log('유저의 연결이 종료되었습니디.');
  });
});


//8000번 포트 실행:
const $PORT = process.env.PORT || 8000;
console.log("http://localhost:"+$PORT+"/main");
console.log("http://192.168.0.2:"+$PORT+"/main");

server.listen($PORT);
