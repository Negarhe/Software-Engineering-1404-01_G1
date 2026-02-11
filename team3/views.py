from django.http import JsonResponse
from django.shortcuts import render
from core.auth import api_login_required
from team3.models import ExamPack, Exam, ExamSystem, ExamSection, UserExam, UserExamStatus

TEAM_NAME = "team3"

SYSTEM_MAP = {
    "IELTS": ExamSystem.IELTS,
    "TOEFL": ExamSystem.TOEFL,
    "GENERAL": ExamSystem.GENERAL,
}

FINISHED_STATUSES = [
    UserExamStatus.SUBMITTED,
    UserExamStatus.REVIEWED,
    UserExamStatus.GRADED,
]

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

@api_login_required
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

@api_login_required
def feedback(request):
    return render(request, f"{TEAM_NAME}/feedback.html")

def speaking_exam(request):
    exam_id = request.GET.get("exam_id")

    exam = None
    if exam_id:
        exam = get_object_or_404(Exam, id=exam_id)

    context = {
        "exam": exam,
        "exam_id": exam_id,
    }
    return render(request, f"{TEAM_NAME}/speaking_exam.html", context)
    # 1) all finished user_exams for this user
    user_exams = (
        UserExam.objects
        .select_related("exam", "exam__pack")
        .filter(
            user=request.user,
            is_deleted=False,
            status__in=FINISHED_STATUSES,
            exam__is_deleted=False,
            exam__pack__is_deleted=False,
        )
        .order_by("-created_at")
    )


    cards_by_pack = {}

    for ue in user_exams:
        user_exam = ue.exam
        pack = user_exam.pack
        if not pack:
            continue

        card = cards_by_pack.get(pack.id)
        if not card:
            card = {
                "pack_id": pack.id,
                "title": pack.title,
                "system": pack.system,
                "sections": {
                    "speaking": None,
                    "writing": None,
                    "reading": None,
                    "listening": None,
                },
                "last_attempt_at": ue.created_at,
            }
            cards_by_pack[pack.id] = card

        if ue.created_at and (card["last_attempt_at"] is None or ue.created_at > card["last_attempt_at"]):
            card["last_attempt_at"] = ue.created_at

        if user_exam.section == ExamSection.SPEAKING and card["sections"]["speaking"] is None:
            card["sections"]["speaking"] = user_exam.id
        elif user_exam.section == ExamSection.WRITING and card["sections"]["writing"] is None:
            card["sections"]["writing"] = user_exam.id
        elif user_exam.section == ExamSection.READING and card["sections"]["reading"] is None:
            card["sections"]["reading"] = user_exam.id
        elif user_exam.section == ExamSection.LISTENING and card["sections"]["listening"] is None:
            card["sections"]["listening"] = user_exam.id

    cards = sorted(cards_by_pack.values(), key=lambda c: c["last_attempt_at"], reverse=True)

    return render(request, f"{TEAM_NAME}/feedback.html", {"cards": cards})
