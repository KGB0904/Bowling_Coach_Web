const fs = require('fs');
const path = require('path');

class GetGraphUseCase{
    updateGraphHtml(html, recodeFilePath, numberOutput) {
    // HTML 파일 읽기
        //let html = fs.readFileSync((htmlFilePath), 'utf8');
        let fileContent_pre = fs.readFileSync((recodeFilePath), 'utf8');
        let lines_pre = fileContent_pre.trim().split('\n');
        let lastLine_pre = lines_pre[lines_pre.length - 1];
        
        if (lastLine_pre !== numberOutput) {
            fs.appendFileSync((recodeFilePath), `\n${numberOutput}`);
        }
      

        // 파일 내용 읽기 및 처리
        let fileContent = fs.readFileSync((recodeFilePath), 'utf8');
        let lines = fileContent.trim().split('\n');
        let lineCount = lines.length;
        let limitedLineCount = Math.min(lineCount, 5);
        let lastNumber = lines.slice(-limitedLineCount).map(Number);

        // HTML 파일에 JSON 문자열 삽입
        let recodeString = JSON.stringify(lastNumber);
        //console.log(recodeString);  
        html = html.replace("{{accuracys}}", recodeString);
        let array = [];
       
        for (let i = lineCount - 4; i <= lineCount; i++) {
            array.push(i + 3);
        }
        //console.log(array)

        let xarray = JSON.stringify(array);
        html = html.replace("{{count}}", xarray);
        //console.log("왔다감");
        //console.log(html);

        return html;
    }
}

module.exports = {GetGraphUseCase};
