"""
Discord Components V2 한국어 예제
made by Noah Des

참고로 컴포넌트는 한번에 40개가 최대임.

사용된 컴포넌트 (메시지에서 쓸 수 있는 모든 타입):
  type  1  Action Row
  type  2  Button         — style 1(Primary) 2(Secondary) 3(Success) 4(Danger) 5(Link)
  type  3  String Select
  type  5  User Select
  type  6  Role Select
  type  7  Mentionable Select
  type  8  Channel Select
  type  9  Section        — 텍스트 + Thumbnail accessory
  type  9  Section        — 텍스트 + Button accessory
  type 10  Text Display
  type 11  Thumbnail      (Section accessory)
  type 12  Media Gallery
  type 13  File           (attachment:// 참조)
  type 14  Separator      — divider=True/False, spacing=1/2
  type 17  Container      — accent_color, spoiler
"""

import discord
from discord.ext import commands

TOKEN = "토큰 넣는 자리."

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# Raw HTTP

async def send_v2(interaction: discord.Interaction, components: list, ephemeral=False):
    flags = (1 << 15) | (64 if ephemeral else 0)
    route = discord.http.Route(
        "POST",
        "/interactions/{interaction_id}/{interaction_token}/callback",
        interaction_id=interaction.id,
        interaction_token=interaction.token,
    )
    await bot.http.request(route, json={
        "type": 4,
        "data": {"flags": flags, "components": components},
    })


async def edit_v2(interaction: discord.Interaction, components: list):
    route = discord.http.Route(
        "POST",
        "/interactions/{interaction_id}/{interaction_token}/callback",
        interaction_id=interaction.id,
        interaction_token=interaction.token,
    )
    await bot.http.request(route, json={
        "type": 7,
        "data": {"flags": 1 << 15, "components": components},
    })


# 전체 예제 컴포넌트
# 총 40개 카운트 (Discord 상한선):
# 1=type10헤더 2=type14 3=type17 4=type10 5=type14 6=type9 7=type10 8=type10
# 9=type10 10=type11 11=type9 12=type10 13=type10 14=type2 15=type17 16=type10
# 17=type10갤러리헤더 18=type12 19=type13 20=type1 21=type2 22=type2 23=type2
# 24=type2 25=type2 26=type1 27=type2 28=type1 29=type3 30=type1 31=type5
# 32=type1 33=type6 34=type1 35=type7 36=type1 37=type8 38=type10리셋힌트
# 39=type1 40=type2

