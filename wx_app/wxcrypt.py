from wechatpy.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException


def wxencrypt(xml, request, appid, aescode, token):
    encrypt_type = request.GET.get('encrypt_type', None)
    if encrypt_type == 'aes':
        try:
            crypto = WeChatCrypto(token, aescode, appid)
            nonce = request.GET.get("nonce", None)
            timestamp = request.GET.get("timestamp", None)
            return crypto.encrypt_message(xml, nonce, timestamp)
        except Exception:
            error_msg='亲，加密我搞不定！'
            return error_msg
    else:
        return xml

def wxdecrypt(request, appid, aescode, token):
    encrypt_type = request.GET.get('encrypt_type', None)
    xml = request.body
    if encrypt_type == 'aes':
        try:
            crypto = WeChatCrypto(token, aescode, appid)
            nonce = request.GET.get("nonce", None)
            timestamp = request.GET.get("timestamp", None)
            msgsignature = request.GET.get("msg_signature", None)
            return crypto.decrypt_message(
                xml,
                msgsignature,
                timestamp,
                nonce
            )
        except (InvalidAppIdException, InvalidSignatureException):
            error_msg = '亲，消息太复杂，解密我搞不定！'
            return error_msg
    else:
        return xml
