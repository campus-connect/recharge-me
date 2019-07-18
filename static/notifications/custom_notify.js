var notify_badge_class;
var notify_menu_class;
var notify_api_url;
var notify_fetch_count;
var notify_unread_url;
var notify_mark_all_unread_url;
var notify_refresh_period = 15000;
var consecutive_misfires = 0;
var registered_functions = [];

function fill_notification_badge(data) {
    var badges = document.getElementsByClassName(notify_badge_class);
    if (badges) {
        for(var i = 0; i < badges.length; i++){
            badges[i].innerHTML = data.unread_count;
            if (badges[i].getAttribute('class').split(" ").includes('notification-tag')) {
                badges[i].innerHTML = `${data.unread_count} New`;
            } else {
                badges[i].innerHTML = data.unread_count;
            }
        }
    }
}

function fill_notification_list(data) {
    var menus = document.getElementsByClassName(notify_menu_class);
    if (menus) {
        var messages = data.unread_list.map(function (item) {
            var message = "";
            if(typeof item.target == 'undefined'){
                item.target = '';
            }
            return `
            <a href="javascript:void(0)">
                <div class="media">
                    <div class="media-left align-self-center"><i
                        class="ft-download-cloud icon-bg-circle bg-red bg-darken-1"></i></div>
                    <div class="media-body">
                    <h6 class="media-heading red darken-1">${item.actor}</h6>
                    <p class="notification-text font-small-3 text-muted">${item.verb} ${item.target}</p>
                    <small>
                        <time class="media-meta text-muted" datetime="${item.timestamp}">${humanized_time_span(item.timestamp)}</time></small>
                    </div>
                </div>
            </a>
            `;
        }).join('')

        for (var i = 0; i < menus.length; i++){
            menus[i].innerHTML = messages;
        }
    }
}

function register_notifier(func) {
    registered_functions.push(func);
}

function fetch_api_data() {
    if (registered_functions.length > 0) {
        //only fetch data if a function is setup
        var r = new XMLHttpRequest();
        r.addEventListener('readystatechange', function(event){
            if (this.readyState === 4){
                if (this.status === 200){
                    consecutive_misfires = 0;
                    var data = JSON.parse(r.responseText);
                    registered_functions.forEach(function (func) { func(data); });
                }else{
                    consecutive_misfires++;
                }
            }
        })
        r.open("GET", notify_api_url+'?max='+notify_fetch_count, true);
        r.send();
    }
    if (consecutive_misfires < 10) {
        setTimeout(fetch_api_data,notify_refresh_period);
    } else {
        var badges = document.getElementsByClassName(notify_badge_class);
        if (badges) {
            for (var i = 0; i < badges.length; i++){
                badges[i].innerHTML = "!";
                badges[i].title = "Connection lost!"
            }
        }
    }
}

setTimeout(fetch_api_data, 1000);