def showcase_components(state: dict) -> list:
    s = state
    return [
        # 1 - type 10 - Text Display
        # IS_COMPONENTS_V2 플래그 메시지에서 content= 대신 사용
        # Discord 마크다운 전부 지원: ##, **, *, ||spoiler||, -#(작은글씨), 코드블럭
        # 선택 현황을 한 블록에 모아 컴포넌트 수 절약
        {
            "type": 10,
            "content": (
                "# Components V2 — 전체 쇼케이스\n"
                "메시지에서 사용할 수 있는 **모든 컴포넌트 타입**을 담은 예제입니다.\n"
                "-# type 1·2·3·5·6·7·8·9·10·11·12·13·14·17\n\n"
                "**현재 선택값**\n"
                f"String: `{s.get('string_select') or '없음'}` | "
                f"User: `{s.get('user_select') or '없음'}` | "
                f"Role: `{s.get('role_select') or '없음'}` | "
                f"Mentionable: `{s.get('mentionable_select') or '없음'}` | "
                f"Channel: `{s.get('channel_select') or '없음'}`"
            ),
        },

        # 2 - type 14 - Separator
        # divider=True  = 가로선 + 여백
        # divider=False = 여백만 (선 없음)
        # spacing=1     = 작은 여백 / spacing=2 = 큰 여백
        {"type": 14, "divider": True, "spacing": 1},

        # 3 - type 17 - Container
        # 내부 컴포넌트들을 하나의 카드처럼 시각적으로 묶음
        # accent_color: 왼쪽 세로 색상 바 (RGB int)
        # spoiler=True: 전체 내용이 블러 처리, 클릭해야 보임
        {
            "type": 17,
            "accent_color": 0x57F287,
            "spoiler": False,
            "components": [

                # 4 - type 10 내부
                {"type": 10, "content": "## Container (type 17)\n`accent_color=0x57F287`  |  `spoiler=False`"},

                # 5 - type 14 내부
                {"type": 14, "divider": True, "spacing": 1},

                # 6 - type 9 - Section (Thumbnail accessory)
                # components: Text Display 1~3개 (왼쪽)
                # accessory:  Thumbnail 또는 Button (오른쪽)
                {
                    "type": 9,
                    "components": [
                        # 7
                        {"type": 10, "content": "### Section (type 9) — Thumbnail accessory"},
                        # 8
                        {"type": 10, "content": "텍스트가 왼쪽, Thumbnail이 오른쪽에 나란히 렌더됩니다.\n`description`은 alt text, `spoiler=True`면 클릭해야 이미지가 보입니다."},
                        # 9
                        {"type": 10, "content": "-# 최대 3개의 Text Display를 넣을 수 있습니다"},
                    ],
                    "accessory": {
                        # 10 - type 11 - Thumbnail
                        # Section의 오른쪽 accessory로만 사용 가능
                        # media.url: 외부 URL 또는 attachment://파일명
                        "type": 11,
                        "media": {"url": "https://i.imgur.com/AfFp7pu.png"},
                        "description": "썸네일 alt text",
                        "spoiler": False,
                    },
                },

                # 11 - type 9 - Section (Button accessory)
                {
                    "type": 9,
                    "components": [
                        # 12
                        {"type": 10, "content": "### Section (type 9) — Button accessory"},
                        # 13
                        {"type": 10, "content": "accessory로 Thumbnail 대신 **Button**을 넣을 수도 있습니다."},
                    ],
                    "accessory": {
                        # 14
                        "type": 2,
                        "custom_id": "section_btn",
                        "label": "Section 버튼",
                        "style": 1,
                    },
                },

            ],
        },

        # 15 - type 17 - Container (spoiler=True 예시)
        {
            "type": 17,
            "accent_color": 0xED4245,
            "spoiler": True,
            "components": [
                # 16
                {"type": 10, "content": "### Container with `spoiler=True`\n이 Container는 클릭 전까지 내용이 블러 처리됩니다."},
            ],
        },

        # 17 - type 10 - Media Gallery 헤더
        # type 12 - Media Gallery
        # items: 1~10개. 2장=나란히, 3장=1+2, 4장=2+2 레이아웃
        # spoiler=True인 항목은 클릭해야 보임
        {"type": 10, "content": "## Media Gallery (type 12)"},

        # 18 - type 12
        {
            "type": 12,
            "items": [
                {
                    "media": {"url": "https://i.imgur.com/AfFp7pu.png"},
                    "description": "이미지 1 — spoiler=False",
                    "spoiler": False,
                },
                {
                    "media": {"url": "https://i.imgur.com/AfFp7pu.png"},
                    "description": "이미지 2 — spoiler=True",
                    "spoiler": True,
                },
                {
                    "media": {"url": "https://i.imgur.com/AfFp7pu.png"},
                    "description": "이미지 3",
                    "spoiler": False,
                },
            ],
        },

        # 19 - type 13 - File
        # attachment:// 프로토콜로 업로드된 파일 참조
        # 실제 사용 시 multipart form으로 파일을 함께 전송해야 함
        {
            "type": 13,
            "file": {"url": "attachment://example.txt"},
            "spoiler": False,
        },

        # 20 - type 1 - Action Row
        # type 2 - Button (style 1~5 전부)
        # Action Row 하나당 최대 5개
        # style 1 Primary   — custom_id 필수
        # style 2 Secondary — custom_id 필수
        # style 3 Success   — custom_id 필수
        # style 4 Danger    — custom_id 필수
        # style 5 Link      — url 필수, custom_id 없음, 인터랙션 없음
        # disabled=True 로 비활성화 가능
        # emoji: name(유니코드) 또는 id(커스텀 이모지)
        {
            "type": 1,
            "components": [
                # 21
                {"type": 2, "custom_id": "btn_primary",   "label": "Primary",   "style": 1, "emoji": {"name": "1️⃣"}},
                # 22
                {"type": 2, "custom_id": "btn_secondary", "label": "Secondary", "style": 2, "emoji": {"name": "2️⃣"}},
                # 23
                {"type": 2, "custom_id": "btn_success",   "label": "Success",   "style": 3, "emoji": {"name": "3️⃣"}},
                # 24
                {"type": 2, "custom_id": "btn_danger",    "label": "Danger",    "style": 4, "emoji": {"name": "4️⃣"}},
                # 25
                {"type": 2,                               "label": "Link",      "style": 5, "url": "https://discord.com", "emoji": {"name": "5️⃣"}},
            ],
        },

        # 26 - disabled 예시
        {
            "type": 1,
            "components": [
                # 27
                {"type": 2, "custom_id": "btn_disabled", "label": "Disabled 버튼", "style": 1, "disabled": True},
            ],
        },

        # 28 - type 1 Action Row
        # type 3 - String Select
        # 개발자가 직접 options를 정의하는 드롭다운
        # min_values/max_values로 단일/다중 선택 설정
        {
            "type": 1,
            "components": [
                # 29
                {
                    "type": 3,
                    "custom_id": "string_select",
                    "placeholder": "String Select — 옵션을 선택하세요 (다중선택 가능)",
                    "min_values": 1,
                    "max_values": 3,
                    "options": [
                        {"label": "옵션 A", "value": "A", "description": "첫 번째 옵션", "emoji": {"name": "🔴"}, "default": False},
                        {"label": "옵션 B", "value": "B", "description": "두 번째 옵션", "emoji": {"name": "🟡"}, "default": False},
                        {"label": "옵션 C", "value": "C", "description": "세 번째 옵션", "emoji": {"name": "🟢"}, "default": False},
                        {"label": "옵션 D", "value": "D", "description": "네 번째 옵션", "emoji": {"name": "🔵"}, "default": False},
                    ],
                },
            ],
        },

        # 30 - type 1 Action Row
        # type 5 - User Select
        # 서버 유저 목록에서 선택. options 정의 불필요 (자동 채워짐)
        {
            "type": 1,
            "components": [
                # 31
                {
                    "type": 5,
                    "custom_id": "user_select",
                    "placeholder": "User Select — 유저를 선택하세요",
                    "min_values": 1,
                    "max_values": 3,
                },
            ],
        },

        # 32 - type 1 Action Row
        # type 6 - Role Select
        # 서버 역할 목록에서 선택
        {
            "type": 1,
            "components": [
                # 33
                {
                    "type": 6,
                    "custom_id": "role_select",
                    "placeholder": "Role Select — 역할을 선택하세요",
                    "min_values": 1,
                    "max_values": 3,
                },
            ],
        },

        # 34 - type 1 Action Row
        # type 7 - Mentionable Select
        # 유저 + 역할 둘 다 선택 가능
        {
            "type": 1,
            "components": [
                # 35
                {
                    "type": 7,
                    "custom_id": "mentionable_select",
                    "placeholder": "Mentionable Select — 유저 또는 역할을 선택하세요",
                    "min_values": 1,
                    "max_values": 5,
                },
            ],
        },

        # 36 - type 1 Action Row
        # type 8 - Channel Select
        # 서버 채널 목록에서 선택
        # channel_types: 채널 타입 필터 (0=텍스트, 2=음성, 4=카테고리 등)
        {
            "type": 1,
            "components": [
                # 37
                {
                    "type": 8,
                    "custom_id": "channel_select",
                    "placeholder": "Channel Select — 텍스트 채널을 선택하세요",
                    "channel_types": [0],
                    "min_values": 1,
                    "max_values": 2,
                },
            ],
        },

        # 38 - type 10
        {"type": 10, "content": "-# 모든 선택값을 초기화하려면 아래 버튼을 누르세요"},

        # 39 - type 1 Action Row
        {
            "type": 1,
            "components": [
                # 40
                {"type": 2, "custom_id": "btn_reset", "label": "전체 초기화", "style": 4, "emoji": {"name": "🔄"}},
            ],
        },
    ]


