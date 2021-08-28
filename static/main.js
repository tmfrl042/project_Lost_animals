// 공통
$(document).ready(function () {
    showCenter();
    showDogs().hide();
    showList().hide();
    tab_acv();
    $('.nav2-content').hide();
    $('.nav3-content').hide();
    $('.nav4-content').hide();


});
function tab_acv(){
    $('#nav1').on('click', function () {
        $('#nav1').addClass('acv')
        $('#nav2').removeClass('acv')
        $('#nav3').removeClass('acv')
        $('#nav4').removeClass('acv')
        $('.nav1-content').show();
        $('.nav2-content').hide();
        $('.nav3-content').hide();
        $('.nav4-content').hide();
    })
    $('#nav2').on('click', function () {
        $('#nav2').addClass('acv')
        $('#nav1').removeClass('acv')
        $('#nav3').removeClass('acv')
        $('#nav4').removeClass('acv')
        $('.nav2-content').show();
        $('.nav1-content').hide();
        $('.nav3-content').hide();
        $('.nav4-content').hide();
    })
    $('#nav3').on('click', function () {
        $('#nav3').addClass('acv')
        $('#nav1').removeClass('acv')
        $('#nav2').removeClass('acv')
        $('#nav4').removeClass('acv')
        $('.nav3-content').show();
        $('.nav1-content').hide();
        $('.nav2-content').hide();
        $('.nav4-content').hide();
    })
    $('#nav4').on('click', function () {
        $('#nav4').addClass('acv')
        $('#nav1').removeClass('acv')
        $('#nav2').removeClass('acv')
        $('#nav3').removeClass('acv')
        $('.nav4-content').show();
        $('.nav1-content').hide();
        $('.nav2-content').hide();
        $('.nav3-content').hide();
    })

}

// nav1-content
function showCenter() {
    $.ajax({
        type: 'GET',
        url: '/center',
        data: {},
        success: function (response) {
            let centers = response['bohocenters']
            for (let i = 0; i < centers.length; i++) {
                let sigun = centers[i]['SIGUN_NM']
                let name = centers[i]['SHTER_NM']
                let add = centers[i]['PROTECT_PLC']
                let telno = centers[i]['SHTER_TELNO']

                let temp_html = `<tr>
                                    <td>${sigun}</td>
                                    <td>${name}</td>
                                    <td>${add}</td>
                                    <td>${telno}</td>
                                 </tr>`
                $('#center-list').append(temp_html)
            }
        }
    })
}

function search() {
    let address1 = $('#input-sido').val();
    let address2 = $('#input-sigun').val();
    $.ajax({
        type: "POST",
        url: "/center",
        data: {address1_give: address1, address2_give: address2},
        success: function (response) {
            if (response["result"] == "success") {
                alert(response["msg"]);
                window.location.reload();
            }
        }
    })
}


// nav2-content


function showDogs() {
    // 서버의 데이터 받아오기 (이미지경로,공고고유번호,품종,체중,발견장소,공고시작일자,종료일자)
    $.ajax({
        type: 'GET',
        url: '/dogs',
        data: {},
        success: function (response) {
            let dogs = response['dogs_notices']
            for (let i = 0; i < dogs.length; i++) {
                let image = dogs[i]['IMAGE_COURS']
                let number = dogs[i]['PBLANC_IDNTFY_NO']
                let breed = dogs[i]['SPECIES_NM']
                let weight = dogs[i]['BDWGH_INFO']
                let discovery = dogs[i]['DISCVRY_PLC_INFO']
                let start = dogs[i]['PBLANC_BEGIN_DE']
                let end = dogs[i]['PBLANC_END_DE']

                let temp_html = `<div class="card">
                                     <img src="${image}" class="card-img-top" alt="...">
                                            <div class="card-body">
                                                <a href="###" class="card-title">${number}</a>
                                                <hr>
                                                <p class="card-text"><span style="color: gray">품종</span> ${breed}</p>
                                                <p class="card-text"><span style="color: gray">체중</span> ${weight}</p>
                                                <p class="card-text"><span style="color: gray">발견</span> ${discovery}</p>
                                                <p class="card-text"><small class="text-muted">${start}~${end}</small></p>
                                            </div>
                                   </div>`
                $('#dogs-list').append(temp_html)
            }
        }
    })
}

