from neo4j import GraphDatabase
import networkx as nx
import matplotlib.pyplot as plt

#更改Neo4j Bolt連線設定
uri = "neo4j+s://cd122923.databases.neo4j.io "
driver = GraphDatabase.driver(uri, auth=("neo4j", "XMvLaxouvDASwAcmMpcndl7W9j6pf6RpLs7ahPjjxQg"))

def do_Cypher(tx, text):
    result = tx.run(text)
    return result

#建立節點函式
def create_knowledge_point(tx, label, relation, obj):
    command = []
    
    # 查看 node A 是否存在 (類別)
    text = "MATCH (n:Categorical {name: $label}) RETURN n"
    result = tx.run(text, label=label)    
    # 檢查查詢結果
    if not result.peek():
        # 如果節點不存在，則建立它
        text = "CREATE (" + label + ":Categorical {name: $label})"
        tx.run(text, label=label)
        command.append(text)
        print("Node created.")
    else:
        print("Node already exists.")
    print(command)
    
    # 查看 node B 是否存在
    text = "MATCH (n:"+label+" {name: $obj}) RETURN n"
    result = tx.run(text, obj=obj)
    # 檢查查詢結果
    if not result.peek():
        # 如果節點不存在，則建立它
        text = "CREATE (" + obj + ":" + label + " {name: $obj})"
        tx.run(text, obj=obj)
        command.append(text)
        print("Node created.")
    else:
        print("Node already exists.")
    print(command)


    # 查看 node A 與 node B 之間的關係是否存在
    text = "MATCH (a:Categorical {name: $label}), (b:" + label + " {name: $obj}) RETURN EXISTS((a)-[:" + relation + "]->(b)) AS relationship_exists"
    result = tx.run(text, label=label, obj=obj)
    single_result = result.single()
    if single_result is not None:
        exists = single_result["relationship_exists"]
    else:
        exists = False
    
    # 如果關聯不存在，則建立它
    if exists is False:
        text = "MATCH (a:Categorical {name: $label}), (b:" + label + " {name: $obj}) CREATE (a)-[:" + relation + "]->(b)"
        tx.run(text, label=label, obj=obj)
        command.append(text)
        print("Relationship created.")
    else:
        print("Relationship already exists.")
    
    print(command)

#-------------------------------以下為建立資料庫的code------------------------------------------
# 國泰卡片
with driver.session() as session:
    card12 = ["蝦皮購物聯名卡", 
             "長榮航空聯名卡", 
             "CUBE卡_玩數位", "CUBE卡_樂饗購", "CUBE卡_趣旅行", "CUBE卡_集精選", "CUBE卡_慶生月",
             "國泰世界卡",
             "亞洲萬里通聯名卡",
             "台塑聯名卡",
             "雙幣卡",
             "eTag聯名卡"]
    for card in card12:
        session.write_transaction(create_knowledge_point, "國泰信用卡", "include", card)
print("----------------------------------------------------------------")

# 富邦卡片
with driver.session() as session:
    card23 = [
        "富邦富利生活系列卡", "富邦數位生活卡", "DHC聯名卡", "福華聯名卡", "富邦無限卡",
        "富邦財神系列卡", "富邦銀行卡", "廣三SOGO悠遊聯名卡", "麗嬰房聯名卡", "OpenPossible聯名卡",
        "富邦Costco聯名卡", "廣三SOGO聯名卡", "台茂聯名卡", "采盟聯名卡", "富邦數位生活悠遊聯名卡",
        "富邦鈦金卡", "富邦數位生活一卡通聯名卡", "富邦IMPERIAL尊御世界卡", "富邦世界卡", "富邦悍將悠遊聯名卡",
        "momo卡", "富邦J卡", "富邦鑽保卡"
    ]
    for card in card23:
        session.write_transaction(create_knowledge_point, "富邦信用卡", "include", card)
print("----------------------------------------------------------------")

# 中信卡片
with driver.session() as session:
    card51 = [
        "中信現金回饋鈦金卡", "南紡購物中心聯名卡_鼎極無限卡", "中國信託鼎極卡_無限卡",
        "TAIPEI101聯名卡_新鼎極卡", "英雄聯盟信用卡", "中信兄弟聯名卡_白金卡",
        "TAIPEI101聯名卡_尊榮鼎極卡", "GlobalMall聯名卡_無限卡", "南紡購物中心聯名卡_御璽卡",
        "中信兄弟聯名卡_御璽卡", "Agoda聯名卡", "中信紅利御璽卡", "秀泰聯名卡_白金卡",
        "中信現金回饋御璽卡", "GlobalMall聯名卡_白金卡", "漢神百貨聯名卡_晶緻卡",
        "中信紅利卡", "中信商旅鈦金卡", "LEXUS聯名卡", "ALL_ME卡", "中油聯名卡_御璽卡",
        "漢神百貨聯名卡_御璽卡", "中信紅利晶緻卡", "漢神百貨聯名卡_無限卡", "TAIPEI101聯名卡_新御璽卡",
        "中國信託鼎極卡_極緻卡", "Mitsui_Shopping_Park_LaLaport聯名卡", "中華電信聯名卡_白金卡",
        "大葉髙島屋百貨聯名卡_御璽卡", "秀泰聯名卡_晶緻卡", "中華電信聯名卡_世界卡", "大葉髙島屋百貨聯名卡_晶緻卡",
        "大葉髙島屋百貨聯名卡_鈦金卡", "中油聯名卡_白金卡", "勤美天地聯名卡_御璽卡", "中華電信聯名卡_御璽卡",
        "漢神百貨聯名卡_世界卡", "GlobalMall聯名卡_御璽卡", "大葉髙島屋百貨聯名卡_白金卡", "LINE_Pay信用卡",
        "中信兄弟聯名卡_鼎極卡", "中國信託鼎極卡_世界卡", "漢神百貨聯名卡_鈦金卡", "大葉髙島屋百貨聯名卡_世界卡",
        "大葉髙島屋百貨聯名卡_無限卡", "SuperLife_VISA卡", "中信商務卡_雙幣商務卡", "和泰聯名卡",
        "中華電信聯名卡_無限卡", "中信兄弟聯名卡_鈦金卡", "中華電信聯名卡_鈦金卡"
    ]
    
    
    for card in card51:
        session.write_transaction(create_knowledge_point, "中信信用卡", "include", card)
print("------------------done------------------")