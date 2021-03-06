// 공통
$(document).ready(function () {

    $(".nav_content").hide();
    $(".nav_content").eq(0).show();
    $(".nav_btn_group button").click(function () {
        $(".nav_btn_group button").removeClass("active")
        $(this).addClass("active")
        $(".nav_content").hide();
        var tabid = $(this).attr("rel");
        $("#" + tabid).fadeIn();
    })

    showCenter()
    showDogs()
    showBlog()
    showList()

    var link = document.location.href;  //현재 접속 url
    var tab = link.split('/').pop();   //배열의 맨 마지막 요소를 삭제하고 삭제된 해당 값을 반환함
    $('a[href$=' + tab + ']').trigger("click"); //해당 앵커 트리거를이용 클릭 이벤트

});
/*
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
*/

// nav1-content
function showCenter() {
    $('#center-list').empty();
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

                if ($('#input-sido').val() == "시/도" && $('#input-sigun').val() == "시/군/구") {
                    $('#center-list').append(temp_html);
                } else if ($('#input-sido').val() == "시/도") {
                    alert("시나 도를 입력하세요");
                    break;
                } else if ($('#input-sido').val() == "경기도") {
                    if ($('#input-sigun').val() == "시/군/구") {
                        alert("시나 군,구를 입력하세요");
                        break;
                    } else if ($('#input-sigun').val() == sigun) {
                        $('#center-list').append(temp_html);
                    }
                }
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
                                                <a href="###" class="card-title2">${number}</a>
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
function showBlog() {
    $.ajax({
        type: 'GET',
        url: '/blog',
        data: {},
        success: function (response) {
            let blogs = response['blog_texts']
            for (let i = 0; i < blogs.length; i++) {
                let title = blogs[i]['title']
                let url = blogs[i]['url']
                let writer = blogs[i]['writer']
                let content = blogs[i]['content']
                let date = blogs[i]['date']
                let img_url = blogs[i]['img_url']
                let temp_html = `<div class="card blog mb-3" style="max-width: 1100px;">
                                    <div class="row g-0">
                                        <div class="col-md-3">
                                            <img src=${img_url} class="blog_img img-fluid rounded-start" alt="...">
                                        </div>
                                        <div class="col-md-9">
                                            <div class="card-body">
                                                <a href="${url}" target="_blank" ><h5 class="card-title text-warning hrefs">${title}</h5></a>
                                                <h6 class="card-subtitle mb-2 text-muted publisher">published by ${writer}</h6>
                                                <a href="${url}" target="_blank" ><p class="card-text text-dark description hrefs">${content}</p></a>
                                                <p class="card-text date"><small class="text-muted">${date}</small></p>
                                            </div>
                                        </div>
                                    </div>
                                </div>`
                $('.inner').append(temp_html)
            }

        }

    })
}

// nav4-content
function openClose() {
    if ($("#review-form").css("display") == "block") {
        $("#review-form").hide();
        $(".btn-submit").text('후기작성');

    } else {
        $("#review-form").show();
        $(".btn-submit").text('접어두기');
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
            showList()
        }
    })
}

function showList() {
    $.ajax({
        type: "GET",
        url: "/review",
        data: {},
        success: function (response) {
            $('#list').empty();
            $("#review-form").hide();

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

                                         <p id="${id}-description" class="card-text description">${comment}</p>
                                         <textarea name="" id="${id}-edit_area" class="edit_area" cols="20" rows="10"></textarea>                                    
                                         <div class="btnGroup d-flex align-items-center">
<!--                                             <button id="more_openClose" onclick="reviewMore()" class="btn btn-more btn-light">전체글 보기</a>-->
                                             <button type="button" onclick="reviewUpdate('modify','${id}')" class="btn ${id}-btn-modify btn-light">수정</button>
                                             <button type="button" onclick="reviewUpdate('delete','${id}')" class="btn ${id}-btn-delete btn-light">삭제</button>
                                            
                                                <div id="${id}-pw_confirm" class="pw-box">
                                                     <div class="p-2">
                                                        <label class="col-form-label">비밀번호</label>
                                                     </div>
                                                     <div class="p-2">
                                                         <input type="password" id="${id}-pwd_confirm" class="form-control" aria-describedby="passwordHelpInline">
                                                     </div>
                                                     <div class="p-2">
                                                         <button type="button" id="${id}-pw_confirm_btn" class="btn btn-confirm btn-warning ">확인</button>
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
    let targetUrl =''
    if ($(`#${id}-pw_confirm`).is(':visible') == true) {
        $(`#${id}-pw_confirm`).hide();
        $(`#${id}-pw_confirm`).removeClass('d-flex')
    } else {
        $(`#${id}-pw_confirm`).show();
        $(`#${id}-pw_confirm`).addClass('d-flex')
    }

    if (type == "modify") {
        targetUrl = "/update"
        startEdit(id)

    } else if (type == "delete") {
        targetUrl = "/delete"
    }

    $(`#${id}-pw_confirm_btn`).click(function () {
        reviewUpdateTransac(id, targetUrl)
        return;
    })
}

function reviewUpdateTransac(id, targetUrl) {
    let confirmPassword =  $(`#${id}-pwd_confirm`).val()
    let reviseContent = $(`#${id}-edit_area`).val()
    console.log(confirmPassword)
    console.log(reviseContent)
    $.ajax({
        type: "POST",
        url: targetUrl,
        data: {id_give: id, confirmPassword_give: confirmPassword, reviseContent_give: reviseContent},
        success: function (response) {
            alert(response["msg"]);
            showList();
        }
    })
}

function startEdit(id){
    let originContent = $(`#${id}-description`).text();
    if ($(`#${id}-edit_area`).css("display") == "none"){
        $(`#${id}-description`).hide();
        $(`#${id}-edit_area`).show();
        $(`#${id}-edit_area`).val(originContent);
        $(`.${id}-btn-modify`).text("닫기");
    } else {
        $(`#${id}-description`).show();
        $(`#${id}-edit_area`).hide();
        $(`.${id}-btn-modify`).text("수정");
    }

}