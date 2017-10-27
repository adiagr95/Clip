import random
import string
import uuid
from datetime import datetime
from operator import itemgetter as i

from hashids import Hashids
from util.constants import core_const
from datetime import timedelta
from itertools import tee
from calendar import monthrange
from conf import DEBUG

hashids = Hashids(alphabet='0123456789ADUXYM', min_length=5)


def get_secret():
    return str(uuid.uuid1())


def get_random_otp():
    if DEBUG:
        return "1234"
    else:
        return "".join([random.choice('0123456789') for _ in range(4)])


def get_random_number(factor=1):
    return round(random.random()*factor, 2)


def from_seconds(seconds):
    seconds = int(float(seconds))
    return datetime.fromtimestamp(seconds)


def to_seconds(dt):
    return int(float(dt.strftime("%s")))


def delta_time(tm, ch_dict):
    if tm is None:
        tm = datetime.now()
    return tm + timedelta(**ch_dict)


def get_current_time():
    timestamp = datetime.now()
    return timestamp


def start_of_day(dt=None):
    if dt is None:
        dt = datetime.now()
    return from_seconds(to_seconds(dt)).replace(hour=0, minute=0, second=0, microsecond=0)


def end_of_day(dt=None):
    if dt is None:
        dt = datetime.now()
    return from_seconds(to_seconds(dt)).replace(hour=23, minute=59, second=59, microsecond=999)


def start_of_week(dt=None):
    if dt is None:
        dt = datetime.now()
    return start_of_day(from_seconds(to_seconds(dt))) - timedelta(days=dt.weekday())


def end_of_week(dt=None):
    if dt is None:
        dt = datetime.now()
    return end_of_day(delta_time(start_of_week(dt), {'days': 6}))


def start_of_fortnight(dt=None):
    if dt is None:
        dt = datetime.now()
    if dt.day > 15:
        return delta_time(start_of_month(), {'days': 15})
    else:
        return start_of_month()


def end_of_fortnight(dt=None):
    if dt is None:
        dt = datetime.now()
    if dt.day > 15:
        return end_of_month()
    else:
        return end_of_day(delta_time(delta_time(start_of_month(), {'days': 15}), {'seconds': -1}))


def start_of_month(dt=None):
    if dt is None:
        dt = datetime.now()
    return start_of_day(from_seconds(to_seconds(dt)).replace(day=1))


def end_of_month(dt=None):
    if dt is None:
        dt = datetime.now()
    return delta_time(start_of_month(delta_time(start_of_month(dt), {'days': 32})), {'seconds': -1})


def add_time(delta, tm=None):
    if not tm:
        tm = get_current_time()
    return tm + timedelta(seconds=delta)


def format_date(object):
    return object.strftime("%a, %d %b %Y")


def format_date_time(object):
    return object.strftime("%I:%M %p  %d %b %Y")


def format_time_to(object, format_str):
    return object.strftime(format_str)


def get_error(errors):
    error = ""
    for key, value in errors.iteritems():
        if key == 'non_field_errors':
            return value[0]
        return key + ": " + value[0]


def get_push_tokens(users, excludes=None):
    tokens = []
    if users and users is not None:
        eligible_users = []
        if excludes is not None:
            for a in users:
                flag = 0
                for b in excludes:
                    if a.id == b.id:
                        flag = 1
                if flag == 0:
                    eligible_users.append(a)
        for a in eligible_users:
            tokens += ([secret.push_key for secret in a.secrets.filter(expiry__gt=get_current_time())])
    return list(set(tokens))


def get_dict_array(post, name):
    dic = {}
    result = []
    for k in post.keys():
        if k.startswith(name):
            rest = k[len(name):]

            # split the string into different components
            parts = [p[:-1] for p in rest.split('[')][1:]
            id = int(parts[0])

            # add a new dictionary if it doesn't exist yet
            if id not in dic:
                dic[id] = {}

            # add the information to the dictionary
            dic[id][parts[1]] = post.get(k)
    for key, value in dic.iteritems():
        result.append(value)
    return result


