import Check from './Check.js';
import Video from './Video.js';
import Input from './Input.js';
import Form_upload from './Form_upload.js';
import Utils from './Utils.js';

const A_HUNDRED_MEGA_BYTES = 104857600; // 100MB

const video = Video.$video; // 프리뷰(윈도우 창에 띄워진) 비디오
const iFrom = Input.$iFrom; // from
const iTo = Input.$iTo;     // to
const iFile = Input.$iFile; // 파일 자체를 의미
const iSubmit = Input.$iSubmit; // 자르기 버튼
const iFeedback = Input.$iFeedback; // 자르기 버튼



const videoScrubber = document.getElementById('slider'); // noUiSlider(이중 스크롤바)
//const videoScrubber = document.getElementById('video-scrubber'); // 단일 스크롤바

const errorMsg = document.querySelector('.message'); // 에러 메세지
const form_upload = Form_upload.$form; 

// 용량 너무 크면 진행 막음.
function checkFS(e) {
    const canCut = form_upload.checkFS(iFile, errorMsg, A_HUNDRED_MEGA_BYTES);

    if (!canCut) { // 자를 수 없다면
        e.preventDefault(); // 진행 막음
    }
}

// 파일 읽어오고 처리
function readFile(e) {
    form_upload.removeEventListener('submit', checkFS); // 폼 제출 시 checkFS 이벤트리스너 제거
    form_upload.addEventListener('submit', checkFS); // 폼 제출 시 다시 checkFS, 제거와 제출로 이벤트리스너 중복 방지
    Input.readFile(e, video, errorMsg, A_HUNDRED_MEGA_BYTES); // 파일 다시 읽기(url)
}

// 시간 형식 맞게 설정(format)
function formatTime(e) {
    Input.formatTime(e, video, Utils)
}


// 스크롤바와 비디오 시간 동기화
function syncScrubberWithVideo() {
    // 업데이트 슬라이더의 최대값을 비디오의 지속 시간으로 설정
    videoScrubber.noUiSlider.updateOptions({
        range: {
            min: 0,
            max: video.duration
        }
    });
    
    // 슬라이더의 현재 값을 비디오의 현재 시간으로 설정
    //videoScrubber.noUiSlider.set(video.currentTime);
}



//단일 스크롤바와 비디오 시간 동기화
/*
function syncVideoWithScrubber() {
    video.currentTime = videoScrubber.value;
}
*/


window.addEventListener("DOMContentLoaded", () => {
    if (Check.errorOnTruncate(errorMsg)) { // 잘라 내기 작업 중에 오류가 발생했으면
        return;
    }

    if (Check.successfulOnTruncate(video)) { // 잘라내기 성공했으면
        Input.insertVideo(video.src); // 비디오 소스 삽입
        iSubmit.removeAttribute('disabled'); // 자르기 버튼 활성화
        iFeedback.removeAttribute('disabled'); // 자르기 버튼 활성화

    }
});

var from_can_change=false;


//시작이라는 숫자 나오게
video.addEventListener('timeupdate', () => {
    
    if(from_can_change) {
    Video.timeupdate(iFrom, Utils); // ifrom.value를 현재시간으로 업데이트
    }
    //syncScrubberWithVideo(); // 스크롤바 동기화
});

//끝 이라는 숫자 나오게
video.addEventListener('loadeddata', () => {
    Video.loadeddata(iFrom,iTo, Utils); // iTo.value를 영상 총 길이로 업데이트
    syncScrubberWithVideo(); // 스크롤바 동기화
    videoScrubber.noUiSlider.set(0)
});

iFrom.addEventListener("change", formatTime); // 시작시간 변할 때마다
iTo.addEventListener("change", formatTime); // 위와 동일
iFile.addEventListener('change', readFile); // 파일 읽는 이벤트 추가

//videoScrubber.addEventListener('input', syncVideoWithScrubber);   // 스크롤바 드래그 시 비디오 시간 동기화
var from_time =0
slider.noUiSlider.on('slide', function (values, handle) {           //이중스크롤바 슬라이드 이벤트 핸들러
    
    if (handle === 0) {
        from_can_change=true;
        video.currentTime = values[0];
        from_time=video.currentTime
    }
    else{

        iTo.value=Utils.secondsToClockTime(values[1]);
        from_can_change=false;
        if(from_can_change===false) {
        video.currentTime=values[1]
        

        }
    }
    iFrom.value=Utils.secondsToClockTime(from_time);
});

form_upload.addEventListener('submit', checkFS); // 파일 제출할 때 확인하는 이벤트 추가
