from django.http import JsonResponse
from django.shortcuts import render
from core.auth import api_login_required
from team3.models import ExamPack, Exam, ExamSystem, ExamSection

TEAM_NAME = "team3"

SYSTEM_MAP = {
    "IELTS": ExamSystem.IELTS,
    "TOEFL": ExamSystem.TOEFL,
    "GENERAL": ExamSystem.GENERAL,
}

SYSTEM_DISPLAY_FA = {
    ExamSystem.IELTS: "آیلتس",
    ExamSystem.TOEFL: "تافل",
    ExamSystem.GENERAL: "جنرال",
}

@api_login_required
def ping(request):
    return JsonResponse({"team": TEAM_NAME, "ok": True})

def base(request):
    return render(request, f"{TEAM_NAME}/index.html")

def exam(request):
    system_param = (request.GET.get("system") or "").upper()
    system = SYSTEM_MAP.get(system_param)

    if not system:
        system = ExamSystem.IELTS

    packs_qs = (
        ExamPack.objects
        .filter(system=system, is_deleted=False)
        .order_by("id")
    )

    pack_cards = []
    for p in packs_qs:
        exams = (
            Exam.objects
            .filter(pack=p, is_deleted=False)
            .values("id", "section")
        )
        section_to_exam_id = {e["section"]: e["id"] for e in exams}

        pack_cards.append({
            "id": p.id,
            "title": p.title,
            "sections": {
                "writing": section_to_exam_id.get(ExamSection.WRITING),
                "speaking": section_to_exam_id.get(ExamSection.SPEAKING),
                "reading": section_to_exam_id.get(ExamSection.READING),
                "listening": section_to_exam_id.get(ExamSection.LISTENING),
            }
        })

    ctx = {
        "system_key": system_param,
        "system": system,
        "system_fa": SYSTEM_DISPLAY_FA.get(system, "آزمون"),
        "packs": pack_cards,
    }
    return render(request, f"{TEAM_NAME}/exam.html", ctx)
