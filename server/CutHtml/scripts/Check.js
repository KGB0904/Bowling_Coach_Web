class Check {
    // 오류 발생시 호출
    // location : 현재 url
    // .search : 현재 url의 쿼리 문자열
    // 쿼리 문자열 : ?뒤에 오는 key=value형태로 오는 문자열
    // 이 서버에서는 url 만들 때 ? 안 넣음
    errorOnTruncate(errorMsg) {
        if(location.search.indexOf("?") !== 0 || !location.search) { //현재 url의 쿼리 문자열이 ?로 시작하지 않거나, 쿼리 문자열이 비어있으면         
            return false;
        }
    
        errorMsg.innerText = "동영상을 처리하는데 오류가 발생하였습니다.";
        return true;
    }
    //url에 /cut/가 들어가 있으면 비디오의 경
    //http://localhost:8080/cut/dHJ1bmNhdGVkLTA1OGIwZGY2ODE5MTJmMGMxYzk2Lm1wNA==
    successfulOnTruncate(video) {
        if(location.href.includes("/cut/")) { //현재 페이지의 문자열에 /cut/가 포함되어 있으면면
            const filepath = `/${atob(location.pathname.slice(5))}`; //filepath는 앞의 /cut/제거된 값

            video.controls = true;  //비디오 재생 컨트롤 활성화
            video.autoplay = true;  //비디오 자동재생 허용
            video.src = filepath;   //비디오 경로 설정

            return true;            //페이지 성공적 실행
        }
        
        return false;
    }
}

export default new Check();

// 1. errorOnTruncate : 에러메세지 들어오면 `