# 슬래시 커맨드

@tree.command(name="showcase", description="Components V2 전체 컴포넌트 쇼케이스")
async def showcase(interaction: discord.Interaction):
    import aiohttp, json

    # defer로 3초 제한 해제
    await interaction.response.defer()

    file_content = b"Components V2 File (type 13) example file."

    payload = {
        "flags": 1 << 15,
        "components": showcase_components({}),
    }

    form = aiohttp.FormData()
    form.add_field("payload_json", json.dumps(payload), content_type="application/json")
    form.add_field("files[0]", file_content, filename="example.txt", content_type="text/plain")

    async with aiohttp.ClientSession() as session:
        # defer된 @original 메시지를 파일+컴포넌트로 교체
        url = f"https://discord.com/api/v10/webhooks/{interaction.application_id}/{interaction.token}/messages/@original"
        resp = await session.patch(url, data=form, headers={"Authorization": f"Bot {TOKEN}"})


# 인터랙션 핸들러

_state: dict[int, dict] = {}

@bot.listen()
async def on_interaction(interaction: discord.Interaction):

    if interaction.type != discord.InteractionType.component:
        return

    data      = interaction.data
    ctype     = data.get("component_type")
    custom_id = data.get("custom_id", "")
    msg_id    = interaction.message.id

    state = _state.setdefault(msg_id, {})

    # String Select (type 3)
    if ctype == 3 and custom_id == "string_select":
        state["string_select"] = ", ".join(data["values"])
        await edit_v2(interaction, showcase_components(state))

    # User Select (type 5)
    elif ctype == 5 and custom_id == "user_select":
        users = data.get("resolved", {}).get("users", {})
        names = [u["username"] for u in users.values()]
        state["user_select"] = ", ".join(names) if names else ", ".join(data["values"])
        await edit_v2(interaction, showcase_components(state))

    # Role Select (type 6)
    elif ctype == 6 and custom_id == "role_select":
        roles = data.get("resolved", {}).get("roles", {})
        names = [r["name"] for r in roles.values()]
        state["role_select"] = ", ".join(names) if names else ", ".join(data["values"])
        await edit_v2(interaction, showcase_components(state))

    # Mentionable Select (type 7)
    elif ctype == 7 and custom_id == "mentionable_select":
        resolved = data.get("resolved", {})
        names = (
            [u["username"] for u in resolved.get("users", {}).values()] +
            [r["name"]     for r in resolved.get("roles", {}).values()]
        )
        state["mentionable_select"] = ", ".join(names) if names else ", ".join(data["values"])
        await edit_v2(interaction, showcase_components(state))

    # Channel Select (type 8)
    elif ctype == 8 and custom_id == "channel_select":
        channels = data.get("resolved", {}).get("channels", {})
        names = [f"#{c['name']}" for c in channels.values()]
        state["channel_select"] = ", ".join(names) if names else ", ".join(data["values"])
        await edit_v2(interaction, showcase_components(state))

    # Buttons (type 2)
    elif ctype == 2:
        if custom_id == "btn_reset":
            _state.pop(msg_id, None)
            await edit_v2(interaction, showcase_components({}))

        elif custom_id == "section_btn":
            await interaction.response.send_message(
                "Section의 Button accessory 클릭됨!", ephemeral=True
            )

        else:
            label_map = {
                "btn_primary":   "Primary (style 1)",
                "btn_secondary": "Secondary (style 2)",
                "btn_success":   "Success (style 3)",
                "btn_danger":    "Danger (style 4)",
            }
            await interaction.response.send_message(
                f"`{label_map.get(custom_id, custom_id)}` 버튼 클릭됨!", ephemeral=True
            )

@bot.event
async def on_ready():
    await tree.sync()
    print(f"[ready] {bot.user}  |  /showcase 로 실행")


bot.run(TOKEN)