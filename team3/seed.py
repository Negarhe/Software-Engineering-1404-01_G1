# team3/seed_exams.py
import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app404.settings')
django.setup()

from team3.models import Exam, Question, ExamSection, ExamSystem, ExamPack


def get_or_create_pack(system, title: str):
    pack, created = ExamPack.objects.get_or_create(
        system=system,
        title=title,
        defaults={},
    )
    return pack, created


def create_exam_with_questions(pack, system, section, time_seconds, questions_data):
    """
    Create section exam under a pack (unique by pack+section),
    and seed its questions if exam created.
    """
    exam, created = Exam.objects.get_or_create(
        pack=pack,
        system=system,
        section=section,
        defaults={'exam_time_seconds': time_seconds},
    )

    # If exam already existed, do NOT duplicate questions
    if created:
        Question.objects.bulk_create([
            Question(exam=exam, number=q_num, description=q_desc)
            for q_num, q_desc in questions_data
        ])

    return exam, created


def seed_ielts_packs():
    print("🌐 Seeding IELTS ExamPacks (3 packs: Speaking+Writing each)...")

    # ---------------- Pack 1 ----------------
    pack1, _ = get_or_create_pack(ExamSystem.IELTS, "IELTS Pack 1")

    speaking1_questions = [
        (1, "Part 1 (4-5 minutes):\n• Where is your hometown?\n• What do you like about living there?\n• How has your hometown changed in recent years?\n• Do you prefer living in a city or the countryside?"),
        (2, "Part 2 (3-4 minutes):\nDescribe a time you had to wait for something special.\nYou should say:\n• What you were waiting for\n• How long you had to wait\n• What you did while waiting\nAnd explain how you felt when it finally happened."),
        (3, "Part 3 (4-5 minutes):\n• Is patience important in modern life?\n• What are some situations where people need to be patient?\n• Do you think people are less patient now than in the past?\n• How can children learn to be more patient?")
    ]
    create_exam_with_questions(pack1, ExamSystem.IELTS, ExamSection.SPEAKING, 840, speaking1_questions)

    writing1_questions = [
        (1, "Task 1 (Academic - 20 minutes):\nThe charts below show the percentage of water used for different purposes in six areas of the world.\n\nSummarize the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words."),
        (2, "Task 2 (40 minutes):\nSome people believe that children should be allowed to stay at home and play until they are six or seven years old. Others believe that it is important for young children to go to school as early as possible.\n\nDiscuss both views and give your own opinion.\n\nWrite at least 250 words.")
    ]
    create_exam_with_questions(pack1, ExamSystem.IELTS, ExamSection.WRITING, 3600, writing1_questions)

    # ---------------- Pack 2 ----------------
    pack2, _ = get_or_create_pack(ExamSystem.IELTS, "IELTS Pack 2")

    speaking2_questions = [
        (1, "Part 1 (4-5 minutes):\n• How often do you use the internet?\n• What do you usually do online?\n• Do you prefer reading news online or in newspapers?\n• How has technology changed your life?"),
        (2, "Part 2 (3-4 minutes):\nDescribe a useful piece of technology you use regularly.\nYou should say:\n• What the technology is\n• How you use it\n• How long you have been using it\nAnd explain why you find it useful."),
        (3, "Part 3 (4-5 minutes):\n• What are the advantages of modern technology?\n• Are there any disadvantages of relying too much on technology?\n• How has technology changed education?\n• Do you think technology makes people more isolated?")
    ]
    create_exam_with_questions(pack2, ExamSystem.IELTS, ExamSection.SPEAKING, 840, speaking2_questions)

    writing2_questions = [
        (1, "Task 1 (Academic - 20 minutes):\nThe diagram below shows the process by which bricks are manufactured for the building industry.\n\nSummarize the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words."),
        (2, "Task 2 (40 minutes):\nSome people think that governments should give financial support to creative artists such as painters and musicians. Others believe that creative artists should be funded by alternative sources.\n\nDiscuss both views and give your own opinion.\n\nWrite at least 250 words.")
    ]
    create_exam_with_questions(pack2, ExamSystem.IELTS, ExamSection.WRITING, 3600, writing2_questions)

    # ---------------- Pack 3 ----------------
    pack3, _ = get_or_create_pack(ExamSystem.IELTS, "IELTS Pack 3")

    speaking3_questions = [
        (1, "Part 1 (4-5 minutes):\n• Do you work or are you a student?\n• What do you like about your job/studies?\n• What would you like to change about your workplace/school?\n• Do you prefer working alone or in a team?"),
        (2, "Part 2 (3-4 minutes):\nDescribe a person who has been an important influence in your life.\nYou should say:\n• Who the person is\n• How long you have known them\n• What qualities this person has\nAnd explain why they have been important in your life."),
        (3, "Part 3 (4-5 minutes):\n• What qualities make someone a good leader?\n• Is it better to have young or old people in leadership positions?\n• How can people develop leadership skills?\n• What are the challenges of being a leader?")
    ]
    create_exam_with_questions(pack3, ExamSystem.IELTS, ExamSection.SPEAKING, 840, speaking3_questions)

    writing3_questions = [
        (1, "Task 2 (40 minutes):\nIn some countries, the average weight of people is increasing and their levels of health and fitness are decreasing.\n\nWhat do you think are the causes of these problems and what measures could be taken to solve them?\n\nWrite at least 250 words."),
        (2, "Task 2 (40 minutes):\nSome people believe that we should not use animals for food, clothing, or any other purposes. Others believe that it is acceptable to use animals for human benefit.\n\nDiscuss both views and give your own opinion.\n\nWrite at least 250 words.")
    ]
    create_exam_with_questions(pack3, ExamSystem.IELTS, ExamSection.WRITING, 4800, writing3_questions)


