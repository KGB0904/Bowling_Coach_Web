const fs = require('fs');
const { resolve } = require('path');
const { promisify } = require('util');
const exec = promisify(require('child_process').exec);
const { removeVideoUseCase } = require("../RemoveVideo")
const ffmpeg = require('fluent-ffmpeg');

class CutVideoUseCase {
    execute({ input = '', output = '', from = 0, to = 0, rawFolder, editedFolder }) {
        if(from >= 1) {
            from -= 1;
        }

        output = resolve(editedFolder, output);
        return this.cut(input, output, from, to, rawFolder, editedFolder);
    }


    async cut(input, output, from, to, rawFolder, editedFolder) {
        try {
            await new Promise((resolve, reject) => {
                ffmpeg(input)                           //ffmpeg 인스턴스 생성
                    .setStartTime(from)                 //잘라낼 시작시간 선정
                    .setDuration(to - from)             //잘라낼 시간의 길이 선정
                    .output(output)                     //자른 비디오 저장할 경로
                    .on('end', () => resolve())         //resolve : 이행(계속진행) 상태  
                    .on('error', (err) => reject(err))  //reject : 거절 상태
                    .run();                             //실행
            });

            // 잘라내기가 완료된 후 필요한 작업 수행
            fs.unlinkSync(input);                       //input 파일 링크(연결) 끊기
            removeVideoUseCase.execute(output);         //1분뒤 파일 삭제
            
            return true;
        } catch (error) {                                       //에러 발생시
            console.error(error);                               //콘솔에 출력
            fs.rmdirSync(editedFolder, { recursive: true });    //edited 폴더를 재귀적으로 삭제
            fs.rmdirSync(rawFolder, { recursive: true });       //raw 폴더 재귀적으로 삭제
            return false;
        }
    }

}

module.exports = { CutVideoUseCase };