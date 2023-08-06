import json

import requests

__all__ = ['TEST_SEYFERT_URL', 'SEYFERT_URL', 'SeyfertAPI']

TEST_SEYFERT_URL = 'https://stg5.paygate.net/'
SEYFERT_URL = 'https://v5.paygate.net/'


class SeyfertAPI(object):
    """
    Usage
    """
    def __init__(self, member_guid, seyfert_url=SEYFERT_URL):
        self.reqMemGuid = member_guid
        self.seyfert_url = seyfert_url
        requests_session = requests.Session()
        # deploy시에 살려두기
        requests_adapters = requests.adapters.HTTPAdapter(max_retries=3)
        requests_session.mount('https://', requests_adapters)
        self.requests_session = requests_session

    class ResponseError(Exception):
        def __init__(self, code=None, message=None, desc=None):
            self.code = code
            self.message = message
            self.desc = desc

    class HttpError(Exception):
        def __init__(self, code=None, reason=None):
            self.code = code
            self.reason = reason

    @staticmethod
    def print_response(response):
        try:
            result = response.json()
        except json.JSONDecodeError:
            return response
        # return response
        try:
            if result['status'] != 'SUCCESS':
                result = result.get('data')
                raise SeyfertAPI.ResponseError(result.get('cdKey'), result.get('cdNm'), result.get('cdDesc'))
        except KeyError:
            raise SeyfertAPI.HttpError(response.status_code, response.reason)
        return result

    def _set_required_params(self, params, method):
        if not params:
            params = {}
        params['reqMemGuid'] = self.reqMemGuid
        params['_method'] = method
        return params

    def _get(self, url, payload=None, params=None):
        params = self._set_required_params(params, 'GET')
        response = self.requests_session.get(url, data=payload, params=params)
        return self.print_response(response)

    def _post(self, url, payload=None, params=None):
        params = self._set_required_params(params, 'POST')
        response = self.requests_session.post(url, data=payload, params=params)
        return self.print_response(response)

    def _put(self, url, payload=None, params=None):
        params = self._set_required_params(params, 'PUT')
        response = self.requests_session.put(url, data=payload, params=params)
        return self.print_response(response)

    # MEMBER
    def member_create(self, payload):
        """
        valid_payload = {
            'emailTp': 'PERSONAL',
            'nmLangCd': 'ko',
            'phoneCntryCd': 'KOR',
            'phoneTp': 'MOBILE',
            'emailAddrss': 'test@test.com',
            'fullname': 'seulchankim',
            'phoneNo': '01011111111',
        }
        이 경우에 emailAddrss, phoneNo unique해야함
        """
        url = '{}v5a/member/createMember'.format(self.seyfert_url)
        return self._post(url, payload=payload)

    def member_create_with_email(self, payload):
        """
        valid_payload = {
            'emailAddrss': 'test@test.com',
            'emailTp': 'PERSONAL',
            'nmLangCd': 'ko',
            'keyTp': 'EMAIL'
        }
        member_create와 동일한 payload 사용 위해서 아래 항목 추가
        """
        try:
            del payload['phoneCntryCd']
            del payload['phoneTp']
            del payload['phoneNo']
            del payload['fullname']
        except KeyError:
            pass
        payload['keyTp'] = 'EMAIL'
        url = '{}v5a/member/createMember'.format(self.seyfert_url)
        print(payload)
        return self._post(url, payload=payload)

    # def member_create_with_phone
    # def member_create_with_name
    # def member_create_with_unique_key

    # MEMBER
    def member_profile_with_guid(self, guid):
        """
        user profile 조회
        - response (http://km.paygate.net/pages/viewpage.action?pageId=10912197)
        {
            "data":{
                "result":{
                    ...
                    "emailList": [],
                    "phoneList": [],
                    "namesList": [],
                    "namesList": [],
                    "bnkAccnt": [],
                }
            }
        }
        """
        url = '{}v5a/member/privateInfo'.format(self.seyfert_url)
        params = {
            'dstMemGuid': guid,
        }
        return self._get(url, params=params)

    def member_update(self, guid, params):
        """
        멤버 정보 수정
        - 한번에 다, 혹은 일부만 수정 가능
        - phone, address, name,  email, ssn, corpRegNo, memberType
        - 주로 phone, name만 수정할듯
        """
        url = '{}v5a/member/allInfo'.format(self.seyfert_url)
        params['dstMemGuid'] = guid
        params['nmLangCd'] = 'ko'
        # params = {
        #     'dstMemGuid': guid,
        # }
        return self._put(url, params=params)

    def member_update_fullname(self, guid, name):
        """
        멤버 정보중 fullname만 수정
        - response 예시
        {
            "data": {
                "result": {
                    "name": {
                        "status": "STORED"
                    },
                },
                "e2e": false
            },
            "_debug": null,
            "status": "SUCCESS"
        }
        """
        url = '{}v5a/member/allInfo'.format(self.seyfert_url)
        params = {
            'fullname': name,
            'dstMemGuid': guid,
            'nmLangCd': 'ko',
        }
        return self._put(url, params=params)

    def member_update_phone(self, guid, phone):
        """
        멤버 정보중 phone만 수정
        - response 예시
        {
            "data": {
                "result": {
                    "phone": {
                        "status": "STORED"
                    },
                },
                "e2e": false
            },
            "_debug": null,
            "status": "SUCCESS"
        }
        """
        url = '{}v5a/member/allInfo'.format(self.seyfert_url)
        params = {
            'dstMemGuid': guid,
            'phoneNo': phone,
            'phoneCntryCd': 'KOR',
        }
        return self._put(url, params=params)

    # ACCOUNT
    def banks_list(self):
        """
        은행 name / code list 반환
        """
        url = '{}v5/code/listOf/banks'.format(self.seyfert_url)
        return self._get(url)

    def register_account(self, guid, account_number, bank_code, cntryCd='KOR'):
        """
        계좌 등록
        """
        url = '{}v5a/member/bnk'.format(self.seyfert_url)
        payload = {
            'dstMemGuid': guid,
            'bnkCd': bank_code,
            'accntNo': account_number,
            'cntryCd': cntryCd,
        }
        return self._post(url, payload=payload)

    def check_account_exists(self, guid):
        """
        guid(멤버)의 계좌가 존재하는지 확인
        """
        url = '{}v5/transaction/seyfert/checkbankexistence'.format(self.seyfert_url)
        payload = {
            'dstMemGuid': guid,
        }
        return self._post(url, payload=payload)

    def verify_account_name(self, guid):
        """
        멤버의 실 계좌 예금주 검증 (http://km.paygate.net/pages/viewpage.action?pageId=10912214)
        필수적으로 해주어야하는지?
        example_response = {
            "data":{
                "bnkCd":"KIUP_003",
                "accntNo":"010*****586",
                "tid":"TADRBK",
                "status":"CHECK_BNK_NM_FINISHED",
                # "status":"CHECK_BNK_NM_DENIED",
                "e2e":false
            },
            "_debug":null,
            "status":"SUCCESS"
        }
        """
        url = '{}v5/transaction/seyfert/checkbankname'.format(self.seyfert_url)
        payload = {
            'dstMemGuid': guid,
        }
        return self._post(url, payload=payload)

    def verify_account_ownership(self, guid):
        """
        해당 번호로 1원 전송
        이후 인증코드 발신시
        "status": "VRFY_BNK_CD_SENDING_1WON" => "status": "CHECK_BNK_CD_FINISHED"
        (http://km.paygate.net/pages/viewpage.action?pageId=10912216)
        """
        url = '{}v5/transaction/seyfert/checkbankcode'.format(self.seyfert_url)
        payload = {
            'dstMemGuid': guid,
        }
        return self._post(url, payload=payload)

    # 내부함수
    def is_account_exist_and_verified_name(self, guid):
        try:
            exist_result = self.check_account_exists(guid).get('data').get('status')
            name_result = self.verify_account_name(guid).get('data').get('status')
        except (SeyfertAPI.ResponseError) as e:
            print(e)
            return False, e.message
        message = ''
        if not exist_result == 'CHECK_BNK_EXISTANCE_CHECKED':
            message += exist_result
        if not name_result == 'CHECK_BNK_NM_FINISHED':
            message += name_result
        return exist_result == 'CHECK_BNK_EXISTANCE_CHECKED' and name_result == 'CHECK_BNK_NM_FINISHED', message

    def is_account_ownership_verified(self, guid):
        banks = self.get_members_accounts(guid)
        priority_bank = [x for x in banks if x['priority'] == 1]
        try:
            return priority_bank[0].get('verify').get('verifySt') == 'VERIFIED'
        except KeyError:
            return False
        return False

    def get_members_accounts(self, guid):
        """
        Return lists of banks
        """
        result = self.member_profile_with_guid(guid)
        banks = result.get('data').get('result').get('bnkAccnt')
        return banks
