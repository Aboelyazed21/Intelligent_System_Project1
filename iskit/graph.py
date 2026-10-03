# استيراد مكتبة json للتعامل مع بيانات JSON
import json

# استيراد مكتبة heapq لاستخدام Priority Queue
# وهي مستخدمة في Dijkstra و A*
import heapq

# استيراد deque لاستخدام Queue في BFS
from collections import deque


# تعريف Class اسمه Graph لتمثيل الـ Graph
class Graph:

    # الـ Constructor ويتم تنفيذه عند إنشاء Object جديد من Graph
    # directed=False معناها أن الـ Graph غير موجه بشكل افتراضي
    def __init__(self, directed=False):

        # إنشاء Dictionary لتخزين الـ Nodes والـ Neighbors الخاصة بها
        self.adj = {}

        # تخزين هل الـ Graph Directed أم Undirected
        self.directed = directed

        # List لتخزين خطوات الخوارزمية لاستخدامها في الـ Visualization
        self.steps = []

    # دالة لإضافة Edge بين Node و Node أخرى
    # u = الـ Node الأولى
    # v = الـ Node الثانية
    # w = وزن الـ Edge والقيمة الافتراضية له 1.0
    def add_edge(self, u, v, w=1.0):

        # التأكد أن الـ Weight ليس سالبًا
        if w < 0:

            # إذا كان الوزن سالبًا يتم إظهار ValueError
            raise ValueError("Negative weights are not allowed")

        # التأكد هل الـ Node الأولى موجودة في الـ Graph أم لا
        if u not in self.adj:

            # إذا لم تكن موجودة ننشئ لها List فارغة
            self.adj[u] = []

        # التأكد هل الـ Node الثانية موجودة في الـ Graph أم لا
        if v not in self.adj:

            # إذا لم تكن موجودة ننشئ لها List فارغة
            self.adj[v] = []

        # إضافة Edge من u إلى v مع الـ Weight
        self.adj[u].append((v, w))

        # التأكد هل الـ Graph غير موجه
        if not self.directed:

            # إضافة Edge عكسية من v إلى u بنفس الـ Weight
            self.adj[v].append((u, w))

    # دالة للحصول على جميع الـ Neighbors الخاصة بـ Node معينة
    def neighbors(self, u):

        # إرجاع الـ Neighbors الخاصة بـ u
        # وإذا كانت u غير موجودة يتم إرجاع List فارغة
        return self.adj.get(u, [])

    # تحويل JSON إلى Graph
    # @classmethod تجعل الدالة مرتبطة بالـ Class نفسه
    @classmethod
    def from_json(cls, text):

        # تحويل النص الموجود في text من JSON إلى Python Dictionary
        data = json.loads(text)

        # التأكد أن JSON يحتوي على directed و edges
        if "directed" not in data or "edges" not in data:

            # إذا كانت البيانات ناقصة يتم إظهار Error
            raise ValueError("Invalid JSON")

        # إنشاء Graph جديد باستخدام قيمة directed الموجودة في JSON
        g = cls(directed=data["directed"])

        # المرور على كل Edge موجودة داخل JSON
        for edge in data["edges"]:

            # إذا كانت الـ Edge تحتوي على عنصرين فقط
            # مثال: ["A", "B"]
            if len(edge) == 2:

                # تخزين الـ Node الأولى والثانية
                u, v = edge

                # وضع Weight افتراضي قيمته 1.0
                w = 1.0

            # إذا كانت الـ Edge تحتوي على 3 عناصر
            # مثال: ["A", "B", 5]
            elif len(edge) == 3:

                # تخزين الـ Node الأولى والثانية والـ Weight
                u, v, w = edge

            # إذا كان عدد عناصر الـ Edge ليس 2 أو 3
            else:

                # إظهار Error لأن شكل الـ Edge غير صحيح
                raise ValueError("Edge must have 2 or 3 values")

            # إضافة الـ Edge إلى الـ Graph
            g.add_edge(u, v, w)

        # إرجاع الـ Graph بعد الانتهاء من إضافة كل الـ Edges
        return g

    # دالة لتسجيل كل خطوة من خطوات الخوارزمية
    # لاستخدام هذه المعلومات في الرسم والـ Visualization
    def record_step(self, node, visited, path, cost=0):

        # إضافة معلومات الخطوة الحالية إلى List اسمها steps
        self.steps.append({

            # تخزين الـ Node الحالية التي تعمل عليها الخوارزمية
            "current": node,

            # تخزين جميع الـ Nodes التي تمت زيارتها حتى الآن
            "visited": list(visited),

            # تخزين المسار الحالي من Start إلى الـ Node الحالية
            "path": list(path),

            # تخزين الـ Cost الحالية
            "cost": cost
        })

    # تعريف خوارزمية BFS
    # s = Start Node
    # goal = الـ Node التي نريد الوصول إليها
    def bfs(self, s, goal):

        # مسح أي خطوات قديمة قبل بداية BFS جديدة
        self.steps = []

        # إنشاء Queue باستخدام deque
        # نضع Start Node والمسار الحالي الذي يحتوي على Start
        q = deque([(s, [s])])

        # إنشاء Set لتخزين الـ Nodes التي تمت زيارتها
        # ونضع Start Node فيها لأنها تمت زيارتها
        visited = {s}

        # متغير لحساب عدد الـ Nodes التي تم توسيعها
        expanded = 0

        # List لتخزين الـ Nodes التي تم معالجتها
        processed = []

        # الاستمرار طالما الـ Queue ليست فارغة
        while q:

            # أخذ أول عنصر من الـ Queue وحذفه
            # node = الـ Node الحالية
            # path = المسار الذي وصلنا به إليها
            node, path = q.popleft()

            # زيادة عدد الـ Nodes التي تم توسيعها بمقدار واحد
            expanded += 1

            # إضافة الـ Node الحالية إلى Nodes التي تمت معالجتها
            processed.append(node)

            # تسجيل الخطوة الحالية لكي تظهر في الـ Visualization
            self.record_step(
                node,
                processed,
                path
            )

            # التأكد هل الـ Node الحالية هي الـ Goal
            if node == goal:

                # إذا وصلنا للهدف نرجع الـ Path وعدد الـ Nodes التي تم توسيعها
                return path, expanded

            # المرور على كل Neighbor للـ Node الحالية
            # nxt = الـ Neighbor
            # _ = الـ Weight
            # نستخدم _ لأن BFS لا تعتمد على الـ Weight
            for nxt, _ in self.neighbors(node):

                # التأكد أن الـ Neighbor لم تتم زيارتها من قبل
                if nxt not in visited:

                    # تسجيل الـ Neighbor على أنها تمت زيارتها
                    visited.add(nxt)

                    # إضافة الـ Neighbor إلى نهاية الـ Queue
                    # وإضافة الـ Neighbor إلى الـ Path
                    q.append((
                        nxt,
                        path + [nxt]
                    ))

        # إذا انتهت الـ Queue ولم نصل للهدف
        # نرجع None بدل الـ Path وعدد الـ Nodes التي تم توسيعها
        return None, expanded

    # تعريف خوارزمية Dijkstra
    # الهدف منها إيجاد أقل مسار من s إلى goal
    def dijkstra(self, s, goal):

        # مسح الخطوات القديمة قبل بداية Dijkstra
        self.steps = []

        # إنشاء Priority Queue
        # 0 = التكلفة في البداية
        # s = Start Node
        # [s] = المسار الحالي
        pq = [(0, s, [s])]

        # Dictionary لتخزين أقل Cost معروفة للوصول لكل Node
        # تكلفة الوصول إلى Start تساوي صفر
        dist = {s: 0}

        # List لتخزين الـ Nodes التي تم زيارتها أو معالجتها
        visited = []

        # الاستمرار طالما Priority Queue ليست فارغة
        while pq:

            # أخذ العنصر الذي يمتلك أقل Cost من Priority Queue
            # cost = التكلفة
            # node = الـ Node الحالية
            # path = المسار الحالي
            cost, node, path = heapq.heappop(pq)

            # إذا كانت التكلفة الحالية أكبر من أفضل تكلفة مسجلة للـ Node
            if cost > dist.get(node, float("inf")):

                # تجاهل هذه الحالة والانتقال للحالة التالية
                continue

            # إضافة الـ Node الحالية إلى الـ Nodes التي تمت زيارتها
            visited.append(node)

            # تسجيل الخطوة الحالية للـ Visualization
            self.record_step(
                node,
                visited,
                path,
                cost
            )

            # التأكد هل وصلنا إلى الـ Goal
            if node == goal:

                # إرجاع أقصر Path والتكلفة الخاصة به
                return path, cost

            # المرور على كل Neighbor للـ Node الحالية
            for nxt, w in self.neighbors(node):

                # حساب التكلفة الجديدة
                # التكلفة الحالية + وزن الـ Edge
                new_cost = cost + w

                # التأكد هل الطريق الجديد أرخص من الطريق القديم
                if new_cost < dist.get(nxt, float("inf")):

                    # تحديث أقل Cost معروفة للـ Node الجديدة
                    dist[nxt] = new_cost

                    # إضافة الـ Node الجديدة إلى Priority Queue
                    heapq.heappush(
                        pq,
                        (
                            new_cost,
                            nxt,
                            path + [nxt]
                        )
                    )

        # إذا لم نجد طريقًا للـ Goal
        # نرجع None للـ Path و Infinity للتكلفة
        return None, float("inf")

    # تعريف خوارزمية A*
    # h هي Heuristic Function التي تقدر المسافة المتبقية للهدف
    def astar(self, s, goal, h):

        # مسح الخطوات القديمة قبل تشغيل A*
        self.steps = []

        # إنشاء Priority Queue
        # h(s) = قيمة الـ Heuristic للـ Start
        # 0 = التكلفة الفعلية g في البداية
        # s = Start Node
        # [s] = المسار الحالي
        pq = [(h(s), 0, s, [s])]

        # Dictionary لتخزين أفضل قيمة g لكل Node
        # g هي التكلفة الفعلية من Start إلى Node
        best_g = {s: 0}

        # List لتخزين الـ Nodes التي تمت زيارتها
        visited = []

        # الاستمرار طالما Priority Queue ليست فارغة
        while pq:

            # أخذ العنصر صاحب أقل قيمة f
            #
            # f = g + h
            # g = التكلفة الفعلية
            # node = الـ Node الحالية
            # path = المسار الحالي
            f, g, node, path = heapq.heappop(pq)

            # التأكد هل وجدنا طريقًا أفضل سابقًا لنفس الـ Node
            if g > best_g.get(node, float("inf")):

                # إذا كان الطريق الحالي أسوأ نتجاهله
                continue

            # إضافة الـ Node الحالية إلى قائمة الـ Nodes التي تمت زيارتها
            visited.append(node)

            # تسجيل الخطوة الحالية للـ Visualization
            self.record_step(
                node,
                visited,
                path,
                g
            )

            # التأكد هل وصلنا إلى الـ Goal
            if node == goal:

                # إرجاع الـ Path والتكلفة الفعلية g
                return path, g

            # المرور على كل Neighbor للـ Node الحالية
            for nxt, w in self.neighbors(node):

                # حساب التكلفة الفعلية الجديدة
                # g الجديدة = g الحالية + Weight
                new_g = g + w

                # التأكد هل التكلفة الجديدة أفضل من التكلفة القديمة
                if new_g < best_g.get(nxt, float("inf")):

                    # تحديث أفضل تكلفة g للـ Node الجديدة
                    best_g[nxt] = new_g

                    # إضافة الحالة الجديدة إلى Priority Queue
                    #
                    # new_g = التكلفة الفعلية من البداية
                    # h(nxt) = التقدير المتبقي للوصول للهدف
                    # new_g + h(nxt) = f
                    heapq.heappush(
                        pq,
                        (
                            new_g + h(nxt),
                            new_g,
                            nxt,
                            path + [nxt]
                        )
                    )

        # إذا لم نجد طريقًا إلى الـ Goal
        # نرجع None للـ Path و Infinity للتكلفة
        return None, float("inf")