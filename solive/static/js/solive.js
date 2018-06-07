/**
 * Created by lenovo on 2018/4/22.
 */


// 侧边栏响应式显示/隐藏
/*
$(window).resize(function (event) {
   if($(this).width() < 768) {
       $("#toggleSidebarCheck").attr('checked', true);
   }
   else {
       $("#toggleSidebarCheck").attr('checked', false);
   }
});
*/

// 全局搜索
$("#keyword-form").submit(function (event) {
    if(!$(this.keyword).val()) {
        event.preventDefault();
    }
    else {
        event.returnValue = true;
    }
});

// 登陆模态框
$("#login-form").submit(function (event) {
    event.preventDefault();
    var self = this;
    $.ajax({
        type: 'post',
        url: '/auth/login',
        data: $(self).serializeArray(),
        success: function (result) {
            if(result.code == 400) {
                $.each(result.data, function(key, val) {
                    var ele = $("#" + key);
                    ele.parent().addClass('has-error');
                    ele.after('<p class="help-block">' + JSON.stringify(val) + '</p>');
                })
            }
            else {
                window.location.reload();
            }
        }
    });
});

// 注册模态框
$("#register-form").submit(function (event) {
    event.preventDefault();
    var self = this;
    $.ajax({
        type: 'post',
        url: '/auth/register',
        data: $(self).serializeArray(),
        success: function (result) {
            if(result.code == 400) {
                $.each(result.data, function(key, val) {
                    var ele = $("#" + key);
                    ele.parent().addClass('has-error');
                    ele.after('<p class="help-block">' + JSON.stringify(val) + '</p>');
                })
            }
            else {
                $("#register-modal").modal('hide');
                $("#login-modal").modal('show');
            }
        }
    });
});

// so主播
$(".so-control").change(function (event) {
    $.ajax({
        type: 'get',
        url: '/api/videos/hosts',
        data: {
            'source': $("#select-source").val(),
            'cate': $("#select-cate").val()
        }
    }).done(function (result) {
        $(".so-list").empty();
        $.each(result.data, function () {
            $(".so-list").append(
                `<a href="${this.room}" target="_blank"${this.is_live?' class="live"':''}>
                    <div class="host-name">
                        <span title="${this.nickname}">${this.nickname}</span>
                        ${this.is_live?'<i class="badge">live</i>':''}
                    </div>
                    <span class="host-cate" title="${this.cate}">${this.cate}</span>
                    <span class="host-source" title="${this.source}">${this.source}</span>
                </a>`
            );
        });
    });
});

// 渲染so游戏、so娱乐等栏目
$(".cate-label").click(function (event) {
    $(event.target).siblings().removeClass('selected');
    $(event.target).addClass('selected');
    var self = this;
    $.ajax({
        type: 'get',
        url: '/api/videos',
        data: {cate: $(self).text()}
    }).done(function (result) {
        var roomList = $(self).parent().next().children();
        $.each(result.data, function (index, item) {
            $(roomList[index]).find('a:eq(0)').attr('href', this.room);
            $(roomList[index]).find('img').attr('src', this.cover);
            $(roomList[index]).find('.video-title').attr('title', this.title).text(this.title);
            $(roomList[index]).find('.video-number').attr('title', this.viewers_num).html('<i class="glyphicon glyphicon-eye-open"></i>' + this.viewers_num);
            $(roomList[index]).find('.video-nickname').attr('title', this.nickname).text(this.nickname);
            $(roomList[index]).find('.video-category').attr('title', this.cate).text(this.cate);
            $(roomList[index]).find('.video-source').attr('title', `${this.source}直播`).text(`${this.source}直播`);
            $(roomList[index]).find('.video-favorite').attr('data-room', this.room);
        });
        /* TODO 需要考虑data的长度小于8 */
    });
});

// 添加/取消收藏
$(".video-favorite").click(function (event) {
    event.preventDefault();
    var self = this;
    $.ajax({
        type: 'post',
        url: '/favorite',
        data: {
            video: $(self).data('room'),
            operation: $(self).text()
        },
        success: function (result) {
            if(result.code == 200) {
                $(self).text(result.operation);
            }
        }
    });
});

// 添加观看历史
$(".video-box .thumbnail").click(function (event) {
    var self = this;
    $.ajax({
        type: 'post',
        url: '/history',
        data: {
            video: $(self).attr('href')
        }
    });
});

// 上传头像时显示
$("#avatar").change(function (event) {
   var pic = this.files[0];
   var r = new FileReader();
   r.readAsDataURL(pic);
   r.onload = function (event) {
       $(".show-avatar>img").attr("src", this.result);
       $(".avatar").attr("src", this.result);
   };
});

// 修改密码
$("#modify-passwd").submit(function (event) {
    event.preventDefault();
    var self = this;
    $.ajax({
        type: 'post',
        url: '/user/password',
        data: $(self).serialize()
    }).always(function (result) {
        $(self).find(".form-group").each(function () {
            $(this).removeClass('has-error');
        });
        $(self).find(".help-block").each(function () {
            $(this).remove();
        });
        if(result.code == 200) {
            alert('密码修改成功！');
        }
        else {
            $.each(result.data, function (key, val) {
                var ele = $("#" + key);
                ele.parent().addClass('has-error');
                ele.after('<p class="help-block">' + JSON.stringify(val) + '</p>');
            })
        }
    })
});
