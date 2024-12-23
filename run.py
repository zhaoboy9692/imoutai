
key = 'qbhajinldepmucsonaaaccgypwuvcjaa'
iv = '2018534749963515'
def aes_encode(data):
    while len(data) % 16 != 0:  # 补足字符串长度为16的倍数
        data += (16 - len(data) % 16) * chr(16 - len(data) % 16)
    data = str.encode(data)
    aes = AES.new(key.encode('utf8'), AES.MODE_CBC, iv.encode('utf8'))  # 初始化加密器
    return base64.b64encode(aes.encrypt(data)).decode()


def aes_decode(data):
    aes = AES.new(key.encode('utf8'), AES.MODE_CBC, iv.encode('utf8'))  # 初始化加密器
    decrypted_text = aes.decrypt(data).decode()
    decrypted_text = decrypted_text[:-ord(decrypted_text[-1])]  # 去除多余补位
    return decrypted_text
def mt_add(itemId, shopId, sessionId, userId, token, Device_ID):
    MT_K = f'{int(time.time() * 1000)}'
    Version = '1.2.15'
    headers = {'User-Agent': 'iOS;16.0;Apple;iPhone 14',
               'MT-Token': token,
               'MT-Network-Type': 'WIFI', 'MT-User-Tag': '0',
               'MT-R': mt_r, 'MT-Lat': '', 'MT-K': MT_K,
               'MT-Lng': '', 'MT-Info': '028e7f96f6369cafe1d105579c5b9377', 'MT-APP-Version': Version,
               'MT-Request-ID': f'{int(time.time() * 1000)}18342', 'Accept-Language': 'zh-Hans-CN;q=1',
               'MT-Device-ID': Device_ID, 'MT-V': get_mtv(Device_ID, MT_K, Version),
               'MT-Bundle-ID': 'com.moutai.mall'}
    d = {"itemInfoList": [{"count": 1, "itemId": str(itemId)}], "sessionId": sessionId, "userId": str(userId),
         "shopId": str(shopId)}
    r = aes_encode(
        json.dumps(d).replace(' ', ''))
    d['actParam'] = r
    json_data = d
    response = requests.post('https://app.moutai519.com.cn/xhr/front/mall/reservation/add', headers=headers,
                             json=json_data)
    code = response.json().get('code', 0)
    if code == 2000:
        return response.json().get('data', {}).get('successDesc', "未知")
    return '申购失败:' + response.json().get('message', "未知原因")