def encode(value):
    return hashids.encode(value)


def get_separate_names(full_name):
    names = full_name.strip().split()
    if len(names) == 3:
        return names[0], names[2]
    if len(names) == 2:
        return names[0], names[1]
    if len(names) == 1:
        return names[0], ""
    else:
        return "", ""


def get_next_user_id(user_model):
    count = 0
    try:
        count = user_model.objects.order_by("-id")[0].id
    except Exception:
        pass
    return "U"+str(count+1).zfill(5)


def get_next_contact_id(contact_model):
    count = 0
    try:
        count = contact_model.objects.order_by("-id")[0].id
    except Exception:
        pass
    return "C"+str(count+1).zfill(5)


def get_next_order_id(order_model):
    count = 0
    try:
        count = order_model.objects.order_by("-id")[0].id
    except Exception:
        pass
    return str(count+1).zfill(5)


def get_next_business_id(business_model):
    count = 0
    try:
        count = business_model.objects.order_by("-id")[0].id
    except Exception:
        pass
    return int2str(count+1)


def get_next_invoice_id(invoice_model, business):
    count = 0
    try:
        count = invoice_model.objects.filter(business=business).order_by("-id")[0].id
    except Exception:
        pass
    return str(count+1).zfill(3)


def get_next_id(model):
    count = 0
    try:
        count = model.objects.order_by("-id")[0].id
    except Exception:
        pass
    return hashids.encode(count + 1)


def get_consumption_cache_key(business_id, item_id=None, start_date=None, end_date=None, type=None, take_average=None):
    key = str(business_id)
    if item_id:
        key += str(item_id)
    if start_date:
        key += str(start_date)
    if end_date:
        key += str(end_date)
    if type:
        key += str(type)
    if take_average:
        key += str(take_average)
    return key


def int2str(i):
    chars = "".join(str(n) for n in range(10)) +"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    s = ""
    while i:
        s += chars[i % len(chars)]
        i //= len(chars)
    return s.zfill(3)


def multikeysort(items, columns):
    comparers = [
        ((i(col[1:].strip()), -1) if col.startswith('-') else (i(col.strip()), 1))
        for col in columns
    ]

    def comparer(left, right):
        comparer_iter = (
            cmp(fn(left), fn(right)) * mult
            for fn, mult in comparers
        )
        return next((result for result in comparer_iter if result), 0)

    return sorted(items, cmp=comparer)


def dict_intersection(obj1, obj2):
    obj = {}
    for k1, v1 in obj1.iteritems():
        if type(v1) == type(True):
            obj[k1] = False
    for k2, v2 in obj2.iteritems():
        if type(v2) == type(True):
            obj[k2] = False
    for k1, v1 in obj1.iteritems():
        for k2, v2 in obj2.iteritems():
            if k1 == k2:
                obj[k1] = v1 and v2
    return obj


def get_suggested_order_start_date():
    current_time = get_current_time()
    if 0 <= current_time.hour < core_const.SUGGESTED_ORDER_END_TIME:
        return start_of_day()
    else:
        return delta_time(start_of_day(), {'days': 1})


def get_date_array(start, end, sorting=1, type='days'):
    if type == 'months':
        days = 30
        factor = 'days'
    else:
        days = 1
        factor = type
    if end < start:
        temp = end
        end = start
        start = temp

    l = [start]
    while (end - start).days > 0:
        start = delta_time(start, {factor: days})
        l.append(start)
    if sorting == -1:
        l = sorted(l, reverse=True)
    return l


def capitalize(strin):
    return string.capwords(strin)


def array_diff(includes, excludes):
    return list(set(includes) - set(excludes))


# def pairwise(iterable):
    # "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    # a, b = tee(iterable)
    # next(b, None)
    # return izip(a, b)


def monthdelta(d1, d2):
    delta = 0
    while True:
        mdays = monthrange(d1.year, d1.month)[1]
        d1 += timedelta(days=mdays)
        if d1 <= d2:
            delta += 1
        else:
            break
    return delta
