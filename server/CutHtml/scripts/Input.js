class Input {
    $iFrom;
    $iTo;
    $iFile;
    $iSubmit = document.querySelector(".input-submit input");   //html input-submit 클래스의 input 요소를 참조
    $iFeedback = document.querySelector(".test-submit input");   //html input-submit 클래스의 input 요소를 참조
    
    constructor() {
        this.$iFrom = document.querySelector("#from");          //from이라는 id(#)참조
        this.$iTo = document.querySelector("#to");              //to
        this.$iFile = document.getElementById('raw');           //raw(id)의 첫번째 요소 : input type ="file" 참조
    }

    //입력된 문자열 배열로 분리후 각 문자마다 :와 숫자만 남기고 다시 문자열로 합치는 함수
    //시간 입력칸에 문자로 들어올 수도 있으니까 문자 다 쳐내는 함수임
    filterInputValue(value) {
        return value.split('').filter(
            char => { //각 문자 분리 후 배열로
            char = char.replace(/[^\d:]/, "");  //숫자와 : 제외한 모든 문자 제거
    
            if (char) {
                return char; //비어 있지 않으면 숫자와 :만 return
            }
        }).join('');
    }

    //시작초 끝초 설정 밑 시간 형식에 맞게 수정
    // e(이벤트 객체), video(비디오 요소), Utils(유틸리티 함수 객체)
    formatTime(e, video, Utils) {
        e.target.maxLength = 8;                         //최대 8개의 숫자 00:00:00
        e.target.pattern = "[0-9]{2}:[0-9]{2}:[0-9]{2}";//0부터 9까지 2번반복 :기준으로 3번
    
        let value = e.target.value;                     //html value
        let seconds;
        value = this.filterInputValue(value);           //숫자와 : 빼고 다 제거
        seconds = Number(value);                        //숫자로 변환하여 시간 값 저장
    
        if (seconds <= 0 && !isNaN(seconds) || !value) {//초가 음수, 숫자가 아닌 혹은 value가 공백이면 0초로 지정
            value = "00:00:00";
            seconds = Number(value);
        }
    
        if (!isNaN(seconds) && seconds > Utils.DAY_IN_SECONDS) { //숫자가 아니고 24시간 초과하면 23시간으로맞춤
            value = "23:59:59";
            seconds = Number(value);
        }
    
        if (!e.target.checkValidity()) {                //이벤트 객체의 타겟이 유효하지 않는다면 숫자만 남김
            value = value.replace(/\D/g, "");
            seconds = Number(value);
        }
    
        if (!isNaN(seconds)) {                          //초가 숫자라면
            value = Utils.secondsToClockTime(seconds);  //초를 시간, 분, 초단위로 나눔
        }
    
        const actualSeconds = Utils.goTo(value);        //초단위로 변환하여 actualSeconds에 저장
        if (e.target === this.$iFrom) {                 //이벤트가 발생한 요소(target)가 실행시간이면
            video.currentTime = actualSeconds;          //재생시작 시작 시간 입력값으로 설정 //비디오이 현재 시간을 입력된(변경된) 초값으로 바꿈
        } else if (video.duration && actualSeconds > video.duration) { //비디오 재생시간이라는게 있고(비디오가 잘 로드 되었고) 비디오의 재생시간보다 입력된 초 값이 크다면
            value = Utils.secondsToClockTime(video.duration);//동영상길이를 최대 길이로 설정
        }
    
        e.target.value = value; //html요소로 보내서, 화면에 표시
    }

    //e.target.files[0] : 파일 입력 이벤트에서 선택된 파일
    //파일 읽는 함수
    readFile(e, video, errorMsg, limitSize) {
        if (e.target.files[0].size <= limitSize) {
            errorMsg.innerText = '';
            this.$iSubmit.removeAttribute('disabled');  //자르기 버튼 활성화
            this.$iFeedback.removeAttribute('disabled'); 
        } else {    //파일크기가 제한크기보다 크면
            this.$iSubmit.setAttribute('disabled', 'disabled'); //자르기 버튼 비활성화
            errorMsg.innerText = '파일이 너무 큽니다. (최대 크기 100MB)';
        }
    
        let file = e.target.files[0];   //선택된 파일
        let fr = new FileReader();      //파일리더 객체 : 클라이언트 측에서 파일 처리 가능
    
        fr.addEventListener("load", () => { //fr에 load이벤트(파일 읽기 작업 완료시 발생) 추가
            video.autoplay = true;          //비디오 자동재생 활성화
            video.controls = true;          //비디오에 컨트롤러 표시
            video.src = fr.result;          //로드된 파일 비디오 src에 할당
        });
    
        fr.readAsDataURL(file);             //선택된 파일 데이터 url로 읽어드림
    }

    //비디오 dto 객체에 넣어서 삽입
    async insertVideo(path) {
        const res = await fetch(path);  //path에서 비디오(리소스) 가져오기
        const blob = await res.blob();  //res(비디오)를 이진데이터로 변환
        const pos = path.lastIndexOf(".");// path의 . 인덱스 반환
        const extname = path.slice(pos);//path의 확장자 추출 ex)mp4,mov 

        const dto = new DataTransfer() || new ClipboardEvent("").clipboardData; //dto : 데이터 전송될 때 담기는 객체
        dto.clearData();                //dto 객체 초기화

        const file = new File([blob], `truncated-video${extname}`, { type: blob.type }); //비디오를 MINE파일로 다시 저장
        dto.items.add(file);            //수정된 파일 전송될 화물칸에 담기
        this.$iFile.files = dto.files;  //선택된 파일로 삽입
    }
}

export default new Input();
