'''Utils.'''

__author__ = 'healplease'

import os
import json
import time

import requests

FT_APP_ICON = 0
FT_APP_VIDEO_AND_POSTER = 1
FT_APP_SCREENSHOT = 2
FT_RECOMMENDATION_VIDEO = 3
FT_RECOMMENDATION_IMAGE = 4
FT_APK_OR_RPK = 5
FT_PROXY_CERTIFICATE_OR_COPYRIGHT_IMAGE = 6
FT_CERTIFICATE_PDF = 7
FT_CULTURE_OPERATION_SCREENSHOT = 8
FT_CULTURE_OPERATION_IMAGE_OR_PDF = 9
FT_VR_COVER_IMAGE = 10
FT_VR_APP_SCREENSHOT = 11
FT_VR_APP_RECOMMENDATION_IMAGE = 12
FT_VR_COVER_LAYERING_IMAGE = 13
FT_VR_IMAGE_4_TO_3_RATIO = 14
FT_VR_IMAGE_1_TO_1_RATIO = 15
FT_VR_IMAGE_PANORAMA = 16

class Credentials():
    '''Initialize the Credentials object.
    
    Keyword parameters have higher priority then environ JSON file.'''
    def __init__(self, client_id: str=None, client_secret: str=None, grant_type: str=None):
        if os.environ.get('HUAWEI_CREDENTIALS_PATH'):
            with open(os.environ['HUAWEI_CREDENTIALS_PATH'], 'r', encoding='utf-8') as credentials_json:
                credentials_parsed = json.load(credentials_json)
            self.client_id = credentials_parsed.get('client_id') 
            self.client_secret = credentials_parsed.get('client_secret')
            self.grant_type = credentials_parsed.get('grant_type')

        self.client_id = client_id if client_id else self.client_id
        self.client_secret = client_secret if client_secret else self.client_secret
        self.grant_type = grant_type if grant_type else self.grant_type


class AccessToken():
    def __init__(self, parsed: dict):
        self.token = parsed.get('access_token')
        self.expires_in = int(parsed.get('expires_in'))

    def __repr__(self):
        return self.token

    def auth(self):
        return 'Bearer {}'.format(self.token)

    def is_expired(self):
        return time.time() > self.expires_in

class Upload():
    def __init__(self, parsed: dict):
        self.URL = parsed.get('uploadUrl')
        self.chunk_URL = parsed.get('chunkUploadUrl')
        self.verification_code = parsed.get('authCode')

    def upload_file(self, filepath: str, count: int=1, parse_type: int=0, name: str=None):
        data = {
            'authCode': self.verification_code,
            'fileCount': count
        }
        if name:
            data.update({ 'name': name })
        if parse_type:
            data.update({ 'parseType': parse_type })

        files = {
            'file': open(filepath, 'rb')
        }

        self.last_response = requests.post(self.URL, data, files=files)
        response = json.loads(self.last_response.text, encoding='utf-8')
        if self.last_response.status_code == 200:
            info = response.get('result').get('UploadFileRsp').get('fileInfoList')
            return FileInfo(info[0])
        else:
            raise requests.RequestException(f'Unsuccessful request. Error code: {self.last_response.status_code}')



class Message():
    def __init__(self, parsed: dict):
        self.code = parsed.get('code', 0)
        self.description = parsed.get('msg', '')

class HuaweiException(BaseException):
    def __init__(self, *args, **kwargs):
        ret = kwargs.get('response', None)
        if ret:
            self.code = ret['code']
            self.msg = ret['msg']
        super(HuaweiException, self).__init__(f'\nError {self.code}: {self.msg}')

class AppInfo():
    def __init__(self, parsed: dict):
        self.releaseState = parsed.get('releaseState')
        self.defaultLang = parsed.get('defaultLang')
        self.parentType = parsed.get('parentType')
        self.childType = parsed.get('childType')
        self.grandChildType = parsed.get('grandChildType')
        self.privacyPolicy = parsed.get('privacyPolicy')
        self.appNetType = parsed.get('appNetType')
        self.isFree = parsed.get('isFree')
        self.price = parsed.get('price')
        self.publishCountry = parsed.get('publishCountry')
        self.contentRate = parsed.get('contentRate')
        self.isAppForcedUpdate = parsed.get('isAppForcedUpdate')
        self.sensitivePermissionDesc = parsed.get('sensitivePermissionDesc')
        self.hispaceAutoDown = parsed.get('hispaceAutoDown')
        self.appTariffType = parsed.get('appTariffType')
        self.publicationNumber = parsed.get('publicationNumber')
        self.cultureRecordNumber = parsed.get('cultureRecordNumber')
        self.developerAddr = parsed.get('developerAddr')
        self.developerEmail = parsed.get('developerEmail')
        self.developerPhone = parsed.get('developerPhone')
        self.developerWebsite = parsed.get('developerWebsite')
        self.developerNameCn = parsed.get('developerNameCn')
        self.developerNameEn = parsed.get('developerNameEn')
        self.elecCertificateUrl = parsed.get('elecCertificateUrl')
        self.certificateURLs = parsed.get('certificateURLs')
        self.publicationURLs = parsed.get('publicationURLs')
        self.cultureRecordURLs = parsed.get('cultureRecordURLs')
        self.updateTime = parsed.get('updateTime')
        self.versionNumber = parsed.get('versionNumber')
        self.familyShareTag = parsed.get('familyShareTag')

    def JSON(self):
        return json.dumps(self, default=lambda x: x.__dict__)

class LangInfo():
    def __init__(self, parsed: dict):
        self.lang = parsed.get('lang')
        self.appName = parsed.get('appName')
        self.appDesc = parsed.get('appDesc')
        self.briefInfo = parsed.get('briefInfo')
        self.newFeatures = parsed.get('newFeatures')
        self.icon = parsed.get('icon')
        self.showType = parsed.get('showType')
        self.videoShowType = parsed.get('videoShowType')
        self.introPic = parsed.get('introPic')
        self.introVideo = parsed.get('introVideo')
        self.rcmdPic = parsed.get('rcmdPic')
        self.rcmdVideo = parsed.get('rcmdVideo')

    def JSON(self):
        return json.dumps(self, default=lambda x: x.__dict__)

class AuditInfo():
    def __init__(self, parsed: dict):
        self.auditOpinion = parsed.get('auditOpinion')
        self.copyRightAuditResult = parsed.get('copyRightAuditResult')
        self.copyRightAuditOpinion = parsed.get('copyRightAuditOpinion')
        self.copyRightCodeAuditResult = parsed.get('copyRightCodeAuditResult')
        self.copyRightCodeAuditOpinion = parsed.get('copyRightCodeAuditOpinion')
        self.recordAuditResult = parsed.get('recordAuditResult')
        self.recordAuditOpinion = parsed.get('recordAuditOpinion')

    def JSON(self):
        return json.dumps(self, default=lambda x: x.__dict__)

class FileInfo():
    def __init__(self, parsed: dict):
        self.destination_URL = parsed.get('fileDestUlr')
        self.name = self.destination_URL.split('/')[-1]
        self.size = parsed.get('size')
        self.image_resolution = parsed.get('imageResolution')
        self.image_resolution_signature = parsed.get('imageResolutionSingature')

    def JSON(self):
        return json.dumps({
            'fileDestUlr': self.destination_URL,
            'name': self.name,
            'size': self.size,
            'imageResolution': self.image_resolution,
            'imageResolutionSingature': self.image_resolution_signature
        })