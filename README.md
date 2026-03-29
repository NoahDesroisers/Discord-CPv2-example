# Discord-CPv2-example

Discord Components V2 (https://docs.discord.com/developers/components/reference)의
봇 메시지용 **모든 컴포넌트 타입**을 사용한 한국어 예제입니다.
문서를 보기 싫거나 이미 만들어진, 실제 사용 가능한 모델 예제가 필요하신 분들을 위해 제작되었습니다.

## 사용된 컴포넌트

| 타입 | 이름 |
|------|------|
| type 1 | Action Row |
| type 2 | Button (style 1~5 + disabled) |
| type 3 | String Select |
| type 5 | User Select |
| type 6 | Role Select |
| type 7 | Mentionable Select |
| type 8 | Channel Select |
| type 9 | Section (Thumbnail / Button accessory) |
| type 10 | Text Display |
| type 11 | Thumbnail |
| type 12 | Media Gallery |
| type 13 | File |
| type 14 | Separator |
| type 17 | Container |

## 실행 방법
```bash
pip install discord.py aiohttp
```

`cpv2.py`의 `TOKEN`을 본인 봇 토큰으로 교체 후 실행:
```bash
python main.py
```

슬래시 커맨드 `/showcase` 로 실행합니다.

## 기타

- discord.py 2.x 이상 필요
- 수정시 Components V2는 `flags = 1 << 15` 필수
- 기존에 사용하던 `content=`, `embed=` 사용 불가 → Text Display (type 10) 로 대체