def seed_toefl_packs():
    print("\n🇺🇸 Seeding TOEFL ExamPacks (3 packs: Speaking+Writing each)...")

    # ---------------- Pack 1 ----------------
    pack1, _ = get_or_create_pack(ExamSystem.TOEFL, "TOEFL Pack 1")

    speaking1_questions = [
        (1, "Independent Task (15s prep, 45s speak):\nSome students prefer to study alone, while others prefer to study in groups. Which method do you prefer and why? Use specific reasons and examples to support your answer."),
        (2, "Integrated Task (45s read, 60s listen, 30s prep, 60s speak):\nReading: University plans to require all first-year students to take a public speaking course.\nListening: Two students discuss the announcement.\nQuestion: The man expresses his opinion about the plan. State his opinion and explain the reasons he gives for holding that opinion."),
        (3, "Integrated Task (90s listen, 20s prep, 60s speak):\nListen to part of a lecture in a psychology class about memory consolidation.\nQuestion: Using points and examples from the lecture, explain how sleep affects memory consolidation."),
        (4, "Integrated Task (90s listen, 20s prep, 60s speak):\nListen to a conversation between two students about a problem with a group project.\nQuestion: The students discuss two possible solutions. Describe the problem and the two solutions. Then explain which solution you prefer and why.")
    ]
    create_exam_with_questions(pack1, ExamSystem.TOEFL, ExamSection.SPEAKING, 1020, speaking1_questions)

    writing1_questions = [
        (1, "Integrated Task (20 minutes):\nReading: The article presents three benefits of remote learning for university students.\nListening: The professor challenges each of these benefits with counterarguments.\n\nQuestion: Summarize the points made in the lecture, being sure to explain how they cast doubt on the specific benefits presented in the reading passage."),
        (2, "Independent Task (30 minutes):\nDo you agree or disagree with the following statement?\n'It is better to have a few close friends than to have many casual acquaintances.'\n\nUse specific reasons and examples to support your answer.")
    ]
    create_exam_with_questions(pack1, ExamSystem.TOEFL, ExamSection.WRITING, 3000, writing1_questions)

    # ---------------- Pack 2 ----------------
    pack2, _ = get_or_create_pack(ExamSystem.TOEFL, "TOEFL Pack 2")

    speaking2_questions = [
        (1, "Independent Task (15s prep, 45s speak):\nDo you agree or disagree with the following statement? 'Technology has made our lives easier but less meaningful.' Use specific reasons and examples to support your answer."),
        (2, "Integrated Task (45s read, 60s listen, 30s prep, 60s speak):\nReading: Proposal to limit social media use on campus Wi-Fi during class hours.\nListening: Two students discuss the proposal.\nQuestion: The woman expresses her opinion about the proposal. State her opinion and explain the reasons she gives for holding that opinion."),
        (3, "Integrated Task (90s listen, 20s prep, 60s speak):\nListen to part of a lecture in a sociology class about urbanization trends.\nQuestion: Using points and examples from the lecture, explain two effects of rapid urbanization mentioned by the professor."),
        (4, "Integrated Task (90s listen, 20s prep, 60s speak):\nListen to a conversation between a student and a professor about a research paper topic.\nQuestion: The professor suggests two possible approaches. Describe the student's situation and the two suggestions. Then explain which suggestion you think is better and why.")
    ]
    create_exam_with_questions(pack2, ExamSystem.TOEFL, ExamSection.SPEAKING, 1020, speaking2_questions)

    writing2_questions = [
        (1, "Integrated Task (20 minutes):\nReading: The article discusses three potential benefits of genetic engineering in agriculture.\nListening: The professor raises concerns about each of these benefits.\n\nQuestion: Summarize the points made in the lecture, being sure to explain how they challenge the specific benefits presented in the reading passage."),
        (2, "Independent Task (30 minutes):\nDo you agree or disagree with the following statement?\n'Governments should spend more money on space exploration than on solving problems on Earth.'\n\nUse specific reasons and examples to support your answer.")
    ]
    create_exam_with_questions(pack2, ExamSystem.TOEFL, ExamSection.WRITING, 3000, writing2_questions)

    # ---------------- Pack 3 ----------------
    pack3, _ = get_or_create_pack(ExamSystem.TOEFL, "TOEFL Pack 3")

    speaking3_questions = [
        (1, "Independent Task (15s prep, 45s speak):\nSome people prefer to exercise outdoors, while others prefer to exercise at home or in a gym. Which do you prefer and why? Use specific reasons and examples to support your answer."),
        (2, "Integrated Task (45s read, 60s listen, 30s prep, 60s speak):\nReading: University health center proposes a mandatory wellness program for all students.\nListening: Two students discuss the proposal.\nQuestion: The woman expresses her opinion about the proposal. State her opinion and explain the reasons she gives for holding that opinion."),
        (3, "Integrated Task (90s listen, 20s prep, 60s speak):\nListen to part of a lecture in a nutrition class about processed foods.\nQuestion: Using points and examples from the lecture, explain two negative effects of highly processed foods."),
        (4, "Integrated Task (90s listen, 20s prep, 60s speak):\nListen to a conversation between a student and a campus housing advisor.\nQuestion: The student has a problem with her roommate. The advisor offers two possible solutions. Describe the problem and the two solutions. Then explain which solution you think is better and why.")
    ]
    create_exam_with_questions(pack3, ExamSystem.TOEFL, ExamSection.SPEAKING, 1020, speaking3_questions)

    writing3_questions = [
        (1, "Integrated Task (20 minutes):\nReading: The article presents three arguments in favor of corporate social responsibility programs.\nListening: The professor questions the effectiveness of these programs.\n\nQuestion: Summarize the points made in the lecture, being sure to explain how they cast doubt on the arguments presented in the reading passage."),
        (2, "Independent Task (30 minutes):\nSome people believe that economic growth is the most important goal for a country. Others believe that protecting the environment should be given higher priority.\n\nDiscuss both views and give your own opinion.")
    ]
    create_exam_with_questions(pack3, ExamSystem.TOEFL, ExamSection.WRITING, 3000, writing3_questions)


