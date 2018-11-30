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
def wx_web(request):
    return render(request, 'wx_app/wx_main.html')

TOKEN = 'wuchen_TOKEN'
APPID = 'wx1c53a7cf55314e85'
ENCODING_AES_KEY = 'Hv85gW0hkQVwzNvn7pih0eo0Bv9UPXxyTRgSXuAiVPN'
APPSCRET = 'd28ecedbf5ff74fe268595ea035a6b6f'

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
        print(msg)

        if msg.type == 'text':
            #获取文本内容
            content = msg.content
            try:
                reply = TextReply(content=content, message=msg)
                #render()返回XML格式消息
                r_xml = reply.render()
                encryptmsg=wxencrypt(r_xml,request,APPID,ENCODING_AES_KEY,TOKEN)
                return HttpResponse(encryptmsg)
            except Exception as e:
                #自行处理
                return HttpResponse('回复文本信息给你的时候出错啦')
        elif msg.type == 'image':
            return HttpResponse('还未处理')
        elif msg.type == 'location':
            reply = TextReply(
            content="我发现你了，你在" + msg.label, message=msg)
            r_xml = reply.render()
            encryptmsg = wxencrypt(
                    r_xml, request, APPID, ENCODING_AES_KEY, TOKEN)
            return HttpResponse(encryptmsg)

        elif msg.type == 'voice':
            return HttpResponse('还未处理')
        elif msg.type == 'link':
            return HttpResponse('还未处理')
        elif msg.type == 'video':
            return HttpResponse('还未处理')
        elif msg.type == 'shortvideo':
            return HttpResponse('还未处理')
        elif msg.type == 'event':
            try:
                if msg.event == 'subscribe':
                    reply = TextReply(content="欢迎关注我，你真帅！", message=msg)
                    r_xml = reply.render()
                    encryptmsg = wxencrypt(
                        r_xml, request, APPID, ENCODING_AES_KEY, TOKEN)
                    return HttpResponse(encryptmsg)
                elif msg.event == 'unsubscribe':
                    return HttpResponse('还未处理')
                elif msg.event == 'subscribe_scan':
                    return HttpResponse('还未处理')
                elif msg.event == 'scan':
                    return HttpResponse('还未处理')
                elif msg.event == 'location':
                    reply = TextReply(
                        content="我发现你了，你在" + msg.lable, message=msg)
                    r_xml = reply.render()
                    encryptmsg = wxencrypt(
                        r_xml, request, APPID, ENCODING_AES_KEY, TOKEN)
                    return HttpResponse(encryptmsg)
                elif msg.event == 'click':
                    reply = TextReply(
                        content="我知道你刚才click了某个菜单", message=msg)
                    r_xml = reply.render()
                    encryptmsg = wxencrypt(
                        r_xml, request, APPID, ENCODING_AES_KEY, TOKEN)
                    return HttpResponse(encryptmsg)

                elif msg.event == 'view':
                    print('hhhh哈哈哈哈哈啊哈')
                    reply = TextReply(
                        content="我知道你刚才点了哪个菜单", message=msg)
                    r_xml = reply.render()
                    encryptmsg = wxencrypt(
                        r_xml, request, APPID, ENCODING_AES_KEY, TOKEN)
                    #对于跳转页面，也许是Django会转到后面的执行函数再返回页面，此处无法提前回复消息到客户端。
                    return HttpResponse(encryptmsg)
                #群发任务状态
                elif msg.event == 'masssendjobfinish':
                    return HttpResponse('还未处理')
                #模板消息任务完成事件
                elif msg.event == 'templatesendjobfinish':
                    return HttpResponse('还未处理')
                #扫码推事件
                elif msg.event == 'scancode_push':
                    return HttpResponse('还未处理')
                #扫码推事件且弹出“消息接收中”提示框的事件
                elif msg.event == 'scancode_waitmsg':
                    return HttpResponse('还未处理')
                #弹出系统拍照发图的事件
                elif msg.event == 'pic_sysphoto':
                    return HttpResponse('还未处理')
                #弹出拍照或者相册发图的事件
                elif msg.event == 'pic_photo_or_album':
                    return HttpResponse('还未处理')
                #弹出微信相册发图器的事件
                elif msg.event == 'pic_weixin':
                    return HttpResponse('还未处理')
                #弹出地理位置选择器的事件
                elif msg.event == 'location_select':
                    return HttpResponse('还未处理')
                
                #微信认证事件推送
                #资质认证成功事件
                elif msg.event == 'qualification_verify_success':
                    return HttpResponse('还未处理')
                #资质认证失败事件
                elif msg.event == 'qualification_verify_fail':
                    return HttpResponse('还未处理')
                #名称认证成功事件
                elif msg.event == 'naming_verify_success':
                    return HttpResponse('还未处理')
                #名称认证失败事件
                elif msg.event == 'naming_verify_fail':
                    return HttpResponse('还未处理')
                #年审通知事件
                elif msg.event == 'annual_renew':
                    return HttpResponse('还未处理')
                #认证过期失效通知
                elif msg.event == 'verify_expired':
                    return HttpResponse('还未处理')
                
                #微信扫一扫事件
                #打开商品主页事件
                elif msg.event == 'user_scan_product':
                    return HttpResponse('还未处理')
                #进入公众号事件
                elif msg.event == 'user_scan_product_enter_session':
                    return HttpResponse('还未处理')
                #地理位置信息异步推送事件
                elif msg.event == 'user_scan_product_async':
                    return HttpResponse('还未处理')
                #商品审核结果事件
                elif msg.event == 'user_scan_product_verify_action':
                    return HttpResponse('还未处理')
                #用户在商品主页中关注公众号事件
                elif msg.event == 'subscribe_scan_product':
                    return HttpResponse('还未处理')
                #用户授权发票事件 （会包含一个订单号，不成功就失败）
                elif msg.event == 'user_authorize_invoice':
                    return HttpResponse('还未处理')
                #发票状态更新事件
                elif msg.event == 'update_invoice_status':
                    return HttpResponse('还未处理')
                #用户提交发票抬头事件
                elif msg.event == 'submit_invoice_title':
                    return HttpResponse('还未处理')
                else:
                    
                    reply = TextReply(content="干嘛呢！"+msg.event, message=msg)
                    r_xml = reply.render()
                    encryptmsg = wxencrypt(
                        r_xml, request, APPID, ENCODING_AES_KEY, TOKEN)
                    return HttpResponse(encryptmsg)


                # push = ScanCodeWaitMsgEvent(msg)
                # #获取二维码信息，字符串
                # content = msg.scan_result
                # print(content)
                # # 如何处理，自行处理，回复一段文本或者图文
                # reply = TextReply(content="something", message=msg)
                # r_xml = reply.render()
                # encryptmsg = wxencrypt(
                #     r_xml, request, APPID, ENCODING_AES_KEY, TOKEN)
                # return HttpResponse(encryptmsg)
            except Exception as e:
                #暂时不处理
                return HttpResponse('出错啦')
        else:
            return HttpResponse('不明消息')

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
                        "name": "访客预约",
                        "url": "http://3fcba1c69bb95399.natapp.cc/wx",
                        "sub_button": []
                    }
                ]
            },
            {
                "name": "产品演示",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "资产管理",
                        "url": "http://127.0.0.1",
                        "sub_button": []
                    }
                ]
            },
            {
                "type": "click",
                "name": "关于戊辰",
                "key": "V1001_GOOD"
            }
        ]
    })
    return HttpResponse('ok')
