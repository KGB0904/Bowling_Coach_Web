const { resolve } = require("path");

class GetVideoController {
    getVideoUseCase;

    constructor(getVideoUseCase) {
        this.getVideoUseCase = getVideoUseCase;
    }

    async handle(request, response) {
        const fileExists = this.getVideoUseCase.execute(request.params.name);   //name가져오기

        if(fileExists) {
            return response.status(200)                                         //HTTP 응답의 상태 코드를 200(성공)으로 설정
            .sendFile('/index.html', {                                          //클라이언트에게 파일 전송
                root: resolve(__dirname, '..', '..', '..', 'CutHtml') 
            });
        }

        return response.redirect("/");                                          //파일이 존재하지 않으면 root 경로로
    }
}

module.exports = { GetVideoController };