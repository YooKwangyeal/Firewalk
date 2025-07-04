import re
from apis.model.aiModel import aiResponse


def parse_ai_response(raw_text: str) -> aiResponse:
    print("AI 응답 원본:", raw_text)
    # 폭발 반경 (미터, m, M 모두 허용)
    blast_match = re.search(r"폭발 반경.*?(\d+)\s*(?:미터|m|M)", raw_text)
    blast_radius = int(blast_match.group(1)) if blast_match else 0

    # 대피 반경 (미터, m, M 모두 허용)
    evac_match = re.search(r"대피 반경.*?(\d+)\s*(?:미터|m|M)", raw_text)
    evacuation_radius = int(evac_match.group(1)) if evac_match else 0

    # 좌표
    coord_match = re.search(r"\[([\d\.]+),\s*([\d\.]+)\]", raw_text)
    coords = [float(coord_match.group(1)), float(coord_match.group(2))] if coord_match else None

    return aiResponse(
        response=raw_text.strip(),
        blast_radius_m=blast_radius,
        evacuation_radius_m=evacuation_radius,
        danger_zone_coords=coords 
    )