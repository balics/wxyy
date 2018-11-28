from django.shortcuts import render
from wechatpy.utils import check_signature
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from wechatpy import WeChatClient, parse_message
from wechatpy.replies import TextReply
from wechatpy.events import ScanCodeWaitMsgEvent
from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException
from wx_app.wxcrypt import wxdecrypt, wxencrypt


# Create your views here.

TOKEN = 'wuchen_TOKEN'
APPID = 'wx1c53a7cf55314e85'
ENCODING_AES_KEY = 'Hv85gW0hkQVwzNvn7pih0eo0Bv9UPXxyTRgSXuAiVPN'

@csrf_exempt
def wx_main(request):
    if request.method == 'GET':
        signature = request.GET.get("signature", None)
        timestamp = request.GET.get("timestamp", None)
        nonce = request.GET.get("nonce", None)
        echostr = request.GET.get("echostr", None)
        try:
            check_signature(TOKEN, signature, timestamp, nonce)
            return HttpResponse(echostr)
        except InvalidSignatureException:
            return HttpResponse('微信接口Token验证失败！')
    else:
        msg = parse_message(wxdecrypt(request, APPID, ENCODING_AES_KEY, TOKEN))
        
        # xml = request.body
        # #根据加密方式决定是否解密
        # encrypt_type = request.GET.get('encrypt_type', None)
        # if encrypt_type == 'aes':
        #     msgsignature = request.GET.get("msg_signature", None)
        #     timestamp = request.GET.get("timestamp", None)
        #     nonce = request.GET.get("nonce", None)
        #     crypto = WeChatCrypto(TOKEN, ENCODING_AES_KEY, APPID)
        #     try:
        #         decrypted_xml = crypto.decrypt_message(
        #             xml,
        #             msgsignature,
        #             timestamp,
        #             nonce
        #         )
        #     except (InvalidAppIdException, InvalidSignatureException):
        #         # 处理异常或忽略
        #         return HttpResponse('解密信息出错！')
        #     msg = parse_message(decrypted_xml)
        # else:
        #     msg = parse_message(xml)

        if msg.type == 'text':
            #获取文本内容
            content = msg.content
            try:
                reply = TextReply(content=content, message=msg)
                #render()返回XML格式消息
                r_xml = reply.render()


                #根据加密与否对回复的消息进行加密或不加密

                # crypto = WeChatCrypto(TOKEN, ENCODING_AES_KEY, APPID)
                # encryptmsg = crypto.encrypt_message(r_xml, nonce, timestamp)
                # 获取唯一标记用户的openid，下文介绍获取用户信息会用到
                openid = msg.source
                encryptmsg=wxencrypt(r_xml,request,APPID,ENCODING_AES_KEY,TOKEN)
                return HttpResponse(encryptmsg)
            except Exception as e:
                #自行处理
                pass
        elif msg.type == 'event':
            try:
                push = ScanCodeWaitMsgEvent(msg)
                #获取二维码信息，字符串
                content = msg.scan_result
                print(content)
                # 如何处理，自行处理，回复一段文本或者图文
                reply = TextReply(content="something", message=msg)
                r_xml = reply.render()
                encryptmsg = wxencrypt(
                    r_xml, request, APPID, ENCODING_AES_KEY, TOKEN)
                return HttpResponse(encryptmsg)
            except Exception as e:
                #暂时不处理
                pass
        elif msg.type == 'subscribe':
            create_menu(request)
        elif msg.type == 'unsubscribe':
            create_menu(request)
        else: pass


def create_menu(request):
	# 第一个参数是公众号里面的appID，第二个参数是appsecret
    client = WeChatClient("wx1c53a7cf55314e85",
                          "d28ecedbf5ff74fe268595ea035a6b6f")
    client.menu.create({
        "button": [
            {
                "name": "智能访客",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "微信预约",
                        "url": "http://3fcba1c69bb95399.natapp.cc/wx"
                    }
                ]
            },
            {
                "name": "案例展示",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "资产管理",
                        "url": "http://sw.dahongye.cn"
                    }
                ]
            },
            {
                "name": "关于戊辰",
                "sub_button": [
                    {
                        "type": "click",
                        "name": "联系我们",
                        "url": "V1001_GOOD"
                    },
                    {
                        "type": "click",
                        "name": "戊辰历程",
                        "url": "W1000"
                    }
                ]
            }
        ],
        "matchrule": {
            "group_id": "2",
            "sex": "1",
            "country": "中国",
            "province": "广东",
            "city": "广州",
            "client_platform_type": "2"
        }
    })
    return HttpResponse('ok')