def seed_general_packs():
    print("\n🌍 Seeding General English ExamPacks (3 packs: Speaking+Writing each)...")

    # ---------------- Pack 1 ----------------
    pack1, _ = get_or_create_pack(ExamSystem.GENERAL, "General Pack 1")

    speaking1_questions = [
        (1, "Part 1 (4-5 minutes):\n• Have you ever traveled to another country?\n• What type of holiday do you prefer?\n• Do you like trying new foods when you travel?\n• What's the most interesting place you've visited?"),
        (2, "Part 2 (3-4 minutes):\nDescribe a traditional festival in your country.\nYou should say:\n• What the festival is\n• When it is celebrated\n• What people do during this festival\nAnd explain why this festival is important in your culture."),
        (3, "Part 3 (4-5 minutes):\n• Why are traditional festivals important?\n• How have festivals changed over time?\n• Do you think young people are losing interest in traditional festivals?\n• What can be done to preserve cultural traditions?")
    ]
    create_exam_with_questions(pack1, ExamSystem.GENERAL, ExamSection.SPEAKING, 840, speaking1_questions)

    writing1_questions = [
        (1, "Task 1 (Letter - 20 minutes):\nYou recently stayed at a hotel for a business trip. The service was excellent, but there was a problem with the billing.\n\nWrite a letter to the hotel manager. In your letter:\n• Thank them for the good service\n• Explain the billing problem\n• Provide details of what should be corrected\n• Suggest a solution"),
        (2, "Task 2 (Essay - 40 minutes):\nSome people think that the government should provide free housing for everyone. Others believe that individuals should be responsible for their own housing.\n\nDiscuss both views and give your own opinion.")
    ]
    create_exam_with_questions(pack1, ExamSystem.GENERAL, ExamSection.WRITING, 3600, writing1_questions)

    # ---------------- Pack 2 ----------------
    pack2, _ = get_or_create_pack(ExamSystem.GENERAL, "General Pack 2")

    speaking2_questions = [
        (1, "Part 1 (4-5 minutes):\n• What do you do for a living?\n• What skills are important for your job?\n• Do you prefer email or phone calls for work communication?\n• How important is teamwork in your workplace?"),
        (2, "Part 2 (3-4 minutes):\nDescribe a time you had to communicate in a foreign language.\nYou should say:\n• Where you were\n• Who you were talking to\n• What you were talking about\nAnd explain how you felt about the experience."),
        (3, "Part 3 (4-5 minutes):\n• Why is learning foreign languages important?\n• What are the challenges of learning a new language?\n• How has technology helped language learning?\n• Do you think everyone should learn at least one foreign language?")
    ]
    create_exam_with_questions(pack2, ExamSystem.GENERAL, ExamSection.SPEAKING, 840, speaking2_questions)

    writing2_questions = [
        (1, "Task 1 (Letter - 20 minutes):\nYou saw an advertisement for a part-time job at a local bookstore. You are interested in applying.\n\nWrite a letter to the bookstore manager. In your letter:\n• Express your interest in the position\n• Describe your relevant experience\n• Explain why you would be suitable for the job\n• Suggest a time for an interview"),
        (2, "Task 2 (Essay - 40 minutes):\nSome people believe that job satisfaction is more important than a high salary. Others argue that a good salary leads to better quality of life.\n\nDiscuss both views and give your own opinion.")
    ]
    create_exam_with_questions(pack2, ExamSystem.GENERAL, ExamSection.WRITING, 3600, writing2_questions)

    # ---------------- Pack 3 ----------------
    pack3, _ = get_or_create_pack(ExamSystem.GENERAL, "General Pack 3")

    speaking3_questions = [
        (1, "Part 1 (4-5 minutes):\n• What do you do in your free time?\n• Do you prefer indoor or outdoor activities?\n• How often do you watch movies?\n• What kind of music do you like?"),
        (2, "Part 2 (3-4 minutes):\nDescribe a book you recently read and enjoyed.\nYou should say:\n• What the book is about\n• Why you decided to read it\n• What you liked about it\nAnd explain why you would recommend it to others."),
        (3, "Part 3 (4-5 minutes):\n• Do people read less now than in the past?\n• What are the benefits of reading?\n• How has digital technology affected reading habits?\n• Should children be encouraged to read more?")
    ]
    create_exam_with_questions(pack3, ExamSystem.GENERAL, ExamSection.SPEAKING, 840, speaking3_questions)

    writing3_questions = [
        (1, "Task 1 (Letter - 20 minutes):\nYou are concerned about a dangerous intersection near your home where several accidents have occurred.\n\nWrite a letter to the local council. In your letter:\n• Explain the location of the intersection\n• Describe the problem and recent accidents\n• Suggest solutions to improve safety\n• Request action from the council"),
        (2, "Task 2 (Essay - 40 minutes):\nIn many cities, traffic congestion is becoming a serious problem.\n\nWhat are the causes of this problem?\nWhat measures can be taken to solve it?\n\nGive reasons for your answer and include any relevant examples.")
    ]
    create_exam_with_questions(pack3, ExamSystem.GENERAL, ExamSection.WRITING, 3600, writing3_questions)


