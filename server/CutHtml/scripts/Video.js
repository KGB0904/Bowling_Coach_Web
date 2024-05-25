class Video {
    $video;
    constructor() {
        this.$video = document.querySelector("#preview video"); //preview의 비디오 가져오기
    }

    //비디오의 현재시간을 가져와서 시간입력 from부분에 넣기, 보통 0초
    timeupdate(iFrom, Utils) {
        const currentTime = this.$video.currentTime; //비디오 현재시간 업데이트

        iFrom.value = Utils.secondsToClockTime(currentTime); //비디오의 현재시간을 시분초로 변환해서 시작시간(ifrom)의 value에 넣기
    }
    
    //비디오의 끝 부분을 가져와서 시간입력 to 부분에 넣기
    loadeddata(iFrom,iTo, Utils) {
        iFrom.value="00:00:00"
        iTo.value = Utils.secondsToClockTime(this.$video.duration);
        this.$video.currentTime = 0;
        //현재시간 0으로 초기화하는 이유 : 
        //비디오가 새로 로드될 때마다 비디오를 다시 시작하게 함.
    }
}

export default new Video();

