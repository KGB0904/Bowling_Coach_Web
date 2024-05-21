const multer = require("multer");
const { randomBytes } = require("crypto");
const { resolve, extname } = require("path"); //resolve : 경로, extname : 확장자 추출
const { createTemporaryFolder } = require("../useCases/CreateTemporaryFolder");

//
const storage = multer.diskStorage({
    //저장될 위치
    destination: (req, file, cb) => {//req: http 요청 객체, file : 업로드된 파일, cb : 콜백함수
        createTemporaryFolder.execute(true, 'raw', 'edited'); //임시 폴더 생성

        //request객체에 editedFolder와 rawFolder 속성 추가
        req.editedFolder = resolve(createTemporaryFolder.path, 'edited');
        req.rawFolder = resolve(createTemporaryFolder.path, 'raw');

        cb(null, req.rawFolder); //num : 오류없음을 의미, 업로드된 파일 저장경로 설정.
    },

    //저장할 파일명
    filename: (req, file, cb) => {
        cb(null, file.originalname);
    }
    
})

//호환되는 파일 인지확인하고 cb 함수 실행

const fileFilter = (req, file, cb) => {
    const isAcceptable = [
        'video/mp4',
        'video/webm',
        'video/ogg',
        'video/x-flv',
        'video/3gpp',
        'video/x-msvideo',
        'video/x-ms-wmv',
        'video/mpg'
    ].find(acceptable => acceptable === file.mimetype);

    if(isAcceptable) {
        return cb(null, true);
    }

    return cb(null, false);
}

module.exports = {
    storage,
    fileFilter
}