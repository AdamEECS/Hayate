from models import User
from models import Tweet
from models import Comment

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


def new(request):
    headers = {
        'Content-Type': 'text/html',
    }
    # uid = current_user(request)
    header = response_with_headers(headers)
    # user = User.find(uid)
    tid = request.query.get('tweet_id', -1)
    body = template('comment_new.html', tweet_id=tid)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def add(request):
    user = current_user(request)
    # 创建评论
    form = request.form()
    c = Comment(form)
    c.user_id = user.id
    c.save()
    log('comment add', c, c.tweet_id)
    t = Tweet.find(c.tweet_id)
    u = User.find(t.user_id)
    return redirect('/tweet/index?user_id={}'.format(u.id))


def delete(request):
    user = current_user(request)
    # 删除评论
    comment_id = int(request.query.get('id', -1))
    c = Comment.find(comment_id)
    t = Tweet.find(c.tweet_id)
    uid = t.user_id
    if user.id == t.user_id:
        Comment.delete(comment_id)
    return redirect('/tweet/index?user_id={}'.format(uid))


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
    # '/tweet/index': index,
    '/new': login_required(new),
    '/add': login_required(add),
    '/delete': login_required(delete),
    '/edit': login_required(edit),
    '/update': login_required(update),
}