def run_seed():
    print("=" * 70)
    print("📚 SEEDING EXAMPACKS: 3 PACKS PER SYSTEM (IELTS, TOEFL, GENERAL)")
    print("=" * 70)

    seed_ielts_packs()
    seed_toefl_packs()
    seed_general_packs()

    print("\n" + "=" * 70)
    print("📊 SEEDING COMPLETE - 3 ExamPacks per system")
    print("=" * 70)

    total_packs = ExamPack.objects.count()
    total_exams = Exam.objects.count()
    total_questions = Question.objects.count()

    print(f"\n🎯 Total ExamPacks: {total_packs}")
    print(f"🎯 Total Exams: {total_exams}")
    print(f"🎯 Total Questions: {total_questions}")

    print("\n📋 PACK BREAKDOWN (each pack should have Speaking + Writing):")
    for system_code, system_name in ExamSystem.choices:
        packs = ExamPack.objects.filter(system=system_code)
        if packs.exists():
            print(f"\n  {system_name.upper()}: packs={packs.count()}")
            for p in packs.order_by("id"):
                sections = list(p.exams.values_list("section", flat=True))
                print(f"    • {p.title}: {sections}")

    print("\n✅ Ready for 3 test cards per system (UI)")

if __name__ == "__main__":
    run_seed()
