import json

import requests

from kit.dingding import corp_id, corp_secret, agent_id, app_secret, app_key


def get_access_token():
    # url = 'https://oapi.dingtalk.com/gettoken?appkey=%s&appsecret=%s' % (app_key, app_secret)
    url = 'https://oapi.dingtalk.com/gettoken?corpid=%s&corpsecret=%s' % (corp_id, corp_secret)

    response = requests.get(url)
    response_dict = json.loads(response.text)
    error_code_key = "errcode"
    access_token_key = "access_token"
    if error_code_key in response_dict and response_dict[error_code_key] == 0 and access_token_key in response_dict:
        return response_dict[access_token_key]
    else:
        return ''


def get_userid_by_unionid(access_token, unionId):
    url = 'https://oapi.dingtalk.com/user/getUseridByUnionid?access_token=%s&unionid=%s' % (access_token, unionId)
    response = requests.get(url)
    return response.text


def get_user(access_token, user_id):
    url = 'https://oapi.dingtalk.com/user/get?access_token=%s&userid=%s' % (access_token, user_id)
    response = requests.get(url)
    response_dict = json.loads(response.text)
    return response_dict


def get_dept_member(access_token):
    print("get_dept")
    if access_token == '':
        print('invalid access token: ' + access_token)
        return ''
    url = 'https://oapi.dingtalk.com/user/getDeptMember?access_token=%s&deptId=%d' % (access_token, 1)
    response = requests.get(url)
    response_dict = json.loads(response.text)
    error_code_key = "errcode"
    error_msg = 'errmsg'
    user_ids = 'userIds'
    if error_code_key in response_dict and response_dict[error_code_key] == 0 and user_ids in response_dict:
        return response_dict[user_ids]
    if error_code_key in response_dict and response_dict[error_code_key] != 0:
        print('错误: %s' % response_dict[error_msg])
    return ''


def get_persistent_code(access_token):
    url = 'https://oapi.dingtalk.com/sns/get_persistent_code?access_token=%s' % access_token
    response = requests.post(url)
    return response.text


def send_text_to_users(access_token, user, text):
    msg_type, msg = _gen_text_msg(text)
    return _send_msg_to_users(access_token, [user], msg_type, msg)


def _gen_text_msg(text):
    msg_type = 'text'
    msg = {"content": text}
    return msg_type, msg


def _send_msg_to_users(access_token, users, msg_type, msg):
    to_users = '|'.join(users)
    body_dict = {"touser": to_users, "agentid": agent_id, "msgtype": msg_type, msg_type: msg}
    body = json.dumps(body_dict)
    return _send_msg("https://oapi.dingtalk.com/message/send?access_token=", access_token, body)


def _send_msg(url, token, body):
    return requests.post(url + token, body)