// nav3-content

// nav4-content


function openClose() {
    if ($("#form").css("display") == "block") {
        $("#form").hide();
        $(".submit").text('후기작성');

    } else {
        $("#form").show();
        $(".submit").text('접어두기');
    }
}

function reviewMore() {
    if ($(".description").is(':visible') == true) {
        $("#description").removeClass('description')
        $("#more_openClose").text("닫기");
    } else {
        $("#description").addClass('description');
        $("#more_openClose").text("전체글 보기");
    }

}

function makeList() {
    let nickname = $('#nickname').val()
    let title = $('#title').val()
    let comment = $('#comment').val()
    let password = $('#password').val()

    $.ajax({
        type: "POST",
        url: "/review",
        data: {nickname_give: nickname, title_give: title, comment_give: comment, password_give: password},
        success: function (response) {
            alert(response["msg"]);
            window.location.reload();
        }
    })
}

function showList() {
    $.ajax({
        type: "GET",
        url: "/review",
        data: {},
        success: function (response) {
            let reviews = response['all_reviews']
            for (let i = 0; i < reviews.length; i++) {
                let id = reviews[i]['id']
                let nickname = reviews[i]['nickname']
                let title = reviews[i]['title']
                let comment = reviews[i]['comment']

                let temp_html = `<div class="card written-review" style="max-width: 1200px;">
                                     <div class="card-body">
                                         <div class="review-title">
                                            <h5 class="card-title">${title}</h5>
                                            <h6 class="card-subtitle mb-2 text-muted name">by ${nickname}</h6>
                                         </div>

                                         <p id="description" class="card-text description">${comment}</p>
                                         <div class="btnGroup d-flex align-items-center">
                                             <button id="more_openClose" onclick="reviewMore()" class="btn btn-more btn-light">전체글 보기</a>
                                             <button type="button" onclick="reviewUpdate('modify','${id}')" class="btn btn-modify btn-light">수정</button>
                                             <button type="button" onclick="reviewUpdate('delete','${id}')" class="btn btn-delete btn-light">삭제</button>
                                         <div id="pw_confirm">
                                             <div class="p-2">
                                                <label class="col-form-label">비밀번호</label>
                                             </div>
                                             <div class="p-2">
                                                 <input type="password" id="pwd_confirm" class="form-control" aria-describedby="passwordHelpInline">
                                             </div>
                                             <div class="p-2">
                                                 <button type="button" id="pw_confirm_btn" class="btn btn-confirm btn-secondary">확인</button>
                                             </div>
                                         </div>
                                      </div>

                                     </div>
                                  </div>`

                $('#list').append(temp_html)
            }
        }

    })
}

function reviewUpdate(type, id) {
    let targetUrl;
    if ($("#pw_confirm").is(':visible') == true) {
        $("#pw_confirm").hide();
        $("#pw_confirm").removeClass('d-flex')
    } else {
        $("#pw_confirm").show();
        $("#pw_confirm").addClass('d-flex')
    }
    if (type == "modify") {
        alert('이건 ' + id + ' 수정')
        targetUrl = "/update"
    } else if (type == "delete") {
        alert('이건 ' + id + ' 삭제')
        targetUrl = "/delete"

    }

    $("#pw_confirm_btn").click(function () {
        reviewUpdateTransac(id, targetUrl)
    })
}

function reviewUpdateTransac(id, targetUrl) {
    let confirmPassword = $('#pwd_confirm').val()
    $.ajax({
        type: "POST",
        url: targetUrl,
        data: {id_give: id, confirmPassword_give: confirmPassword},
        success: function (response) {
            alert(response["msg"]);
            window.location.reload();
        }
    })
}