const fs = require("fs");
const { resolve } = require("path");
const atob = require("atob");
const { createTemporaryFolder } = require("../CreateTemporaryFolder")


//파일 edited 경로에 존재하면 true, 아니면 false 반환
class GetVideoUseCase {
    execute(path) {
        const fileExists = fs.existsSync(resolve(createTemporaryFolder.path, 'edited', atob(path)));

        if(fileExists) {
            return true;
        }

        return false;
    }
}

module.exports = { GetVideoUseCase };