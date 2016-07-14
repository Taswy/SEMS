
jQuery(document).ready(function() {
    /*
        Form validation
    */
    $('.register form').submit(function(){
        $(this).find("label[for='number']").html('学号');
        $(this).find("label[for='username']").html('用户名');
        $(this).find("label[for='password']").html('密码');
        ////
        var number = $(this).find('input#number').val();
        var username = $(this).find('input#username').val();
        var password = $(this).find('input#password').val();
        if(number == '') {
            $(this).find("label[for='number']").append("<span style='display:none' class='red'> - 请输入学号.</span>");
            $(this).find("label[for='number'] span").fadeIn('medium');
            return false;
        }
        if(username == '') {
            $(this).find("label[for='username']").append("<span style='display:none' class='red'> - 请输入用户名.</span>");
            $(this).find("label[for='username'] span").fadeIn('medium');
            return false;
        }
        if(password == '') {
            $(this).find("label[for='password']").append("<span style='display:none' class='red'> - 请输入密码.</span>");
            $(this).find("label[for='password'] span").fadeIn('medium');
            return false;
        }
    });


});


