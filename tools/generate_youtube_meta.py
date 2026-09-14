"""
YouTube Metadata Generation & Validation Tool for Brimir Busters
Enforces zero-explanation, exact-template YouTube titles & descriptions.
"""
import os
import sys
import re
import json

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

TEMPLATE = """[유튜브 제목]
{title}

[설명란 내용]
브리미르 {floor}층 {grade}등급 보스 '{display_name}' 실전 스킬 대응 분류표입니다.

[실전 패턴 대응 가이드]

1. cc기로 끊거나 교전컨트롤로 회피해야됨
{cat1}

2. 패링
{cat2}

3. cc기로 무조건 끊기
{cat3}

자세한 룬·몬스터 정보는 검색창에 '브리미르 버스터즈'를 검색하세요.
게임은 스팀(Steam)에서 『브리미르: 순례자의 탑』을 검색하면 확인하실 수 있습니다.

{hashtags}"""

CURATED_DATA = {
    "사령군주": {
        "id": "reaper_lord",
        "floor": 7,
        "grade": 3,
        "display_name": "사령군주",
        "name_en": "ReaperLord",
        "cat1": ["뼈 브레스", "영혼 징수"],
        "cat2": ["해골의 아귀", "석화 응시!"],
        "cat3": ["저주 파동!", "사령의 부름!", "죽음의 선고", "죽음의 군림"]
    },
    "비탄의 망령": {
        "id": "wailing_wraith",
        "floor": 8,
        "grade": 3,
        "display_name": "비탄의 망령",
        "name_en": "WailingWraith",
        "cat1": ["마법 공격", "공포의 장막"],
        "cat2": ["원한의 손톱!", "원한의 통곡", "공포의 응시", "비탄의 절규!"],
        "cat3": ["저주 파동!", "통곡에 뼈 무리가 일어선다!", "원한의 선고"]
    },
    "심연의 흑기사": {
        "id": "vol_herchan",
        "floor": 8,
        "grade": 3,
        "display_name": "심연의 흑기사",
        "name_en": "AbyssalBlackKnight",
        "cat1": ["흑기사가 검을 세운다 — 치지 마라!", "대검을 땅에 꽂는다!", "대검이 갈고리처럼 날아온다!", "칠흑의 파도!"],
        "cat2": ["대검 3연참!", "검 투척!", "돌진 강타!", "방벽 강타!", "심연 가르기"],
        "cat3": ["철옹성!"]
    },
    "보물미믹": {
        "id": "raphremmik",
        "floor": 6,
        "grade": 4,
        "display_name": "보물 미믹",
        "name_en": "TreasureMimic",
        "cat1": ["약탈의 아가리"],
        "cat2": ["의태 도약", "암흑 일격", "리바이어던의 손아귀"],
        "cat3": ["약탈의 아가리"]
    },
    "보물 미믹": {
        "id": "raphremmik",
        "floor": 6,
        "grade": 4,
        "display_name": "보물 미믹",
        "name_en": "TreasureMimic",
        "cat1": ["약탈의 아가리"],
        "cat2": ["의태 도약", "암흑 일격", "리바이어던의 손아귀"],
        "cat3": ["약탈의 아가리"]
    },
    "해골 와이번": {
        "id": "bone_dragonian",
        "floor": 8,
        "grade": 3,
        "display_name": "해골 와이번",
        "name_en": "SkeletalWyvern",
        "cat1": [
            "뼈 브레스",
            "날개 바람!",
            "뼛가루 장판 — 발밑이 좀먹는다!",
            "뼈 무더기가 무너진다!",
            "뼈 비가 쏟아진다!",
            "날개가 빨아들인다!"
        ],
        "cat2": [
            "발톱 연격!",
            "뼈날개 방패!",
            "낚아챈다!"
        ],
        "cat3": [
            "골수 저주!",
            "뼈가 일어선다!",
            "뼛조각 폭풍"
        ]
    },
    "해골와이번": {
        "id": "bone_dragonian",
        "floor": 8,
        "grade": 3,
        "display_name": "해골 와이번",
        "name_en": "SkeletalWyvern",
        "cat1": [
            "뼈 브레스",
            "날개 바람!",
            "뼛가루 장판 — 발밑이 좀먹는다!",
            "뼈 무더기가 무너진다!",
            "뼈 비가 쏟아진다!",
            "날개가 빨아들인다!"
        ],
        "cat2": [
            "발톱 연격!",
            "뼈날개 방패!",
            "낚아챈다!"
        ],
        "cat3": [
            "골수 저주!",
            "뼈가 일어선다!",
            "뼛조각 폭풍"
        ]
    }
}

def validate_metadata(output_text: str) -> bool:
    """
    Strict Structural Linter:
    1. Zero-Explanation Rule: Bullet items MUST NOT contain colons, parentheses, or narrative sentences.
    2. Category Headers MUST match exactly.
    3. Mandatory links & hashtags MUST be present.
    """
    lines = output_text.splitlines()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- "):
            item = stripped[2:]
            if ":" in item or "이러" in item or "해야" in item or "설명" in item or "(" in item:
                raise ValueError(f"[VIOLATION] Narrative prose or invalid chars found in bullet: '{stripped}'")
            if len(item) > 35:
                raise ValueError(f"[VIOLATION] Bullet item suspiciously long: '{stripped}'")

    assert "[실전 패턴 대응 가이드]" in output_text, "Missing header: [실전 패턴 대응 가이드]"
    assert "1. cc기로 끊거나 교전컨트롤로 회피해야됨" in output_text, "Missing Cat 1"
    assert "2. 패링" in output_text, "Missing Cat 2"
    assert "3. cc기로 무조건 끊기" in output_text, "Missing Cat 3"
    assert "자세한 룬·몬스터 정보는 검색창에 '브리미르 버스터즈'를 검색하세요." in output_text, "Missing footer link 1"
    assert "게임은 스팀(Steam)에서 『브리미르: 순례자의 탑』을 검색하면 확인하실 수 있습니다." in output_text, "Missing footer link 2"
    assert "#브리미르" in output_text and "#Brimir" in output_text, "Missing mandatory hashtags"
    return True

def generate_boss_meta(boss_key: str) -> str:
    data = CURATED_DATA.get(boss_key)
    if not data:
        raise KeyError(f"Monster '{boss_key}' not found in curated data.")
    
    display_name = data["display_name"]
    clean_tag_name = display_name.replace(" ", "")
    title = f"{data['floor']}층 {data['grade']}등급 {display_name} 실전 공략 가이드 [브리미르]"
    
    cat1_str = "\n".join([f"- {s}" for s in data["cat1"]])
    cat2_str = "\n".join([f"- {s}" for s in data["cat2"]])
    cat3_str = "\n".join([f"- {s}" for s in data["cat3"]])
    
    hashtags = f"#브리미르 #{clean_tag_name} #{data['name_en']} #Brimir"
    
    result = TEMPLATE.format(
        title=title,
        floor=data['floor'],
        grade=data['grade'],
        display_name=display_name,
        cat1=cat1_str,
        cat2=cat2_str,
        cat3=cat3_str,
        hashtags=hashtags
    )
    
    validate_metadata(result)
    return result

if __name__ == "__main__":
    targets = sys.argv[1:] if len(sys.argv) > 1 else ["비탄의 망령", "심연의 흑기사", "보물미믹"]
    for t in targets:
        try:
            out = generate_boss_meta(t)
            print(out)
            print("\n" + "="*60 + "\n")
        except Exception as e:
            print(f"Error processing {t}: {e}", file=sys.stderr)
