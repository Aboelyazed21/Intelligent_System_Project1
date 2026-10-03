# استيراد Class اسمه Graph من ملف graph.py الموجود داخل package اسمها iskit
from iskit.graph import Graph


# اختبار إضافة Edge في Graph غير موجه Undirected Graph
def test_add_edge_undirected():

    # إنشاء Graph جديد، والافتراضي أنه Undirected
    g = Graph()

    # إضافة Edge بين A و B والـ Weight الخاص بها = 2
    g.add_edge("A", "B", 2)

    # نتأكد أن B موجودة كجار لـ A والوزن بينهم 2
    assert ("B", 2) in g.neighbors("A")

    # نتأكد أن A موجودة كجار لـ B والوزن بينهم 2
    # لأن الـ Graph غير موجه، فالطريق يعمل في الاتجاهين
    assert ("A", 2) in g.neighbors("B")


# اختبار إضافة Edge في Graph موجه Directed Graph
def test_add_edge_directed():

    # إنشاء Graph موجه Directed Graph
    g = Graph(directed=True)

    # إضافة Edge من A إلى B والـ Weight = 2
    g.add_edge("A", "B", 2)

    # نتأكد أن B موجودة كجار لـ A
    assert ("B", 2) in g.neighbors("A")

    # نتأكد أن B ليس لديها A كجار
    # لأن الـ Graph موجه، فالطريق A -> B فقط
    assert g.neighbors("B") == []


# اختبار إنشاء Graph باستخدام بيانات JSON
def test_from_json():

    # إنشاء نص بصيغة JSON يحتوي على Graph غير موجه
    # ويوجد Edge من A إلى B بوزن 3
    # و Edge من B إلى C بوزن 2
    text = '{"directed": false, "edges": [["A", "B", 3], ["B", "C", 2]]}'

    # تحويل الـ JSON إلى Graph باستخدام from_json
    g = Graph.from_json(text)

    # نتأكد أن B موجودة كجار لـ A والوزن = 3
    assert ("B", 3) in g.neighbors("A")


# اختبار خوارزمية BFS
def test_bfs():

    # إنشاء Graph غير موجه
    g = Graph()

    # إضافة Edge من A إلى B
    g.add_edge("A", "B")

    # إضافة Edge من B إلى C
    g.add_edge("B", "C")

    # تشغيل BFS من A إلى C
    # الدالة ترجع path وعدد الـ nodes التي تم توسيعها
    # نضع _ لأننا لا نحتاج عدد الـ nodes هنا
    path, _ = g.bfs("A", "C")

    # نتأكد أن المسار الذي وجدته BFS هو A -> B -> C
    assert path == ["A", "B", "C"]


# اختبار خوارزمية Dijkstra
def test_dijkstra():

    # إنشاء Graph غير موجه
    g = Graph()

    # إضافة Edge من A إلى B ووزنها = 1
    g.add_edge("A", "B", 1)

    # إضافة Edge من B إلى C ووزنها = 2
    g.add_edge("B", "C", 2)

    # إضافة Edge مباشرة من A إلى C ووزنها = 10
    g.add_edge("A", "C", 10)

    # تشغيل Dijkstra للبحث عن أقل تكلفة من A إلى C
    # الدالة ترجع المسار والتكلفة
    path, cost = g.dijkstra("A", "C")

    # نتأكد أن Dijkstra اختارت المسار A -> B -> C
    assert path == ["A", "B", "C"]

    # تكلفة المسار A -> B -> C تساوي 1 + 2 = 3
    assert cost == 3


# اختبار خوارزمية A*
def test_astar():

    # إنشاء Graph غير موجه
    g = Graph()

    # إضافة Edge من A إلى B ووزنها = 1
    g.add_edge("A", "B", 1)

    # إضافة Edge من B إلى C ووزنها = 2
    g.add_edge("B", "C", 2)

    # إضافة Edge مباشرة من A إلى C ووزنها = 10
    g.add_edge("A", "C", 10)

    # إنشاء Heuristic Function
    # lambda n: 0 معناها أن قيمة الـ Heuristic لأي Node تساوي صفر
    h = lambda n: 0

    # تشغيل A* من A إلى C
    # وإرسال الـ Heuristic Function معها
    # الدالة ترجع المسار والتكلفة
    path, cost = g.astar("A", "C", h)

    # نتأكد أن A* وجدت المسار A -> B -> C
    assert path == ["A", "B", "C"]

    # تكلفة المسار = 1 + 2 = 3
    assert cost == 3


# اختبار منع استخدام Negative Weight
def test_negative_weight():

    # إنشاء Graph جديد
    g = Graph()

    # بداية محاولة تنفيذ كود قد ينتج عنه ValueError
    try:

        # محاولة إضافة Edge بوزن سالب -1
        g.add_edge("A", "B", -1)

        # لو السطر السابق لم ينتج عنه Error
        # فهذا يعني أن الاختبار فشل
        assert False

    # نتوقع أن add_edge تطلع ValueError عند استخدام وزن سالب
    except ValueError:

        # إذا حدث ValueError فهذا يعني أن الاختبار نجح
        assert True


# اختبار حالة عدم وجود طريق إلى الهدف
def test_unreachable_goal():

    # إنشاء Graph جديد
    g = Graph()

    # إضافة Edge بين A و B فقط
    g.add_edge("A", "B", 1)

    # محاولة استخدام Dijkstra للوصول من A إلى Z
    # لا يوجد أي طريق إلى Z
    # لذلك المفروض path تكون None
    # و cost تكون Infinity
    path, cost = g.dijkstra("A", "Z")

    # نتأكد أن Dijkstra لم تجد أي مسار إلى Z
    assert path is None
    
    # اختبار التعامل مع JSON غير صحيح
def test_invalid_json():

    # محاولة إنشاء Graph من JSON لا يحتوي على edges
    # وبالتالي JSON غير مطابق للصيغة المطلوبة
    try:

        # محاولة تحويل JSON غير صحيح إلى Graph
        Graph.from_json('{"directed": false}')

        # إذا لم يحدث Error فهذا يعني أن الاختبار فشل
        assert False

    # نتوقع أن from_json تطلع ValueError
    # لأن JSON لا يحتوي على البيانات المطلوبة
    except ValueError:

        # حدوث ValueError يعني أن الاختبار نجح
        assert True