const btoa = require("btoa");
const bars="-----------------------------------------------------------------"

class CutVideoController {
    cutVideoUseCase;            //클래스의 속성 선언

    constructor(cutVideoUseCase) {
        this.cutVideoUseCase = cutVideoUseCase;
    }

    toSeconds(time) {
        let [hours, minutes, seconds] = time.split(":").map(Number);

        minutes = hours * 60 + minutes;
        seconds = minutes * 60 + seconds;

        return seconds;
    }

    async handle(request, response) {
        let { from, to } = request.body;
        // 요청에 파일이 포함되어 있는지 확인
        if (!request.file) {
            console.log(bars);

            console.log("업로드 파일 인식 실패");
            return response.status(400).json({ error: "No file uploaded" });

        }
        else{
            console.log(bars);
            console.log("업로드 파일 인식 성공 및 비디오 정보");
        }
        console.log("비디오 형식 : ", request.file.mimetype);
    
        const { filename, path: input } = request.file;
        console.log("현재 영상이 피드백 시 저장될 경로 : "  ,input);
        const { editedFolder, rawFolder } = request;
    
        const output = `truncated-${filename}`;
    
        from = this.toSeconds(from);
        to = this.toSeconds(to);
    
        const truncated = await this.cutVideoUseCase.execute({ 
            input,
            output,
            from,
            to,
            rawFolder,
            editedFolder
        });
    
        if (truncated) {
            return response.status(200).redirect(`/cut/${btoa(output)}`);
        }
    
        return response.status(500).redirect("/?truncated=false");
    }
    
}

module.exports = { CutVideoController };
