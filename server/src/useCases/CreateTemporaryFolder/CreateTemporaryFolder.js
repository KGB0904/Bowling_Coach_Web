const fs = require("fs");
const { resolve } = require("path");

class CreateTemporaryFolder {
    constructor(path = '') {    //임시폴더 경로
        this.path = path;
    }

    //execute : 폴더 생성 메서드
    //arg : 임시폴더 이름 ex) args=['folder1', 'folder2', 'folder3']
    execute(recursive = false, ...args) { //recursive : 재귀적으로 : 상위폴더가 존재하지 않으면 상위폴더도 생성한다는 의미
        if(recursive === null || recursive === undefined) {
            recursive = false;
        }

        if(!fs.existsSync(this.path)) {                 //this.path가 존재하지 않으면
            fs.mkdirSync(this.path, { recursive });     //재귀적, 동기적으로 경로에 폴더 생성
        }

        //각 폴더 이름별로 재귀적으로 폴더 생성
        args.forEach(path => {
            path = resolve(this.path, path);

            if(!fs.existsSync(path)) {
                fs.mkdirSync(path, { recursive });
            }
        });
    }
}

module.exports = { CreateTemporaryFolder };