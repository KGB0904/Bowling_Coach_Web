const fs = require('fs');
const path = require('path');

class GetGraphUseCase {
    updateGraphHtml(html, recodeFilePath, numberOutput, cnt = 5) {
        // recode 파일 내용 읽기
        let fileContent_pre = fs.readFileSync((recodeFilePath), 'utf8');
        let lines_pre = fileContent_pre.trim().split('\n');
        let lastLine_pre = lines_pre[lines_pre.length - 1];
        
        // numberOutput이 마지막 라인과 다를 경우, 파일에 추가
        if (lastLine_pre !== numberOutput) {
            fs.appendFileSync((recodeFilePath), `\n${numberOutput}`);
        }
      
        // 업데이트된 recode 파일 내용 읽기
        let fileContent = fs.readFileSync((recodeFilePath), 'utf8');
        let lines = fileContent.trim().split('\n');
        let lineCount = lines.length;
        
        // 마지막 5줄 (혹은 그 이하) 가져오기
        let limitedLineCount = Math.min(lineCount, 5);
        let lastNumber = lines.slice(-limitedLineCount).map(Number);

        // 마지막 5개의 숫자를 JSON 문자열로 변환
        let recodeString = JSON.stringify(lastNumber);
        html = html.replace("{{accuracys}}", recodeString);

        // xarray 인덱스 계산
        let array = [];
        for (let i = lineCount - limitedLineCount + 1; i <= lineCount; i++) {
            array.push(i);
        }
        
        // xarray를 JSON 문자열로 변환
        let xarray = JSON.stringify(array);
        html = html.replace("{{count}}", xarray);

        return html;
    }
}

module.exports = { GetGraphUseCase };
