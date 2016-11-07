from models import User
from models import Tweet

from .session import session
from utils import template
from utils import response_with_headers
from utils import redirect
from utils import error

from utils import log


def current_user(request):
    session_id = request.cookies.get('user', '')
    user_id = session(session_id)
    if user_id is not None:
        return User.find(user_id)
    else:
        return None

# 微博相关页面
def index(request):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(headers)
    user_id = request.query.get('user_id', -1)
    user_id = int(user_id)
    user = User.find(user_id)
    if user is None:
        return error(request)
    # 找到 user 发布的所有 weibo
    weibos = Tweet.find_all(user_id=user_id)
    for w in weibos:
        w.load_comments()
    log('weibos', weibos)
    body = template('weibo_index.html', weibos=weibos, user=user)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def new(request):
    headers = {
        'Content-Type': 'text/html',
    }
    uid = current_user(request)
    header = response_with_headers(headers)
    user = User.find(uid)
    body = template('weibo_new.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def add(request):
    user = current_user(request)
    # 创建微博
    form = request.form()
    w = Tweet(form)
    w.user_id = user.id
    w.save()
    return redirect('/tweet/index?user_id={}'.format(user.id))


def delete(request):
    user = current_user(request)
    # 删除微博
    weibo_id = int(request.query.get('id', -1))
    Tweet.delete(weibo_id)
    return redirect('/tweet/index?user_id={}'.format(user.id))


def edit(request):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(headers)
    # r = header + '\r\n' + body
    # return r.encode(encoding='utf-8')
    pass


def update(request):
    # 重定向到用户的主页
    # return redirect('/tweet/index?user_id={}'.format(user.id))
    pass


# 定义一个函数统一检测是否登录
def login_required(route_function):
    def func(request):
        u = current_user(request)
        log('登录鉴定, u ', u)
        if u is None:
            log('u is none')
            # 没登录 不让看 重定向到 /login
            return redirect('/login')
        else:
            log('u is not NONE')
            # 登录了, 正常返回路由函数响应
            return route_function(request)
    return func


route_dict = {
    '/tweet/index': index,
    '/tweet/new': login_required(new),
    '/tweet/add': login_required(add),
    '/tweet/delete': login_required(delete),
    '/tweet/edit': login_required(edit),
    '/tweet/update': login_required(update),
}
