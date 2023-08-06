# Seyfert

파이썬을 이용한 seyfert api 연동 모듈입니다.


## Install

```
pip install seyfert-api-python
```


# Usage

## 발급받은 guid로 seyfert 준비
```
from seyfert-api import SeyfertAPI
from seyfert-api.client import TEST_SEYFERT_URL

seyfert = SeyfertAPI('your-guid')
# 테스트 url을 사용할 경우에는 명시적으로 추가해준다.
# seyfert = SeyfertAPI('your-guid', seyfert_url=TEST_SEYFERT_URL)
```

## api list

```
# Members
seyfert.member_create(payload)
seyfert.member_create_with_email(payload)
seyfert.member_profile_with_guid(guid)
seyfert.member_update(guid, params)
seyfert.member_update_fullname(guid, name)
seyfert.member_update_phone(guid, phone)
seyfert.get_members_accounts(guid)

# Accounts
seyfert.banks_list()
seyfert.register_account(guid, accont_number, bank_code)
seyfert.check_account_exists(guid)
seyfert.verify_account_name(guid)
seyfert.verify_account_ownership(guid)
seyfert.is_account_exist_and_verify_name(guid)
seyfert.is_account_ownership_verified(guid)
```

## TODO
- transaction api 추가
- test 추가
- refactoring (member / account / transaction 분리)


---
# 상세 기능 설명

## Member 기능


### member 생성
```
# 멤버 만들기
# 필요한 정보 준비
valid_payload = {
    'emailTp': 'PERSONAL',
    'nmLangCd': 'ko',
    'phoneCntryCd': 'KOR',
    'phoneTp': 'MOBILE',
    'emailAddrss': 'test@test.com',
    'fullname': 'test name',
    'phoneNo': '01011111111',
}

# 일반 멤버 생성 (email, 번호가 달라야함. 하나라도 같을경우 기존멤버 반환)
response = seyfert.member_create(payload=valid_payload)

# email로 멤버 생성
response = seyfert.member_create_with_email(payload=valid_payload)
```

### member 조회

특정 member의 guid로 프로필 정보 조회 가능

```
# 모든 정보 조회
guid = 'test_guid'
response = seyfert.member_profile_with_guid(guid)

# 해당 멤버의 계좌정보 조회
resopnse = seyfert.get_members_accounts(guid)
```

### member 업데이트

특정 member의 guid로 프로필 정보 업데이트 가능

```
resopnse = seyfert
```
