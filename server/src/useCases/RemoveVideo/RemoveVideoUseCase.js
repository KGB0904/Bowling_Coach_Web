const fs = require("fs");
const { resolve } = require("path");
const { createTemporaryFolder } = require("../CreateTemporaryFolder")

//30분뒤에 파일 삭제 예약
class RemoveVideoUseCase {
    execute(path) {
        const filepath = resolve(createTemporaryFolder.path, 'edited', path);
        const fileExists = fs.existsSync(filepath);
        const TWENTY_NINE_MINUTES = 29 * 60 * 1000; //30분

        //파일 존재하면 
        if(fileExists) {
            setTimeout(() => {              //비동기적 함수
                fs.unlinkSync(filepath);    //TWENTY_NINE_MINUTES 시간뒤에 filepath에 있는 파일 삭제
            }, TWENTY_NINE_MINUTES);

            return true;
        }

        //파일이 존재하지 않는 경우
        return false;
    }
}

module.exports = { RemoveVideoUseCase };