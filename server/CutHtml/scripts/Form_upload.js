class Form_upload {
    $form;
    constructor() {
        this.$form = document.getElementById('upload-form'); //업로드 폼
    }
    //bool(True, False)
    //파일 크기 확인 후 제한 크기 초과하면 오류
    //window : 브라우저 창
    //iFile : 파일 객체
    //errorMsg : 오류메세지
    // LimitSize : 허용된 초대 파일 크기
    checkFS(iFile, errorMsg, limitSize) {
        //브라우저 창에 파일읽기, 파일객체, 파일목록, 바이너리 파일 데이터가 정의되어 있고
        if (window.FileReader && window.File && window.FileList && window.Blob) {
            //파일리스트의 첫번째가 존재하면
            if (typeof iFile.files[0] !== "undefined") {
                //파일 사이즈가 한계치보다 크다면
                if (iFile.files[0].size > limitSize) {
                    //errormsg와 false return
                    errorMsg.innerText = '당신이 보내려는 파일이 너무 큽니다! 허용된 최대 크기는 100MB입니다.';
                    return false;
                }
            } else {
                return false; //파일리스트에 첫번째가 존재하지 않다면 false
            }
        }
        return true; 
    }
}



export default new Form_upload();